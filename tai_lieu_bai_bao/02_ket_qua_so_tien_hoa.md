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

## 2b. Thử nghiệm lịch bước tăng tốc: kết quả âm tính

Ý tưởng đã thử: bài toán chiếu lên quả cầu biến phân toàn phần có hàm mục tiêu lồi mạnh với tham số 1, nên về nguyên tắc dùng được lịch bước tăng tốc của Chambolle-Pock (thuật toán 2) để giảm số bước nội. Điều này vừa hứa hẹn giảm chi phí vừa vá giả thiết tốc độ của mệnh đề chi phí.

Kết quả: không cải thiện. Với cùng ngân sách bước nội, bản tăng tốc cho phần dư cao hơn bản cơ bản. Để đạt cùng mức phần dư trên mờ Gauss, số bước nội của bản tăng tốc so với bản cơ bản là 1,00 lần ở ngân sách hai bước, 0,84 lần ở ngân sách năm bước, 0,76 lần ở ngân sách log, và 0,69 lần ở chiếu chính xác; nghĩa là tăng tốc tốn nhiều hơn ở hầu hết chế độ.

Nguyên nhân: lịch tăng tốc làm bước nguyên thủy co lại ngay từ những bước đầu và được đặt lại ở mỗi bước ngoài, nên trong chế độ khởi tạo ấm với ngân sách nhỏ nó không kịp phát huy. Đo riêng trên bài toán chiếu từ khởi tạo lạnh xác nhận đúng cơ chế này: bản tăng tốc nhanh hơn 2,61 lần ở sai số tương đối một phần trăm và 1,82 lần ở một phần nghìn, nhưng chậm hơn, còn 0,82 lần, ở một phần trăm nghìn. Nó có lợi khi chiếu lạnh chạy dài ở độ chính xác thấp, đúng chế độ mà phương pháp này không dùng.

Một bẫy đo lường cần ghi lại. Nếu áp tăng tốc cho mọi chế độ, hệ số tiết kiệm so với chiếu chính xác trông tăng từ 2,37 lên 3,46 lần. Nhưng đó là vì baseline chiếu chính xác bị làm chậm đi, từ 384 lên 560 bước nội, chứ không phải vì phép chiếu xấp xỉ tốt lên. Báo con số 3,46 lần sẽ là phóng đại giả tạo. Theo nguyên tắc cho baseline cơ hội mạnh nhất mà báo cáo thực nghiệm đã đặt ra, baseline đúng là bản cơ bản, và hệ số tiết kiệm thật ở cấu hình này là khoảng 2,4 lần.

Quyết định: giữ Chambolle-Pock cơ bản cho mọi chế độ. Cờ tăng tốc được giữ lại trong mã nguồn như một tùy chọn đã kiểm thử và như hồ sơ của một hướng đã thử và đóng; mặc định tắt. Quan sát này cũng đáng đưa vào bài như lý do biện minh cho việc dùng bản cơ bản, thay vì để người phản biện hỏi tại sao không khai thác tính lồi mạnh.

## 2c. Chứng chỉ sai số tính được và ngân sách thích nghi: kết quả dương tính

Đây là tiến bộ có giá trị nhất của vòng tiến hóa, vì nó vá một lỗ hổng mức chặn mà vòng phản biện đã bắt, đồng thời cải thiện kết quả.

Vấn đề. Tiêu chuẩn sai số cũ đòi biết khoảng cách tới nghiệm chiếu chính xác, tức chính đại lượng mà thuật toán được thiết kế để né. Vì vậy chế độ ngân sách cố định chỉ là heuristic nằm ngoài định lý, và cả chế độ chiếu chính xác dùng làm baseline cũng phải dựa vào nghiệm tham chiếu, là thông tin oracle mà một triển khai thật không có.

Cách vá. Bài toán chiếu có hàm mục tiêu lồi mạnh với tham số 1, nên khoảng cách đối ngẫu cho một chứng chỉ tính được: khoảng cách tới nghiệm chiếu bị chặn bởi căn của hai lần khoảng cách đối ngẫu, tính trực tiếp từ cặp biến gốc và đối ngẫu mà Chambolle-Pock đã có sẵn. Từ đó dựng được chế độ ngân sách thích nghi: chạy vòng lặp nội tới khi chứng chỉ đạt lịch sai số đặt trước, với lịch giảm theo lũy thừa lớn hơn một nên dãy sai số tổng được. Đây là chế độ duy nhất thực thi được đúng như định lý đòi hỏi.

