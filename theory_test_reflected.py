"""Driver LÝ THUYẾT — sơ đồ phản xạ bốn pha với chiếu xấp xỉ trên quả cầu TV.

Chạy lưới cấu hình {blur ∈ [gauss, motion]} x {chế độ ngân sách bước nội} trên
CÙNG tập ảnh kiểm tra (data.make_patches, cùng hạt giống nhiễu), thuần suy diễn
(rho=1, G=0, F = B^T(B·-y)), box=None. Ghi CSV vào results/theory/:
  - mỗi cấu hình một file  theory_<blur>_<mode>.csv  (vết đầy đủ mỗi bước ngoài,
    theo từng ảnh): k, img, e_abs, e_rel (sai số chiếu đo được so P_ref 1500 bước
    ấm), delta (||x^{k+1}-x^k||), resid (phần dư biến phân, tham chiếu thích
    nghi), psnr, inner_k, inner_cum, tv_ratio, ref_check (chênh lệch P_ref 1500
    vs 3000 bước tại 3 mốc k), alpha, beta, m_k;
  - một file tổng hợp summary.csv (cấu hình, PSNR cuối, phần dư cuối, tổng bước
    nội, thời gian).

Gợi ý quy mô: K=300 cho nghiên cứu độ dốc, K=40 cho bảng chi phí (CPU laptop).

Chạy:
  python theory_test_reflected.py                     # lưới đầy đủ, K=300
  python theory_test_reflected.py --quick             # K=30, size=64, gauss, m2+mlog
  python theory_test_reflected.py --K 40 --size 96 --beta0 0.0
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import torch

from pie_net.constraints import tv_isotropic
from pie_net.data import make_patches, degrade
from pie_net.operators import BlurOperator, gaussian_kernel, motion_kernel
from pie_net.reflected_solver import Budget, run_reflected, power_iteration_L

RESULT_DIR = os.path.join("results", "theory")

ALL_MODES = {
    "m1":       Budget(kind="fixed", m=1),
    "m2":       Budget(kind="fixed", m=2),
    "m5":       Budget(kind="fixed", m=5),
    "mlog":     Budget(kind="log"),
    "exact":    Budget(kind="exact", delta=1e-3),
    "epsconst": Budget(kind="epsconst", eps_const=5e-3),
}


def make_blur(name: str) -> BlurOperator:
    kernel = gaussian_kernel(9, 1.6) if name == "gauss" else motion_kernel(9, 30.0)
    return BlurOperator(kernel)


def write_trace_csv(path: str, trace: dict) -> None:
    keys = ["e_abs", "e_rel", "delta", "resid", "psnr", "inner_k",
            "inner_cum", "tv_ratio", "ref_check", "alpha", "beta", "m_k"]
    K, B = trace["e_abs"].shape
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["k", "img"] + keys)
        for k in range(K):
            for b in range(B):
                wr.writerow([k, b] + [f"{trace[key][k, b].item():.6e}"
                                      for key in keys])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=300,
                    help="số bước ngoài (300: độ dốc; 40: bảng chi phí)")
    ap.add_argument("--size", type=int, default=64, help="cạnh patch (64..96)")
    ap.add_argument("--beta0", type=float, default=0.05,
                    help="hệ số độ nhớt beta_k = beta0/(k+1); 0 để ablation")
    ap.add_argument("--quick", action="store_true",
                    help="smoke test: K=30, size=64, chỉ gauss với m2 và mlog")
    ap.add_argument("--n_test", type=int, default=4, help="số ảnh kiểm tra")
    ap.add_argument("--measure_every", type=int, default=1,
                    help="đo e_k và phần dư mỗi N bước ngoài (đắt); delta_k luôn đo")
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--tau_frac", type=float, default=0.55,
                    help="tau = tau_frac * TV(ảnh sạch) (oracle, ràng buộc kích hoạt)")
    ap.add_argument("--blurs", nargs="+", default=None,
                    choices=["gauss", "motion"])
    ap.add_argument("--modes", nargs="+", default=None,
                    choices=list(ALL_MODES.keys()))
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    if args.quick:
        args.K, args.size = 30, 64
        blurs = ["gauss"]
        modes = ["m2", "mlog"]
    else:
        blurs = args.blurs or ["gauss", "motion"]
        modes = args.modes or list(ALL_MODES.keys())

    os.makedirs(RESULT_DIR, exist_ok=True)
    torch.manual_seed(0)
    dev = args.device
    print(f"== LÝ THUYẾT: sơ đồ phản xạ 4 pha + chiếu xấp xỉ TV | device={dev} ==")
    print(f"   K={args.K} | size={args.size} | beta0={args.beta0} | "
          f"noise={args.noise} | tau_frac={args.tau_frac} | n_test={args.n_test}")
    print(f"   blur={blurs} | modes={modes}")

    # CÙNG tập ảnh kiểm tra + CÙNG hạt giống nhiễu cho mọi cấu hình
    _, x_test = make_patches(patch=args.size, n_train=2,
                             n_test=args.n_test, seed=1)
    x_gt = x_test.to(dev, torch.float32)
    tau = (args.tau_frac * tv_isotropic(x_gt)).detach()

    rows = []
    for blur_name in blurs:
        blur = make_blur(blur_name).to(dev)
        y = degrade(x_gt, blur, noise_std=args.noise, seed=2024)  # cùng seed nhiễu
        L = power_iteration_L(blur, (1, 1, args.size, args.size),
                              n_iter=100, device=dev)
        lam = 0.9 * (2.0 ** 0.5 - 1.0) / max(L, 1e-12)
        print(f"\n[{blur_name}] L=||B^T B||={L:.6f} (power iteration) -> "
              f"lambda=0.9(sqrt2-1)/L={lam:.4f} | tau tb={tau.mean().item():.1f}")

        for mode in modes:
            budget = ALL_MODES[mode]
            print(f"  [chạy] {blur_name} / {mode} ...")
            t0 = time.perf_counter()
            out = run_reflected(blur, y, tau, K=args.K, budget=budget,
                                beta0=args.beta0, lam=lam, x_clean=x_gt,
                                measure_every=args.measure_every, verbose=True)
            wall = time.perf_counter() - t0
            out_path = os.path.join(RESULT_DIR,
                                    f"theory_{blur_name}_{mode}.csv")
            write_trace_csv(out_path, out.trace)
            tr = out.trace
            row = {
                "config": f"{blur_name}_{mode}",
                "blur": blur_name, "mode": mode,
                "K": args.K, "size": args.size, "beta0": args.beta0,
                "L": f"{L:.6f}", "lambda": f"{lam:.6f}",
                "psnr_final": f"{tr['psnr'][-1].mean().item():.4f}",
                "resid_final": f"{tr['resid'][-1].mean().item():.6e}",
                "e_final": f"{tr['e_abs'][-1].mean().item():.6e}",
                "total_inner": out.total_inner,
                "time_alg_s": f"{out.time_alg:.3f}",
                "time_total_s": f"{wall:.3f}",
            }
            rows.append(row)
            print(f"    -> {out_path} | PSNR={row['psnr_final']} dB | "
                  f"resid={row['resid_final']} | tổng bước nội={out.total_inner} "
                  f"| t_alg={row['time_alg_s']}s (t_total={row['time_total_s']}s)")

    sum_path = os.path.join(RESULT_DIR, "summary.csv")
    with open(sum_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print(f"\n-> tổng hợp: {sum_path}")

    print("\n" + "=" * 88)
    print(f"{'cấu hình':<18s} {'PSNR(dB)':>9s} {'phần dư cuối':>13s} "
          f"{'e_k cuối':>12s} {'tổng nội':>9s} {'t_alg(s)':>9s}")
    print("-" * 88)
    for r in rows:
        print(f"{r['config']:<18s} {r['psnr_final']:>9s} {r['resid_final']:>13s} "
              f"{r['e_final']:>12s} {r['total_inner']:>9d} {r['time_alg_s']:>9s}")
    print("=" * 88)


if __name__ == "__main__":
    main()
