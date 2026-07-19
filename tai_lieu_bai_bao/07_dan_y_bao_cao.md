# Dàn ý báo cáo về các đóng góp của giai đoạn nghiên cứu

Tài liệu này là dàn ý, chưa phải báo cáo. Mỗi mục ghi rõ mục tiêu, nội dung cần viết, số liệu cần trích và độ dài ước tính, để khi viết chỉ việc điền. Độ dài toàn báo cáo dự kiến 18 đến 22 trang.

Quy ước chung khi viết: dùng một thuật ngữ duy nhất cho một khái niệm từ đầu đến cuối, theo bảng ở phụ lục A; không phóng đại; mọi con số phải trích từ tệp kết quả có thật, không gõ tay.

---

## Phần mở đầu

### Mục 1. Tóm tắt

Mục tiêu: để người đọc nắm toàn bộ trong một trang.

Nội dung cần viết, theo thứ tự:
- Điểm xuất phát: đề tài đã có một báo cáo thực nghiệm kết luận rằng bốn khẳng định ban đầu chỉ có một đứng vững, và hướng thực nghiệm đã đóng.
- Việc đã làm trong giai đoạn này: chuyển trọng tâm sang phần thuật toán và giải tích số, xây lại sơ đồ cho đúng, tìm được một đóng góp kỹ thuật dùng được, và viết bản thảo bài báo.
- Đóng góp chính, nêu đúng ba điều: chứng chỉ sai số tính được cho phép chiếu xấp xỉ; chế độ ngân sách thích nghi dựa trên chứng chỉ đó, rẻ hơn phép chiếu chính xác từ 5 đến 9,7 lần về thời gian thuật toán; và một giao thức đo chi phí công bằng.
- Kết luận về mức công bố: bài phù hợp một tạp chí thuộc nhóm Q2, không phải Q1, và nêu lý do trong một câu là phần định lý hội tụ chỉ là mở rộng của kết quả đã có.
- Một câu về phần chưa xong: hai chi tiết kỹ thuật trong chứng minh.

Độ dài: 1 trang. Không đưa bảng vào mục này.

### Mục 2. Bối cảnh và điểm xuất phát

Mục tiêu: nối liền với báo cáo thực nghiệm trước, để thầy thấy tính liên tục.

Nội dung cần viết:
- Nhắc lại ngắn gọn bài toán: bài toán ngược trong xử lý ảnh đặt dưới dạng bất đẳng thức biến phân trên tập ràng buộc.
- Nhắc lại kết luận của báo cáo trước: ba trên bốn khẳng định không đạt, nguyên nhân có tính cấu trúc chứ không do lỗi cài đặt. Trích đúng ba con số làm bằng chứng: hệ số vô hướng học được đạt 28,31 dB so với 28,91 dB của hệ số hằng; phương pháp của đề tài thua Plug-and-Play 0,59 dB ở chế độ khớp và 0,88 dB ở chế độ lệch.
- Nêu điều duy nhất còn đứng vững: lợi thế chi phí của phép chiếu xấp xỉ có khởi tạo ấm.
- Phát biểu câu hỏi của giai đoạn này: có thể biến điều còn đứng vững đó thành một đóng góp công bố được hay không.

Độ dài: 1,5 trang.

### Mục 3. Phương pháp làm việc

Mục tiêu: giải thích vì sao kết quả trong báo cáo này đáng tin. Đây là mục nên viết kỹ vì nó là điểm mạnh của công trình.

Nội dung cần viết:
- Nguyên tắc thứ nhất, đặt tiêu chí trước khi chạy. Mọi mức phần dư biến phân mục tiêu được ấn định trước và độc lập với kết quả của mọi cấu hình.
- Nguyên tắc thứ hai, cho phương pháp đối chứng cơ hội mạnh nhất. Phương pháp đối chứng được dò tham số với cùng số cấu hình như phương pháp đề xuất, cụ thể tám cấu hình mỗi bên.
- Nguyên tắc thứ ba, phản biện đối kháng. Mỗi bản thảo chứng minh và mỗi kết luận số đều được đưa qua một vòng phản biện độc lập trước khi chấp nhận. Nêu con số: quy trình này đã bác hai bản thảo chứng minh và tìm ra ba lỗi phương pháp luận trong chính phần đo của chúng ta.
- Nguyên tắc thứ tư, ghi lại kết quả âm tính. Mọi hướng đã thử và thất bại đều được ghi kèm số liệu để không lặp lại.

