"""So chi phí giữa chế độ ngân sách thích nghi và chiếu chính xác, theo giao thức công bằng.

Bản trước có ba lỗi phương pháp luận mà vòng phản biện đã bắt; bản này sửa cả ba:

1. Chỉ đếm bước nội. Bước nội của chế độ thích nghi đắt hơn nhiều vì phải tính chứng
   chỉ, nên hệ số theo bước nội thổi phồng lợi thế. Bản này báo CẢ tổng bước nội lẫn
   thời gian THUẬT TOÁN (đã tách khỏi chi phí đo đạc, và đồng bộ hóa trên GPU).
2. Mục tiêu so sánh định nghĩa vòng tròn: mức phần dư mục tiêu lấy từ chính phần dư
   cuối của baseline, tức chọn hậu nghiệm có lợi cho bên thách thức. Bản này dùng một
   danh sách mức phần dư ẤN ĐỊNH TRƯỚC, độc lập với mọi cấu hình.
3. Bất đối xứng ngân sách dò: phương pháp đề xuất được dò 16 cấu hình, baseline chỉ 2.
   Bản này dò baseline trên cùng số cấu hình.

Kết quả báo dưới dạng đường đánh đổi chi phí theo mức phần dư, cho cả hai thước đo.

    python3 grid_schedule.py --device cuda --K 150 --size 96 --n_test 8 --blur gauss
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

# Mức phần dư mục tiêu ẤN ĐỊNH TRƯỚC, độc lập với kết quả của mọi cấu hình.
MUC_TIEU = [3.0e-2, 2.0e-2, 1.5e-2, 1.2e-2, 1.0e-2]


def make_blur(name: str) -> BlurOperator:
    return BlurOperator(gaussian_kernel(9, 1.6) if name == "gauss"
                        else motion_kernel(9, 30.0))


def chi_phi_toi_muc(resid, inner, t_alg_total, K_do, target):
    """Chi phí (bước nội, và thời gian thuật toán ước lượng) tại thời điểm phần dư
    đo được lần đầu đạt mức target. Thời gian được nội suy theo tỉ lệ bước ngoài,
    vì thời gian thuật toán chỉ có ở mức tổng."""
    for i in range(len(resid)):
        if np.isfinite(resid[i]) and resid[i] <= target:
            ti = t_alg_total * (i + 1) / max(K_do, 1)
            return float(inner[i]), float(ti)
    return float("nan"), float("nan")


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
    print(f"== so chi phí, giao thức công bằng | blur={args.blur} | K={args.K} "
          f"| size={args.size} | n_test={args.n_test} | device={dev} ==")
    print(f"   L={L:.6f} -> lambda={lam:.4f}")
    print(f"   mức phần dư mục tiêu (ấn định TRƯỚC): {MUC_TIEU}")

    # Hai nhóm được dò với CÙNG ngân sách: 8 cấu hình mỗi nhóm.
    cfgs = []
    for eps0 in (1.0, 2.0, 4.0, 8.0):
        for p in (1.01, 1.1):
            cfgs.append((f"thich_nghi e{eps0} p{p}", "thich_nghi",
                         Budget(kind="adaptive", eps0=eps0, p=p, cap=args.cap)))
    for ec in (0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.2):
        cfgs.append((f"chieu_chinh_xac {ec}", "chieu_chinh_xac",
                     Budget(kind="exact_bound", eps_const=ec, cap=args.cap)))

    rows, data = [], {}
    for name, nhom, b in cfgs:
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
        data[name] = (nhom, resid, inner, out.time_alg, args.K)
        rows.append({"cau_hinh": name, "nhom": nhom, "psnr": f"{psnr:.4f}",
                     "phan_du_cuoi": f"{rf:.6e}", "tong_buoc_noi": out.total_inner,
                     "thoi_gian_thuat_toan_s": f"{out.time_alg:.3f}",
                     "vi_pham_tv": f"{tv:.4f}",
                     "thoi_gian_tong_s": f"{time.perf_counter()-t0:.1f}"})
        print(f"  {name:>22s} | PSNR={psnr:7.3f} | phần dư={rf:.3e} | "
              f"bước nội={out.total_inner:7d} | t_thuật_toán={out.time_alg:7.2f}s | TV={tv:.4f}")

    # Đường đánh đổi: ở mỗi mức phần dư mục tiêu, lấy cấu hình RẺ NHẤT của mỗi nhóm.
    print("\n=== so sánh công bằng: cấu hình rẻ nhất của mỗi nhóm ở từng mức phần dư ===")
    print(f"{'mức phần dư':>12s} | {'nhóm':>16s} | {'bước nội':>9s} | {'t_thuật_toán(s)':>15s} | {'cấu hình':>22s}")
    ket_qua = []
    for target in MUC_TIEU:
        tot = {}
        for name, (nhom, resid, inner, t_alg, K) in data.items():
            bi, ti = chi_phi_toi_muc(resid, inner, t_alg, K, target)
            if not np.isfinite(bi):
                continue
            if nhom not in tot or bi < tot[nhom][0]:
                tot[nhom] = (bi, ti, name)
        for nhom in ("thich_nghi", "chieu_chinh_xac"):
            if nhom in tot:
                bi, ti, name = tot[nhom]
                print(f"{target:>12.1e} | {nhom:>16s} | {bi:>9.0f} | {ti:>15.2f} | {name:>22s}")
        if len(tot) == 2:
            b_tn, t_tn, _ = tot["thich_nghi"]
            b_cx, t_cx, _ = tot["chieu_chinh_xac"]
            hs_b, hs_t = b_cx / b_tn, t_cx / t_tn
            print(f"{'':>12s} | {'-> hệ số':>16s} | {hs_b:>8.2f}x | {hs_t:>14.2f}x |"
                  f"  (bước nội / THỜI GIAN)")
            ket_qua.append({"muc_phan_du": f"{target:.1e}",
                            "buoc_noi_thich_nghi": f"{b_tn:.0f}",
                            "buoc_noi_chieu_chinh_xac": f"{b_cx:.0f}",
                            "he_so_buoc_noi": f"{hs_b:.2f}",
                            "t_thich_nghi": f"{t_tn:.2f}",
                            "t_chieu_chinh_xac": f"{t_cx:.2f}",
                            "he_so_thoi_gian": f"{hs_t:.2f}"})

    for path, rr in ((f"grid_fair_{args.blur}.csv", rows),
                     (f"grid_fair_{args.blur}_pareto.csv", ket_qua)):
        if rr:
            with open(os.path.join(OUT_DIR, path), "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(rr[0].keys()))
                w.writeheader(); w.writerows(rr)
            print(f"-> {os.path.join(OUT_DIR, path)}")


if __name__ == "__main__":
    main()
