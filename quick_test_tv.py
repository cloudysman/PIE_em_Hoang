"""PHÉP THỬ NHANH (1-2 ngày) - khẳng định sống còn của hướng 2.

Khẳng định DUY NHẤT: trên quả cầu TV (chiếu chính xác cần vòng lặp nội tốn kém),
chiếu XẤP XỈ ít bước nội đạt CÙNG chất lượng ảnh nhưng tốn ÍT chi phí hơn rõ rệt
so với chiếu CHÍNH XÁC CÓ KHỞI TẠO ẤM, trong khi vẫn giữ hội tụ.

Cô lập đúng khẳng định, KHÔNG cần huấn luyện: khử mờ ràng buộc TV thuần
    M(x) = B^T(B x - y)            (rho = 1, G_phi = 0)
    lặp ngoài (chiếu - gradient):  x_{k+1} = P_D( x_k - lam * M(x_k) ),  D={TV<=tau}.
Cố định K, lam, tau; chỉ thay CÁCH chiếu:
    exact_cold : chiếu tới sai số <= delta so với nghiệm hội tụ, khởi tạo LẠNH.
    exact_warm : NHƯ TRÊN nhưng khởi tạo ẤM (BASELINE KHÓ NHẤT, bắt buộc) — cùng
                 quỹ đạo/chất lượng với exact_cold, chỉ khác CHI PHÍ.
    inexact_m  : chiếu xấp xỉ ĐÚNG m bước nội (ngân sách cố định), khởi tạo ẤM.

Chi phí 'chính xác' đo TRUNG THỰC = số bước CP để đạt sai số tương đối <= delta
so với nghiệm chiếu hội tụ (N_REF bước) — KHÔNG dùng tiêu chí thay-đổi-nguyên-thủy
(đã chứng minh là kích hoạt sớm giả tạo).

TIÊU CHÍ DỪNG (đặt TRƯỚC): nếu ở cùng chất lượng (trong 0.1 dB của exact_warm)
chiếu xấp xỉ KHÔNG dùng ít hơn rõ rệt tổng bước nội so với exact_warm -> phép thử
THẤT BẠI -> chuyển hướng 3.

Chạy:  python quick_test_tv.py [--quick] [--blur gauss|motion] [--device cpu|cuda]
"""

from __future__ import annotations

import argparse
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from pie_net.constraints import TVBallConstraint, grad2d, div2d, tv_isotropic
from pie_net.data import make_patches, degrade
from pie_net.metrics import psnr
from pie_net.operators import BlurOperator, gaussian_kernel, motion_kernel


# --------------------------------------------------------------------------- #
def check_adjoint(device, n=4, H=40, W=44):
    x = torch.randn(n, 1, H, W, device=device)
    p = torch.randn(n, 2, H, W, device=device)
    lhs = (grad2d(x) * p).sum()
    rhs = -(x * div2d(p)).sum()
    err = (lhs - rhs).abs().item() / (lhs.abs().item() + 1e-12)
    print(f"[kiểm tra] adjoint grad/div: rel-err = {err:.2e} "
          f"({'OK' if err < 1e-4 else 'SAI'})")
    return err < 1e-4


