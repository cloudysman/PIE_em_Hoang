"""PIE-Net - Thực nghiệm khử mờ ảnh (WP4).

Chạy:  python run_experiment.py [--quick] [--blur gauss|motion] [--device cpu|cuda]

Nội dung:
  1. Sinh dữ liệu suy biến  y = B x + eps  (khử mờ Gauss/chuyển động + nhiễu).
  2. Huấn luyện PIE-Net với rho_theta HỌC ĐƯỢC  (mô hình chính).
  3. Huấn luyện PIE-Net với rho HẰNG SỐ          (thí nghiệm THEN CHỐT).
  4. Ablation cấu trúc: bỏ quán tính / bỏ viscosity / chiếu chính xác / L-free Tseng.
  5. Đánh giá: PSNR, SSIM, phần dư VI, số vòng lặp, thời gian; lưu hình & bảng CSV.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from copy import deepcopy

# Console Windows mặc định cp1252 không mã hóa được tiếng Việt -> ép UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from pie_net.data import make_patches, degrade
from pie_net.metrics import psnr, ssim
from pie_net.operators import (BlurOperator, MonotoneNet, RhoNet, ConstantRho,
                               CostOperator, gaussian_kernel, motion_kernel)
from pie_net.solver import PIENet, Schedules
from pie_net.train import TrainCfg, train

RESULTS = "results"


# --------------------------------------------------------------------------- #
def build_net(blur, sched: Schedules, rho_kind: str, device: str) -> PIENet:
    """Tạo một PIE-Net mới với loại rho cho trước ('learned' | 'const')."""
    G = MonotoneNet(channels=32, depth=3)
    rho = RhoNet() if rho_kind == "learned" else ConstantRho(init=1.0)
    cost = CostOperator(blur, G, rho)
    return PIENet(cost, sched).to(device)


@torch.no_grad()
def evaluate(net, blur, x_test, noise_std, device):
    net.eval()
    x = x_test.to(device)
    y = degrade(x, blur, noise_std=noise_std, seed=2024)
    t0 = time.time()
    xhat = net(y)
    dt = (time.time() - t0) / x.shape[0] * 1000.0          # ms/ảnh
    return {
        "PSNR": psnr(xhat, x), "SSIM": ssim(xhat, x),
        "VI_res": net.vi_residual(xhat, y).item(),
        "iters": net.s.K, "ms/img": dt,
    }, y.cpu(), xhat.cpu()


def fmt_row(name, m):
    return (f"{name:<28s} {m['PSNR']:7.2f}  {m['SSIM']:6.3f}  "
            f"{m['VI_res']:9.2e}  {m['iters']:5d}  {m['ms/img']:7.1f}")


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true",
                    help="chạy nhanh (ít epoch/patch) để kiểm thử")
    ap.add_argument("--blur", choices=["gauss", "motion"], default="gauss")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--noise", type=float, default=0.01)
    args = ap.parse_args()

    import os
    os.makedirs(RESULTS, exist_ok=True)
    torch.manual_seed(0)
    device = args.device
    print(f"== PIE-Net | device={device} | blur={args.blur} | noise={args.noise} ==")

    # 1) toán tử suy biến + dữ liệu ---------------------------------------- #
    kernel = gaussian_kernel(9, 1.6) if args.blur == "gauss" else motion_kernel(9, 30.0)
    blur = BlurOperator(kernel).to(device)
    patch = 48 if args.quick else 64
    n_tr = 32 if args.quick else 96
    x_train, x_test = make_patches(patch=patch, n_train=n_tr, n_test=8, seed=0)
    print(f"   train patches: {tuple(x_train.shape)} | test: {tuple(x_test.shape)}")

    # baseline chất lượng ảnh mờ (chưa khôi phục)
    y_test = degrade(x_test.to(device), blur, noise_std=args.noise, seed=2024)
    base = {"PSNR": psnr(y_test.cpu(), x_test), "SSIM": ssim(y_test.cpu(), x_test),
            "VI_res": float("nan"), "iters": 0, "ms/img": 0.0}

    sched = Schedules(K=8 if args.quick else 12)
    cfg = TrainCfg(epochs=15 if args.quick else 45, batch=8, noise_std=args.noise)

    results = {}
    recons = {}

    # 2) MÔ HÌNH CHÍNH: rho_theta học được --------------------------------- #
    print("\n[1/2] Huấn luyện PIE-Net (rho_theta HỌC ĐƯỢC)...")
    net_learned = build_net(blur, deepcopy(sched), "learned", device)
    train(net_learned, blur, x_train, cfg, device=device)
    m_learned, y_show, xhat_learned = evaluate(net_learned, blur, x_test, args.noise, device)
    results["PIE-Net (rho hoc duoc)"] = m_learned
    recons["learned"] = xhat_learned

    # 3) THÍ NGHIỆM THEN CHỐT: rho hằng số --------------------------------- #
    print("\n[2/2] Huấn luyện PIE-Net (rho HẰNG SỐ - thí nghiệm then chốt)...")
    net_const = build_net(blur, deepcopy(sched), "const", device)
    train(net_const, blur, x_train, cfg, device=device)
    m_const, _, xhat_const = evaluate(net_const, blur, x_test, args.noise, device)
    results["PIE-Net (rho hang so)"] = m_const
    recons["const"] = xhat_const

    # 4) Ablation cấu trúc (huấn luyện ngắn để tiết kiệm thời gian) --------- #
    cfg_ab = TrainCfg(epochs=max(8, cfg.epochs // 3), batch=8, noise_std=args.noise)
    ablations = {
        "Bo quan tinh (no inertial)": dict(use_inertial=False),
        "Bo viscosity (no viscosity)": dict(use_viscosity=False),
        "Chieu chinh xac (exact proj)": dict(inexact_proj=False),
        "L-free (Tseng linesearch)": dict(tseng_linesearch=True, learn_lambda=False),
    }
    print("\n[ablation] huấn luyện ngắn các biến thể cấu trúc...")
    for name, kw in ablations.items():
        s = deepcopy(sched)
        for k, v in kw.items():
            setattr(s, k, v)
        net = build_net(blur, s, "learned", device)
        train(net, blur, x_train, cfg_ab, device=device, verbose=False)
        m, _, _ = evaluate(net, blur, x_test, args.noise, device)
        results[name] = m
        print(f"   {name:<30s} PSNR {m['PSNR']:.2f} | VIres {m['VI_res']:.2e}")

    # 5) Bảng kết quả ------------------------------------------------------- #
    print("\n" + "=" * 70)
    print("KẾT QUẢ (test) | PSNR(dB)  SSIM   VI_res     iters   ms/img")
    print("-" * 70)
    print(fmt_row("Anh mo (degraded input)", base))
    for name, m in results.items():
        print(fmt_row(name, m))
    print("=" * 70)

    with open(f"{RESULTS}/metrics.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["method", "PSNR", "SSIM", "VI_res", "iters", "ms_per_img"])
        w.writerow(["degraded", base["PSNR"], base["SSIM"], "", 0, 0])
        for name, m in results.items():
            w.writerow([name, m["PSNR"], m["SSIM"], m["VI_res"], m["iters"], m["ms/img"]])
    print(f"-> đã lưu {RESULTS}/metrics.csv")

    # 6) Hội tụ thuật toán (T2) + ghi chú trung thực về semi-convergence --- #
    # Lấy toán tử F_theta ĐÃ HUẤN LUYỆN, chạy thuật toán thuần nhiều bước
    # (Tseng/L-free). Hai sự thật song song, đều được trình bày trung thực:
    #   (T2)  phần dư VI r(x^k) -> 0  => thuật toán HỘI TỤ (đúng nội dung T2).
    #   (semi-convergence) PSNR đạt ĐỈNH ở chân trời hữu hạn rồi giảm, vì
    #         nghiệm-VI *chính xác* của F_theta là nghiệm bám dữ liệu; khôi
    #         phục chất lượng cao chính là điểm-lặp ở chân trời hữu hạn
    #         (chế độ vận hành = deep unfolding K bước).
    net_learned.eval()
    K_long = 60 if args.quick else 200
    _, hist = net_learned.solve_long(y_test, K_long=K_long, lam=0.4,
                                     use_tseng=True, ref=x_test.to(device))
    psnrs = hist["psnr_step"]
    k_peak = int(max(range(len(psnrs)), key=lambda i: psnrs[i])) + 1
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(range(1, len(hist["vi"]) + 1), hist["vi"], "-")
    ax[0].set_xlabel("buoc lap k"); ax[0].set_ylabel("phan du VI  r(x^k)")
    ax[0].set_title("Thuat toan HOI TU: VI residual -> 0 (T2)")
    ax[0].set_yscale("log"); ax[0].grid(True, alpha=.3)
    ax[1].plot(range(1, len(psnrs) + 1), psnrs, "-", color="C1")
    ax[1].axvline(k_peak, ls="--", c="gray", lw=1)
    ax[1].annotate(f"dinh ~{psnrs[k_peak-1]:.1f}dB @k={k_peak}\n(che do van hanh)",
                   xy=(k_peak, psnrs[k_peak - 1]), xytext=(k_peak + len(psnrs)*0.12,
                   psnrs[k_peak-1]-3), fontsize=8,
                   arrowprops=dict(arrowstyle="->", color="gray"))
    ax[1].set_xlabel("buoc lap k"); ax[1].set_ylabel("PSNR (dB)")
    ax[1].set_title("PSNR: dinh o chan troi huu han (semi-convergence)")
    ax[1].grid(True, alpha=.3)
    fig.tight_layout(); fig.savefig(f"{RESULTS}/convergence.png", dpi=130)
    print(f"   T2 (hoi tu thuat toan): VI residual {hist['vi'][0]:.2e} -> "
          f"{hist['vi'][-1]:.2e} qua {K_long} buoc")
    print(f"   semi-convergence: PSNR dinh {psnrs[k_peak-1]:.2f} dB @ k={k_peak}, "
          f"cuoi {psnrs[-1]:.2f} dB (khoi phuc tot = diem-lap chan troi huu han)")
    print(f"-> đã lưu {RESULTS}/convergence.png")

    # 7) Hình khôi phục ---------------------------------------------------- #
    nshow = min(4, x_test.shape[0])
    fig, ax = plt.subplots(4, nshow, figsize=(2.4 * nshow, 9.2))
    rows = [("Goc x", x_test), ("Mo y", y_show.cpu()),
            ("PIE-Net rho hoc", recons["learned"]), ("PIE-Net rho hang", recons["const"])]
    for r, (title, imgs) in enumerate(rows):
        for c in range(nshow):
            ax[r, c].imshow(imgs[c, 0].clamp(0, 1), cmap="gray", vmin=0, vmax=1)
            ax[r, c].axis("off")
            if c == 0:
                ax[r, c].set_ylabel(title, rotation=90, fontsize=11)
                ax[r, c].axis("on"); ax[r, c].set_xticks([]); ax[r, c].set_yticks([])
    fig.suptitle("PIE-Net - khu mo anh", fontsize=13)
    fig.tight_layout(); fig.savefig(f"{RESULTS}/reconstructions.png", dpi=130)
    print(f"-> đã lưu {RESULTS}/reconstructions.png")

    # 8) Báo cáo rho học được --------------------------------------------- #
    with torch.no_grad():
        r_vals = net_learned.cost.rho(x_test.to(device)).flatten()
        print(f"\nrho_theta hoc duoc tren test: min={r_vals.min():.3f} "
              f"max={r_vals.max():.3f} mean={r_vals.mean():.3f}")
    print("\nHoan tat. Xem thu muc 'results/'.")


if __name__ == "__main__":
    main()
