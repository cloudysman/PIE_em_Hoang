## Mệnh đề chi phí và khởi tạo ấm

Các định lý hội tụ mạnh cho sơ đồ chiếu xấp xỉ có quán tính và độ nhớt trên bất đẳng thức biến phân giả đơn điệu đều dựa vào một tiêu chuẩn sai số: sai số ε_k của phép chiếu xấp xỉ ở bước ngoài thứ k phải lập thành dãy sai số tổng được, Σ_k ε_k < ∞. Trong các công trình hiện có, tiêu chuẩn này được đặt làm giả thiết trừu tượng: định lý cho biết nếu sai số tổng được thì dãy lặp hội tụ mạnh, nhưng không cho biết một thuật toán cụ thể phải trả bao nhiêu bước nội để bảo đảm điều đó. Ngược lại, về phía tính toán, thí nghiệm thứ hai (mục 6) cho thấy trên quả cầu biến phân toàn phần, phép chiếu xấp xỉ với ngân sách bước nội cố định và khởi tạo ấm đạt chất lượng ngang phép chiếu chính xác có khởi tạo ấm trong ngưỡng 0,1 dB, đồng thời tốn ít hơn từ 7,6 tới 8,2 lần tổng bước nội; nhưng cấu hình ngân sách cố định này lại không đi kèm chứng chỉ nào rằng tiêu chuẩn sai số của lý thuyết được thỏa. Mục này phát biểu mệnh đề nối hai phía đó: với khởi tạo ấm, ngân sách bước nội cố định tự nó bảo đảm tiêu chuẩn sai số, kèm một chặn hữu hạn tường minh cho tổng bước nội.

### Thiết lập và giả thiết

Xét bước ngoài thứ k của sơ đồ gồm bước quán tính, phép chiếu xấp xỉ, hiệu chỉnh phản xạ và trộn độ nhớt: sau bước quán tính, điểm cần chiếu là u^k = w^k − λ_k F(w^k), và phép chiếu xấp xỉ trả về y^k ≈ P_D(u^k), trong đó tập ràng buộc D là quả cầu biến phân toàn phần {x : TV(x) ≤ τ}. Phép chiếu lên D không có công thức đóng và được giải bằng thuật toán Chambolle-Pock. Gọi T_u là toán tử một bước Chambolle-Pock cho bài toán chiếu min_x ½‖x − u‖² trên D, tác động lên cặp biến gốc và đối ngẫu ζ; điểm bất động ζ*(u) của T_u có thành phần gốc đúng bằng P_D(u). Khởi tạo ấm nghĩa là trạng thái nội cuối của bước ngoài trước được dùng làm điểm xuất phát của vòng nội kế tiếp: ζ^{k,0} = ζ^{k−1,m}. Sai số được đo bằng e_k = ‖ζ^{k,m} − ζ*(u^k)‖_* trong một chuẩn ‖·‖_* trên không gian gốc–đối ngẫu; e_k chặn trên khoảng cách ‖y^k − P_D(u^k)‖ sai khác một hằng số, tức đúng dạng sai số mà tiêu chuẩn sai số của định lý ngoài yêu cầu.

Ba giả thiết được dùng:

(A1) tính co rút của toán tử Chambolle-Pock: tồn tại q ∈ (0,1) sao cho ‖T_u ζ − ζ*(u)‖_* ≤ q ‖ζ − ζ*(u)‖_* với mọi u trong một tập bị chặn chứa quỹ đạo ngoài và mọi ζ trong vùng chứa các trạng thái nội;

(A2) phụ thuộc Lipschitz của nghiệm chiếu: ‖ζ*(u) − ζ*(u′)‖_* ≤ L_P ‖u − u′‖ trên cùng tập bị chặn; thành phần gốc thỏa điều này với hằng số 1 vì phép chiếu không giãn, phần cần giả thiết là thành phần đối ngẫu;

(A3) độ trôi của quỹ đạo ngoài δ_k = ‖u^k − u^{k−1}‖ giảm theo cấp số nhân, δ_k ≤ C_δ θ^k với θ ∈ (0,1); phương án yếu hơn là chỉ đòi dãy (δ_k) tổng được.

### Phát biểu mệnh đề

Mệnh đề (chi phí của phép chiếu xấp xỉ có khởi tạo ấm). Giả sử (A1)–(A3) và ngân sách bước nội cố định m ≥ 1 cho mỗi bước ngoài. Khi đó:

(i) sai số của phép chiếu xấp xỉ thỏa truy hồi e_k ≤ q^m (e_{k−1} + L_P δ_k) với mọi k ≥ 1;