# --------------------------------------------------------------------------- #
@torch.no_grad()
def run_exact(cons, blur, y, x_gt, K, lam, n_ref, delta, cap):
    """Quỹ đạo CHIẾU CHÍNH XÁC (tới sai số <= delta). exact_cold và exact_warm
    DÙNG CHUNG quỹ đạo/chất lượng (đều là chiếu chính xác), chỉ khác CHI PHÍ:
    số bước CP để đạt delta khi khởi tạo lạnh (None) vs ấm (state bước trước)."""
    x = blur.adjoint(y).clamp(0, 1)
    star_state = None
    tot_cold = tot_warm = 0
    t_cold = t_warm = 0.0
    psnr_hist = []
    for k in range(K):
        grad = blur.adjoint(blur(x) - y)
        v = x - lam * grad
        # nghiệm chiếu HỘI TỤ (tham chiếu), khởi tạo ấm để bản thân ref cũng rẻ
        res = cons.project(v, tol=0.0, max_inner=n_ref, state=star_state)
        x_star = res.x
        # chi phí chính xác: số bước đạt delta, lạnh vs ấm (đo cả thời gian)
        t0 = time.time()
        n_cold = cons.iters_to_tol(v, x_star, delta, cap, state=None)
        t_cold += time.time() - t0
        t0 = time.time()
        n_warm = cons.iters_to_tol(v, x_star, delta, cap, state=star_state)
        t_warm += time.time() - t0
        tot_cold += n_cold
        tot_warm += n_warm
        x = x_star
        star_state = res.state
        psnr_hist.append(psnr(x.clamp(0, 1), x_gt))
    feas = (cons.value(x) / cons.tau.to(x.device)).mean().item()
    p = psnr_hist[-1]
    return {
        "exact_cold": {"psnr": p, "total_inner": tot_cold, "time_s": t_cold,
                       "feas": feas, "psnr_hist": psnr_hist},
        "exact_warm": {"psnr": p, "total_inner": tot_warm, "time_s": t_warm,
                       "feas": feas, "psnr_hist": psnr_hist},
    }


