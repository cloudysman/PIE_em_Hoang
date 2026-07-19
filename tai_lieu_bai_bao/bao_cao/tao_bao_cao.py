"""Sinh tệp báo cáo, gồm bìa và mục 1, theo bố cục bìa của báo cáo SoundGuard.

Chạy: python tai_lieu_bai_bao/bao_cao/tao_bao_cao.py
"""

from __future__ import annotations

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Pt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "Bao_cao_dong_gop_PIE-Net.docx")

TIEU_DE_NGAN = "Biết khi nào phép chiếu đã đủ chính xác"
DE_TAI = ("Đề tài: chứng chỉ sai số tính được cho phép chiếu xấp xỉ và phân tích "
          "chi phí trong phương pháp chiếu phản xạ giải bất đẳng thức biến phân "
          "(PIE-Net)")
GIANG_VIEN = "Giảng viên hướng dẫn: Đặng Văn Chiến"
TAC_GIA = "Học viên: Đào Trọng Hiếu — M25VMCS07"
LOP = "Lớp: M25VMCS"
DIA_DIEM = "Hà Nội - 2026"


def dat_font(doc, ten="Times New Roman", co=13):
    s = doc.styles["Normal"]
    s.font.name = ten
    s.font.size = Pt(co)


def doan(doc, text, dam=False, canh=None, co=None, truoc=0, sau=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = dam
    if co:
        r.font.size = Pt(co)
    if canh is not None:
        p.alignment = canh
    p.paragraph_format.space_before = Pt(truoc)
    p.paragraph_format.space_after = Pt(sau)
    p.paragraph_format.line_spacing = 1.4
    return p


def main():
    doc = Document()
    dat_font(doc)
    C = WD_ALIGN_PARAGRAPH.CENTER
    J = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ------------------------------- bìa ------------------------------- #
    doan(doc, "BỘ KHOA HỌC VÀ CÔNG NGHỆ", canh=C, co=13, truoc=24, sau=2)
    doan(doc, "HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG", canh=C, co=13, sau=90)

    doan(doc, TIEU_DE_NGAN, canh=C, co=20, sau=14)
    doan(doc, DE_TAI, canh=C, co=13, sau=90)

    doan(doc, GIANG_VIEN, canh=C, co=13, sau=4)
    doan(doc, TAC_GIA, canh=C, co=13, sau=4)
    doan(doc, LOP, canh=C, co=13, sau=110)

    doan(doc, DIA_DIEM, canh=C, co=13, sau=0)

    doc.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)

    # ------------------------------ mục 1 ------------------------------ #
    doan(doc, "Mục 1. Tóm tắt", co=16, sau=10)

    doan(doc,
         "Báo cáo này trình bày các đóng góp của giai đoạn nghiên cứu tiếp nối "
         "báo cáo thực nghiệm trước đó của đề tài PIE-Net. Điểm xuất phát là một "
         "kết luận không thuận lợi. Báo cáo thực nghiệm trước đã kiểm bốn khẳng "
         "định của thiết kế ban đầu qua năm thí nghiệm, mỗi thí nghiệm có tiêu "
         "chí đạt hay không đạt đặt trước khi chạy, và chỉ một khẳng định đứng "
         "vững. Hệ số vô hướng học được đạt 28,31 dB so với 28,91 dB của hệ số "
         "hằng được tinh chỉnh tốt, tức thấp hơn 0,60 dB; phương pháp của đề tài "
         "thua Plug-and-Play 0,59 dB ở chế độ khớp mức nhiễu và 0,88 dB ở chế độ "
         "lệch mức nhiễu. Các kết quả này có tính cấu trúc, tức xuất phát từ bản "
         "chất toán học của cách dựng mô hình chứ không từ lỗi cài đặt, nên hướng "
         "thực nghiệm đã được đóng lại. Khẳng định duy nhất còn đứng vững là lợi "
         "thế chi phí của phép chiếu xấp xỉ có khởi tạo ấm.",
         canh=J)

    doan(doc,
         "Câu hỏi của giai đoạn này vì thế được thu hẹp lại: có thể biến điều duy "
         "nhất còn đứng vững đó thành một đóng góp công bố được hay không. Để trả "
         "lời, trọng tâm được chuyển từ phần học sang phần thuật toán và giải tích "
         "số, sơ đồ lặp được dựng lại cho đúng với tài liệu, và toàn bộ phần đo "
         "chi phí được thiết kế lại.",
         canh=J)

    doan(doc,
         "Báo cáo có ba đóng góp. Đóng góp thứ nhất là một chứng chỉ sai số tính "
         "được cho phép chiếu xấp xỉ. Định nghĩa phép chiếu xấp xỉ trong tài liệu "
         "đòi kiểm khoảng cách tới phép chiếu chính xác, mà phép chiếu chính xác "
         "lại chính là đại lượng thuật toán được thiết kế để tránh tính; đây là "
         "một vòng luẩn quẩn khiến chế độ ngân sách trong thực thi nằm ngoài phạm "
         "vi của định lý. Vì bài toán chiếu có hàm mục tiêu lồi mạnh, khoảng cách "
         "tới nghiệm chiếu bị chặn bởi căn của hai lần khoảng cách đối ngẫu, và "
         "khoảng cách đối ngẫu tính trực tiếp từ cặp biến gốc và đối ngẫu mà bộ "
         "giải nội đã có sẵn. Nhờ đó tiêu chuẩn dừng trở thành thứ một chương "
         "trình có thể kiểm được.",
         canh=J)

    doan(doc,
         "Đóng góp thứ hai là chế độ ngân sách thích nghi dựa trên chứng chỉ đó, "
         "cùng với kết quả chi phí. Trên bài toán khử mờ ảnh với tập ràng buộc là "
         "quả cầu biến phân toàn phần, để đạt cùng một mức phần dư biến phân, chế "
         "độ thích nghi rẻ hơn phép chiếu chính xác từ 13,2 đến 19,2 lần tính "
         "theo tổng bước nội và từ 4,7 đến 9,7 lần tính theo thời gian thuật toán "
         "trên mờ Gauss; trên mờ chuyển động các hệ số tương ứng là 17,2 đến 23,6 "
         "lần và 7,2 đến 14,7 lần. Mọi cấu hình đều cho nghiệm khả thi, với mức "
         "vi phạm ràng buộc không vượt 1,0000, trong khi chế độ ngân sách cố định "
         "cho đầu ra vi phạm ràng buộc tới vài phần trăm.",
         canh=J)

    doan(doc,
         "Đóng góp thứ ba là một giao thức đo chi phí công bằng, được xây dựng "
         "sau khi ba lỗi phương pháp luận trong chính phần đo của chúng tôi bị "
         "phát hiện và sửa: chỉ đếm bước nội mà không đo thời gian, trong khi "
         "bước nội của chế độ thích nghi đắt hơn vì phải tính chứng chỉ; lấy mức "
         "phần dư mục tiêu từ chính kết quả của phương pháp đối chứng, tức chọn "
         "sau khi đã thấy số liệu; và dò tham số bất đối xứng, mười sáu cấu hình "
         "cho phương pháp đề xuất so với hai cấu hình cho phương pháp đối chứng. "
         "Giao thức sau khi sửa báo cả hai thước đo chi phí, ấn định mức phần dư "
         "mục tiêu trước khi chạy, và dò tham số cho hai bên với cùng số cấu hình.",
         canh=J)

    doan(doc,
         "Về mức công bố, báo cáo kết luận rằng công trình phù hợp một tạp chí "
         "thuộc nhóm Q2 chứ không phải nhóm Q1. Lý do nằm ở phần lý thuyết: sau "
         "khi dẫn xuất đầy đủ, hằng số của số hạng nhiễu do phép chiếu xấp xỉ "
         "không chứa nghịch đảo bước nhảy, nên việc thêm bước phản xạ vào khung "
         "phép chiếu xấp xỉ không tạo ra một cơ chế nhiễu mới về bản chất; định "
         "lý hội tụ vì thế là một mở rộng của các kết quả đã công bố. Giá trị "
         "công bố được của công trình nằm ở phần chứng chỉ, chế độ ngân sách "
         "thích nghi và phân tích chi phí, tức ở phần thuật toán và thực nghiệm.",
         canh=J)

    doan(doc,
         "Phần chứng minh chưa hoàn tất ở hai chi tiết kỹ thuật: phát biểu chính "
         "xác bổ đề tựa Fejér loại nhân tính sao cho nó không hấp thụ mất số hạng "
         "âm, và bước chuyển giới hạn yếu trong không gian vô hạn chiều; chi tiết "
         "thứ hai là thường quy trong không gian hữu hạn chiều của phần thực nghiệm.",
         canh=J)

    doc.save(OUT)
    print(f"da tao: {OUT}")


if __name__ == "__main__":
    main()
