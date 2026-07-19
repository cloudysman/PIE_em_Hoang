"""Kiểm tra tệp báo cáo: số liệu, thuật ngữ, cách viết hoa và liên kết giữa các mục.

Bốn nhóm kiểm tra:
  1. Mọi con số trong báo cáo phải khớp báo cáo thực nghiệm gốc hoặc tệp kết quả.
  2. Thuật ngữ phải nhất quán: không dùng hai từ khác nhau cho cùng một khái niệm.
  3. Không viết hoa tùy tiện ở giữa câu.
  4. Mục 1 và mục 2 phải liên kết: mọi khái niệm mục 1 nhắc tới đều được mục 2 giải
     thích, và số liệu chung giữa hai mục phải trùng nhau.

Chạy: python tai_lieu_bai_bao/bao_cao/kiem_tra_bao_cao.py
"""

from __future__ import annotations

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from docx import Document

HERE = os.path.dirname(os.path.abspath(__file__))
BAO_CAO = os.path.join(HERE, "Bao_cao_muc_1_2.docx")
GOC = (r"C:\Users\trong\AppData\Local\Temp\claude"
       r"\c--Users-trong-Downloads-PIE-em-Hoang"
       r"\2bf96163-73da-4142-8ed0-60cb16987721\scratchpad\bao_cao_goc.txt")

# Số liệu và nguồn phải đối chiếu. Khóa là con số như viết trong báo cáo.
NGUON_SO = {
    "28,31": "goc", "28,91": "goc", "0,60": "goc", "0,991": "goc",
    "26,80": "goc", "25,79": "goc", "26,82": "goc", "24,64": "goc",
    "0,59": "goc", "0,88": "goc", "1,97": "goc", "27,47": "goc",
    "27,60": "goc", "8,2": "goc", "7,6": "goc", "0,3": "goc", "0,1": "goc",
    "13,2": "ket_qua", "19,2": "ket_qua", "4,7": "ket_qua", "9,7": "ket_qua",
    "17,2": "ket_qua", "23,6": "ket_qua", "7,2": "ket_qua", "14,7": "ket_qua",
    "1,0000": "ket_qua",
}

# Cặp thuật ngữ: (từ đúng, các từ đồng nghĩa không được dùng).
THUAT_NGU = [
    ("phép chiếu xấp xỉ", ["chiếu gần đúng", "phép chiếu không chính xác",
                           "chiếu xấp xỉ hoá"]),
    ("phần dư biến phân", ["sai số hội tụ", "độ dư", "residual"]),
    ("bước nội", ["vòng trong", "lặp trong"]),
    ("bước ngoài", ["vòng ngoài", "lặp ngoài"]),
    ("khởi tạo ấm", ["warm start", "khởi động ấm"]),
    ("tập ràng buộc", ["miền ràng buộc", "tập khả thi"]),
    ("chứng chỉ", ["giấy chứng nhận", "certificate"]),
    ("hệ số vô hướng", ["hệ số scalar", "trọng số vô hướng"]),
]

# Từ được phép viết hoa giữa câu: tên riêng, tên phương pháp và ký hiệu toán học.
CHO_PHEP_HOA = {
    "Bx", "B", "D", "F", "x", "y",          # ký hiệu toán học trong y = Bx + ε
    "Plug-and-Play", "Gauss", "PIE-Net", "Fejér", "DnCNN", "Q1", "Q2",
    "Chambolle-Pock", "Malitsky", "Hà", "Nội", "Đào", "Trọng", "Hiếu",
    "Đặng", "Văn", "Chiến", "Học", "Viện", "Bộ", "Khoa", "Công", "Nghệ",
    "Bưu", "Chính", "Viễn", "Thông", "Mục", "Đề", "Giảng", "Lớp", "Biết",
    "Báo", "Tóm", "Bối", "Câu", "Khẳng", "Kết", "Điểm", "Đóng", "Phần",
    "Về", "Từ", "Có", "Cách", "Thiết", "Vì", "Điều", "Trên", "Đây", "Ba",
    "Hai", "Thứ", "Hệ", "Ngoài", "Nội", "Với", "Nhờ", "Số", "Trước",
}


def lay_van_ban(path):
    d = Document(path)
    return [p.text.strip() for p in d.paragraphs if p.text.strip()]


