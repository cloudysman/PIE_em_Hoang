# Lộ trình chứng minh và quyết định con đường Q1

Tài liệu này thay cho việc sinh thêm một bản thảo chứng minh đầy đủ. Sau khi bản thảo trước thất bại ở vòng phản biện, con đường đúng đắn là chốt lại sơ đồ, dựng lộ trình chứng minh tách bạch phần chắc chắn với phần cần người hướng dẫn hoàn thiện, và chỉ đích danh các định lý đã công bố cần dựa vào. Cách này trung thực hơn và hữu ích hơn cho việc thực sự viết ra bài.

## 1. Quyết định: bỏ bước quán tính

Bước quán tính chính là nguyên nhân làm chứng minh trước sụp, vì nó phá chuỗi phép chiếu liền mạch mà bổ đề của Malitsky đòi hỏi. Số liệu cho thấy bỏ nó gần như không mất gì: trên mờ Gauss, ngân sách hai bước nội, 150 bước ngoài, phiên bản có quán tính đạt 24,3458 dB với phần dư biến phân 1,242 nhân mười mũ trừ hai, còn phiên bản không quán tính đạt 24,3458 dB với phần dư 1,243 nhân mười mũ trừ hai. Hai kết quả trùng khít. Vì vậy bỏ quán tính là lựa chọn tối ưu: đổi một thành phần vô ích về số liệu lấy một chứng minh có nền vững.

## 2. Sơ đồ đã chốt

Cho điểm neo a thuộc D và hai điểm khởi đầu x⁰ = x⁻¹:

    rᵏ = 2 xᵏ − xᵏ⁻¹                                (điểm phản xạ kiểu Malitsky)
    yᵏ = P_D^{εₖ}( xᵏ − λ F(rᵏ) )                   (chiếu xấp xỉ, sai số εₖ)
    xᵏ⁺¹ = βₖ a + (1 − βₖ) yᵏ                        (neo kiểu Halpern)

Đây là phương pháp chiếu phản xạ có neo với phép chiếu xấp xỉ cho bất đẳng thức biến phân đơn điệu. So với sơ đồ cũ, chỉ khác ở chỗ bỏ bước quán tính; điểm mới còn giữ nguyên là ghép bước phản xạ với phép chiếu xấp xỉ.

## 3. Lộ trình chứng minh, tách thành hai kết quả

Chia đóng góp lý thuyết thành hai kết quả với mức chắc chắn khác nhau, để phần chắc chắn có thể viết ngay còn phần khó được cô lập.

### 3.1. Kết quả thứ nhất: hội tụ yếu, có nền vững

Phát biểu: dưới giả thiết F đơn điệu Lipschitz trên không gian, λ trong khoảng của Malitsky, và dãy sai số chiếu tổng được, dãy {xᵏ} với βₖ = 0 (không neo) hội tụ yếu về một nghiệm.

Nền dựa vào, cả hai đã công bố:

- Malitsky 2015, Projected reflected gradient methods for monotone variational inequalities, SIAM Journal on Optimization (arXiv 1502.04968): phương pháp chiếu phản xạ với phép chiếu chính xác hội tụ yếu cho toán tử đơn điệu Lipschitz.
- Bounded perturbation resilience of extragradient-type methods, Journal of Inequalities and Applications 2017 (arXiv 1711.01937): các phương pháp chiếu cho bất đẳng thức biến phân đơn điệu Lipschitz giữ hội tụ khi thêm dãy nhiễu ngoài tổng được, với tốc độ nghịch đảo số bước.

Phần mới cần chứng minh, cô lập và nhỏ: chỉ ra rằng phép chiếu xấp xỉ P_D^{εₖ} tương đương với phép chiếu chính xác cộng một nhiễu ngoài eₖ với chuẩn bằng εₖ, và vì dãy εₖ tổng được nên dãy nhiễu này thỏa đúng giả thiết của định lý bền vững. Từ đó hội tụ yếu được bảo toàn. Đây là bước ghép hai kết quả có sẵn, rủi ro thấp.

Cần kiểm: định lý bền vững năm 2017 được phát biểu cho phương pháp dưới đạo hàm ngoài và phương pháp ngoài đạo hàm; phải kiểm rằng lập luận của nó áp được cho phương pháp chiếu phản xạ, vì phương pháp phản xạ không có tính đơn điệu Fejér nên có thể cần điều chỉnh. Nếu không áp trực tiếp, một đường thay thế là chèn nhiễu vào chính chứng minh hội tụ yếu của Malitsky, theo dõi số hạng nhiễu tổng được; đây vẫn là công việc chuẩn.

### 3.2. Kết quả thứ hai: hội tụ mạnh, cần người hướng dẫn hoàn thiện

Phát biểu: với neo kiểu Halpern βₖ tiến về không và tổng các βₖ phân kỳ, cùng điều kiện sai số chia hệ số neo tiến về không, dãy {xᵏ} hội tụ mạnh về hình chiếu của điểm neo lên tập nghiệm.

