# Khung bài báo: phương pháp chiếu phản xạ có quán tính và độ nhớt với phép chiếu xấp xỉ khởi tạo ấm cho bất đẳng thức biến phân giả đơn điệu

Tài liệu này là khung chi tiết cho con đường thứ hai đã chốt trong `00_ket_luan_dieu_hanh.md`. Nó đã tích hợp các sửa lỗi từ vòng phản biện và bám sát thuật toán đã cài trong `pie_net/reflected_solver.py`. Các con số thực nghiệm được điền từ `results/theory/phan_tich.md` sau khi lưới chạy xong; chỗ chờ số được đánh dấu bằng ngoặc vuông.

Quy ước trung thực áp dụng toàn tài liệu: mọi phát biểu về định lý hội tụ được ghi rõ là dự kiến và chưa chứng minh đầy đủ; các chỗ khó về mặt kỹ thuật được nêu thẳng thay vì che đi.

## 1. Bài toán và ký hiệu

Xét bất đẳng thức biến phân trên tập ràng buộc: cho không gian Hilbert thực H (trong phần thực nghiệm là không gian ảnh hữu hạn chiều), một tập con lồi đóng khác rỗng D của H, và một toán tử F từ H vào H, tìm điểm x* thuộc D sao cho

    ⟨F(x*), x − x*⟩ ≥ 0  với mọi x thuộc D.

Ký hiệu tập nghiệm là S. Bài toán này bao trùm bài toán khôi phục ảnh y = Bx + ε khi ta đặt F(x) = Bᵀ(Bx − y) và D là một tập ràng buộc vật lý, ví dụ quả cầu biến phân toàn phần D = {x : TV(x) ≤ τ}. Với lựa chọn này F là toán tử đơn điệu affine, nên đây là một trường hợp riêng của lớp giả đơn điệu mà lý thuyết nhắm tới.

Phần dư biến phân dùng để đo mức độ một điểm là nghiệm được định nghĩa là

    r(x) = ‖x − P_D(x − λ F(x))‖,

với λ dương cố định; r(x) = 0 khi và chỉ khi x thuộc S.

## 2. Giả thiết

Bài báo làm việc dưới các giả thiết sau, là các giả thiết chuẩn của dòng phương pháp chiếu cho bất đẳng thức biến phân giả đơn điệu.

- Giả thiết A1: D là tập con lồi đóng khác rỗng của H.
- Giả thiết A2: F liên tục Lipschitz trên D với hằng số L, và giả đơn điệu trên D, nghĩa là với mọi x, y thuộc D, nếu ⟨F(y), x − y⟩ ≥ 0 thì ⟨F(x), x − y⟩ ≥ 0.
- Giả thiết A3: tập nghiệm S khác rỗng.
- Giả thiết A4 (chỉ cho không gian vô hạn chiều): F liên tục yếu theo dãy trên D, để chuyển điểm tụ yếu qua toán tử. Trong không gian hữu hạn chiều của phần thực nghiệm, giả thiết này thỏa tự động.

Một lưu ý cần nêu rõ ngay: với toán tử dạng tích ρ(x)·M(x) trong thiết kế gốc của dự án, khi ρ không phải hằng số thì tích này nói chung không Lipschitz toàn cục trên H. Vì vậy bài báo phát biểu giả thiết A2 trên tập bị chặn chứa quỹ đạo, hoặc làm việc trong không gian hữu hạn chiều; trong phần thực nghiệm ta lấy ρ bằng 1 nên F là affine và Lipschitz toàn cục, giả thiết A2 thỏa đúng.

## 3. Thuật toán

Cho điểm neo x_anchor thuộc H và ánh xạ co f (trong thực nghiệm f là ánh xạ hằng về x_anchor). Cho hai điểm khởi đầu x⁰ = x⁻¹. Mỗi bước ngoài k gồm bốn pha:

    wᵏ = xᵏ + αₖ (xᵏ − xᵏ⁻¹)                       (quán tính)
    rᵏ = 2 wᵏ − wᵏ⁻¹                               (bước phản xạ kiểu Malitsky)
    yᵏ = P_D^{εₖ}( wᵏ − λ F(rᵏ) )                  (chiếu xấp xỉ, sai số εₖ)
    xᵏ⁺¹ = βₖ f(xᵏ) + (1 − βₖ) yᵏ                  (trộn độ nhớt)