Kiểm chứng chứng chỉ: chặn trên hợp lệ ở mọi số bước, không bao giờ đánh giá thấp sai số thật. Cái giá là nó bi quan, tỉ lệ giữa chặn trên và sai số thật tăng từ 2,2 lên khoảng 12 lần khi tiến gần nghiệm; đo riêng cho thấy dừng theo chứng chỉ tốn khoảng 2,6 đến 5,8 lần nhiều bước hơn dừng theo sai số thật. Đây là cái giá phải trả cho một tiêu chuẩn thực thi được, và phải nói rõ trong bài.

Kết quả, đo trên mờ Gauss, ảnh cạnh 48 điểm ảnh, 40 bước ngoài, hai ảnh kiểm tra:

| chế độ | PSNR (dB) | phần dư | tổng bước nội | mức vi phạm ràng buộc |
|---|---|---|---|---|
| ngân sách thích nghi, tính được | 23,969 | 4,38 nhân mười mũ trừ hai | 124 | 1,0000 |
| chiếu chính xác theo chứng chỉ, tính được | 23,913 | 4,92 nhân mười mũ trừ hai | 268 | 1,0000 |
| ngân sách cố định hai bước, dùng oracle | 23,875 | 5,03 nhân mười mũ trừ hai | 80 | 1,0038 |
| chiếu chính xác, dùng oracle | 23,994 | 2,99 nhân mười mũ trừ hai | 352 | 1,0004 |

Ba kết luận.

Thứ nhất, lợi thế chi phí đứng vững trong thế giới thực thi được: ngân sách thích nghi đạt cùng mức phần dư với 124 bước nội so với 268 của chiếu chính xác theo chứng chỉ, tức rẻ hơn 2,16 lần. So với chiếu chính xác dùng oracle thì rẻ hơn khoảng 2,8 lần. Đây là con số so trong cùng một thế giới, không mượn oracle cho bên nào.

Thứ hai, chế độ thích nghi cho nghiệm khả thi tuyệt đối, mức vi phạm bằng 1,0000, vì nó trả về điểm đã ép khả thi. Điều này giải quyết luôn một điểm yếu cũ: ngân sách cố định cho đầu ra vi phạm ràng buộc, ở đây là 0,38 phần trăm và trong các thí nghiệm trước lên tới 1 đến 8 phần trăm. Nhờ vậy không cần bước ép khả thi riêng khi đo.

Thứ ba, chế độ thích nghi tốt hơn ngân sách cố định về cả chất lượng lẫn phần dư lẫn tính khả thi, chỉ tốn thêm bước nội (124 so với 80). Đổi lại nó nằm trong định lý, còn ngân sách cố định thì không.

Lưu ý trung thực về phạm vi: các con số trên đo ở quy mô nhỏ nên mang tính định hướng; lịch sai số quá lỏng, ví dụ hệ số đầu bằng 5, không đạt mức phần dư mục tiêu, nên việc chọn lịch cần được nêu rõ trong bài.

## 2d. Dò lịch sai số trên GPU: kết quả tốt nhất của dự án, và mặt trái của nó

Chạy trên máy chủ có GPU NVIDIA L40S, ảnh cạnh 96 điểm ảnh, 150 bước ngoài, 8 ảnh kiểm tra, 18 cấu hình cho mỗi loại mờ. Mọi chế độ đều nằm trong thế giới thực thi được: cả chế độ thích nghi lẫn chiếu chính xác đều dừng theo chứng chỉ tính được, không bên nào dùng nghiệm tham chiếu. Mốc so sánh là chiếu chính xác theo chứng chỉ với ngưỡng 0,02, và mức phần dư mục tiêu lấy từ chính mốc đó.

Cảnh báo quan trọng, thêm sau vòng phản biện: các hệ số dưới đây chỉ đúng ở đơn vị bước nội và không chuyển thành lợi thế thời gian. Xem mục 2e trước khi trích bất kỳ con số nào ở đây.

