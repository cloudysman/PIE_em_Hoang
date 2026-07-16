"""Dò lịch sai số cho chế độ ngân sách thích nghi, và so với các chế độ khác.

Chế độ thích nghi dừng vòng lặp nội theo chứng chỉ tính được sqrt(2*gap) <= eps_k
với lịch eps_k = eps0/(k+1)^p. Lịch càng siết (p lớn, eps0 nhỏ) thì sai số càng
nhỏ nhưng càng tốn bước nội; câu hỏi là cấu hình nào cho chi phí thấp nhất ở cùng
mức phần dư biến phân. Điều kiện tổng được đòi p > 1.

Chạy được trên GPU. Ví dụ:
    python3 grid_schedule.py --device cuda --K 150 --size 96 --n_test 8
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

import numpy as np
import torch

from pie_net.constraints import tv_isotropic
from pie_net.data import make_patches, degrade
from pie_net.operators import BlurOperator, gaussian_kernel, motion_kernel
from pie_net.reflected_solver import Budget, power_iteration_L, run_reflected

OUT_DIR = os.path.join("results", "theory")


def make_blur(name: str) -> BlurOperator:
    return BlurOperator(gaussian_kernel(9, 1.6) if name == "gauss"
                        else motion_kernel(9, 30.0))


def inner_to_target(resid, inner, target):
    """Tổng bước nội cộng dồn tại thời điểm phần dư (đo được) lần đầu <= target."""
    for i in range(len(resid)):
        if np.isfinite(resid[i]) and resid[i] <= target:
            return float(inner[i])
    return float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=150)
    ap.add_argument("--size", type=int, default=96)
    ap.add_argument("--n_test", type=int, default=8)
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--tau_frac", type=float, default=0.55)
    ap.add_argument("--beta0", type=float, default=0.05)
    ap.add_argument("--measure_every", type=int, default=5)
    ap.add_argument("--blur", default="gauss", choices=["gauss", "motion"])
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--cap", type=int, default=4000)
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    dev = args.device
    torch.manual_seed(0)
    _, x_test = make_patches(patch=args.size, n_train=2, n_test=args.n_test, seed=1)
    x_gt = x_test.to(dev, torch.float32)
    tau = (args.tau_frac * tv_isotropic(x_gt)).detach()
    blur = make_blur(args.blur).to(dev)
    y = degrade(x_gt, blur, noise_std=args.noise, seed=2024)
    L = power_iteration_L(blur, (1, 1, args.size, args.size), n_iter=100, device=dev)
    lam = 0.9 * (2.0 ** 0.5 - 1.0) / max(L, 1e-12)
    print(f"== dò lịch sai số | blur={args.blur} | K={args.K} | size={args.size} "
          f"| n_test={args.n_test} | device={dev} ==")
    print(f"   L={L:.6f} -> lambda={lam:.4f}")

    # lịch thích nghi: p > 1 để dãy sai số tổng được
    cfgs = []
    for eps0 in (0.5, 1.0, 2.0, 4.0):
        for p in (1.01, 1.05, 1.1, 1.5):
            cfgs.append((f"adaptive e{eps0}_p{p}",
                         Budget(kind="adaptive", eps0=eps0, p=p, cap=args.cap)))
    # mốc đối chiếu: chiếu chính xác theo chứng chỉ (cùng thế giới tính được)
    for ec in (0.02, 0.05):
        cfgs.append((f"exact_bound {ec}",
                     Budget(kind="exact_bound", eps_const=ec, cap=args.cap)))

    rows, curves = [], {}
    for name, b in cfgs:
        t0 = time.perf_counter()
        out = run_reflected(blur, y, tau, K=args.K, budget=b, beta0=args.beta0,
                            lam=lam, x_clean=x_gt, alpha_bar=0.0,
                            measure_every=args.measure_every,
                            ref_steps=800, resid_cap=2000, verbose=False)
        tr = out.trace
        resid = np.nanmean(tr["resid"].numpy(), axis=1)
        inner = np.nanmean(tr["inner_cum"].numpy(), axis=1)
        psnr = np.nanmean(tr["psnr"].numpy(), axis=1)[-1]
        tv = np.nanmean(tr["tv_ratio"].numpy(), axis=1)[-1]
        rf = resid[np.isfinite(resid)][-1]
        curves[name] = (resid, inner)
        rows.append({"cau_hinh": name, "psnr": f"{psnr:.4f}",
                     "phan_du_cuoi": f"{rf:.6e}", "tong_buoc_noi": out.total_inner,
                     "vi_pham_tv": f"{tv:.4f}", "giay": f"{time.perf_counter()-t0:.1f}"})
        print(f"  {name:>22s} | PSNR={psnr:7.3f} | phần dư={rf:.4e} | "
              f"bước nội={out.total_inner:6d} | TV={tv:.4f} | {rows[-1]['giay']}s")

    # bảng chi phí: mốc là chiếu chính xác theo chứng chỉ chặt nhất
    base_name = "exact_bound 0.02"
    base_resid = float(rows[[r["cau_hinh"] for r in rows].index(base_name)]["phan_du_cuoi"])
    target = base_resid * 1.05
    base_inner = inner_to_target(*curves[base_name], target)
    print(f"\n=== chi phí để đạt phần dư <= {target:.4e} (mốc: {base_name} = {base_inner:.0f} bước) ===")
    for r in rows:
        v = inner_to_target(*curves[r["cau_hinh"]], target)
        r["buoc_toi_muc_tieu"] = f"{v:.0f}" if np.isfinite(v) else "khong dat"
        r["re_hon_moc"] = (f"{base_inner/v:.2f}x" if np.isfinite(v) and v > 0
                           and np.isfinite(base_inner) else "-")
        print(f"  {r['cau_hinh']:>22s}: {r['buoc_toi_muc_tieu']:>10s}  {r['re_hon_moc']}")

    path = os.path.join(OUT_DIR, f"grid_schedule_{args.blur}.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"\n-> {path}")


if __name__ == "__main__":
    main()