Trong đó P_D^{εₖ} là phép chiếu xấp xỉ lên D với sai số εₖ, được thực hiện bằng một số bước lặp nội có khởi tạo ấm. Điểm mấu chốt của bước phản xạ là toán tử F chỉ được tính một lần mỗi bước ngoài, tại điểm phản xạ rᵏ; đây là điểm phân biệt với bước hiệu chỉnh kiểu Tseng vốn tính F hai lần.

Điều kiện tham số:

- Bước nhảy λ thuộc khoảng (0, (√2 − 1)/L), theo điều kiện của phương pháp chiếu phản xạ; L được ước lượng bằng phép lặp lũy thừa cho ‖BᵀB‖, không gán bằng một hằng số tùy tiện.
- Hệ số quán tính thích nghi αₖ = min(ᾱ, τₖ / ‖xᵏ − xᵏ⁻¹‖) với τₖ = βₖ/(k+1), bảo đảm αₖ ‖xᵏ − xᵏ⁻¹‖ / βₖ tiến về không, là điều kiện quán tính chuẩn của dòng phương pháp độ nhớt.
- Hệ số độ nhớt βₖ = β₀/(k+1), thỏa βₖ tiến về không và tổng các βₖ phân kỳ.
- Dãy sai số chiếu εₖ thỏa điều kiện tổng được, tức tổng các εₖ hữu hạn; cách bảo đảm điều kiện này một cách tính được là nội dung của mục 5.

## 4. Định lý hội tụ (dự kiến) và phác thảo chứng minh

Trạng thái: phát biểu dưới đây là mục tiêu của bài, chưa được chứng minh đầy đủ. Phần này nêu đường chứng minh dự kiến, đánh dấu rõ đâu là bước thường quy và đâu là bước khó cần kiểm chứng cẩn thận cùng người hướng dẫn.

Định lý dự kiến. Dưới các giả thiết A1 đến A4, với các điều kiện tham số ở mục 3 và dãy sai số chiếu tổng được, dãy {xᵏ} sinh bởi thuật toán hội tụ mạnh về điểm x* = P_S(x_anchor), tức hình chiếu của điểm neo lên tập nghiệm.

Đường chứng minh dự kiến gồm bốn phần.

Phần thứ nhất, bổ đề một bước với phép chiếu xấp xỉ. Đặt điểm chiếu chính xác lý tưởng ȳᵏ = P_D(wᵏ − λ F(rᵏ)). Vì phép chiếu là ánh xạ không giãn, sai lệch giữa điểm chiếu xấp xỉ và điểm chiếu chính xác bị chặn đều bởi εₖ, không phụ thuộc trạng thái. Nhờ đó phân tích giả đơn điệu chạy trên cặp chính xác, còn phép chiếu xấp xỉ chỉ thêm một số hạng nhiễu bị chặn theo εₖ. Đây là bước thường quy sau khi định nghĩa sai số theo khoảng cách tới điểm chiếu chính xác.

Phần thứ hai, bất đẳthức tựa Fejér. Từ bổ đề một bước và tính giả đơn điệu, thu được một bất đẳng thức truy hồi cho ‖xᵏ − p‖ với p là một nghiệm, trong đó phần nhiễu do phép chiếu xấp xỉ là tổng được. Bước này dùng kỹ thuật tựa Fejér chuẩn; số hạng nhiễu phụ thuộc trạng thái được nhân tính hóa theo cách quen thuộc.

Phần thứ ba, hội tụ mạnh qua bổ đề dãy số thực. Do có bước trộn độ nhớt, ta dùng bổ đề dãy số thực kiểu Maingé để kết luận hội tụ mạnh về hình chiếu của điểm neo. Đây là chỗ khó thật sự: bổ đề Maingé có hai nhánh, và nhánh dãy không đơn điệu không khép lại được nếu chỉ giả thiết sai số tổng được. Khả năng cao phải thêm điều kiện εₖ/βₖ tiến về không, hoặc dùng mẹo dịch đuôi cho dãy có cộng thêm số hạng tổng được. Bước này cần viết tường minh và kiểm chứng cẩn thận, không thể coi là chép lại kết quả có sẵn.

