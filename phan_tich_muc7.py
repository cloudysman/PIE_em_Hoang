"""Rút các con số của mục 7 báo cáo từ tệp kết quả, để mọi con số đều truy nguồn được.

Bốn nhóm số:

  1. Hệ số tiết kiệm của chế độ thích nghi so với phép chiếu chính xác, ở năm mức
     phần dư ấn định trước. Lấy từ grid_fair_*_pareto.csv.
  2. Mức khả thi: biến phân toàn phần của đầu ra chia bán kính, lớn nhất trên toàn
     bộ cấu hình. Lớn hơn một nghĩa là vi phạm ràng buộc.
  3. Chi phí của lịch quá siết: cấu hình xấu nhất trong lưới lịch đầy đủ tốn hơn
     mốc phép chiếu chính xác bao nhiêu lần.
  4. Độ nhạy theo lịch trong lưới công bằng: cấu hình thích nghi đắt nhất so với rẻ nhất.

Kết quả ghi vào results/theory/muc7_*.csv.

    python phan_tich_muc7.py
"""

from __future__ import annotations

import csv
import glob
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TH = os.path.join("results", "theory")


def doc(ten):
    with open(os.path.join(TH, ten), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ghi(ten, rows):
    p = os.path.join(TH, ten)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"-> {p}")


def he_so(mo: str):
    """Nhóm 1: hệ số tiết kiệm ở từng mức phần dư."""
    rows = doc(f"grid_fair_{mo}_pareto.csv")
    ra = []
    for r in rows:
        ra.append({
            "muc_phan_du": r["muc_phan_du"],
            "buoc_noi_chieu_chinh_xac": r["buoc_noi_chieu_chinh_xac"],
            "giay_chieu_chinh_xac": r["t_chieu_chinh_xac"],
            "buoc_noi_thich_nghi": r["buoc_noi_thich_nghi"],
            "giay_thich_nghi": r["t_thich_nghi"],
            "he_so_buoc_noi": r["he_so_buoc_noi_thich_nghi"],
            "he_so_thoi_gian": r["he_so_thoi_gian_thich_nghi"],
        })
    return ra


def khoang(ra, cot, bo_muc=()):
    v = [float(r[cot]) for r in ra if r["muc_phan_du"] not in bo_muc]
    return min(v), max(v)


