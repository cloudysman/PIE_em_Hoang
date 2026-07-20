"""Kiểm chứng chỉ sai số tính được, và đo cái giá của một tiêu chuẩn kiểm được.

Hai phép đo, tương ứng hai mục của báo cáo:

  1. Chặn trên có hợp lệ không. Ở nhiều mức số bước nội, so chặn trên lấy từ chứng chỉ
     với sai số thật đo bằng cách so với một nghiệm chiếu tham chiếu chạy rất dài.
     Chứng chỉ chỉ dùng được nếu nó KHÔNG BAO GIỜ đánh giá thấp sai số thật.

  2. Cái giá phải trả. So số bước nội khi dừng theo chứng chỉ với số bước nội khi dừng
     theo sai số thật. Sai số thật không biết được trong thực thi, nên tỉ số giữa hai
     con số chính là cái giá của một tiêu chuẩn kiểm được.

Kết quả ghi vào results/theory/, dùng làm nguồn đối chiếu cho báo cáo.

    python test_certificate.py
"""

from __future__ import annotations

import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import torch

from pie_net.constraints import TVBallConstraint, tv_isotropic
from pie_net.data import make_patches

OUT = os.path.join("results", "theory")
MUC_BUOC = (5, 10, 25, 50, 100, 250, 500, 1500)
MUC_EPS = (1.0, 0.5, 0.2, 0.1, 0.05)


def chuan_bi(size=48, n=2, seed=1):
    torch.manual_seed(0)
    _, x = make_patches(patch=size, n_train=2, n_test=n, seed=seed)
    x = x.to(torch.float32)
    tau = (0.5 * tv_isotropic(x)).detach()
    v = x + 0.25 * torch.randn_like(x)
    cons = TVBallConstraint(tau=tau, box=None)
    return cons, v, cons.tau.view(v.shape[0])


def do_chan_tren(cons, v, tau, ref):
    """Phép đo 1: chặn trên từ chứng chỉ có luôn lớn hơn sai số thật không."""
    rows, hop_le = [], True
    for n in MUC_BUOC:
        x, p = cons.project(v, tol=0.0, max_inner=n).state
        bound, xf = cons.error_bound(x, p, v, tau)
        err = (xf - ref).flatten(1).norm(dim=1)
        gap, _ = cons.duality_gap(x, p, v, tau)
        ok = bool(torch.all(bound >= err - 1e-6))
        hop_le = hop_le and ok
        rows.append({
            "so_buoc_noi": n,
            "khoang_cach_doi_ngau": f"{gap.mean().item():.6e}",
            "chan_tren": f"{bound.mean().item():.6e}",
            "sai_so_that": f"{err.mean().item():.6e}",
            "ti_so": f"{(bound / err.clamp_min(1e-12)).mean().item():.2f}",
            "hop_le": "co" if ok else "KHONG",
        })
    return rows, hop_le


def do_cai_gia(cons, v, tau, ref):
    """Phép đo 2: dừng theo chứng chỉ tốn hơn dừng theo sai số thật bao nhiêu lần."""
    rows = []
    for eps in MUC_EPS:
        n_cc = cons.project_to_bound(v, eps, cap=30000).n_inner
        # số bước để SAI SỐ THẬT đạt eps; không tính được trong thực thi, chỉ để đối chiếu
        x, p = cons._init(v, None)
        xbar = x.clone()
        t, sg = cons.t, cons.sigma
        n_that = 0
        while n_that < 30000:
            e = (cons.make_feasible(x, tau) - ref).flatten(1).norm(dim=1)
            if torch.all(e <= eps):
                break
            x, xbar, p, t, sg = cons._step(x, xbar, p, v, tau, t, sg)
            n_that += 1
        rows.append({
            "muc_sai_so": f"{eps:.2f}",
            "buoc_noi_theo_chung_chi": n_cc,
            "buoc_noi_theo_sai_so_that": n_that,
            "cai_gia": f"{n_cc / max(n_that, 1):.2f}",
        })
    return rows


def ghi(ten, rows):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, ten)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"-> {p}")


def main():
    cons, v, tau = chuan_bi()
    print("Tính nghiệm chiếu tham chiếu (30000 bước nội) ...")
    ref = cons.project(v, tol=0.0, max_inner=30000).x
    print(f"   biến phân toàn phần của nghiệm tham chiếu trên bán kính = "
          f"{(tv_isotropic(ref) / tau).mean().item():.5f}")

    print("\nPhép đo 1: chặn trên có hợp lệ không")
    print(f"{'bước nội':>9s} {'chặn trên':>12s} {'sai số thật':>12s} {'tỉ số':>7s} {'hợp lệ':>7s}")
    rows1, hop_le = do_chan_tren(cons, v, tau, ref)
    for r in rows1:
        print(f"{r['so_buoc_noi']:>9d} {float(r['chan_tren']):>12.4e} "
              f"{float(r['sai_so_that']):>12.4e} {r['ti_so']:>7s} {r['hop_le']:>7s}")
    print(f"=> chặn trên hợp lệ ở mọi mức: {'có' if hop_le else 'KHÔNG'}")
    ghi("certificate_check.csv", rows1)

    print("\nPhép đo 2: cái giá của một tiêu chuẩn kiểm được")
    print(f"{'mức sai số':>11s} {'theo chứng chỉ':>15s} {'theo sai số thật':>17s} {'cái giá':>8s}")
    rows2 = do_cai_gia(cons, v, tau, ref)
    for r in rows2:
        print(f"{r['muc_sai_so']:>11s} {r['buoc_noi_theo_chung_chi']:>15d} "
              f"{r['buoc_noi_theo_sai_so_that']:>17d} {r['cai_gia']:>7s}x")
    gia = [float(r["cai_gia"]) for r in rows2]
    print(f"=> cái giá nằm trong khoảng {min(gia):.2f} đến {max(gia):.2f} lần")
    ghi("certificate_cost.csv", rows2)


if __name__ == "__main__":
    main()