Phần thứ tư, điểm tụ yếu thuộc tập nghiệm. Cần chuỗi các giới hạn: dịch chuyển do quán tính tiến về không, hiệu giữa điểm chiếu và điểm quán tính tiến về không, và bước trộn độ nhớt tiến về không; từ đó tập điểm tụ yếu của dãy nằm trong tập nghiệm. Bước này thường quy nhưng phải viết đủ, không được bỏ qua.

Một khó khăn cấu trúc cần ghi nhận: bước phản xạ không có tính đơn điệu Fejér tự nhiên, nên phân tích phức tạp hơn các sơ đồ chỉ có quán tính và độ nhớt. Trong tài liệu, việc kết hợp bước phản xạ với neo để đạt hội tụ mạnh mới được xử lý cho trường hợp phép chiếu chính xác; thêm phép chiếu xấp xỉ vào đó là phần công việc mới của bài.

## 5. Mệnh đề chi phí và khởi tạo ấm

Đây là phần đóng góp có khả năng bảo vệ tốt nhất, sau khi đã sửa một lỗi thực sự được phát hiện ở vòng phản biện.

Lỗi đã sửa. Phát biểu ban đầu cho rằng một ngân sách bước nội cố định cộng với khởi tạo ấm tự động cho dãy sai số tổng được. Điều này sai trong trường hợp tổng quát: bước trộn độ nhớt tự nó làm dịch chuyển giữa hai bước ngoài liên tiếp cỡ βₖ, mà tổng các βₖ phân kỳ, nên dưới ngân sách cố định dãy sai số chiếu không tổng được. Phần thực nghiệm xác nhận điều này bằng số: độ dốc log-log của dịch chuyển gần bằng [chờ số], khớp với dịch chuyển cỡ βₖ tương ứng dãy phân kỳ.

Phát biểu đã sửa. Dùng ngân sách bước nội tăng chậm theo hàm log, cụ thể mₖ = ⌈1 + 2 ln(k+1)⌉. Nếu vòng lặp nội của phép chiếu hội tụ đủ nhanh với khởi tạo ấm, sai số chiếu sau mₖ bước giảm tới mức tổng được, và tổng số bước nội sau K bước ngoài là cỡ K log K, tức chỉ hơn tuyến tính một thừa số log. Đây là cách bảo đảm điều kiện tổng được một cách tính được thay cho giả thiết trừu tượng. Số liệu ủng hộ lựa chọn này: dưới ngân sách log, sai số chiếu giảm với độ dốc log-log khoảng âm hai, nhanh hơn hẳn ngân sách cố định (độ dốc khoảng âm một phẩy ba); ngân sách cố định chỉ tổng được nếu dịch chuyển ngoài giảm nhanh hơn nghịch đảo số bước, điều không được bảo đảm.

Ba lưu ý trung thực đi kèm mệnh đề này.

Thứ nhất, về tốc độ của vòng lặp nội. Vòng lặp Chambolle-Pock cơ bản cho phép chiếu lên quả cầu biến phân toàn phần chỉ hội tụ với tốc độ cỡ nghịch đảo số bước, không phải tuyến tính, vì bài toán đối ngẫu không lồi mạnh. Do đó câu chuyện sai số giảm nhanh cần một biến thể tăng tốc hoặc một điều kiện chặn sai số bổ sung, và bài phải phát biểu điều này tường minh thay vì giả định tốc độ tuyến tính.

Thứ hai, về tính duy nhất của điểm bất động. Điểm bất động của vòng lặp Chambolle-Pock cho phép chiếu này không duy nhất ở biến đối ngẫu, vì toán tử phân kỳ có hạch không tầm thường. Vì vậy sai số chiếu phải được phát biểu theo khoảng cách tới tập điểm bất động chứ không tới một điểm, và phân tích phải dùng tính chính quy dưới mêtric.