(ii) nếu δ_k ≤ C_δ θ^k thì e_k ≤ C · max{q^m, θ}^k, với hằng số C tường minh theo e_0, L_P, C_δ, q, m, θ (khi q^m ≠ θ): sai số của phép chiếu xấp xỉ giảm theo cấp số nhân qua các bước ngoài. Nói riêng dãy (e_k) tổng được, nên tiêu chuẩn sai số dạng dãy sai số tổng được của định lý hội tụ mạnh được thỏa một cách tự động, không cần phép thử dừng nội và không cần lịch dung sai thích nghi;

(iii) tổng bước nội sau K bước ngoài đúng bằng mK; và với mọi mức suy giảm mục tiêu θ̄ ∈ [θ, 1), chỉ cần m ≥ ln(1/θ̄)/ln(1/q) để có e_k ≤ C θ̄^k. Chặn mK vì thế tuyến tính theo K với hệ số m tường minh, không phụ thuộc độ chính xác đích của từng phép chiếu; trong khi với phép chiếu chính xác, số bước nội mỗi bước ngoài phải tăng không bị chặn khi dung sai đòi hỏi tiến về 0.

Nhận xét thứ nhất: nếu chỉ có phương án yếu của (A3), tức Σ_k δ_k < ∞, thì kết luận cấp số nhân ở (ii) không còn, nhưng từ (i) vẫn suy ra Σ_{k≥1} e_k ≤ q^m (e_0 + L_P Σ_k δ_k) / (1 − q^m), một chặn hữu hạn tường minh; tiêu chuẩn sai số vẫn được thỏa và phần chi phí mK ở (iii) giữ nguyên. Nhận xét thứ hai: vì P_D(u^k) thuộc D, mức vi phạm tập ràng buộc của y^k bị chặn theo e_k, nên cũng giảm theo cấp số nhân; điều này khớp với quan sát ở mục 6.3 rằng vi phạm từ 1 tới 8 phần trăm chỉ xuất hiện ở ngân sách một bước nội và thu hẹp khi tăng ngân sách.

### Phác thảo lập luận

Lập luận gồm hai bất đẳng thức. Thứ nhất, nhờ khởi tạo ấm và (A2), điểm xuất phát của vòng nội thứ k cách điểm bất động mới không quá ‖ζ^{k−1,m} − ζ*(u^{k−1})‖ + ‖ζ*(u^{k−1}) − ζ*(u^k)‖ ≤ e_{k−1} + L_P δ_k. Thứ hai, nhờ (A1), m bước Chambolle-Pock co khoảng cách này lại q^m lần, cho truy hồi (i). Phần còn lại là khai triển truy hồi: so sánh với chuỗi hình học cho (ii), lấy tổng hai vế của (i) theo k cho nhận xét về trường hợp tổng được, và chọn m sao cho q^m ≤ θ̄ cho (iii).

Vai trò của từng thành phần lộ rõ trong truy hồi. Khởi tạo ấm là lý do số hạng e_{k−1} xuất hiện thay cho khoảng cách từ một điểm khởi tạo cố định tới ζ*(u^k), vốn không co lại theo k; nếu khởi tạo lạnh, mỗi bước ngoài phải trả lại từ đầu toàn bộ khoảng cách đó, và chính chênh lệch này hiện ra trong thí nghiệm thứ hai dưới dạng mức tiết kiệm từ 12 tới 24 lần của khởi tạo ấm so với khởi tạo lạnh ngay ở phép chiếu chính xác. Còn tính co rút (A1) là lý do ngân sách m cố định đủ để sai số không tích lũy: mỗi bước ngoài chỉ cần xóa phần trôi L_P δ_k cộng một tỉ lệ q^m của sai số cũ, nên phép chiếu được hoàn thiện dần dọc quỹ đạo ngoài. Đây là nội dung định lượng của quan sát định tính ở mục 6.3 rằng cơ chế thật sự tạo lợi thế là khởi tạo ấm phân bổ vòng lặp nội qua các bước ngoài.

Một điểm kỹ thuật cần nói thẳng: (A3) là tính chất của sơ đồ ngoài, mà chứng minh hội tụ của sơ đồ ngoài lại dùng tiêu chuẩn sai số làm giả thiết; hai phía phụ thuộc lẫn nhau. Chứng minh đầy đủ phải ghép nối hai truy hồi bằng một lập luận quy nạp đồng thời: giả thiết quy nạp giữ cùng lúc chặn cho e_k và chặn cho δ_k tới bước k, rồi suy cả hai ở bước k + 1. Đây là phần việc kỹ thuật chính của bài lý thuyết, không phải một chi tiết hiển nhiên.

### Vai trò cầu nối

