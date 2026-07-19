"""Sinh tệp báo cáo, gồm bìa và mục 1.

Cách làm: dùng tệp báo cáo SoundGuard làm khuôn cho trang bìa, để giữ nguyên khung
viền hoa văn và logo học viện (hai ảnh này nằm ở đoạn 0 và đoạn 3 của tệp gốc, không
phải là đường kẻ nên không thể tạo lại bằng thiết lập viền trang). Chương trình chỉ
thay phần chữ trên bìa, xóa toàn bộ nội dung cũ phía sau, rồi ghi mục 1 vào.

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
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

HERE = os.path.dirname(os.path.abspath(__file__))
KHUON = r"C:\Users\trong\Downloads\SoundGuard_Report_FULL_EN.docx"
OUT = os.path.join(HERE, "Bao_cao_dong_gop_PIE-Net.docx")

# Chữ trên bìa, theo đúng thứ tự đoạn của tệp khuôn.
# Khóa là chỉ số đoạn; đoạn 0 và 3 chứa ảnh nên không đụng tới.
BIA = {
    1: "BỘ KHOA HỌC VÀ CÔNG NGHỆ",
    2: "HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG",
    4: "Biết khi nào phép chiếu đã đủ chính xác",
    5: ("Đề tài: chứng chỉ sai số tính được cho phép chiếu xấp xỉ và phân tích chi "
        "phí trong phương pháp chiếu phản xạ giải bất đẳng thức biến phân (PIE-Net)"),
    6: "Giảng viên hướng dẫn: Đặng Văn Chiến",
    7: "Học viên: Đào Trọng Hiếu — M25VMCS07",
    8: "Lớp: M25VMCS",
    9: "Hà Nội - 2026",
}

DOAN_NGAT_TRANG = 10          # đoạn chứa ngắt trang, giữ lại
MUC_1 = [
    ("Mục 1. Tóm tắt", "de_muc"),
    ("Báo cáo này trình bày các đóng góp của giai đoạn nghiên cứu tiếp nối báo cáo "
     "thực nghiệm trước đó của đề tài PIE-Net. Điểm xuất phát là một kết luận không "
     "thuận lợi. Báo cáo thực nghiệm trước đã kiểm bốn khẳng định của thiết kế ban "
     "đầu qua năm thí nghiệm, mỗi thí nghiệm có tiêu chí đạt hay không đạt đặt trước "
     "khi chạy, và chỉ một khẳng định đứng vững. Hệ số vô hướng học được đạt 28,31 dB "
     "so với 28,91 dB của hệ số hằng được tinh chỉnh tốt, tức thấp hơn 0,60 dB; phương "
     "pháp của đề tài thua Plug-and-Play 0,59 dB ở chế độ khớp mức nhiễu và 0,88 dB ở "
     "chế độ lệch mức nhiễu. Các kết quả này có tính cấu trúc, tức xuất phát từ bản "
     "chất toán học của cách dựng mô hình chứ không từ lỗi cài đặt, nên hướng thực "
     "nghiệm đã được đóng lại. Khẳng định duy nhất còn đứng vững là lợi thế chi phí "
     "của phép chiếu xấp xỉ có khởi tạo ấm.", "thuong"),
    ("Câu hỏi của giai đoạn này vì thế được thu hẹp lại: có thể biến điều duy nhất "
     "còn đứng vững đó thành một đóng góp công bố được hay không. Để trả lời, trọng "
     "tâm được chuyển từ phần học sang phần thuật toán và giải tích số, sơ đồ lặp "
     "được dựng lại cho đúng với tài liệu, và toàn bộ phần đo chi phí được thiết kế "
     "lại.", "thuong"),
    ("Báo cáo có ba đóng góp. Đóng góp thứ nhất là một chứng chỉ sai số tính được cho "
     "phép chiếu xấp xỉ. Định nghĩa phép chiếu xấp xỉ trong tài liệu đòi kiểm khoảng "
     "cách tới phép chiếu chính xác, mà phép chiếu chính xác lại chính là đại lượng "
     "thuật toán được thiết kế để tránh tính; đây là một vòng luẩn quẩn khiến chế độ "
     "ngân sách trong thực thi nằm ngoài phạm vi của định lý. Vì bài toán chiếu có hàm "
     "mục tiêu lồi mạnh, khoảng cách tới nghiệm chiếu bị chặn bởi căn của hai lần "
     "khoảng cách đối ngẫu, và khoảng cách đối ngẫu tính trực tiếp từ cặp biến gốc và "
     "đối ngẫu mà bộ giải nội đã có sẵn. Nhờ đó tiêu chuẩn dừng trở thành thứ một "
     "chương trình có thể kiểm được.", "thuong"),
    ("Đóng góp thứ hai là chế độ ngân sách thích nghi dựa trên chứng chỉ đó, cùng với "
     "kết quả chi phí. Trên bài toán khử mờ ảnh với tập ràng buộc là quả cầu biến phân "
     "toàn phần, để đạt cùng một mức phần dư biến phân, chế độ thích nghi rẻ hơn phép "
     "chiếu chính xác từ 13,2 đến 19,2 lần tính theo tổng bước nội và từ 4,7 đến 9,7 "
     "lần tính theo thời gian thuật toán trên mờ Gauss; trên mờ chuyển động các hệ số "
     "tương ứng là 17,2 đến 23,6 lần và 7,2 đến 14,7 lần. Mọi cấu hình đều cho nghiệm "
     "khả thi, với mức vi phạm ràng buộc không vượt 1,0000, trong khi chế độ ngân sách "
     "cố định cho đầu ra vi phạm ràng buộc tới vài phần trăm.", "thuong"),
    ("Đóng góp thứ ba là một giao thức đo chi phí công bằng, được xây dựng sau khi ba "
     "lỗi phương pháp luận trong chính phần đo của chúng tôi bị phát hiện và sửa: chỉ "
     "đếm bước nội mà không đo thời gian, trong khi bước nội của chế độ thích nghi đắt "
     "hơn vì phải tính chứng chỉ; lấy mức phần dư mục tiêu từ chính kết quả của phương "
     "pháp đối chứng, tức chọn sau khi đã thấy số liệu; và dò tham số bất đối xứng, "
     "mười sáu cấu hình cho phương pháp đề xuất so với hai cấu hình cho phương pháp "
     "đối chứng. Giao thức sau khi sửa báo cả hai thước đo chi phí, ấn định mức phần "
     "dư mục tiêu trước khi chạy, và dò tham số cho hai bên với cùng số cấu hình.",
     "thuong"),
    ("Về mức công bố, báo cáo kết luận rằng công trình phù hợp một tạp chí thuộc nhóm "
     "Q2 chứ không phải nhóm Q1. Lý do nằm ở phần lý thuyết: sau khi dẫn xuất đầy đủ, "
     "hằng số của số hạng nhiễu do phép chiếu xấp xỉ không chứa nghịch đảo bước nhảy, "
     "nên việc thêm bước phản xạ vào khung phép chiếu xấp xỉ không tạo ra một cơ chế "
     "nhiễu mới về bản chất; định lý hội tụ vì thế là một mở rộng của các kết quả đã "
     "công bố. Giá trị công bố được của công trình nằm ở phần chứng chỉ, chế độ ngân "
     "sách thích nghi và phân tích chi phí, tức ở phần thuật toán và thực nghiệm.",
     "thuong"),
    ("Phần chứng minh chưa hoàn tất ở hai chi tiết kỹ thuật: phát biểu chính xác bổ đề "
     "tựa Fejér loại nhân tính sao cho nó không hấp thụ mất số hạng âm, và bước chuyển "
     "giới hạn yếu trong không gian vô hạn chiều; chi tiết thứ hai là thường quy trong "
     "không gian hữu hạn chiều của phần thực nghiệm.", "thuong"),
]


def thay_chu(p, text):
    """Thay chữ của một đoạn nhưng giữ nguyên định dạng của lần chạy chữ đầu tiên."""
    runs = p.runs
    if not runs:
        p.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


def xoa_doan(p):
    p._element.getparent().remove(p._element)


def main():
    if not os.path.exists(KHUON):
        sys.exit(f"Không tìm thấy tệp khuôn: {KHUON}")
    doc = Document(KHUON)

    # 1. Thay chữ trên bìa, giữ nguyên hai ảnh khung viền và logo.
    for i, text in BIA.items():
        thay_chu(doc.paragraphs[i], text)

    # 2. Xóa toàn bộ nội dung cũ phía sau ngắt trang, gồm cả bảng.
    for p in list(doc.paragraphs[DOAN_NGAT_TRANG + 1:]):
        xoa_doan(p)
    for t in list(doc.tables):
        t._element.getparent().remove(t._element)

    # 3. Ghi mục 1.
    for text, kieu in MUC_1:
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        if kieu == "de_muc":
            r.bold = True
            r.font.size = Pt(15)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(12)
        else:
            r.font.size = Pt(13)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.first_line_indent = Pt(28)
        p.paragraph_format.line_spacing = 1.4

    doc.save(OUT)
    print(f"đã tạo: {OUT}")


if __name__ == "__main__":
    main()