Thứ ba, về mức lợi thế. Lợi thế của chiếu xấp xỉ so với chiếu chính xác có khởi tạo ấm là một hệ số hằng, không phải chênh lệch giữa hữu hạn và vô hạn. Chiếu chính xác có khởi tạo ấm cũng chỉ tốn tuyến tính theo số bước ngoài; chiếu xấp xỉ ngân sách nhỏ rẻ hơn một hệ số hằng, và hệ số này lớn hơn khi bài toán chiếu khó hơn. Trên mờ Gauss, để đạt cùng một mức phần dư biến phân, chiếu xấp xỉ ngân sách một bước nội tốn khoảng 2,8 lần ít bước nội hơn chiếu chính xác khởi tạo ấm, ngân sách hai bước khoảng 2,5 lần. Trên mờ chuyển động, nơi chiếu chính xác tốn kém hơn nhiều, hệ số lên tới khoảng 4 đến 7 lần. Mọi phát biểu phải giữ đúng mức hệ số hằng này, không được phóng đại thành khác biệt bậc.

Đối chiếu tài liệu bắt buộc. Nguyên lý sai số tổng được cộng với vòng lặp nội hội tụ nhanh và khởi tạo ấm cho chi phí nội bị chặn là kinh điển trong phương pháp điểm gần kề xấp xỉ (Rockafellar 1976; Salzo và Villa 2012; Schmidt, Le Roux và Bach 2011, nơi khẳng định sai số giảm đủ nhanh bảo toàn tốc độ được chứng minh tường minh). Đóng góp của bài không phải nguyên lý này, mà là việc chuyển nó sang khung phương pháp chiếu bốn pha cho bất đẳng thức biến phân, trong đó sai số bị nối với hệ số độ nhớt βₖ, và định lượng cụ thể trên quả cầu biến phân toàn phần với vòng lặp Chambolle-Pock khởi tạo ấm.

## 6. Định vị so với tài liệu

Bài định vị so với hai nhánh, với các bài chặn quan trọng nhất được nêu đích danh để không bị phản biện là đã có.

Nhánh thứ nhất là các phương pháp có quán tính, độ nhớt hoặc kiểu Halpern cho bất đẳng thức biến phân giả đơn điệu với phép chiếu chính xác. Malitsky (2015, SIAM Journal on Optimization) đưa ra phương pháp chiếu phản xạ cho toán tử đơn điệu với phép chiếu chính xác, một phép chiếu mỗi bước. Maingé (2018) kết hợp bước phản xạ với neo để đạt hội tụ mạnh, vẫn với phép chiếu chính xác. Tan và Qin (2020) kết hợp quán tính, độ nhớt và hiệu chỉnh kiểu Tseng cho toán tử giả đơn điệu, phép chiếu chính xác, hội tụ mạnh. Yan, An, Cai và Dong (2025, Communications in Nonlinear Science and Numerical Simulation) có sơ đồ quán tính, độ nhớt, một phép chiếu, giả đơn điệu, hội tụ mạnh. Toàn nhánh này dùng phép chiếu chính xác.

Nhánh thứ hai là phép chiếu xấp xỉ. Díaz Millán, Ferreira và Ugon (2024, Computational Optimization and Applications) đưa ra phép chiếu xấp xỉ khả thi với tiêu chuẩn sai số tương đối bị khống chế bởi dãy tổng được cho toán tử giả đơn điệu, nhưng không có quán tính, không có độ nhớt, và dùng hai phép chiếu mỗi bước. Bài về phương pháp chiếu xấp xỉ có độ nhớt (2025, Communications in Nonlinear Science and Numerical Simulation) kết hợp phép chiếu xấp xỉ với độ nhớt và lặp kiểu Mann cho toán tử giả đơn điệu, chứng minh hội tụ mạnh, nhưng không có quán tính và không có bước phản xạ.

Phần khác biệt của bài, phát biểu trung thực: chưa có bài nào kết hợp bước phản xạ kiểu Malitsky với phép chiếu xấp xỉ, và chưa có bài nào trong dòng bất đẳng thức biến phân đưa phân tích định lượng nối tiêu chuẩn sai số với chi phí khởi tạo ấm của vòng lặp nội. Cần nói thẳng đây là loại đóng góp hợp nhất kỹ thuật cộng một mệnh đề chi phí, không phải một cơ chế hoàn toàn mới. Giá trị bảo vệ được nằm ở cặp phản xạ và chiếu xấp xỉ chưa ai ghép, và ở mệnh đề chi phí đã sửa.