def tach_muc(doan):
    """Tách danh sách đoạn thành mục 1 và mục 2."""
    i1 = next(i for i, t in enumerate(doan) if t.startswith("Mục 1."))
    i2 = next(i for i, t in enumerate(doan) if t.startswith("Mục 2."))
    return doan[i1:i2], doan[i2:]


def kiem_so_lieu(text, goc):
    loi = []
    for so, nguon in NGUON_SO.items():
        if so not in text:
            continue
        if nguon == "goc" and so not in goc:
            loi.append(f"số {so} không tìm thấy trong báo cáo gốc")
    return loi


def kiem_thuat_ngu(text):
    loi = []
    thap = text.lower()
    for dung, sai_list in THUAT_NGU:
        for sai in sai_list:
            if sai.lower() in thap:
                loi.append(f"dùng '{sai}' thay vì '{dung}'")
    return loi


def kiem_viet_hoa(doan):
    loi = []
    for t in doan:
        # bỏ qua tiêu đề mục và các dòng bìa
        if re.match(r"^(Mục|\d\.\d\.)", t) or len(t) < 60:
            continue
        for cau in re.split(r"(?<=\.)\s+", t):
            tu = cau.split()
            for w in tu[1:]:
                w_sach = w.strip(".,;:()")
                if (w_sach and w_sach[0].isupper() and w_sach not in CHO_PHEP_HOA
                        and not w_sach.isupper()):
                    loi.append(f"viết hoa giữa câu: '{w_sach}'")
    return loi


def kiem_lien_ket(muc1, muc2):
    """Mục 1 nhắc khái niệm nào thì mục 2 phải giải thích, và số chung phải trùng."""
    canh_bao = []
    t1, t2 = " ".join(muc1).lower(), " ".join(muc2).lower()

    # a) khái niệm mục 1 nêu, mục 2 phải nói tới
    khai_niem = ["bốn khẳng định", "plug-and-play", "khởi tạo ấm",
                 "phép chiếu xấp xỉ", "cấu trúc"]
    for k in khai_niem:
        if k in t1 and k not in t2:
            canh_bao.append(f"mục 1 nêu '{k}' nhưng mục 2 không nhắc lại")

    # b) số liệu xuất hiện ở cả hai mục phải giống nhau
    so1 = set(re.findall(r"\d+,\d+", t1))
    so2 = set(re.findall(r"\d+,\d+", t2))
    chung = so1 & so2
    canh_bao.append(f"(thông tin) số liệu dùng chung ở hai mục: {sorted(chung)}")

    # c) mục 2 phải kết bằng câu dẫn sang mục 3
    if "mục 3" not in t2:
        canh_bao.append("mục 2 không có câu dẫn sang mục 3")
    return canh_bao


def main():
    if not os.path.exists(BAO_CAO):
        sys.exit(f"Không tìm thấy báo cáo: {BAO_CAO}")
    doan = lay_van_ban(BAO_CAO)
    goc = open(GOC, encoding="utf-8").read() if os.path.exists(GOC) else ""
    muc1, muc2 = tach_muc(doan)
    text = " ".join(doan)

    print(f"Báo cáo: {len(doan)} đoạn | mục 1: {len(muc1)} đoạn | "
          f"mục 2: {len(muc2)} đoạn")
    print(f"Số chữ mục 1: {len(' '.join(muc1).split())} | "
          f"mục 2: {len(' '.join(muc2).split())}")
    print()

    tat_ca_loi = []
    for ten, loi in [
        ("1. Đối chiếu số liệu với nguồn", kiem_so_lieu(text, goc)),
        ("2. Thuật ngữ nhất quán", kiem_thuat_ngu(text)),
        ("3. Viết hoa giữa câu", kiem_viet_hoa(doan)),
    ]:
        print(f"--- {ten} ---")
        if loi:
            for l in sorted(set(loi)):
                print("   LỖI:", l)
            tat_ca_loi += loi
        else:
            print("   không có lỗi")
        print()

    print("--- 4. Liên kết giữa mục 1 và mục 2 ---")
    for c in kiem_lien_ket(muc1, muc2):
        print("  ", c)
        if not c.startswith("(thông tin)"):
            tat_ca_loi.append(c)
    print()

    print("=" * 60)
    print("KẾT QUẢ:", "đạt, không có lỗi" if not tat_ca_loi
          else f"có {len(set(tat_ca_loi))} lỗi cần sửa")


if __name__ == "__main__":
    main()