Mệnh đề này là cầu nối giữa phần lý thuyết và phần tính toán, và theo hiểu biết của chúng tôi là điểm chưa có trong các công trình đã công bố về sơ đồ chiếu xấp xỉ cho bất đẳng thức biến phân giả đơn điệu. Các phân tích hiện có nằm ở một trong hai phía: hoặc giả định trừu tượng dãy sai số tổng được mà không chỉ ra cách đạt nó với chi phí bị chặn, hoặc dùng phép thử dừng nội theo dung sai giảm dần, khiến số bước nội mỗi bước ngoài tăng không bị chặn và tổng chi phí không kiểm soát được từ trước. Mệnh đề trên đóng khoảng trống đó theo cả hai chiều: cấu hình rẻ nhất trong thực hành, tức ngân sách bước nội cố định cộng khởi tạo ấm, được chứng nhận là thỏa đúng giả thiết của định lý hội tụ mạnh, với hằng số tường minh.

Hệ quả đáng giá nhất nằm ở cách đọc tốc độ hội tụ. Định lý chính của bài lý thuyết phát biểu tốc độ hội tụ điểm cuối cho phần dư biến phân theo số bước ngoài K; nhưng mỗi bước ngoài giấu một phép chiếu có chi phí riêng, nên tốc độ theo K chưa phải tốc độ theo chi phí thật. Nhờ (iii), tổng bước nội chỉ là mK với m là hằng số tường minh, nên mọi tốc độ theo bước ngoài chuyển thẳng thành tốc độ theo tổng bước nội, sai khác hệ số m. Với phép chiếu chính xác, phép chuyển này không tồn tại vì chi phí mỗi bước ngoài không bị chặn đều. Khoảng cách giữa hai cách đọc không chỉ là chuyện hình thức: trên quả cầu biến phân toàn phần, nó hiện ra bằng số liệu là mức chênh từ 7,6 tới 8,2 lần tổng bước nội ở cùng chất lượng trong thí nghiệm thứ hai.

### Trung thực về giả thiết

Ba giới hạn sau cần được nêu cùng mệnh đề.

Thứ nhất, (A1) là giả thiết chịu lực và không miễn phí. Với bài toán chiếu lên quả cầu biến phân toàn phần, bảo đảm tổng quát của Chambolle-Pock chỉ là tốc độ O(1/N), hoặc O(1/N²) cho biến thể gia tốc nhờ phần gốc lồi mạnh; tính co rút toàn cục không tự có vì bài toán đối ngẫu không lồi mạnh. Con đường khả dĩ là qua tính chính quy dưới mêtric hoặc điều kiện chặn sai số: với biến phân toàn phần bất đẳng hướng, cấu trúc đa diện của tập ràng buộc cho phép chứng minh tính co rút địa phương của sơ đồ gốc–đối ngẫu; với biến phân toàn phần đẳng hướng, (A1) phải được phát biểu như một giả thiết. Số liệu hiện có, gồm mức tiết kiệm lớn của khởi tạo ấm và việc ngân sách một tới hai bước nội đã đủ, nhất quán với hành vi co rút ở đuôi nhưng chưa phải phép đo trực tiếp; minh họa số của bài lý thuyết cần đo thẳng tốc độ giảm sai số nội để ước lượng q thực nghiệm.

Thứ hai, (A2) chỉ hiển nhiên ở thành phần gốc; thành phần đối ngẫu đòi nghiệm đối ngẫu phụ thuộc đủ đều vào điểm cần chiếu, chẳng hạn qua tính duy nhất và tính calm của nghiệm, và điều này cũng chỉ trông đợi được dưới cùng loại cấu trúc như ở (A1).

Thứ ba, (A3) và tính bị chặn của quỹ đạo là tính chất phải chứng minh cùng lúc với kết luận, qua lập luận ghép nối đã nêu; mệnh đề vì thế nên được đọc như một bổ đề chi phí bên trong một định lý trọn gói, không phải một khẳng định độc lập vô điều kiện. Cuối cùng, về phía số liệu, các tỉ lệ 7,6 tới 8,2 lần được đo ở quy mô nhỏ và với bán kính τ đặt theo thông tin oracle như đã khai ở mục 11, nên chúng minh họa cơ chế chứ không phải hằng số phổ quát; và bản thân cơ chế ngân sách cố định cộng khởi tạo ấm là kỹ thuật một vòng đã biết trong tối ưu, nên phần mới của mệnh đề không nằm ở cơ chế mà nằm ở chứng chỉ nối cơ chế đó với tiêu chuẩn sai số của định lý hội tụ mạnh và ở chặn chi phí tường minh đi kèm.