## 7. Kế hoạch thực nghiệm số

Thực nghiệm không nhằm chứng minh phương pháp thắng baseline về chất lượng ảnh, mà nhằm minh họa các phát biểu lý thuyết. Toàn bộ chạy trên máy tính cá nhân, ảnh xám cạnh 64 điểm ảnh, thuần suy diễn với ρ bằng 1 và không có thành phần học, phép chiếu lên quả cầu biến phân toàn phần bằng Chambolle-Pock khởi tạo ấm.

Thí nghiệm thứ nhất, hội tụ và vai trò của phép chiếu xấp xỉ. Chạy sơ đồ bốn pha ở các chế độ ngân sách bước nội cố định và ngân sách log, ghi phần dư biến phân và sai số chiếu theo bước ngoài. Kết quả trên mờ Gauss, ảnh cạnh 64 điểm ảnh, 150 bước ngoài: phần dư giảm ở mọi chế độ; dịch chuyển giảm với độ dốc log-log khoảng âm một phẩy hai đến âm một phẩy ba dưới ngân sách cố định, khớp với dịch chuyển cỡ βₖ; sai số chiếu giảm với độ dốc khoảng âm một phẩy ba dưới ngân sách cố định và khoảng âm hai dưới ngân sách log, cho thấy ngân sách log ép sai số về không nhanh hơn hẳn. Số liệu chi tiết trong `results/theory/phan_tich.md`.

Thí nghiệm thứ hai, bảng chi phí. Để đạt cùng mức phần dư biến phân trên mờ Gauss, tổng bước nội của chiếu chính xác khởi tạo ấm là 382, của chiếu xấp xỉ một bước nội là 136 (rẻ hơn 2,81 lần), hai bước nội là 152 (rẻ hơn 2,51 lần), năm bước nội là 230 (rẻ hơn 1,66 lần). Trên mờ chuyển động, chiếu chính xác tốn 1684 bước nội, còn chiếu xấp xỉ hai bước nội tốn 232 (rẻ hơn 7,26 lần), năm bước nội 330 (rẻ hơn 5,10 lần), ngân sách log 426 (rẻ hơn 3,95 lần). Lợi thế là một hệ số hằng, lớn hơn khi bài toán chiếu khó hơn và giảm dần khi đòi hỏi độ chính xác cao hơn, đúng như mệnh đề chi phí dự đoán.

Thí nghiệm thứ ba, ví dụ giả đơn điệu không đơn điệu. Trên toán tử F(x) = exp(−‖x‖²) A(x − b) với A nửa xác định dương suy biến trong không gian năm mươi chiều, tập ràng buộc là quả cầu đơn vị: chứng chỉ số tìm được cặp điểm với tích vô hướng âm khoảng −5,6 nhân mười mũ trừ sáu, xác nhận toán tử không đơn điệu; thuật toán vẫn hội tụ, phần dư biến phân giảm từ 5,0 nhân mười mũ trừ hai về 1,25 nhân mười mũ trừ bốn, và với biến thể không suy biến dãy lặp hội tụ về hình chiếu của điểm neo lên quả cầu như lý thuyết dự đoán. Ví dụ này bảo đảm định lý phát biểu cho lớp giả đơn điệu không rộng hơn ví dụ minh họa.

Kết quả trên mờ chuyển động lặp lại xu hướng của mờ Gauss trên một loại suy biến thứ hai, với hệ số tiết kiệm lớn hơn do bài toán chiếu khó hơn. Điều này củng cố rằng lợi thế chi phí không phụ thuộc một loại suy biến cụ thể.

## 8. Tạp chí mục tiêu

Theo đúng dòng và mức đóng góp đã định vị trung thực: Optimization, Journal of Computational and Applied Mathematics, hoặc Numerical Algorithms là các lựa chọn thực tế. Nhóm hàng đầu như SIAM Journal on Optimization hay Mathematical Programming đòi một cơ chế mới, mà bài này ở dạng hợp nhất cộng mệnh đề chi phí thì chưa đạt; không nên nhắm tới để tránh vòng phản biện kéo dài không cần thiết. Quyết định cuối thuộc về người hướng dẫn.