Cấu hình tốt nhất trên mờ Gauss là lịch với hệ số đầu 2,0 và số mũ 1,01: đạt mức phần dư mục tiêu với 448 bước nội so với 5763 của chiếu chính xác, tức rẻ hơn 12,86 lần tính theo bước nội. Trên mờ chuyển động, lịch với hệ số đầu 4,0 và số mũ 1,01 đạt 570 bước so với 8494, tức rẻ hơn 14,90 lần theo bước nội; ở cấu hình này PSNR gần như bằng chiếu chính xác (26,8253 so với 26,8265 dB) trong khi phần dư còn thấp hơn (1,047 so với 1,141 nhân mười mũ trừ hai). Mọi cấu hình đều cho mức vi phạm ràng buộc bằng 1,0000, tức khả thi tuyệt đối.

Tính theo bước nội thì đây là con số cao nhất của dự án, nhưng mục 2e cho thấy nó không phản ánh chi phí thực.

Mặt trái, phải nêu ngang hàng với kết quả trên: việc chọn lịch quyết định tất cả, và lịch sai lầm còn tệ hơn không dùng chế độ thích nghi. Lịch quá siết, tức hệ số đầu nhỏ hoặc số mũ lớn, làm chi phí bùng nổ: với hệ số đầu 0,5 và số mũ 1,5 trên mờ Gauss, tổng bước nội lên tới 522808 và chỉ đạt 0,02 lần so với mốc, tức tốn gấp khoảng 50 lần chiếu chính xác. Nguyên nhân là lịch tuyệt đối siết sai số về không nhanh hơn mức bài toán cần, trong khi chứng chỉ lại bi quan, nên vòng lặp nội chạy thừa rất nhiều.

Quy luật rút ra từ bảng: số mũ nên lấy sát 1 từ phía trên, đủ để dãy sai số tổng được nhưng không siết thừa; hệ số đầu nên lấy lớn, cỡ 2 đến 4. Các cấu hình có số mũ 1,5 đều thất bại ở mọi hệ số đầu.

Một lưu ý về phạm vi của hệ số: con số 12,86 và 14,90 lần được đo tại một mức phần dư mục tiêu cụ thể, lấy từ mốc chiếu chính xác với ngưỡng 0,02. Nếu đòi mức phần dư thấp hơn nhiều, chế độ thích nghi buộc phải dùng lịch siết hơn và khi đó nó thua chiếu chính xác. Nói cách khác, tồn tại một vùng vận hành mà chế độ thích nghi thắng lớn và một vùng mà nó thua; bài phải trình bày cả đường đánh đổi chứ không chỉ điểm thắng.

## 2e. Hội đồng phản biện mô phỏng bác bỏ hệ số 12,86 và 14,90 lần

Bốn phản biện mô phỏng độc lập đều cho phán quyết từ chối và đều xác nhận hồ sơ chưa nộp được ở đâu. Quan trọng nhất, họ bắt được một lỗi nghiêm trọng trong chính con số ở mục 2d. Ghi lại đầy đủ ở đây vì đây là bài học phương pháp luận, không phải chi tiết nhỏ.

Lỗi thứ nhất, mức chặn: hệ số chỉ tồn tại ở đơn vị bước nội và bốc hơi ở thời gian thực. Đọc thẳng từ hai tệp kết quả:

| loại mờ | cấu hình | bước nội | thời gian (giây) | hệ số theo bước nội | hệ số theo thời gian |
|---|---|---|---|---|---|
| Gauss | thích nghi 2,0 và 1,01 | 486 | 46,9 | 11,88 | 1,19 |
| Gauss | chiếu chính xác 0,02 | 5772 | 55,8 | 1 | 1 |
| chuyển động | thích nghi 4,0 và 1,01 | 596 | 31,4 | 14,27 | 1,18 |
| chuyển động | chiếu chính xác 0,02 | 8503 | 37,1 | 1 | 1 |

Nguyên nhân: mỗi bước nội của chế độ thích nghi phải tính chứng chỉ, tức thêm một lần tính hàm mục tiêu gốc và đối ngẫu cùng một phép ép khả thi, nên đắt hơn nhiều một bước Chambolle-Pock trần. Tiết kiệm được mười hai lần số bước nhưng mỗi bước đắt lên khoảng mười lần thì lợi thế gần như triệt tiêu. Đây đúng là điều mà báo cáo thực nghiệm gốc đã yêu cầu ở phần đo chi phí trung thực: phải báo cả tổng bước nội lẫn thời gian chạy thực, vì tổng bước nội không phản ánh độ nặng của mỗi bước. Hồ sơ đã vi phạm chính nguyên tắc của mình.