Độ dài: 2 trang.

---

## Phần đóng góp

### Mục 4. Định vị lại hướng nghiên cứu

Mục tiêu: cho thấy việc chọn hướng dựa trên khảo sát tài liệu chứ không phải cảm tính.

Nội dung cần viết:
- Mô tả cách khảo sát: năm góc độc lập, mỗi góc trả về danh sách bài kèm thuộc tính phân biệt.
- Kết quả khảo sát, chia tài liệu thành hai nhánh: nhánh các phương pháp có quán tính và độ nhớt dùng phép chiếu chính xác; nhánh phép chiếu xấp xỉ nhưng không có quán tính, không có độ nhớt.
- Nêu tên các bài chặn quan trọng nhất, mỗi bài một câu về nội dung: Malitsky 2015 về phương pháp chiếu phản xạ; Díaz Millán, Ferreira và Ugon 2024 về phép chiếu xấp xỉ với tiêu chuẩn sai số tương đối; bài về phép chiếu xấp xỉ có độ nhớt năm 2025; Tan và Qin 2020.
- Kết luận của khảo sát: khe hở còn lại là ghép bước phản xạ với phép chiếu xấp xỉ, và đây là khe hở hẹp.
- Một đoạn về việc kiểm rủi ro: bài trên tạp chí mục tiêu năm 2023 có tên gợi ý đã bao gồm phép chiếu xấp xỉ, đã kiểm và xác nhận không phải, nên khe hở vẫn còn.

Độ dài: 2 trang. Kèm một bảng hai cột liệt kê các bài chặn và điểm khác biệt.

### Mục 5. Sửa sai trong thiết kế và danh pháp

Mục tiêu: đây là đóng góp ít hào nhoáng nhưng quan trọng, nên viết thẳng thắn.

Nội dung cần viết:
- Phát hiện thứ nhất, sai danh pháp: pha thứ ba của sơ đồ ban đầu được gọi là hiệu chỉnh phản xạ, nhưng thực chất là hiệu chỉnh kiểu Tseng, vốn tính toán tử hai lần mỗi bước; bước phản xạ kiểu Malitsky dùng điểm phản xạ và chỉ tính toán tử một lần. Nêu hệ quả: cách gọi sai đã che mờ việc định vị so với tài liệu, vì gọi đúng tên thì sơ đồ gần trùng một bài đã công bố.
- Phát hiện thứ hai, bỏ bước quán tính. Nêu lý do lý thuyết là nó cắt đứt chuỗi phép chiếu mà bổ đề một bước cần, và lý do số liệu là bỏ nó không làm mất kết quả. Trích số: có quán tính đạt 24,3458 dB với phần dư 1,242 nhân mười mũ trừ hai; không quán tính đạt 24,3458 dB với phần dư 1,243 nhân mười mũ trừ hai.
- Phát hiện thứ ba, bỏ bước neo, kèm lý do kép sẽ nói ở mục 7.
- Phát hiện thứ tư, sửa một niềm tin sai tồn tại lâu: phép kẹp về ràng buộc hộp không phá cấu trúc toán tử gần kề, vì hộp tách được theo từng tọa độ. Đã kiểm bằng tìm kiếm vét cạn, sai lệch một phần mười nghìn do lưới.

Độ dài: 2 trang.

### Mục 6. Chứng chỉ sai số tính được

Mục tiêu: đây là đóng góp kỹ thuật chính, nên viết kỹ nhất trong các mục đóng góp.

Nội dung cần viết:
- Phát biểu vấn đề cho rõ: định nghĩa phép chiếu xấp xỉ trong tài liệu đòi kiểm khoảng cách tới phép chiếu chính xác, mà phép chiếu chính xác lại chính là thứ thuật toán sinh ra để tránh tính. Đây là một vòng luẩn quẩn, và nó khiến chế độ ngân sách trong thực thi nằm ngoài phạm vi định lý.
- Cách gỡ: bài toán chiếu có hàm mục tiêu lồi mạnh với tham số một, nên khoảng cách tới nghiệm chiếu bị chặn bởi căn của hai lần khoảng cách đối ngẫu; khoảng cách đối ngẫu tính trực tiếp từ cặp biến gốc và đối ngẫu mà thuật toán Chambolle-Pock đã có sẵn.
- Viết công thức hàm mục tiêu gốc và hàm mục tiêu đối ngẫu cho bài toán chiếu lên quả cầu biến phân toàn phần.
- Nêu rõ vị thế của đóng góp, không phóng đại: bất đẳng thức này là kiến thức chuẩn trong giải tích lồi; đóng góp nằm ở việc dùng nó làm giao diện giữa lý thuyết và bộ giải nội, điều mà các bài về phép chiếu xấp xỉ đều bỏ ngỏ.
- Kiểm chứng: chứng chỉ là chặn trên hợp lệ ở mọi số bước nội đã thử, không bao giờ đánh giá thấp sai số thật.
- Cái giá phải trả, nêu thẳng: chứng chỉ bi quan, tỉ lệ giữa chặn trên và sai số thật tăng từ khoảng 2 lên khoảng 12 khi tiến gần nghiệm; dừng theo chứng chỉ tốn nhiều hơn dừng theo sai số thật từ 2,6 đến 5,8 lần.