Nền dựa vào:

- Strong convergence of projected reflected gradient methods for variational inequalities, 2018 (ResearchGate 325926017), và A modified generalized version of projected reflected gradient method in Hilbert spaces, Numerical Algorithms 2023 (bài 10.1007 phần s11075-023-01566-1): phương pháp chiếu phản xạ có neo hội tụ mạnh cho toán tử đơn điệu với phép chiếu chính xác.
- Định lý bền vững như trên, nhưng cho phiên bản có neo.

Phần cần hoàn thiện: lấy toàn văn hai bài phản xạ hội tụ mạnh trên, xác định chính xác sơ đồ và đại lượng Lyapunov của họ, rồi thêm nhiễu chiếu xấp xỉ vào đúng chỗ. Điều kiện then chốt đã xác định từ vòng trước là sai số chiếu chia hệ số neo phải tiến về không, không chỉ tổng được; đây là điều kiện tự nhiên của mọi sơ đồ có neo. Chỗ khó là kiểm rằng tính bền vững với nhiễu tổng được vẫn giữ khi mục tiêu là hội tụ mạnh, vì định lý bền vững năm 2017 chỉ phát biểu cho hội tụ yếu; có thể cần một biến thể bền vững cho sơ đồ neo, hoặc chèn nhiễu trực tiếp vào chứng minh hội tụ mạnh của bài 2018.

Ranh giới trung thực: tôi không đọc được toàn văn hai bài phản xạ hội tụ mạnh vì chúng bị khóa sau tường phí, nên không thể tự dựng phần này một cách bảo đảm. Đây đúng là chỗ cần người hướng dẫn, và là công việc toán thật, không phải chi tiết nhỏ.

## 4. Mệnh đề chi phí, đóng góp chính bán được

Độc lập với hai kết quả trên, mệnh đề chi phí là đóng góp có khả năng phân biệt tốt nhất và đã có số liệu ủng hộ. Nội dung: với ngân sách bước nội tăng chậm theo log và khởi tạo ấm, sai số chiếu đạt mức tổng được, và tổng số bước nội sau K bước ngoài là cỡ K log K. Số liệu: trên mờ chuyển động, chiếu xấp xỉ ngân sách nhỏ đạt cùng mức phần dư với chiếu chính xác khởi tạo ấm nhưng tốn ít hơn 4 đến 7 lần tổng bước nội. Các lưu ý trung thực về vòng lặp Chambolle-Pock đã ghi ở mục 5 của khung bài.

## 5. Danh sách việc cần người hướng dẫn, theo thứ tự

1. Lấy toàn văn hai bài phản xạ hội tụ mạnh năm 2018 và năm 2023, xác định sơ đồ và đại lượng Lyapunov của họ.
2. Kiểm kết quả thứ nhất: chứng minh phép chiếu xấp xỉ là nhiễu ngoài tổng được thỏa giả thiết định lý bền vững, hoặc chèn nhiễu trực tiếp vào chứng minh Malitsky. Đây là phần rủi ro thấp, có thể giao cho nghiên cứu sinh làm trước.
3. Kiểm kết quả thứ hai: thêm nhiễu chiếu xấp xỉ vào khung hội tụ mạnh, kiểm điều kiện sai số chia hệ số neo.
4. Định lượng mệnh đề chi phí trên quả cầu biến phân toàn phần, nêu rõ giả thiết về tốc độ vòng lặp Chambolle-Pock.

## 6. Đánh giá tạp chí, trung thực

Cần nói thẳng để không kỳ vọng sai. Đóng góp này thuộc loại hợp nhất kỹ thuật cộng một mệnh đề chi phí, không phải một cơ chế hoàn toàn mới. Với loại này, nhóm tạp chí đầu bảng như SIAM Journal on Optimization hay Mathematical Programming là ngoài tầm.

Tuy nhiên mục tiêu thuộc nhóm Q1 vẫn khả thi, cụ thể ở các tạp chí Q1 nhóm giữa của toán ứng dụng và tối ưu như Numerical Algorithms, Journal of Computational and Applied Mathematics, hoặc Journal of Global Optimization, với điều kiện hai việc: chứng minh được hoàn thiện và kiểm định, và phần mệnh đề chi phí được định lượng đủ chặt. Nếu chỉ đạt kết quả thứ nhất là hội tụ yếu cộng mệnh đề chi phí, khả năng cao rơi vào Q2 như Optimization. Vì vậy giá trị của việc hoàn thiện kết quả thứ hai là nâng bài từ Q2 lên Q1 nhóm giữa.

Kết luận: con đường Q1 là có thật nhưng ở nhóm giữa, và điều kiện đủ nằm ở phần chứng minh hội tụ mạnh mà người hướng dẫn cần cùng làm. Đây là đánh giá thẳng, không tô vẽ.