@torch.no_grad()
def run_inexact(cons, blur, y, x_gt, K, lam, m):
    """Quỹ đạo CHIẾU XẤP XỈ: mỗi bước ngoài chiếu ĐÚNG m bước CP, khởi tạo ẤM."""
    x = blur.adjoint(y).clamp(0, 1)
    state = None
    total = 0
    psnr_hist = []
    t0 = time.time()
    for k in range(K):
        v = x - lam * blur.adjoint(blur(x) - y)
        res = cons.project(v, tol=0.0, max_inner=m, state=state)
        x = res.x
        state = res.state
        total += res.n_inner
        psnr_hist.append(psnr(x.clamp(0, 1), x_gt))
    dt = time.time() - t0
    feas = (cons.value(x) / cons.tau.to(x.device)).mean().item()
    return {"psnr": psnr_hist[-1], "total_inner": total, "time_s": dt,
            "feas": feas, "psnr_hist": psnr_hist}


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--blur", choices=["gauss", "motion"], default="gauss")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--tau_frac", type=float, default=0.55,
                    help="tau = tau_frac * TV(ảnh sạch); chọn để ràng buộc bị kích hoạt")
    args = ap.parse_args()

    import os
    os.makedirs("results", exist_ok=True)
    torch.manual_seed(0)
    dev = args.device
    print(f"== PHÉP THỬ NHANH (TV-ball) | device={dev} | blur={args.blur} "
          f"| noise={args.noise} | tau_frac={args.tau_frac} ==")

    if not check_adjoint(dev):
        print("  -> adjoint sai, dừng."); return

    patch = 96 if args.quick else 128
    n_img = 4 if args.quick else 6
    _, x_test = make_patches(patch=patch, n_train=2, n_test=n_img, seed=1)
    x_gt = x_test.to(dev)
    kernel = gaussian_kernel(9, 1.6) if args.blur == "gauss" else motion_kernel(9, 30.0)
    blur = BlurOperator(kernel).to(dev)
    y = degrade(x_gt, blur, noise_std=args.noise, seed=2024)
    print(f"   ảnh test: {tuple(x_gt.shape)} | PSNR ảnh mờ (đầu vào): "
          f"{psnr(y.clamp(0,1), x_gt):.2f} dB")

    tau = (args.tau_frac * tv_isotropic(x_gt)).detach()
    cons = TVBallConstraint(tau=tau, box=(0.0, 1.0))
    print(f"   tau trung bình = {tau.mean().item():.0f} | TV ảnh mờ = "
          f"{tv_isotropic(y).mean().item():.0f}")

    K = 20 if args.quick else 40
    lam = 1.0
    N_REF, DELTA, CAP = 400, 1e-3, 400
    print(f"   K={K} | lambda={lam} | chiếu chính xác: sai số <= delta={DELTA} "
          f"(tham chiếu {N_REF} bước CP)")

    print("\n[chạy] chiếu chính xác (cold & warm, cùng quỹ đạo)...")
    runs = run_exact(cons, blur, y, x_gt, K, lam, N_REF, DELTA, CAP)
    print("[chạy] chiếu xấp xỉ ngân sách cố định m bước...")
    m_list = [1, 2, 5] if args.quick else [1, 2, 3, 5, 10]
    for m in m_list:
        runs[f"inexact_m{m}"] = run_inexact(cons, blur, y, x_gt, K, lam, m)

    # bảng kết quả
    print("\n" + "=" * 74)
    print(f"{'chế độ chiếu':<16s} {'PSNR(dB)':>9s} {'tổng bước nội':>14s} "
          f"{'thời gian(s)':>13s} {'TV/tau':>8s}")
    print("-" * 74)
    order = ["exact_cold", "exact_warm"] + [f"inexact_m{m}" for m in m_list]
    for name in order:
        r = runs[name]
        print(f"{name:<16s} {r['psnr']:9.3f} {r['total_inner']:14d} "
              f"{r['time_s']:13.3f} {r['feas']:8.3f}")
    print("=" * 74)

    # PHÁN QUYẾT
    ref = runs["exact_warm"]
    target = ref["psnr"]
    print(f"\nBaseline khó nhất = exact_warm: PSNR {target:.3f} dB | "
          f"{ref['total_inner']} bước nội | {ref['time_s']:.3f}s")
    print(f"(so chiếu lạnh exact_cold: {runs['exact_cold']['total_inner']} bước nội "
          f"-> warm-start tiết kiệm "
          f"{runs['exact_cold']['total_inner']/max(ref['total_inner'],1):.1f}x)")
    cand = {k: v for k, v in runs.items()
            if k.startswith("inexact") and v["psnr"] >= target - 0.1}
    if cand:
        name, r = min(cand.items(), key=lambda kv: kv[1]["total_inner"])
        su = ref["total_inner"] / max(r["total_inner"], 1)
        su_t = ref["time_s"] / max(r["time_s"], 1e-9)
        ok = r["total_inner"] < ref["total_inner"]
        print(f"Chiếu xấp xỉ rẻ nhất đạt cùng chất lượng (≤0.1 dB): {name} | "
              f"PSNR {r['psnr']:.3f} dB | {r['total_inner']} bước nội "
              f"({su:.1f}x ít hơn) | {r['time_s']:.3f}s ({su_t:.1f}x nhanh hơn)")
        verdict = ("PASS — khẳng định ĐỨNG ở phép thử nhanh: chiếu xấp xỉ thắng "
                   "exact_warm về tổng chi phí ở cùng chất lượng. Tiến hành giai đoạn 1."
                   if ok else
                   "FAIL — không thắng exact_warm về chi phí -> cân nhắc hướng 3.")
    else:
        verdict = ("FAIL — không chế độ xấp xỉ nào đạt cùng chất lượng (≤0.1 dB) "
                   "của exact_warm -> chuyển hướng 3.")
    print("\n>>> " + verdict)

    # Pareto
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    for name in order:
        r = runs[name]
        mk = "s" if name.startswith("exact") else "o"
        ax[0].scatter(r["total_inner"], r["psnr"], marker=mk, s=60, label=name, zorder=3)
        ax[1].scatter(r["time_s"], r["psnr"], marker=mk, s=60, label=name, zorder=3)
    for a in ax:
        a.axhline(target, ls="--", c="gray", lw=1)
        a.set_ylabel("PSNR (dB)"); a.grid(True, alpha=.3); a.legend(fontsize=7)
        a.set_xscale("log")
    ax[0].set_xlabel("tổng số bước nội (chi phí)")
    ax[0].set_title("Đánh đổi: chất lượng vs tổng bước nội")
    ax[1].set_xlabel("thời gian (s)")
    ax[1].set_title("Đánh đổi: chất lượng vs thời gian")
    fig.tight_layout(); fig.savefig("results/quick_tv_pareto.png", dpi=130)
    print("-> đã lưu results/quick_tv_pareto.png")


if __name__ == "__main__":
    main()