Độ dài: 3 trang. Kèm bảng kiểm chứng chặn trên theo số bước nội.

### Mục 7. Ngân sách thích nghi và kết quả chi phí

Mục tiêu: trình bày kết quả số chính.

Nội dung cần viết:
- Mô tả chế độ: chạy vòng lặp nội cho tới khi chứng chỉ đạt lịch sai số đặt trước, với lịch giảm theo lũy thừa lớn hơn một để dãy sai số tổng được.
- Thiết lập thực nghiệm: khử mờ ảnh, hai loại mờ, ảnh xám cạnh 96 điểm ảnh, tám ảnh kiểm tra, 150 bước ngoài, chạy trên máy chủ có bộ xử lý đồ họa.
- Bảng kết quả chính, trích nguyên từ tệp kết quả: ở mức phần dư 2,0 nhân mười mũ trừ hai, phép chiếu chính xác tốn 3858 bước nội và 5,13 giây, chế độ thích nghi tốn 275 bước nội và 0,70 giây; các mức khác tương tự. Hệ số trên mờ Gauss là 13,2 đến 19,2 lần theo bước nội và 4,7 đến 9,7 lần theo thời gian; trên mờ chuyển động là 17,2 đến 23,6 lần và 6,2 đến 8,7 lần.
- Một điểm mạnh phải nêu: mọi cấu hình cho nghiệm khả thi tuyệt đối, mức vi phạm ràng buộc bằng 1,0000, trong khi ngân sách cố định cho đầu ra vi phạm ràng buộc tới vài phần trăm.
- Mục nhỏ về chỗ phương pháp thua, viết ngang hàng với phần thắng: lịch quá siết làm chi phí bùng nổ, cấu hình xấu nhất tốn hơn phép chiếu chính xác khoảng 50 lần; quy luật chọn lịch là số mũ sát một từ phía trên và hệ số đầu lớn.
- Mục nhỏ về tính tổng được của dãy sai số: đo trên 3000 bước ngoài, dịch chuyển của bước chiếu giảm với độ dốc âm 2,34 trên mờ Gauss và âm 2,84 trên mờ chuyển động khi không có bước neo, tổng tích lũy bão hòa. Khi có bước neo, độ dốc tụt về âm 1,011, tức sát ngưỡng phân kỳ. Đây là lý do thứ hai để bỏ bước neo, bên cạnh lý do về chuỗi phép chiếu.

Độ dài: 3 trang. Kèm hai bảng và, nếu có thời gian, một hình về đường đánh đổi chi phí theo mức phần dư.

### Mục 8. Giao thức đo chi phí công bằng

Mục tiêu: đây là đóng góp về phương pháp luận, và cũng là chỗ ta tự sửa mình, nên viết trung thực.

Nội dung cần viết:
- Nêu ba lỗi đã tự phát hiện và sửa, mỗi lỗi một đoạn:
  - Chỉ đếm bước nội mà không đo thời gian. Bước nội của chế độ thích nghi đắt hơn vì phải tính chứng chỉ, nên hệ số theo bước nội thổi phồng lợi thế. Cách sửa là báo cả hai thước đo.
  - Mức phần dư mục tiêu lấy từ chính kết quả của phương pháp đối chứng, tức chọn sau khi thấy số liệu. Cách sửa là ấn định trước.
  - Dò tham số bất đối xứng, mười sáu cấu hình cho phương pháp đề xuất và hai cho phương pháp đối chứng. Cách sửa là dò bằng nhau.
