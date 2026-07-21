"""Sinh ba hình dữ liệu của báo cáo từ tệp kết quả, để chúng tái lập được.

Ba hình:
  Hình 6.1  certificate_check.csv   chứng chỉ là chặn trên của sai số thật
  Hình 7.1  grid_fair_*_pareto.csv  đường đánh đổi chi phí theo mức phần dư
  Hình 7.2  summability_*.csv       độ dốc tổng được, có bước neo so với không

Hình 9.1 là sơ đồ khái niệm vẽ tay, giữ ở hinh/hinh_9_1_so_do.png, nên chương trình
này không sinh nó và không đè lên nó.

Nguyên tắc trình bày, để hình đọc được cả khi in đen trắng:
  - phông Times New Roman, khớp phần chữ của báo cáo;
  - bảng màu Okabe-Ito, vốn an toàn với người mù màu;
  - mỗi đường phân biệt thêm bằng kiểu nét và dấu điểm, không chỉ bằng màu;
  - lưới mờ và mảnh, trục gọn.

    python tai_lieu_bai_bao/bao_cao/sinh_hinh.py
"""

from __future__ import annotations

import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Dấu thập phân trong báo cáo là dấu phẩy, nên số trên trục cũng phải dùng dấu phẩy.
PHAY = FuncFormatter(lambda v, _: ("%g" % v).replace(".", ","))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KET_QUA = os.path.join(HERE, "..", "..", "results", "theory")
HINH = os.path.join(HERE, "hinh")

# Bảng màu Okabe-Ito: xanh dương cho phép chiếu chính xác hoặc chặn trên, đỏ cam cho
# chế độ thích nghi hoặc sai số thật, xám cho đường tham chiếu.
XANH = "#0072B2"
CAM = "#D55E00"
XAM = "#666666"


def dat_kieu():
    plt.rcParams.update({
        "font.family": "Times New Roman",
        "font.size": 11,
        "axes.unicode_minus": True,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#333333",
        "axes.grid": True,
        "grid.color": "#DDDDDD",
        "grid.linewidth": 0.6,
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def doc(ten):
    with open(os.path.join(KET_QUA, ten), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def luu(fig, ten):
    os.makedirs(HINH, exist_ok=True)
    p = os.path.join(HINH, ten)
    fig.savefig(p)
    plt.close(fig)
    print(f"-> {os.path.relpath(p, os.path.join(HERE, '..', '..'))}")


def hinh_6_1():
    """Chặn trên từ chứng chỉ và sai số thật, cả hai theo số bước nội."""
    r = doc("certificate_check.csv")
    x = [int(d["so_buoc_noi"]) for d in r]
    tren = [float(d["chan_tren"]) for d in r]
    that = [float(d["sai_so_that"]) for d in r]

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.fill_between(x, that, tren, color=XANH, alpha=0.08, zorder=1)
    ax.plot(x, tren, color=XANH, lw=2, ls="-", marker="o", ms=6,
            label="Chặn trên từ chứng chỉ", zorder=3)
    ax.plot(x, that, color=CAM, lw=2, ls="--", marker="s", ms=6,
            label="Sai số thật", zorder=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Số bước nội")
    ax.set_ylabel("Giá trị (thang lôgarit)")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(True, which="both", alpha=0.5)
    luu(fig, "hinh_6_1_chung_chi.png")


def hinh_7_1():
    """Chi phí để đạt từng mức phần dư, chế độ thích nghi so với phép chiếu chính xác,
    hai loại mờ trình bày thành hai khung cạnh nhau."""
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.4), sharey=True)
    for ax, mo, ten in zip(axs, ("gauss", "motion"), ("Mờ Gauss", "Mờ chuyển động")):
        r = doc(f"grid_fair_{mo}_pareto.csv")
        x = [float(d["muc_phan_du"]) for d in r]
        cx = [int(d["buoc_noi_chieu_chinh_xac"]) for d in r]
        tn = [int(d["buoc_noi_thich_nghi"]) for d in r]
        ax.plot(x, cx, color=XANH, lw=2, ls="-", marker="o", ms=6,
                label="Phép chiếu chính xác")
        ax.plot(x, tn, color=CAM, lw=2, ls="--", marker="s", ms=6,
                label="Chế độ thích nghi")
        ax.set_yscale("log")
        ax.invert_xaxis()          # mức phần dư nhỏ dần, tức yêu cầu chặt dần
        ax.set_title(ten, fontsize=11)
        ax.set_xlabel("Mức phần dư biến phân")
        ax.xaxis.set_major_formatter(PHAY)
        ax.grid(True, which="both", alpha=0.5)
    axs[0].set_ylabel("Tổng bước nội (thang lôgarit)")
    axs[1].legend(frameon=False, loc="upper left")
    fig.tight_layout()
    luu(fig, "hinh_7_1_chi_phi.png")


def hinh_7_2():
    """Độ dốc tổng được của bốn cấu hình, so với ngưỡng phân kỳ âm một."""
    diem = []
    for mo, ten in (("gauss", "Mờ Gauss"), ("motion", "Mờ chuyển động")):
        for d in doc(f"summability_{mo}.csv"):
            co_neo = float(d["beta0"]) > 0
            diem.append((ten, co_neo, float(d["doc_proj_disp"])))

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    nhom = ["Mờ Gauss", "Mờ chuyển động"]
    ax.axhline(-1.0, color=XAM, lw=1.4, ls=":", zorder=1)
    ax.text(1.5, -1.0, "  ngưỡng phân kỳ", color=XAM, va="center", fontsize=10)
    for co_neo, mau, dau, nhan in ((False, XANH, "o", "Không có bước neo"),
                                   (True, CAM, "s", "Có bước neo")):
        xs = [nhom.index(t) for t, c, _ in diem if c == co_neo]
        ys = [v for _, c, v in diem if c == co_neo]
        ax.scatter(xs, ys, color=mau, marker=dau, s=90, zorder=3, label=nhan)
        for x, y in zip(xs, ys):
            ax.annotate(f"{y:.3f}".replace(".", ","), (x, y),
                        textcoords="offset points", xytext=(0, 10),
                        ha="center", fontsize=10, color=mau)
    ax.set_xticks(range(len(nhom)))
    ax.set_xticklabels(nhom)
    ax.set_xlim(-0.5, 1.9)
    ax.set_ylim(-3.2, -0.4)
    ax.set_ylabel("Độ dốc lôgarit của dịch chuyển bước chiếu")
    ax.yaxis.set_major_formatter(PHAY)
    ax.legend(frameon=False, loc="lower left")
    ax.grid(True, axis="y", alpha=0.5)
    luu(fig, "hinh_7_2_tong_duoc.png")


def main():
    dat_kieu()
    hinh_6_1()
    hinh_7_1()
    hinh_7_2()
    # Hình 9.1 là sơ đồ vẽ tay, không sinh ở đây.


if __name__ == "__main__":
    main()