Cần nói thêm cho chính xác: cột thời gian hiện gồm cả chi phí đo đạc dùng chung cho mọi chế độ, nên nó chưa phải phép so thời gian thuật toán sạch. Bộ giải có sẵn trường thời gian thuật toán tách riêng nhưng chương trình dò lịch không ghi trường đó. Vì vậy kết luận đúng ở mức hiện tại là: chưa có bằng chứng nào cho thấy lợi thế bước nội chuyển thành lợi thế thời gian, và dấu hiệu ban đầu là không. Phải đo lại trước khi tuyên bố bất cứ điều gì.

Lỗi thứ hai, mức chặn: mục tiêu so sánh định nghĩa vòng tròn. Mức phần dư mục tiêu được lấy từ chính phần dư cuối của chiếu chính xác rồi nới 5 phần trăm. Đây là chọn hậu nghiệm, và nó có lợi cơ học cho bên thách thức.

Lỗi thứ ba, mức chặn: bất đối xứng ngân sách dò tham số. Phương pháp đề xuất được dò 16 cấu hình, còn mốc so sánh chỉ 2. Theo đúng nguyên tắc cho baseline cơ hội mạnh nhất mà báo cáo gốc đặt ra, mốc phải được dò với cùng ngân sách.

Lỗi thứ tư: chứng chỉ qua khoảng cách đối ngẫu không phải đóng góp mới. Bất đẳng thức khoảng cách tới nghiệm bị chặn bởi căn hai lần khoảng cách đối ngẫu dưới tính lồi mạnh là kiến thức chuẩn trong tối ưu, không phải phát hiện. Nó là một nhận xét triển khai đúng đắn và hữu ích, nhưng không đứng được như một đóng góp lý thuyết.

Lỗi thứ năm, và là điểm sắc nhất mà cả năm góc khảo sát trước lẫn bốn phản biện chứng minh đều bỏ sót: nghịch lý dễ thì không mới, mới thì chưa chứng minh được. Lộ trình ở tệp 04 định chứng minh bằng cách xem phép chiếu xấp xỉ như một nhiễu ngoài tổng được rồi viện định lý bền vững với nhiễu năm 2017 cộng Malitsky 2015. Nếu làm được thì định lý thu được là hệ quả trực tiếp một dòng của hai kết quả đã in, và người phản biện sẽ viết đúng câu đó. Ngược lại, nếu giữ cấu trúc đủ mới để không viện được định lý bền vững thì phải chứng minh lại từ đầu, và đó chính là chỗ bản thảo cũ đã sụp. Hồ sơ đang đi giữa hai vực mà không nhận ra. Cửa duy nhất được chỉ ra: tìm một chỗ mà nhiễu chiếu không rút gọn về nhiễu ngoài tổng được, ví dụ nhiễu phụ thuộc trạng thái hoặc tiêu chuẩn sai số tương đối theo phần dư, khi đó sai số trở thành đại lượng phụ thuộc quỹ đạo.

Lỗi thứ sáu, rủi ro tồn vong: bài "A modified generalized version of projected reflected gradient method in Hilbert spaces" đăng năm 2023 ở chính tạp chí đang nhắm, chưa được đọc toàn văn. Chữ tổng quát hóa trong dòng này thường bao hàm cả nhiễu hoặc xấp xỉ. Nếu bài đó đã có phép chiếu xấp xỉ thì toàn bộ điểm mới còn lại biến mất. Phải đọc trước mọi việc khác.

Lỗi thứ bảy: hồ sơ tự mâu thuẫn về chính thuật toán. Tệp 04 chốt bỏ bước quán tính, trong khi tệp 01 vẫn mô tả sơ đồ có quán tính.

Điểm được ghi nhận là mạnh: tính trung thực của hồ sơ, được cả bốn phản biện nêu như tài sản thật; nghiệm khả thi tuyệt đối ở toàn bộ 36 cấu hình; nhận định điều kiện sai số chia hệ số neo tiến về không là cần chứ không chỉ tổng được; bộ kiểm thử kiểm tính chất toán học; và ví dụ giả đơn điệu có chứng chỉ số.

