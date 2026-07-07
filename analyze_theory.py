"""Phân tích số liệu của sơ đồ phản xạ bốn pha (results/theory/theory_*.csv).

Tính ba nhóm đại lượng phục vụ bài báo:
  1. Độ dốc log-log của dịch chuyển delta_k = ||x^{k+1}-x^k|| — kiểm chứng số cho
     nhận định rằng bước độ nhớt áp đặt dịch chuyển cỡ beta_k = beta0/(k+1), tức
     độ dốc gần -1; hệ quả: ngân sách bước nội CỐ ĐỊNH không cho dãy sai số tổng
     được (phải dùng ngân sách tăng theo log).
  2. Tính tổng được của sai số chiếu e_k: tổng tích lũy trên các điểm đo, so sánh
     giữa ngân sách cố định (m1/m2/m5) và ngân sách log (mlog).
  3. Bảng chi phí: tổng bước nội để đạt cùng mức phần dư biến phân, so giữa các
     chế độ ngân sách và chiếu chính xác khởi tạo ấm (hệ số tiết kiệm).
"""

from __future__ import annotations

import csv
import glob
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

DIR = os.path.join("results", "theory")
KEYS = ["e_abs", "e_rel", "delta", "resid", "psnr", "inner_k",
        "inner_cum", "tv_ratio", "ref_check", "alpha", "beta", "m_k"]


def load(path):
    """Đọc CSV vết -> dict cột -> ma trận (K, B). Trả về theo từng ảnh."""
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    ks = sorted({int(r["k"]) for r in rows})
    bs = sorted({int(r["img"]) for r in rows})
    K, B = len(ks), len(bs)
    out = {key: np.full((K, B), np.nan) for key in KEYS}
    for r in rows:
        ki, bi = ks.index(int(r["k"])), bs.index(int(r["img"]))
        for key in KEYS:
            out[key][ki, bi] = float(r[key])
    return out, K, B


def mean_over_img(mat):
    """Trung bình theo ảnh, bỏ NaN."""
    return np.nanmean(mat, axis=1)


def loglog_slope(y, lo_frac=0.5):
    """Độ dốc log-log trên đoạn cuối, bỏ NaN và giá trị không dương."""
    k = np.arange(1, len(y) + 1, dtype=float)
    lo = int(len(y) * lo_frac)
    kk, yy = k[lo:], y[lo:]
    m = np.isfinite(yy) & (yy > 1e-14)
    if m.sum() < 3:
        return float("nan")
    return float(np.polyfit(np.log(kk[m]), np.log(yy[m]), 1)[0])


def cum_at_measured(y):
    """Tổng tích lũy trên các điểm đo (bỏ NaN) — đại diện xu hướng tổng được."""
    yy = y[np.isfinite(y)]
    return float(np.nansum(yy)), int(yy.size)


def inner_to_resid(inner_cum, resid, target):
    """Tổng bước nội cộng dồn tại thời điểm phần dư (đo được) lần đầu <= target."""
    for i in range(len(resid)):
        if np.isfinite(resid[i]) and resid[i] <= target:
            return float(inner_cum[i]), i
    return float("nan"), -1


