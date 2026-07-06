"""PHÉP THỬ BA MỐC (rút gọn) trên QUẢ CẦU TV - mốc 1 và mốc 2.

Câu hỏi DUY NHẤT: trên quả cầu TV, thành phần học được (rho_theta + mạng đơn điệu
G_phi) có làm tốt hơn phiên bản không học hay không, khi đo ở cùng chi phí hoặc
cùng PSNR?

  Mốc 1 (không học): toán tử  rho_const * B^T(Bx - y),  G_phi = 0.
  Mốc 2 (có học)  : toán tử  rho_theta(x) * (B^T(Bx - y) + G_phi(x)).
  Mốc 3 (baseline học mạnh, Plug-and-Play): ĐỂ SAU - chỉ chạy nếu mốc 2 thắng mốc 1.

Cả hai mốc dùng CHUNG: sơ đồ chiếu - gradient trên quả cầu TV (pie_net.tv_solver),
số bước ngoài K, ngân sách bước nội m, khởi tạo ấm, tau oracle, ngân sách huấn
luyện, tập dữ liệu. Khác nhau DUY NHẤT ở toán tử.

KHỬ HAI CONFOUND (đã thấy ở smoke test):
  - Vi phạm ràng buộc: chiếu xấp xỉ làm đầu ra có TV > tau, và mốc 2 vi phạm
    nhiều hơn. => đo PSNR trên ĐẦU RA ÉP KHẢ THI (chiếu chính xác lên quả cầu TV
    rồi mới đo), nên hai mốc được so trên cùng tập khả thi. PSNR thô + mức vi
    phạm vẫn báo cáo song song để minh bạch.
  - Semi-convergence: ở CÙNG m hai mốc chịu cùng mức chiếu lỏng, nên so ở cùng m
    đã kiểm soát hiệu ứng chính quy hóa ngầm; khác biệt còn lại là do toán tử.

ĐO CHI PHÍ TRUNG THỰC: ở cùng m, tổng bước nội của hai mốc bằng nhau (K*m), nhưng
toán tử mốc 2 nặng hơn -> BÁO CÁO CẢ thời gian chạy thực.

Chạy:  python milestone_test.py [--quick] [--blur gauss|motion] [--device cpu|cuda]
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from dataclasses import dataclass
from statistics import mean, pstdev

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from pie_net.constraints import tv_isotropic, TVBallConstraint
from pie_net.data import make_patches, degrade
from pie_net.metrics import psnr, ssim
from pie_net.operators import (BlurOperator, MonotoneNet, RhoNet, ConstantRho,
                               CostOperator, gaussian_kernel, motion_kernel)
from pie_net.tv_solver import PIENetTV, TVSchedules, ZeroG

RESULTS = "results"

# ----- NGƯỠNG PHÁN QUYẾT, ĐẶT TRƯỚC KHI CHẠY (không sửa sau khi thấy kết quả) -- #
MARGIN_DB = 0.3      # mốc 2 phải hơn mốc 1 >= 0.3 dB ở cùng m mới tính là thắng
QUAL_TOL_DB = 0.1    # dung sai "cùng PSNR" khi xét tiêu chí chi phí
POLISH_INNER = 300   # số bước Chambolle-Pock để ép đầu ra về khả thi (đo PSNR)
POLISH_TOL = 1e-4


@dataclass
class TrainCfg:
    epochs: int = 20
    batch: int = 8
    lr: float = 2e-3
    mu_mono: float = 1.0
    noise_std: float = 0.05


# --------------------------------------------------------------------------- #
def build_milestone(blur, sched: TVSchedules, which: int, device: str) -> PIENetTV:
    """which=1: không học (rho hằng, G_phi=0). which=2: có học (rho_theta, G_phi)."""
    if which == 1:
        G, rho = ZeroG(), ConstantRho(init=1.0)
    else:
        G, rho = MonotoneNet(channels=32, depth=3), RhoNet()
    cost = CostOperator(blur, G, rho)
    return PIENetTV(cost, sched, box=(0.0, 1.0)).to(device)


def train_milestone(net: PIENetTV, blur, x_train, tau_frac, cfg: TrainCfg,
                    device: str, seed: int):
    """Huấn luyện đầu-cuối: MSE(x^K, x_gt) + mu * phạt_đơn_điệu(G_phi).
    Gradient qua chiếu xấp xỉ TV tính bằng unroll (Chambolle-Pock khả vi)."""
    torch.manual_seed(seed)
    net.to(device).train()
    x_train = x_train.to(device)
    opt = torch.optim.Adam(net.parameters(), lr=cfg.lr)
    n = x_train.shape[0]
    for ep in range(cfg.epochs):
        perm = torch.randperm(n, device=device)
        for i in range(0, n, cfg.batch):
            xb = x_train[perm[i:i + cfg.batch]]
            yb = degrade(xb, blur, noise_std=cfg.noise_std)
            tau = (tau_frac * tv_isotropic(xb)).detach()          # oracle tau
            xhat = net(yb, tau)
            loss = (F.mse_loss(xhat, xb)
                    + cfg.mu_mono * net.cost.G.monotonicity_penalty(xb.detach()))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 5.0)
            opt.step()
    return net


@torch.no_grad()
def eval_milestone(net: PIENetTV, blur, x_test, tau_frac, noise_std, device):
    net.eval()
    x = x_test.to(device)
    y = degrade(x, blur, noise_std=noise_std, seed=2024)           # tập test cố định
    tau = (tau_frac * tv_isotropic(x)).detach()

    # đo thời gian (lặp vài lần lấy trung vị để bớt nhiễu) + lấy đầu ra thô
    ts = []
    for _ in range(3):
        t0 = time.time()
        xhat, inner = net(y, tau, return_cost=True)
        if device == "cuda":
            torch.cuda.synchronize()
        ts.append(time.time() - t0)
    t_per_img = sorted(ts)[len(ts) // 2] / x.shape[0] * 1000.0     # ms/ảnh
    raw = xhat.clamp(0, 1)
    feas_raw = net.feasibility(xhat, tau)

    # ĐẦU RA ÉP KHẢ THI: chiếu chính xác (CP hội tụ) lên quả cầu TV rồi mới đo PSNR
    cons = TVBallConstraint(tau=tau, box=(0.0, 1.0))
    x_feas = cons.project(xhat, tol=POLISH_TOL, max_inner=POLISH_INNER).x
    feas_pol = (tv_isotropic(x_feas) / tau.to(x.device)).mean().item()
    xf = x_feas.clamp(0, 1)

    return {"psnr": psnr(xf, x),          # PSNR ép khả thi - METRIC PHÁN QUYẾT
            "psnr_raw": psnr(raw, x),     # PSNR ở điểm vận hành (đầu ra thô)
            "ssim": ssim(xf, x), "inner": inner, "outer": net.s.K,
            "ms_img": t_per_img, "feas_raw": feas_raw, "feas_pol": feas_pol}


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--blur", choices=["gauss", "motion"], default="gauss")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--tau_frac", type=float, default=0.55,
                    help="tau = tau_frac * TV(ảnh sạch) (oracle - hạn chế đã nêu)")
    ap.add_argument("--seeds", type=int, default=None)
    args = ap.parse_args()

    os.makedirs(RESULTS, exist_ok=True)
    dev = args.device

    # quy mô rút gọn
    if args.quick:
        patch, n_train, n_test, K = 64, 16, 4, 8
        m_list, seeds, epochs = [2, 5], [0], 12
    else:
        patch, n_train, n_test, K = 96, 40, 6, 12
        m_list, seeds, epochs = [2, 3, 5], [0, 1, 2], 20
    if args.seeds is not None:
        seeds = list(range(args.seeds))

    print("=" * 80)
    print(f"PHÉP THỬ BA MỐC (rút gọn) | quả cầu TV | device={dev} | blur={args.blur}")
    print(f"  quy mô: patch={patch} n_train={n_train} n_test={n_test} K={K} "
          f"epochs={epochs} | m={m_list} | seeds={seeds}")
    print(f"  noise={args.noise} | tau_frac={args.tau_frac} (oracle)")
    print(f"  PSNR phán quyết = PSNR trên ĐẦU RA ÉP KHẢ THI (chiếu CP {POLISH_INNER} "
          f"bước, tol={POLISH_TOL})")
    print(f"  NGƯỠNG ĐẶT TRƯỚC: thắng = +{MARGIN_DB} dB ở cùng m (vượt dao động); "
          f"cùng PSNR trong {QUAL_TOL_DB} dB")
    print("=" * 80)

    # dữ liệu (tập test cố định cho mọi mốc/m/seed)
    x_train_full, x_test = make_patches(patch=patch, n_train=n_train,
                                        n_test=n_test, seed=1)
    kernel = (gaussian_kernel(9, 1.6) if args.blur == "gauss"
              else motion_kernel(9, 30.0))
    blur = BlurOperator(kernel).to(dev)
    y_test = degrade(x_test.to(dev), blur, noise_std=args.noise, seed=2024)
    print(f"PSNR ảnh mờ (đầu vào): {psnr(y_test.clamp(0,1), x_test.to(dev)):.2f} dB\n")

    cfg = TrainCfg(epochs=epochs, noise_std=args.noise)
    res = {1: {m: [] for m in m_list}, 2: {m: [] for m in m_list}}

    for which in (1, 2):
        tag = "MỐC 1 (không học)" if which == 1 else "MỐC 2 (có học)"
        for m in m_list:
            for sd in seeds:
                sched = TVSchedules(K=K, m=m, lam0=1.0, learn_lambda=True)
                net = build_milestone(blur, sched, which, dev)
                t0 = time.time()
                train_milestone(net, blur, x_train_full, args.tau_frac, cfg, dev, sd)
                ev = eval_milestone(net, blur, x_test, args.tau_frac, args.noise, dev)
                res[which][m].append(ev)
                print(f"  {tag:<18s} m={m} seed={sd} | PSNR(khả thi) "
                      f"{ev['psnr']:6.3f} | PSNR(thô) {ev['psnr_raw']:6.3f} | "
                      f"bước nội {ev['inner']:4d} | {ev['ms_img']:6.1f} ms/ảnh | "
                      f"TV/tau thô {ev['feas_raw']:.3f}->khả thi {ev['feas_pol']:.3f} "
                      f"| {time.time()-t0:5.1f}s")
        print()

    # ----- tổng hợp (trung bình +- độ lệch theo seed) ----------------------- #
    def agg(which, m, key):
        vals = [e[key] for e in res[which][m]]
        return mean(vals), (pstdev(vals) if len(vals) > 1 else 0.0)

    print("=" * 80)
    print("KẾT QUẢ (trung bình theo seed) | PSNR = ép khả thi | cùng m => cùng bước nội")
    print(f"{'m':>3} {'bước nội':>9} | {'PSNR mốc1':>11} {'PSNR mốc2':>11} "
          f"{'chênh':>8} | {'chênh thô':>10} | {'ms M1':>7} {'ms M2':>7}")
    print("-" * 80)
    gaps = {}
    for m in m_list:
        p1, s1 = agg(1, m, "psnr")
        p2, s2 = agg(2, m, "psnr")
        pr1, _ = agg(1, m, "psnr_raw")
        pr2, _ = agg(2, m, "psnr_raw")
        t1, _ = agg(1, m, "ms_img")
        t2, _ = agg(2, m, "ms_img")
        gaps[m] = (p2 - p1, s1 + s2)
        print(f"{m:>3} {K*m:>9} | {p1:7.3f}±{s1:4.2f} {p2:7.3f}±{s2:4.2f} "
              f"{p2-p1:>+8.3f} | {pr2-pr1:>+10.3f} | {t1:7.1f} {t2:7.1f}")
    print("=" * 80)

    # ----- PHÁN QUYẾT (trên PSNR ép khả thi) -------------------------------- #
    best_m = max(m_list, key=lambda m: gaps[m][0])
    gap, noise = gaps[best_m]
    cond_A = gap >= MARGIN_DB and gap >= max(noise, 1e-9)

    p1_best_m = max(m_list, key=lambda m: agg(1, m, "psnr")[0])
    p1_best = agg(1, p1_best_m, "psnr")[0]
    cheaper_m = [m for m in m_list if agg(2, m, "psnr")[0] >= p1_best - QUAL_TOL_DB]
    cond_B = bool(cheaper_m) and min(cheaper_m) < p1_best_m

    raw_gap = agg(2, best_m, "psnr_raw")[0] - agg(1, best_m, "psnr_raw")[0]

    print("\nPHÁN QUYẾT (PSNR ép khả thi)")
    print(f"  Tiêu chí A (cùng chi phí, PSNR cao hơn): chênh lớn nhất {gap:+.3f} dB "
          f"tại m={best_m} (dao động seed ±{noise:.2f}) -> "
          f"{'ĐẠT' if cond_A else 'KHÔNG ĐẠT'}")
    print(f"     đối chiếu: cùng m={best_m}, chênh PSNR THÔ là {raw_gap:+.3f} dB; "
          f"sau khi ép khả thi còn {gap:+.3f} dB "
          f"(phần chênh do vi phạm ràng buộc = {raw_gap-gap:+.3f} dB)")
    if cond_A:
        t1b, _ = agg(1, best_m, "ms_img")
        t2b, _ = agg(2, best_m, "ms_img")
        print(f"     chi phí thật: ở m={best_m}, mốc 2 chạy {t2b/max(t1b,1e-9):.2f}x "
              f"thời gian của mốc 1 do toán tử nặng hơn")
    print(f"  Tiêu chí B (cùng PSNR, ít chi phí hơn): "
          f"{'ĐẠT (m=' + str(min(cheaper_m)) + ' < ' + str(p1_best_m) + ')' if cond_B else 'KHÔNG ĐẠT'}")

    if cond_A or cond_B:
        verdict = ("PASS - thành phần học được thêm giá trị đo được trên quả cầu TV "
                   "(kể cả khi đã ép khả thi). Tiến hành mốc 3 và các bước khóa.")
    else:
        verdict = ("FAIL - thành phần học được KHÔNG thắng phiên bản không học khi so "
                   "trên cùng tập khả thi. Theo kế hoạch: dừng ở kết quả nhỏ, không "
                   "khóa độ nhạy, chuyển bài toán.")
    print("\n>>> " + verdict)

    # ----- lưu bảng + hình -------------------------------------------------- #
    with open(f"{RESULTS}/milestone_tv_{args.blur}.csv", "w", newline="",
              encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["milestone", "m", "inner_steps", "seed", "psnr_feasible",
                    "psnr_raw", "ssim", "ms_per_img", "feas_raw", "feas_polished"])
        for which in (1, 2):
            for m in m_list:
                for sd, e in zip(seeds, res[which][m]):
                    w.writerow([which, m, K * m, sd, f"{e['psnr']:.4f}",
                                f"{e['psnr_raw']:.4f}", f"{e['ssim']:.4f}",
                                f"{e['ms_img']:.2f}", f"{e['feas_raw']:.4f}",
                                f"{e['feas_pol']:.4f}"])
    print(f"\n-> đã lưu {RESULTS}/milestone_tv_{args.blur}.csv")

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    for which, mk, lab in [(1, "s", "mốc 1 (không học)"), (2, "o", "mốc 2 (có học)")]:
        xs_inner = [K * m for m in m_list]
        ys = [agg(which, m, "psnr")[0] for m in m_list]
        es = [agg(which, m, "psnr")[1] for m in m_list]
        xs_time = [agg(which, m, "ms_img")[0] for m in m_list]
        ax[0].errorbar(xs_inner, ys, yerr=es, marker=mk, capsize=3, label=lab)
        ax[1].errorbar(xs_time, ys, yerr=es, marker=mk, capsize=3, label=lab)
    ax[0].set_xlabel("tổng bước nội (chi phí chiếu)")
    ax[0].set_title("PSNR (ép khả thi) vs bước nội")
    ax[1].set_xlabel("thời gian (ms/ảnh) - gồm cả toán tử")
    ax[1].set_title("PSNR (ép khả thi) vs thời gian")
    for a in ax:
        a.set_ylabel("PSNR (dB)"); a.grid(True, alpha=.3); a.legend()
    fig.tight_layout(); fig.savefig(f"{RESULTS}/milestone_tv_{args.blur}.png", dpi=130)
    print(f"-> đã lưu {RESULTS}/milestone_tv_{args.blur}.png")


if __name__ == "__main__":
    main()