## 2f. Đo lại theo giao thức công bằng: con số cuối cùng và đáng tin nhất

Sau khi vòng phản biện bác bỏ hệ số ở mục 2d, giao thức đo đã được viết lại để sửa cả ba lỗi, rồi chạy lại toàn bộ trên GPU. Đây là con số nên dùng; mọi con số ở mục 2d và 2e đều bị thay thế bởi mục này.

Ba lỗi đã sửa. Thứ nhất, thời gian: bộ giải nay đồng bộ hóa GPU trước và sau mỗi đoạn tính (nếu không, phép đo chỉ tính thời gian xếp lệnh vào hàng đợi chứ không phải thời gian tính thật), và chương trình dò ghi thời gian thuật toán đã tách khỏi chi phí đo đạc. Thứ hai, mức phần dư mục tiêu nay là một danh sách ấn định trước, độc lập với mọi cấu hình, thay vì lấy từ phần dư cuối của baseline. Thứ ba, hai nhóm được dò với cùng ngân sách tám cấu hình, thay vì mười sáu chọi hai.

Kết quả trên mờ Gauss, ảnh cạnh 96 điểm ảnh, 150 bước ngoài, 8 ảnh:

| mức phần dư | bước nội, thích nghi | bước nội, chiếu chính xác | hệ số bước nội | thời gian, thích nghi | thời gian, chiếu chính xác | hệ số thời gian |
|---|---|---|---|---|---|---|
| 3,0e-2 | 198 | 3796 | 19,17 | 0,47 | 2,37 | 5,08 |
| 2,0e-2 | 275 | 3858 | 14,03 | 0,65 | 4,90 | 7,51 |
| 1,5e-2 | 357 | 5738 | 16,07 | 0,80 | 7,37 | 9,20 |
| 1,2e-2 | 476 | 8509 | 17,88 | 0,94 | 9,15 | 9,73 |
| 1,0e-2 | 649 | 8566 | 13,20 | 1,33 | 10,58 | 7,94 |

Trên mờ chuyển động: hệ số bước nội từ 17,23 đến 23,62 và hệ số thời gian từ 6,24 đến 8,68, ở bốn mức phần dư từ 3,0e-2 đến 1,2e-2.

Kết luận: lợi thế là thật và tồn tại ở cả hai thước đo. Tính theo thời gian thuật toán, chế độ thích nghi nhanh hơn chiếu chính xác khoảng 5 đến 9,7 lần trên mờ Gauss và 6,2 đến 8,7 lần trên mờ chuyển động, ổn định qua mọi mức phần dư mục tiêu ấn định trước.

Ba lưu ý trung thực đi kèm.

Thứ nhất, vì sao mục 2e kết luận lợi thế bốc hơi còn 1,18 lần: mục đó lấy cột thời gian tổng, mà cột này gồm chi phí đo đạc dùng chung cho mọi chế độ. Chi phí đo đạc lớn gấp vài chục lần bản thân thuật toán (khoảng 45 giây so với khoảng 1 giây), nên nó nhấn chìm mọi khác biệt. Phản biện đúng khi đòi phải đo thời gian, nhưng con số 1,18 lần là hệ quả của việc dùng sai cột, không phải sự thật về thuật toán. Con số ở mục này mới là con số đúng.

Thứ hai, một hiện vật phải loại: ở mức phần dư 1,0e-2 trên mờ chuyển động, tỉ lệ hiện ra là 563 lần theo bước nội và 312 lần theo thời gian. Đây không phải kết quả thật mà do các cấu hình chiếu chính xác ngưỡng chặt chạm trần bước nội (591795 và 600000 đúng bằng 150 nhân trần 4000), tức chúng không đạt được ngưỡng chứng chỉ trong trần cho phép. Không được trích con số này.

Thứ ba, phạm vi vẫn giới hạn: một tập ràng buộc, hai loại mờ, và chưa so với bất kỳ phương pháp đã công bố nào. Lợi thế đo được là lợi thế so với chính chiếu chính xác của cùng sơ đồ, không phải so với các phương pháp trong tài liệu.

## 2g. Cái giá của tính mới: tiêu chuẩn tương đối so với lịch tuyệt đối

