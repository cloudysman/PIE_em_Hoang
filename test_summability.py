"""Phép thử quyết định: dãy sai số dưới tiêu chuẩn tương đối có tổng được không?

Cả tính mới của bài treo vào câu hỏi này. Tiêu chuẩn tương đối theo dịch chuyển đặt
eps_k = c * ||y^{k-1} - w^{k-1}||, nên dãy sai số tổng được khi và chỉ khi tổng các
dịch chuyển ||y^k - w^k|| hữu hạn.

Lo ngại cụ thể cần bác hoặc xác nhận: bước neo áp đặt dịch chuyển cỡ beta_k = beta0/(k+1),
mà tổng các beta_k phân kỳ. Nếu dịch chuyển của phép chiếu cũng giảm như 1/k thì tổng
phân kỳ và dãy sai số KHÔNG tổng được, tức cửa tính mới đóng lại.

Phép thử: chạy dài, đo độ dốc log-log của ||y^k - w^k|| ở đuôi. Độ dốc nhỏ hơn -1 nghĩa
là tổng hội tụ; độ dốc lớn hơn hoặc bằng -1 nghĩa là phân kỳ. Kiểm chéo bằng cách so
tổng tích lũy ở K và 2K: nếu hội tụ thì tổng phải bão hòa.

    python test_summability.py --device cuda --K 600
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

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

OUT = os.path.join("results", "theory")


def doc_log_log(y, lo_frac=0.5):
    k = np.arange(1, len(y) + 1, dtype=float)
    lo = int(len(y) * lo_frac)
    kk, yy = k[lo:], y[lo:]
    m = np.isfinite(yy) & (yy > 1e-14)
    if m.sum() < 5:
        return float("nan")
    return float(np.polyfit(np.log(kk[m]), np.log(yy[m]), 1)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=600)
    ap.add_argument("--size", type=int, default=64)
    ap.add_argument("--n_test", type=int, default=4)
    ap.add_argument("--beta0", type=float, default=0.05)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--blur", default="gauss", choices=["gauss", "motion"])
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    dev = args.device
    torch.manual_seed(0)
    _, x_test = make_patches(patch=args.size, n_train=2, n_test=args.n_test, seed=1)
    x_gt = x_test.to(dev, torch.float32)
    tau = (0.55 * tv_isotropic(x_gt)).detach()
    blur = (BlurOperator(gaussian_kernel(9, 1.6)) if args.blur == "gauss"
            else BlurOperator(motion_kernel(9, 30.0))).to(dev)
    y = degrade(x_gt, blur, noise_std=0.05, seed=2024)
    L = power_iteration_L(blur, (1, 1, args.size, args.size), n_iter=100, device=dev)
    lam = 0.9 * (2.0 ** 0.5 - 1.0) / max(L, 1e-12)
    print(f"== phép thử tính tổng được | blur={args.blur} | K={args.K} | beta0={args.beta0} ==")

    # Chạy với ngân sách cố định nhỏ để mỗi bước ngoài rẻ, vì ta chỉ cần quỹ đạo NGOÀI;
    # dịch chuyển ||y-w|| là tính chất của sơ đồ ngoài, không phụ thuộc chế độ dừng nội.
    rows = []
    for beta0 in (args.beta0, 0.0):
        out = run_reflected(blur, y, tau, K=args.K, budget=Budget(kind="fixed", m=3),
                            beta0=beta0, lam=lam, x_clean=x_gt, alpha_bar=0.0,
                            measure_every=max(args.K, 1),  # bỏ phép đo đắt
                            ref_steps=200, resid_cap=200, verbose=False)
        pd = np.nanmean(out.trace["proj_disp"].numpy(), axis=1)
        dl = np.nanmean(out.trace["delta"].numpy(), axis=1)
        doc_pd, doc_dl = doc_log_log(pd), doc_log_log(dl)
        tong_K = float(np.nansum(pd))
        tong_nua = float(np.nansum(pd[: len(pd) // 2]))
        ty_le = tong_K / max(tong_nua, 1e-12)
        ket = ("TỔNG ĐƯỢC (độ dốc < -1)" if doc_pd < -1.0
               else "PHÂN KỲ (độ dốc >= -1)")
        nhan = f"beta0={beta0}" + (" (có neo)" if beta0 > 0 else " (TẮT neo)")
        print(f"\n[{nhan}]")
        print(f"  độ dốc log-log của ||y-w||   = {doc_pd:.3f}   -> {ket}")
        print(f"  độ dốc log-log của ||x-x_cũ|| = {doc_dl:.3f}")
        print(f"  tổng ||y-w|| tại K/2 = {tong_nua:.4f} | tại K = {tong_K:.4f} | tỉ lệ = {ty_le:.3f}")
        print(f"  (tỉ lệ gần 1 nghĩa là tổng đã bão hòa, tức hội tụ; tỉ lệ lớn nghĩa là còn tăng)")
        rows.append({"beta0": beta0, "doc_proj_disp": f"{doc_pd:.3f}",
                     "doc_delta": f"{doc_dl:.3f}", "tong_nua_K": f"{tong_nua:.4f}",
                     "tong_K": f"{tong_K:.4f}", "ty_le": f"{ty_le:.3f}",
                     "ket_luan": ket})

    p = os.path.join(OUT, f"summability_{args.blur}.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\n-> {p}")
    print("\nDiễn giải: nếu với neo bật mà độ dốc >= -1 thì dãy sai số dưới tiêu chuẩn")
    print("tương đối KHÔNG tổng được, và giả thiết của định lý không thỏa — cửa tính mới đóng.")


if __name__ == "__main__":
    main()