def analyze_blur(blur):
    files = sorted(glob.glob(os.path.join(DIR, f"theory_{blur}_*.csv")))
    if not files:
        return None
    data = {}
    for f in files:
        mode = os.path.basename(f)[len(f"theory_{blur}_"):-4]
        data[mode] = load(f)

    lines = [f"## Mờ {blur}"]
    lines.append("")
    lines.append("### Độ dốc log-log (nửa cuối quỹ đạo)")
    lines.append("")
    lines.append("| chế độ | dốc delta_k | dốc e_k | dốc phần dư | phần dư cuối | tổng bước nội |")
    lines.append("|---|---|---|---|---|---|")
    resid_curves = {}
    for mode, (d, K, B) in data.items():
        delta = mean_over_img(d["delta"])
        e = mean_over_img(d["e_abs"])
        resid = mean_over_img(d["resid"])
        resid_curves[mode] = (mean_over_img(d["inner_cum"]), resid)
        total_inner = np.nanmax(d["inner_cum"])
        rf = resid[np.isfinite(resid)]
        lines.append(f"| {mode} | {loglog_slope(delta):.3f} | "
                     f"{loglog_slope(e):.3f} | {loglog_slope(resid):.3f} | "
                     f"{(rf[-1] if rf.size else float('nan')):.3e} | {total_inner:.0f} |")

    # tính tổng được của e_k
    lines.append("")
    lines.append("### Tổng tích lũy sai số chiếu e_k (trên điểm đo)")
    lines.append("")
    lines.append("| chế độ | tổng e_k (điểm đo) | số điểm | e_k cuối |")
    lines.append("|---|---|---|---|")
    for mode, (d, K, B) in data.items():
        e = mean_over_img(d["e_abs"])
        s, n = cum_at_measured(e)
        ef = e[np.isfinite(e)]
        lines.append(f"| {mode} | {s:.3f} | {n} | "
                     f"{(ef[-1] if ef.size else float('nan')):.3e} |")

    # bảng chi phí: dùng phần dư mục tiêu = phần dư cuối của 'exact' (nếu có),
    # nếu không, lấy trung vị phần dư cuối các chế độ.
    finals = []
    for mode, (d, K, B) in data.items():
        r = mean_over_img(d["resid"])
        r = r[np.isfinite(r)]
        if r.size:
            finals.append(r[-1])
    target = None
    if "exact" in data:
        r = mean_over_img(data["exact"][0]["resid"])
        r = r[np.isfinite(r)]
        target = float(r[-1] * 1.05) if r.size else None   # nới 5% cho công bằng
    if target is None and finals:
        target = float(np.median(finals))

    if target is not None:
        lines.append("")
        lines.append(f"### Bảng chi phí: tổng bước nội để đạt phần dư <= {target:.3e}")
        lines.append("")
        lines.append("| chế độ | tổng bước nội tới mục tiêu | hệ số so exact |")
        lines.append("|---|---|---|")
        base = None
        rows = {}
        for mode, (ic, resid) in resid_curves.items():
            val, idx = inner_to_resid(ic, resid, target)
            rows[mode] = val
            if mode == "exact":
                base = val
        for mode, val in rows.items():
            ratio = (f"{base/val:.2f}x rẻ hơn" if base and np.isfinite(val)
                     and val > 0 else "-")
            vtxt = f"{val:.0f}" if np.isfinite(val) else "không đạt trong K"
            lines.append(f"| {mode} | {vtxt} | {ratio} |")

    return "\n".join(lines)


def main():
    out = ["# Phân tích số liệu — sơ đồ phản xạ bốn pha với chiếu xấp xỉ", ""]
    # ví dụ giả đơn điệu
    ps = os.path.join(DIR, "pseudomono_summary.csv")
    if os.path.exists(ps):
        out.append("## Ví dụ giả đơn điệu (không đơn điệu)")
        out.append("")
        rows = list(csv.DictReader(open(ps, encoding="utf-8")))
        out.append("| biến thể | chứng chỉ không đơn điệu | phần dư đầu -> cuối | dốc log-log | ghi chú |")
        out.append("|---|---|---|---|---|")
        for r in rows:
            out.append(f"| {r['variant']} | {r['nonmono_worst']} | "
                       f"{r['resid_first']} -> {r['resid_last']} | "
                       f"{r['loglog_slope_tail']} | {r.get('note','')} |")
        out.append("")

    for blur in ["gauss", "motion"]:
        block = analyze_blur(blur)
        if block:
            out.append(block)
            out.append("")

    text = "\n".join(out)
    path = os.path.join(DIR, "phan_tich.md")
    open(path, "w", encoding="utf-8").write(text)
    print(text)
    print(f"\n-> đã ghi {path}")


if __name__ == "__main__":
    main()