Vòng phản biện chỉ ra một nghịch lý quyết định số phận bài: nếu sai số chiếu chỉ là một dãy nhiễu ngoài cho trước và tổng được, thì định lý hội tụ chỉ là hệ quả trực tiếp của định lý bền vững với nhiễu (2017) áp lên Malitsky (2015), tức không có tính mới; còn nếu giữ cấu trúc đủ mới để không viện được định lý bền vững thì phải chứng minh lại từ đầu, đúng chỗ bản thảo cũ đã sụp. Cửa duy nhất được chỉ ra là làm sai số phụ thuộc trạng thái.

Cửa đó đã được cài và đo. Chế độ tiêu chuẩn tương đối đặt sai số cho phép tỉ lệ với độ dài bước gradient tại mỗi bước ngoài, tức tỉ lệ với chuẩn của toán tử tại điểm phản xạ. Sai số khi ấy phụ thuộc quỹ đạo nên không rút gọn về một dãy cho trước; đây cùng họ với tiêu chuẩn tương đối của bài COAP 2024. Ba nhóm được dò với cùng ngân sách tám cấu hình, mọi mức phần dư mục tiêu ấn định trước.

Kết quả, hệ số so với chiếu chính xác theo chứng chỉ, đo bằng thời gian thuật toán:

| mức phần dư | lịch tuyệt đối, mờ Gauss | tiêu chuẩn tương đối, mờ Gauss | lịch tuyệt đối, mờ chuyển động | tiêu chuẩn tương đối, mờ chuyển động |
|---|---|---|---|---|
| 3,0e-2 | 5,14 | 3,26 | 7,42 | 1,80 |
| 2,0e-2 | 7,76 | 4,13 | 8,93 | 2,59 |
| 1,5e-2 | 10,05 | 4,34 | 10,58 | 2,57 |
| 1,2e-2 | 9,60 | 3,48 | 12,90 | 1,84 |

Kết luận, và đây là đánh đổi cốt lõi của bài: tính mới có giá. Lịch tuyệt đối nhanh nhất, 7,9 đến 12,9 lần so với chiếu chính xác, nhưng định lý đi kèm nó là hệ quả một dòng của hai kết quả đã in nên không bán được. Tiêu chuẩn tương đối mở được cửa tính mới nhưng lợi thế chi phí tụt đáng kể, còn 3,3 đến 4,3 lần trên mờ Gauss và chỉ 1,8 đến 2,6 lần trên mờ chuyển động. Tính theo bước nội, trên mờ chuyển động ở mức phần dư 1,2e-2 nó thậm chí tốn hơn chiếu chính xác, hệ số 0,87.

Nói cách khác, cái giá của việc thoát nghịch lý là mất khoảng hai đến năm lần lợi thế chi phí. Tiêu chuẩn tương đối vẫn nhanh hơn chiếu chính xác, nhưng khiêm tốn hơn hẳn.

Khuyến nghị cho quyết định chiến lược: nếu mục tiêu là một bài có tính mới bảo vệ được, phải chọn tiêu chuẩn tương đối và chấp nhận hệ số khiêm tốn hơn, vì hệ số lớn của lịch tuyệt đối đi kèm một định lý không bán được. Đây là lựa chọn cần bàn với người hướng dẫn.

Hai lưu ý trung thực. Thứ nhất, tính tổng được của dãy sai số dưới tiêu chuẩn tương đối không còn hiển nhiên như lịch tuyệt đối; nó phải được chứng minh cùng phân tích hội tụ, và đây chính là phần chưa làm. Thứ hai, phải loại hiện vật ở mức phần dư 1,0e-2 trên mờ chuyển động, nơi hệ số hiện ra là 563 và 489 lần cho lịch tuyệt đối và 44 và 91 lần cho tiêu chuẩn tương đối; con số này chỉ do cấu hình chiếu chính xác ngưỡng chặt chạm trần bước nội (435795 bước, 739 giây), không phải kết quả thật.

## 3. Diễn giải trung thực

Ba kết luận số ủng hộ hướng bài, với mức độ đúng như phát biểu, không phóng đại.