def kha_thi():
    """Nhóm 2: mức khả thi của ĐẦU RA lớn nhất trên mọi tệp kết quả có cột tương ứng.

    Các tệp quỹ đạo ghi mọi bước ngoài, mà những bước đầu thì chưa khả thi; chỉ bước
    ngoài cuối cùng của mỗi ảnh mới là đầu ra, nên chỉ những dòng đó được xét."""
    ra = []
    for p in sorted(glob.glob(os.path.join(TH, "*.csv"))):
        with open(p, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        cot = next((c for c in rows[0] if c in ("vi_pham_tv", "tv_ratio")), None)
        if cot is None:
            continue
        if "k" in rows[0] and "img" in rows[0]:
            cuoi = {}
            for r in rows:
                anh = r["img"]
                if anh not in cuoi or int(r["k"]) > int(cuoi[anh]["k"]):
                    cuoi[anh] = r
            rows = list(cuoi.values())
        v = [float(r[cot]) for r in rows if r.get(cot)]
        ra.append({
            "tep": os.path.basename(p),
            "so_cau_hinh": len(v),
            "muc_kha_thi_lon_nhat": f"{max(v):.6f}",
            "vi_pham": "co" if max(v) > 1.0 + 1e-4 else "khong",
        })
    return ra


def lich_qua_siet(mo: str):
    """Nhóm 3: cấu hình xấu nhất tốn hơn mốc phép chiếu chính xác bao nhiêu lần."""
    rows = doc(f"grid_schedule_{mo}.csv")
    moc = next(r for r in rows if r["cau_hinh"].startswith("exact_bound 0.02"))
    n_moc = int(moc["buoc_toi_muc_tieu"])
    ra = []
    for r in rows:
        if not r["cau_hinh"].startswith("adaptive"):
            continue
        b = r["buoc_toi_muc_tieu"]
        if not b.isdigit():
            continue
        n = int(b)
        ra.append({
            "cau_hinh": r["cau_hinh"],
            "buoc_noi_toi_muc_tieu": n,
            "buoc_noi_cua_moc": n_moc,
            "lan_so_voi_moc": f"{n / n_moc:.2f}",
        })
    ra.sort(key=lambda r: -float(r["lan_so_voi_moc"]))
    return ra


def do_nhay(mo: str):
    """Nhóm 4: trong lưới công bằng, cấu hình thích nghi đắt nhất so với rẻ nhất."""
    rows = [r for r in doc(f"grid_fair_{mo}.csv") if r["nhom"] == "thich_nghi"]
    b = [(int(r["tong_buoc_noi"]), r["cau_hinh"]) for r in rows]
    lo, hi = min(b), max(b)
    return {
        "re_nhat": lo[1], "buoc_noi_re_nhat": lo[0],
        "dat_nhat": hi[1], "buoc_noi_dat_nhat": hi[0],
        "lan": f"{hi[0] / lo[0]:.0f}",
    }


def main():
    print("Nhóm 1: hệ số tiết kiệm của chế độ thích nghi\n")
    for mo, ten in (("gauss", "mờ Gauss"), ("motion", "mờ chuyển động")):
        ra = he_so(mo)
        print(f"  {ten}")
        print(f"  {'phần dư':>9s} {'chính xác':>18s} {'thích nghi':>18s} "
              f"{'hệ số bước':>11s} {'hệ số giây':>11s}")
        for r in ra:
            print(f"  {r['muc_phan_du']:>9s} "
                  f"{r['buoc_noi_chieu_chinh_xac']:>8s} / {r['giay_chieu_chinh_xac']:>6s}s "
                  f"{r['buoc_noi_thich_nghi']:>8s} / {r['giay_thich_nghi']:>6s}s "
                  f"{r['he_so_buoc_noi']:>11s} {r['he_so_thoi_gian']:>11s}")
        bo = ("1.0e-02",) if mo == "motion" else ()
        kb = khoang(ra, "he_so_buoc_noi", bo)
        kt = khoang(ra, "he_so_thoi_gian", bo)
        ghi_chu = " (bốn mức đầu; mức chặt nhất tách riêng)" if bo else ""
        print(f"  => bước nội {kb[0]:.1f} đến {kb[1]:.1f} lần, "
              f"thời gian {kt[0]:.1f} đến {kt[1]:.1f} lần{ghi_chu}\n")
        ghi(f"muc7_he_so_{mo}.csv", ra)

    print("\nNhóm 2: mức khả thi lớn nhất trên mọi cấu hình")
    ra = kha_thi()
    tong = sum(int(r["so_cau_hinh"]) for r in ra)
    lon_nhat = max(float(r["muc_kha_thi_lon_nhat"]) for r in ra)
    co_vp = [r["tep"] for r in ra if r["vi_pham"] == "co"]
    print(f"  {tong} cấu hình trong {len(ra)} tệp, mức khả thi lớn nhất = {lon_nhat:.6f}")
    print(f"  số tệp có vi phạm vượt ngưỡng 1e-4: {len(co_vp)}")
    ghi("muc7_kha_thi.csv", ra)

    print("\nNhóm 3: chi phí của lịch quá siết")
    for mo, ten in (("gauss", "mờ Gauss"), ("motion", "mờ chuyển động")):
        ra = lich_qua_siet(mo)
        xau = ra[0]
        print(f"  {ten}: xấu nhất là {xau['cau_hinh']}, tốn "
              f"{xau['buoc_noi_toi_muc_tieu']} bước nội so với {xau['buoc_noi_cua_moc']} "
              f"của mốc, tức {xau['lan_so_voi_moc']} lần")
        ghi(f"muc7_lich_{mo}.csv", ra)

    print("\nNhóm 4: độ nhạy theo lịch trong lưới công bằng")
    ra = []
    for mo, ten in (("gauss", "mờ Gauss"), ("motion", "mờ chuyển động")):
        d = do_nhay(mo)
        d["loai_mo"] = ten
        print(f"  {ten}: {d['buoc_noi_re_nhat']} bước ({d['re_nhat']}) so với "
              f"{d['buoc_noi_dat_nhat']} bước ({d['dat_nhat']}), chênh {d['lan']} lần")
        ra.append(d)
    ghi("muc7_do_nhay.csv", ra)


if __name__ == "__main__":
    main()
