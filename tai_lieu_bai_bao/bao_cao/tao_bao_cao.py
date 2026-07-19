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
    ("Phần còn lại của báo cáo được tổ chức như sau. Mục 2 trình bày bối cảnh và điểm "
     "xuất phát, tức bài toán và các kết luận của báo cáo thực nghiệm trước. Mục 3 nêu "
     "bốn nguyên tắc làm việc, là cơ sở để đánh giá độ tin cậy của các con số về sau. "
     "Các mục từ 4 đến 9 trình bày lần lượt các đóng góp. Mục 10 ghi lại các kết quả "
     "âm tính, mục 11 mô tả chất lượng mã nguồn và tính tái lập, và các mục cuối nêu "
     "hạn chế cùng việc còn lại.", "thuong"),
]

MUC_2 = [
    ("Mục 2. Bối cảnh và điểm xuất phát", "de_muc"),

    ("2.1. Bài toán", "de_muc_phu"),
    ("Đề tài PIE-Net nhằm giải bài toán ngược trong xử lý ảnh, viết dưới dạng y = Bx + "
     "ε, trong đó x là ảnh gốc cần khôi phục, y là dữ liệu quan sát, B là toán tử suy "
     "biến đã biết, chẳng hạn một phép làm mờ, và ε là nhiễu. Bài toán này được đặt "
     "dưới dạng bất đẳng thức biến phân trên một tập ràng buộc D: tìm điểm x thuộc D "
     "sao cho tích vô hướng của toán tử chi phí tại x với mọi hướng đi từ x tới một "
     "điểm khác của D đều không âm.", "thuong"),
    ("Cách đặt bài toán như vậy có hai hệ quả định hình toàn bộ công việc về sau. Hệ "
     "quả thứ nhất là tập ràng buộc trở thành một thành phần của thuật toán chứ không "
     "phải một điều kiện phụ, vì mỗi bước lặp đều phải chiếu điểm hiện tại về tập ràng "
     "buộc. Hệ quả thứ hai, và đây là điểm quan trọng cho phần sau của báo cáo, là "
     "phép chiếu chỉ rẻ khi tập ràng buộc đủ đơn giản. Với tập ràng buộc được dùng "
     "trong đề tài là quả cầu biến phân toàn phần, phép chiếu không có công thức đóng "
     "và phải giải bằng một vòng lặp nội, nên chi phí của phép chiếu chiếm phần lớn "
     "chi phí của thuật toán.", "thuong"),

    ("2.2. Kết luận của báo cáo thực nghiệm trước", "de_muc_phu"),
    ("Thiết kế ban đầu của đề tài dựa trên bốn khẳng định, mỗi khẳng định được gắn với "
     "một thí nghiệm kiểm chứng và một tiêu chí đạt hay không đạt bằng con số cụ thể, "
     "đặt trước khi chạy và không sửa sau khi thấy số liệu. Báo cáo thực nghiệm trước "
     "đã kiểm cả bốn khẳng định qua năm thí nghiệm, và kết quả là chỉ một khẳng định "
     "đứng vững.", "thuong"),
    ("Khẳng định thứ nhất cho rằng hệ số vô hướng học được cải thiện chất lượng khôi "
     "phục so với hệ số hằng được tinh chỉnh tốt. Kết quả là không đạt: phiên bản có "
     "hệ số vô hướng học được đạt 28,31 dB, còn phiên bản hệ số hằng đạt 28,91 dB, tức "
     "thấp hơn 0,60 dB. Hệ số học được còn tự hội tụ về một hằng số xấp xỉ 1, với giá "
     "trị trung bình 0,991 trên tập kiểm tra, cho thấy phần dung lượng mô hình dành "
     "cho nó không được sử dụng.", "thuong"),
    ("Khẳng định thứ ba cho rằng thành phần học được thêm giá trị so với phiên bản "
     "không học. Kết quả cũng không đạt: tại điểm vận hành ổn định nhất, với mờ Gauss "
     "phiên bản có học đạt 26,80 dB còn phiên bản không học đạt 25,79 dB, và với mờ "
     "chuyển động là 26,82 dB so với 24,64 dB; sau khi tính tới dao động theo hạt "
     "giống, mức chênh không vượt ngưỡng 0,3 dB đặt trước một cách ổn định. Ở ngân "
     "sách bước nội thấp, phiên bản có học còn mất ổn định nghiêm trọng.", "thuong"),
    ("Khẳng định thứ tư cho rằng ràng buộc cứng nhất quán dữ liệu cho lợi thế so với "
     "Plug-and-Play. Kết quả là không đạt, và đây là kết quả dứt khoát nhất: phương "
     "pháp của đề tài thua Plug-and-Play 0,59 dB ở chế độ khớp mức nhiễu và 0,88 dB ở "
     "chế độ lệch mức nhiễu, tức khoảng cách còn nới rộng đúng ở chế độ mà ràng buộc "
     "cứng được kỳ vọng có lợi thế. Trước đó một thí nghiệm riêng đã đo được khoảng "
     "trống 1,97 dB giữa prior thủ công tốt nhất và trần của việc học trên ảnh kết "
     "cấu, nhưng chính thí nghiệm đối đầu cho thấy Plug-and-Play đã lấy gần trọn "
     "khoảng trống đó, khi đạt 27,47 dB so với trần 27,60 dB.", "thuong"),

    ("2.3. Vì sao các kết quả này có tính cấu trúc", "de_muc_phu"),
    ("Điểm quan trọng nhất của báo cáo trước không nằm ở các con số mà ở chẩn đoán "
     "nguyên nhân. Ba kết quả không đạt nêu trên không đến từ lỗi cài đặt hay từ việc "
     "tinh chỉnh chưa tới, mà bắt nguồn từ chính cách dựng mô hình, nên không thể khắc "
     "phục bằng cách dò thêm siêu tham số hay đổi kiến trúc mạng.", "thuong"),
    ("Có thể thấy điều đó qua ba lập luận. Thứ nhất, hệ số vô hướng dương nhân với một "
     "toán tử không làm thay đổi tập nghiệm của bất đẳng thức biến phân; nó chỉ tác "
     "động lên động học hội tụ, mà ở chân trời hữu hạn thì tác động đó quá nhỏ để tạo "
     "khác biệt về chất lượng. Thứ hai, ràng buộc cứng nhất quán dữ liệu buộc nghiệm "
     "bám sát quả cầu quanh dữ liệu quan sát, mà dữ liệu quan sát đã mang nhiễu, nên "
     "ép như vậy chính là nạp nhiễu trở lại ảnh khôi phục; điều này giải thích vì sao "
     "khoảng cách với Plug-and-Play nới rộng đúng ở chế độ lệch mức nhiễu. Thứ ba, hai "
     "thành phần được kỳ vọng của đề tài loại trừ lẫn nhau: toán tử học được chỉ ổn "
     "định khi ngân sách bước nội đủ lớn, mà ngân sách bước nội lớn lại phá hủy đúng "
     "lợi thế chi phí của phép chiếu xấp xỉ ít bước nội.", "thuong"),
    ("Vì các rào cản này có tính cấu trúc, báo cáo trước đã khuyến nghị đóng hướng "
     "thực nghiệm theo khuôn khổ cũ thay vì tiếp tục tinh chỉnh. Báo cáo hiện tại kế "
     "thừa nguyên vẹn khuyến nghị đó và không mở lại bất kỳ nhánh nào đã đóng.",
     "thuong"),

    ("2.4. Điều duy nhất còn đứng vững", "de_muc_phu"),
    ("Khẳng định thứ hai là khẳng định duy nhất đạt tiêu chí đặt trước. Nội dung của "
     "nó là: trên một tập ràng buộc mà phép chiếu chính xác thật sự cần vòng lặp nội, "
     "phép chiếu xấp xỉ với ngân sách bước nội nhỏ đạt chất lượng không thấp hơn phép "
     "chiếu chính xác có khởi tạo ấm, trong ngưỡng 0,1 dB, đồng thời tốn ít hơn rõ rệt "
     "về tổng bước nội. Số liệu cụ thể là rẻ hơn khoảng 8,2 lần với mờ Gauss và khoảng "
     "7,6 lần với mờ chuyển động.", "thuong"),
    ("Báo cáo trước cũng nêu ba điều kiện để hiểu đúng kết quả này, và báo cáo hiện "
     "tại giữ nguyên cả ba. Thứ nhất, lợi thế đo được là lợi thế về chi phí chứ không "
     "phải về chất lượng khôi phục. Thứ hai, phép chiếu chính xác có khởi tạo ấm mới "
     "là mốc so sánh đúng, vì bản thân khởi tạo ấm đã tiết kiệm rất lớn so với khởi "
     "tạo lạnh, và nếu so với khởi tạo lạnh thì phần tiết kiệm ấy sẽ bị gán nhầm cho "
     "phép chiếu xấp xỉ. Thứ ba, cơ chế tạo ra lợi thế là việc phân bổ vòng lặp nội "
     "qua các bước ngoài nhờ khởi tạo ấm, một kỹ thuật đã biết trong tối ưu, nên tự nó "
     "chưa đủ mới để đứng thành một đóng góp riêng.", "thuong"),

    ("2.5. Câu hỏi của giai đoạn nghiên cứu này", "de_muc_phu"),
    ("Từ hiện trạng trên, câu hỏi của giai đoạn nghiên cứu này được phát biểu như sau: "
     "có thể biến điều duy nhất còn đứng vững, tức lợi thế chi phí của phép chiếu xấp "
     "xỉ có khởi tạo ấm, thành một đóng góp công bố được hay không, khi mà bản thân cơ "
     "chế tạo ra lợi thế đó là một kỹ thuật đã biết.", "thuong"),
    ("Câu hỏi này ràng buộc cách làm theo ba hướng. Thứ nhất, không được lặp lại các "
     "nhánh đã đóng, nên trọng tâm phải chuyển từ phần học sang phần thuật toán và "
     "giải tích số. Thứ hai, vì cơ chế nền đã biết, đóng góp nếu có phải nằm ở chỗ "
     "khác, và phần sau của báo cáo cho thấy chỗ đó là tiêu chuẩn dừng của vòng lặp "
     "nội. Thứ ba, vì kết luận trước đây dựa trên so sánh chi phí, mọi phép đo chi phí "
     "trong giai đoạn này phải được thiết kế chặt hơn trước, và mục 3 trình bày các "
     "nguyên tắc được dùng cho việc đó.", "thuong"),
]