Thứ nhất, dịch chuyển giảm với độ dốc gần âm một dưới ngân sách cố định, khớp với việc bước độ nhớt áp đặt dịch chuyển cỡ βₖ bằng β₀ chia cho k cộng một. Đây là bằng chứng số cho đúng lỗi mà phản biện đã bắt: dưới ngân sách cố định, sai số chiếu bị nối với dịch chuyển này nên không bảo đảm tổng được. Ngân sách log cho sai số chiếu giảm với độ dốc khoảng âm hai, nhanh hơn hẳn, nên bảo đảm tổng được. Đây là lý do số học để chọn ngân sách log cho định lý.

Thứ hai, lợi thế chi phí của phép chiếu xấp xỉ so với chiếu chính xác khởi tạo ấm là một hệ số hằng khoảng 2,5 đến 2,8 lần ở mức phần dư trung bình, giảm dần khi đòi hỏi độ chính xác cao hơn. Đây đúng là mức mà mệnh đề chi phí đã sửa dự đoán, và phải giữ đúng mức này, không được trình bày thành khác biệt bậc. Con số này nhỏ hơn hệ số 7,6 đến 8,2 lần trong báo cáo thực nghiệm cũ, vì cấu hình khác: báo cáo cũ dùng sơ đồ chiếu-gradient thuần với ít bước ngoài, còn ở đây là sơ đồ bốn pha đầy đủ với nhiều bước ngoài hơn và định nghĩa chi phí chiếu chính xác chặt hơn.

Thứ ba, ví dụ giả đơn điệu đạt mục tiêu: chứng chỉ số tìm được cặp điểm với tích vô hướng âm, xác nhận toán tử không đơn điệu, trong khi thuật toán vẫn hội tụ. Nhờ đó định lý phát biểu cho lớp giả đơn điệu không rộng hơn ví dụ minh họa, một điểm mà người phản biện dòng này thường đòi hỏi.

## 4. Điều cần tiếp tục

- Lưới đã chạy xong cả mờ Gauss và mờ chuyển động, sáu chế độ ngân sách mỗi loại; số liệu đầy đủ trong `results/theory/phan_tich.md`. Mờ chuyển động cho hệ số tiết kiệm lớn hơn (khoảng 4 đến 7 lần) vì bài toán chiếu khó hơn.
- Bản thảo chứng minh định lý hội tụ mạnh đã được soạn trong `03_chung_minh_dinh_ly.md`, sau đó qua một vòng phản biện đối kháng bốn tác nhân độc lập. Phán quyết thống nhất: có lỗ hổng nghiêm trọng ở phần lõi, nên chứng minh chưa đứng vững. Lỗ hổng cốt lõi là bổ đề một bước của Malitsky đòi hỏi một chuỗi phép chiếu liền mạch, mà bước độ nhớt và bước quán tính trong sơ đồ làm đứt chuỗi đó; việc kết hợp quán tính với bước phản xạ là phần mới chưa có tiền lệ, phải chứng minh lại từ đầu chứ không mượn được. Biên bản lỗi và hai hướng sửa nằm ở mục 10 của `03_chung_minh_dinh_ly.md`. Điều đứng vững là nhận định về vai trò cần thiết của điều kiện sai số chia hệ số độ nhớt tiến về không, và phần khung dùng bước độ nhớt để ra hội tụ mạnh. Chứng minh là công việc toán chưa xong, cần người hướng dẫn quyết định hướng đi; số liệu chỉ minh họa, không thay thế chứng minh.
- Nên đo trực tiếp tốc độ hội tụ của vòng lặp Chambolle-Pock trên bài chiếu này để xác nhận hay bác giả định tốc độ tuyến tính trong mệnh đề chi phí, vì đây là điểm mà một người phản biện kỹ tính sẽ soi.

## 5. Vị trí trong toàn bộ dự án

Giai đoạn này đã biến hạt nhân còn sống của dự án, tức phép chiếu xấp xỉ có khởi tạo ấm, thành một sơ đồ bốn pha đúng chuẩn với bước phản xạ thật, và thu được số liệu ủng hộ mệnh đề chi phí đã sửa. Đóng góp vẫn thuộc loại hợp nhất kỹ thuật cộng một mệnh đề chi phí, phù hợp tạp chí hạng trung như đã định vị, không phải đột phá. Bước quyết định tiếp theo là chứng minh định lý, thuộc về người hướng dẫn.