- Nêu một lỗi kỹ thuật đã sửa: đo thời gian trên bộ xử lý đồ họa mà không đồng bộ hóa thì chỉ đo thời gian xếp lệnh, không phải thời gian tính.
- Nêu một bẫy đo lường đã tránh: nếu áp lịch bước tăng tốc cho mọi chế độ thì hệ số tiết kiệm trông tăng từ 2,37 lên 3,46 lần, nhưng đó là do phương pháp đối chứng bị làm chậm chứ không phải phương pháp đề xuất tốt lên.
- Kết luận của mục: con số đáng tin là con số đo sau khi sửa cả ba lỗi.

Độ dài: 2 trang.

### Mục 9. Phần lý thuyết

Mục tiêu: trình bày trung thực những gì đã chứng minh và những gì chưa.

Nội dung cần viết:
- Phát biểu bài toán và sơ đồ cuối cùng, hai dòng, không quán tính và không neo.
- Liệt kê các giả thiết, và giải thích vì sao tính đơn điệu phải đặt trên toàn không gian chứ không chỉ trên tập ràng buộc, cụ thể vì điểm phản xạ nằm ngoài tập ràng buộc.
- Nêu rõ vai trò của giả thiết khả thi: nó không phải chi tiết cài đặt mà là điều kiện của định lý, vì nó cho phép giữ dấu của số hạng telescoping. Đây cũng là chỗ nối thực nghiệm với lý thuyết, vì mức vi phạm bằng 1,0000 trong thực nghiệm chính là giả thiết này.
- Phần đã chứng minh đầy đủ và đã qua phản biện: bốn bổ đề, và bước ghép thế năng cho trường hợp phép chiếu chính xác, trong đó có đẳng thức làm hai số hạng âm gộp lại cùng một hệ số.
- Phần nhiễu do phép chiếu xấp xỉ: hai đường nhiễu, và kết quả dẫn xuất hằng số.
- Kết luận trung thực nhất của mục này: hằng số nhiễu không chứa nghịch đảo bước nhảy, nên định lý hội tụ là một mở rộng của kết quả đã có chứ không phải cơ chế mới. Nêu rõ đây là lý do bài nhắm nhóm Q2 chứ không phải Q1.
- Hai chi tiết còn lại: phát biểu chính xác bổ đề tựa Fejér, và bước giới hạn yếu trong không gian vô hạn chiều.

Độ dài: 3 trang.

---

## Phần hồ sơ

### Mục 10. Các kết quả âm tính đã ghi nhận

Mục tiêu: ghi lại các hướng đã đóng để không ai lặp lại. Mỗi hướng viết một đoạn ngắn theo cùng khuôn: ý tưởng, lý do hợp lý ban đầu, số liệu, nguyên nhân thất bại.

Bốn hướng cần ghi:
- Lịch bước tăng tốc cho bài toán chiếu. Không cải thiện trong chế độ khởi tạo ấm với ngân sách nhỏ; tốn nhiều hơn từ 0,69 đến 0,84 lần. Nguyên nhân là lịch tăng tốc co bước ngay từ đầu và được đặt lại mỗi bước ngoài.
- Siết chứng chỉ bằng cách theo dõi giá trị tốt nhất. Không giảm được bước nào, vì thuật toán vốn đã cho giá trị gần đơn điệu.
- Tiêu chuẩn sai số tương đối theo chuẩn toán tử. Sai về lý thuyết, vì tại nghiệm có ràng buộc kích hoạt thì chuẩn toán tử không tiến về không, nên sai số cho phép không tiến về không.
- Tiêu chuẩn chiếu nới lỏng. Không thực thi được: kiểm qua cận trên thì quá thô, ở đây vế trái là 120,25 còn vế phải là 0,31; kiểm qua chứng chỉ thì sai bậc, cần sai số nhỏ hơn dịch chuyển tới năm bậc.

Độ dài: 2 trang.

### Mục 11. Chất lượng mã nguồn và tính tái lập

Mục tiêu: cho thấy phần thực thi đủ tin cậy để người khác kiểm.