MUC_3 = [
    ("Mục 3. Phương pháp làm việc", "de_muc"),

    ("Mục này trình bày bốn nguyên tắc được áp dụng thống nhất cho toàn bộ giai đoạn "
     "nghiên cứu. Lý do phải trình bày chúng trước khi nêu kết quả là như sau: đóng "
     "góp của báo cáo này chủ yếu là một so sánh chi phí, mà một so sánh chi phí chỉ "
     "có nghĩa khi phép đo công bằng, phương pháp đối chứng được cho cơ hội mạnh nhất, "
     "và tiêu chí không bị điều chỉnh sau khi đã thấy số liệu. Bốn nguyên tắc dưới đây "
     "nhằm bảo đảm đúng ba điều đó.", "thuong"),

    ("3.1. Nguyên tắc thứ nhất: đặt tiêu chí trước khi chạy", "de_muc_phu"),
    ("Mọi so sánh chi phí trong báo cáo đều được thực hiện tại các mức phần dư biến "
     "phân mục tiêu ấn định trước khi chạy, cụ thể là năm mức từ 3,0 nhân mười mũ trừ "
     "hai xuống 1,0 nhân mười mũ trừ hai. Các mức này độc lập với kết quả của mọi cấu "
     "hình, và không được sửa sau khi có số liệu.", "thuong"),
    ("Nguyên tắc này không phải hình thức. Bản đo đầu tiên của chúng tôi lấy mức phần "
     "dư mục tiêu từ chính phần dư cuối của phương pháp đối chứng rồi nới thêm năm "
     "phần trăm. Cách làm đó tưởng là tự nhiên nhưng thực chất là chọn tiêu chí sau "
     "khi đã thấy số liệu, và nó có lợi một cách cơ học cho phương pháp được đề xuất. "
     "Lỗi này được phát hiện ở một vòng phản biện và đã được sửa bằng cách chuyển sang "
     "danh sách mức ấn định trước.", "thuong"),

    ("3.2. Nguyên tắc thứ hai: cho phương pháp đối chứng cơ hội mạnh nhất", "de_muc_phu"),
    ("Một kết luận rằng phương pháp này rẻ hơn phương pháp kia chỉ có giá trị khi "
     "phương pháp đối chứng đã được chỉnh tốt. Vì vậy phương pháp đối chứng, tức phép "
     "chiếu chính xác dừng theo chứng chỉ, được dò tham số với đúng số cấu hình như "
     "phương pháp được đề xuất, cụ thể là tám cấu hình cho mỗi bên.", "thuong"),
    ("Nguyên tắc này cũng xuất phát từ một lỗi thật. Bản đo trước đó dò mười sáu cấu "
     "hình cho phương pháp được đề xuất nhưng chỉ hai cấu hình cho phương pháp đối "
     "chứng. Sự bất đối xứng ấy làm hệ số tiết kiệm cao hơn thực tế, vì phương pháp "
     "được đề xuất được chọn ở điểm vận hành tốt nhất còn phương pháp đối chứng thì "
     "không.", "thuong"),
    ("Cùng nguyên tắc này, báo cáo giữ lại mốc so sánh khó nhất chứ không chọn mốc dễ. "
     "Phép chiếu chính xác luôn được cho khởi tạo ấm, vì bản thân khởi tạo ấm đã tiết "
     "kiệm rất lớn; nếu so với phép chiếu chính xác khởi tạo lạnh thì phần tiết kiệm "
     "đó sẽ bị gán nhầm cho phép chiếu xấp xỉ. Ngoài ra, hai bên đều dừng theo cùng "
     "một chứng chỉ tính được, nên không bên nào được dùng thông tin mà bên kia không "
     "có.", "thuong"),

    ("3.3. Nguyên tắc thứ ba: phản biện đối kháng trước khi chấp nhận", "de_muc_phu"),
    ("Mỗi bản thảo chứng minh và mỗi kết luận số quan trọng đều được đưa qua một vòng "
     "phản biện độc lập trước khi được chấp nhận. Người phản biện được yêu cầu tự tính "
     "lại từng phép biến đổi và tìm cách bác bỏ kết luận, chứ không phải xác nhận nó.",
     "thuong"),
    ("Kết quả của nguyên tắc này là hai bản thảo chứng minh đã bị bác và ba lỗi phương "
     "pháp luận trong chính phần đo của chúng tôi đã bị phát hiện. Bản thảo chứng minh "
     "thứ nhất bị bác vì một lỗ hổng ở phần lõi: bổ đề một bước được mượn đòi hỏi một "
     "chuỗi phép chiếu liền mạch, mà bước quán tính và bước neo trong sơ đồ khi đó làm "
     "đứt chuỗi ấy. Bản thảo thứ hai bị bác vì một lập luận về tính mới không đứng "
     "vững. Ba lỗi phương pháp luận gồm: chỉ đếm bước nội mà không đo thời gian; chọn "
     "mức phần dư mục tiêu sau khi thấy số liệu; và dò tham số bất đối xứng giữa hai "
     "bên.", "thuong"),
    ("Cần nói rõ rằng việc liệt kê các lần bị bác không phải là tự phê bình cho có. "
     "Trong bốn lỗi nghiêm trọng nhất của giai đoạn này, không lỗi nào được phát hiện "
     "bởi tác giả khi đang viết, mà tất cả đều do vòng phản biện tìm ra. Điều này cho "
     "thấy vòng phản biện là bộ phận không thể bỏ của quy trình chứ không phải một "
     "bước kiểm tra thêm.", "thuong"),

    ("3.4. Nguyên tắc thứ tư: ghi lại kết quả âm tính", "de_muc_phu"),
    ("Mọi hướng đã thử và thất bại đều được ghi lại kèm số liệu và kèm chẩn đoán "
     "nguyên nhân, thay vì bị xóa đi. Trong giai đoạn này có bốn hướng như vậy: lịch "
     "bước tăng tốc cho bài toán chiếu; siết chứng chỉ bằng cách theo dõi giá trị tốt "
     "nhất; tiêu chuẩn sai số tương đối theo chuẩn toán tử; và tiêu chuẩn chiếu nới "
     "lỏng. Mục 10 trình bày đầy đủ bốn hướng này.", "thuong"),
    ("Việc ghi lại có hai lợi ích cụ thể. Lợi ích thứ nhất là tránh lặp lại: mỗi hướng "
     "âm tính đều kèm lý do thất bại đủ rõ để người sau không thử lại, ví dụ tiêu "
     "chuẩn chiếu nới lỏng không thực thi được vì việc kiểm nó đòi tính hàm tựa của "
     "tập ràng buộc, tức đắt ngang chính phép chiếu. Lợi ích thứ hai là các kết quả âm "
     "tính giúp xác định đúng phạm vi của kết quả dương tính, vì chúng cho biết phương "
     "pháp hỏng ở đâu chứ không chỉ chạy tốt ở đâu.", "thuong"),

    ("3.5. Hệ quả đối với cách đọc báo cáo", "de_muc_phu"),
    ("Bốn nguyên tắc trên dẫn tới một hệ quả về cách đọc các con số ở những mục sau. "
     "Các hệ số tiết kiệm được báo cáo là hệ số đo sau khi đã sửa ba lỗi phương pháp "
     "luận nêu trên, nên chúng thấp hơn các con số từng xuất hiện trong những bản đo "
     "trước đó của chính chúng tôi. Đây là điều có chủ ý: bản đo cuối cùng chặt hơn "
     "các bản trước, và con số thấp hơn là con số đáng tin hơn.", "thuong"),
    ("Ngoài ra, mỗi con số trong báo cáo đều được đối chiếu tự động với tệp kết quả "
     "gốc bằng một chương trình kiểm tra, thay vì chép tay. Quy trình đối chiếu này đã "
     "phát hiện hai con số sai trong bản thảo đầu của chính báo cáo này, gồm một hệ số "
     "lấy nhầm từ bản đo cũ và một mức vi phạm ràng buộc ghi không chính xác. Mục 11 "
     "mô tả chương trình kiểm tra đó.", "thuong"),
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

    # 3. Ghi các mục nội dung.
    for text, kieu in MUC_1 + MUC_2 + MUC_3:
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        if kieu == "de_muc":
            r.bold = True
            r.font.size = Pt(15)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(12)
        elif kieu == "de_muc_phu":
            r.bold = True
            r.font.size = Pt(13)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(6)
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
