# Báo cáo giai đoạn tiến hóa: cài đặt sơ đồ phản xạ và kiểm chứng số

Ngày lập: 2026-07-07. Tài liệu này ghi lại việc đã làm và số liệu thu được trong giai đoạn tiến hóa dự án PIE-Net theo con đường thứ hai (bài lý thuyết), sau khi vòng khảo sát và phản biện đã chỉ ra tám lỗi cần sửa (xem `00_ket_luan_dieu_hanh.md`).

## 1. Đã cài đặt

Ba tệp mã nguồn mới, thuần suy diễn, không có thành phần học, chạy được trên máy tính cá nhân.

- `pie_net/reflected_solver.py`: sơ đồ phản xạ bốn pha với phép chiếu xấp xỉ lên quả cầu biến phân toàn phần. Sơ đồ này sửa đúng các lỗi phản biện: pha thứ ba là bước phản xạ kiểu Malitsky đúng nghĩa, toán tử chỉ được tính một lần mỗi bước ngoài tại điểm phản xạ; hệ số quán tính thích nghi thỏa điều kiện chuẩn của dòng phương pháp độ nhớt; bước nhảy đặt theo hằng số Lipschitz ước lượng bằng phép lặp lũy thừa; bỏ kẹp hộp khi chạy lý thuyết. Có bốn chế độ ngân sách bước nội: cố định, log, chiếu chính xác khởi tạo ấm, và sai số hằng. Mọi phép đo đắt được tách khỏi chi phí thuật toán, và sai số chiếu được đo so với một chiếu tham chiếu có kiểm định ổn định.
- `theory_test_reflected.py`: chương trình chạy lưới cấu hình theo loại mờ và chế độ ngân sách, ghi vết đầy đủ ra tệp. Có cơ chế đo thưa để tách phép đo tham chiếu đắt khỏi vòng chính, giảm thời gian chạy từ nhiều giờ xuống chấp nhận được mà không đổi tính đúng đắn.
- `theory_test_pseudomono.py`: ví dụ giả đơn điệu nhưng không đơn điệu trong không gian năm mươi chiều, kèm phép chứng nhận số cho tính không đơn điệu, và một biến thể không suy biến để đối chiếu.
- `analyze_theory.py`: chương trình phân tích, tự tính độ dốc log-log, tính tổng được của sai số chiếu, và bảng chi phí.

## 2. Số liệu chính (mờ Gauss, ảnh cạnh 64 điểm ảnh, 150 bước ngoài)

Bảng chi phí mờ Gauss, tổng bước nội để đạt cùng mức phần dư biến phân:

| chế độ ngân sách | tổng bước nội | hệ số so chiếu chính xác |
|---|---|---|
| chiếu chính xác khởi tạo ấm | 382 | 1,00 |
| cố định một bước nội | 136 | rẻ hơn 2,81 lần |
| cố định hai bước nội | 152 | rẻ hơn 2,51 lần |
| cố định năm bước nội | 230 | rẻ hơn 1,66 lần |

Bảng chi phí mờ chuyển động (chiếu chính xác tốn kém hơn nhiều nên hệ số lớn hơn):

| chế độ ngân sách | tổng bước nội | hệ số so chiếu chính xác |
|---|---|---|
| chiếu chính xác khởi tạo ấm | 1684 | 1,00 |
| cố định hai bước nội | 232 | rẻ hơn 7,26 lần |
| cố định năm bước nội | 330 | rẻ hơn 5,10 lần |
| ngân sách log | 426 | rẻ hơn 3,95 lần |

Độ dốc log-log nửa cuối quỹ đạo:

| chế độ | dịch chuyển | sai số chiếu | phần dư |
|---|---|---|---|
| cố định một bước | −1,20 | −1,30 | −1,28 |
| cố định hai bước | −1,28 | −1,34 | −1,28 |
| cố định năm bước | −1,52 | −1,50 | −1,47 |
| ngân sách log | −1,66 | −2,18 | −1,58 |

Ví dụ giả đơn điệu không đơn điệu:

| biến thể | chứng chỉ không đơn điệu | phần dư đầu | phần dư cuối |
|---|---|---|---|
| suy biến | −5,59 nhân mười mũ trừ sáu | 5,0 nhân mười mũ trừ hai | 1,25 nhân mười mũ trừ bốn |
| không suy biến | −2,50 nhân mười mũ trừ sáu | 5,0 nhân mười mũ trừ hai | 1,25 nhân mười mũ trừ bốn; hội tụ về hình chiếu điểm neo |

## 3. Diễn giải trung thực

Ba kết luận số ủng hộ hướng bài, với mức độ đúng như phát biểu, không phóng đại.

Thứ nhất, dịch chuyển giảm với độ dốc gần âm một dưới ngân sách cố định, khớp với việc bước độ nhớt áp đặt dịch chuyển cỡ βₖ bằng β₀ chia cho k cộng một. Đây là bằng chứng số cho đúng lỗi mà phản biện đã bắt: dưới ngân sách cố định, sai số chiếu bị nối với dịch chuyển này nên không bảo đảm tổng được. Ngân sách log cho sai số chiếu giảm với độ dốc khoảng âm hai, nhanh hơn hẳn, nên bảo đảm tổng được. Đây là lý do số học để chọn ngân sách log cho định lý.

Thứ hai, lợi thế chi phí của phép chiếu xấp xỉ so với chiếu chính xác khởi tạo ấm là một hệ số hằng khoảng 2,5 đến 2,8 lần ở mức phần dư trung bình, giảm dần khi đòi hỏi độ chính xác cao hơn. Đây đúng là mức mà mệnh đề chi phí đã sửa dự đoán, và phải giữ đúng mức này, không được trình bày thành khác biệt bậc. Con số này nhỏ hơn hệ số 7,6 đến 8,2 lần trong báo cáo thực nghiệm cũ, vì cấu hình khác: báo cáo cũ dùng sơ đồ chiếu-gradient thuần với ít bước ngoài, còn ở đây là sơ đồ bốn pha đầy đủ với nhiều bước ngoài hơn và định nghĩa chi phí chiếu chính xác chặt hơn.

Thứ ba, ví dụ giả đơn điệu đạt mục tiêu: chứng chỉ số tìm được cặp điểm với tích vô hướng âm, xác nhận toán tử không đơn điệu, trong khi thuật toán vẫn hội tụ. Nhờ đó định lý phát biểu cho lớp giả đơn điệu không rộng hơn ví dụ minh họa, một điểm mà người phản biện dòng này thường đòi hỏi.

## 4. Điều cần tiếp tục

- Lưới đã chạy xong cả mờ Gauss và mờ chuyển động, sáu chế độ ngân sách mỗi loại; số liệu đầy đủ trong `results/theory/phan_tich.md`. Mờ chuyển động cho hệ số tiết kiệm lớn hơn (khoảng 4 đến 7 lần) vì bài toán chiếu khó hơn.
- Bản thảo chứng minh định lý hội tụ mạnh đã được soạn trong `03_chung_minh_dinh_ly.md`: trường hợp toán tử đơn điệu đi trọn với hai chỗ cần kiểm nặng, trường hợp giả đơn điệu để như mở rộng có điều kiện. Điều kiện then chốt đã xác nhận là sai số chiếu và sai lệch quán tính đều phải nhỏ hơn hệ số độ nhớt theo nghĩa chia cho hệ số đó thì tiến về không. Chứng minh vẫn cần người hướng dẫn kiểm định độc lập; số liệu chỉ minh họa, không thay thế chứng minh.
- Nên đo trực tiếp tốc độ hội tụ của vòng lặp Chambolle-Pock trên bài chiếu này để xác nhận hay bác giả định tốc độ tuyến tính trong mệnh đề chi phí, vì đây là điểm mà một người phản biện kỹ tính sẽ soi.

## 5. Vị trí trong toàn bộ dự án

Giai đoạn này đã biến hạt nhân còn sống của dự án, tức phép chiếu xấp xỉ có khởi tạo ấm, thành một sơ đồ bốn pha đúng chuẩn với bước phản xạ thật, và thu được số liệu ủng hộ mệnh đề chi phí đã sửa. Đóng góp vẫn thuộc loại hợp nhất kỹ thuật cộng một mệnh đề chi phí, phù hợp tạp chí hạng trung như đã định vị, không phải đột phá. Bước quyết định tiếp theo là chứng minh định lý, thuộc về người hướng dẫn.