Nội dung cần viết:
- Bộ kiểm thử: mười bốn kiểm thử cho các tính chất toán học cốt lõi, không phải chi tiết cài đặt. Liệt kê vài kiểm thử tiêu biểu: đặc trưng biến phân của phép chiếu; chứng chỉ là chặn trên thật sự; khởi tạo ấm rẻ hơn khởi tạo lạnh; bước nhảy thỏa điều kiện.
- Dọn dẹp tính trung thực: đã gỡ khẳng định phần dư biến phân tiến về không khỏi cả tài liệu hướng dẫn lẫn mã nguồn, vì số liệu chỉ cho thấy phần dư giảm từ 2,48 xuống 0,199 và giảm không đơn điệu; đã sửa danh pháp pha hiệu chỉnh.
- Tổ chức mã nguồn: liệt kê các tệp chính và vai trò, tổng khoảng 1500 dòng lệnh cho phần lý thuyết.
- Tính tái lập: mã nguồn, dữ liệu thô và kịch bản phân tích công khai trên kho lưu trữ; các lệnh chạy lại từng thí nghiệm được ghi rõ.
- Hạ tầng tính toán: chạy trên máy chủ có bộ xử lý đồ họa, kèm ghi chú về ba trở ngại môi trường đã xử lý.

Độ dài: 1,5 trang.

### Mục 12. Sản phẩm bàn giao

Mục tiêu: liệt kê để thầy biết có gì trong tay.

Nội dung: bảng ba cột gồm tên sản phẩm, vị trí, và mô tả một dòng. Các sản phẩm gồm: bản thảo bài báo bằng tiếng Anh đã biên dịch; tài liệu định vị và khảo sát tài liệu; báo cáo số liệu; hai bản thảo chứng minh kèm biên bản phản biện; bản chứng minh hiện hành; các tệp kết quả thô; mã nguồn và bộ kiểm thử.

Độ dài: 1 trang.

---

## Phần kết

### Mục 13. Hạn chế

Mục tiêu: nêu đủ để người đọc hiểu đúng phạm vi, không tự bào chữa.

Nội dung, mỗi hạn chế một đoạn:
- Chỉ một tập ràng buộc là quả cầu biến phân toàn phần, và hai loại mờ.
- Chưa so sánh với bất kỳ phương pháp đã công bố nào; mọi so sánh là giữa các chế độ của cùng một sơ đồ.
- Bán kính quả cầu đặt theo thông tin của ảnh sạch, tức thông tin mà một triển khai thật không có.
- Lợi thế đo được là chi phí ở cùng độ chính xác, không phải chất lượng khôi phục ảnh.
- Hai chi tiết trong chứng minh chưa viết đầy đủ.

Độ dài: 1,5 trang.

### Mục 14. Việc còn lại và khuyến nghị

Mục tiêu: cho thầy một danh sách quyết định được ngay.

Nội dung, theo thứ tự ưu tiên:
- Việc thứ nhất, kiểm hai chi tiết còn lại của chứng minh. Ước lượng công sức: một đến hai tuần.
- Việc thứ hai, bổ sung so sánh với hai hoặc ba phương pháp đã công bố, vì người phản biện chắc chắn sẽ hỏi. Ước lượng: ba đến năm tuần.
- Việc thứ ba, chọn tạp chí. Đề xuất Optimization là lựa chọn chính.
- Khuyến nghị về mức công bố, nói thẳng: không nên nhắm nhóm Q1 với phần định lý hiện tại, vì đã chứng minh được rằng nó là mở rộng.

Độ dài: 1 trang.

### Mục 15. Phụ lục

- Phụ lục A: bảng thuật ngữ, hai cột tiếng Việt và tiếng Anh, để bảo đảm dùng nhất quán.
- Phụ lục B: các lệnh chạy lại thí nghiệm.
- Phụ lục C: danh mục tệp kết quả kèm chú thích thuộc thí nghiệm nào.
- Phụ lục D: biên bản các vòng phản biện, tóm tắt mỗi vòng vài dòng.

Độ dài: 2 trang.

---

## Ghi chú cho người viết

Ba điều nên giữ khi viết báo cáo này:

Thứ nhất, mỗi con số phải kèm nguồn là tên tệp kết quả. Việc này đã làm được vì mọi con số trong bản thảo bài báo đã được đối chiếu tự động với tệp gốc.

Thứ hai, các mục 8 và 10 là chỗ báo cáo tự nêu sai sót của chính mình. Không nên rút gọn hai mục này; chúng là bằng chứng cho thấy các con số còn lại đáng tin.

Thứ ba, tránh dùng hai từ khác nhau cho cùng một khái niệm. Ví dụ đã thống nhất: luôn viết phép chiếu xấp xỉ, không viết chiếu gần đúng; luôn viết phần dư biến phân, không viết sai số hội tụ; luôn viết bước nội và bước ngoài, không viết vòng trong và vòng ngoài.
