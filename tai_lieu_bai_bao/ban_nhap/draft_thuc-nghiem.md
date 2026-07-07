## Kế hoạch thực nghiệm số

Theo định vị ở phần 12 của báo cáo thực nghiệm, mã nguồn không còn đóng vai trò bằng chứng cho một khẳng định thực nghiệm mà trở thành minh họa số cho kết quả giải tích. Kế hoạch dưới đây gồm ba thí nghiệm, mỗi thí nghiệm gắn với một mục tiêu minh họa cụ thể và một tiêu chí đạt hay không đạt được ấn định trước khi chạy, theo đúng phương pháp luận ở phần 3 của báo cáo. Toàn bộ ba thí nghiệm đều không có thành phần học: đặt ρ = 1 và G_φ = 0, toán tử chi phí được cho tường minh, nên kết quả chỉ phản ánh tính chất của sơ đồ lặp.

### Thí nghiệm A: kiểm chứng tốc độ hội tụ của phần dư biến phân

Mục tiêu. Kiểm chứng bằng số rằng phần dư biến phân r(x^k) = ‖x^k − P_D(x^k − F(x^k))‖ giảm đúng tốc độ hội tụ mà định lý dự đoán, ký hiệu O(k^{−γ}) với γ lấy từ phát biểu định lý, khi thuật toán chạy với phép chiếu xấp xỉ thỏa tiêu chuẩn sai số của định lý.

Thiết lập. Bài toán khử mờ trên quả cầu biến phân toàn phần D = {x : TV(x) ≤ τ}, với toán tử F(x) = Bᵀ(Bx − y) đơn điệu và Lipschitz, đúng thiết lập của thí nghiệm thứ hai trong báo cáo (mảnh ảnh cạnh 128, hai loại mờ Gauss và chuyển động, mức nhiễu 0,05). Sơ đồ chạy đủ bốn pha: bước quán tính, phép chiếu xấp xỉ có khởi tạo ấm, hiệu chỉnh phản xạ, trộn độ nhớt. Số bước ngoài kéo dài tới 500 để quan sát dáng điệu tiệm cận, thay vì 12 bước như chế độ vận hành cũ.

Ba điểm phương pháp cần tuân thủ. Thứ nhất, phần dư biến phân dùng để phán quyết phải được tính bằng phép chiếu chính xác độc lập với thuật toán, cụ thể là Chambolle-Pock 400 bước như cách dựng nghiệm hội tụ tham chiếu ở phần 6 của báo cáo; nếu tính phần dư bằng chính phép chiếu xấp xỉ đang chạy thì thước đo bị nhiễm sai số của sơ đồ. Thứ hai, dãy sai số ε_k của phép chiếu xấp xỉ được điều khiển tường minh theo lịch ε_k = C·k^{−p}: các giá trị p > 1 cho dãy sai số tổng được đúng giả thiết định lý; giá trị p ≤ 1 cho dãy sai số không tổng được, dùng làm nhóm đối chứng để kiểm tra tính sắc của tiêu chuẩn sai số, với kỳ vọng phần dư biến phân dừng ở một mức sàn thay vì tiếp tục giảm. Thứ ba, chỉ số phán quyết là phần dư biến phân, không phải PSNR: do hiện tượng bán hội tụ đã ghi nhận ở phần 5 của báo cáo, PSNR đạt đỉnh rồi giảm khi lặp dài, điều này không mâu thuẫn với lý thuyết vì định lý phát biểu về hội tụ tới nghiệm của bất đẳng thức biến phân, không phát biểu về chất lượng khôi phục; hai đường cong được vẽ song song để minh bạch điểm này.

Tiêu chí đặt trước. Với dãy sai số tổng được, độ dốc của log r(x^k) theo log k trên nửa sau quỹ đạo nằm trong dung sai 10 phần trăm của độ dốc −γ lý thuyết, đồng nhất trên cả 6 mảnh kiểm tra và cả hai loại mờ; với dãy sai số không tổng được, phần dư dừng ở mức sàn cao hơn rõ rệt. Ngoài ra khảo sát phụ tắt lần lượt bước quán tính và độ nhớt để minh họa vai trò của từng giả thiết về hệ số α_k, β_k trong định lý.

### Thí nghiệm B: đường đánh đổi chất lượng theo chi phí trên bài khôi phục ảnh

Mục tiêu. Trình bày ứng dụng của phép chiếu xấp xỉ vào khôi phục ảnh dưới dạng đường đánh đổi giữa chất lượng và chi phí, tái sử dụng kết quả duy nhất đứng vững của báo cáo: trên quả cầu biến phân toàn phần, phép chiếu xấp xỉ với hai bước nội đạt chất lượng trong ngưỡng 0,1 dB của phép chiếu chính xác có khởi tạo ấm, đồng thời tốn ít hơn khoảng 7,6 lần tổng bước nội với mờ chuyển động (80 so với 606 bước nội) và khoảng 8,2 lần với mờ Gauss (40 so với 328 bước nội).

Thiết lập. Giữ nguyên thí nghiệm thứ hai của báo cáo: ba cách chiếu ở cùng số bước ngoài, cùng bước λ và cùng bán kính τ, gồm phép chiếu chính xác khởi tạo lạnh, phép chiếu chính xác khởi tạo ấm và phép chiếu xấp xỉ với ngân sách bước nội m cố định. Chi phí của phép chiếu chính xác đo bằng số bước Chambolle-Pock cần để đạt sai số tương đối 0,001 so với nghiệm hội tụ tham chiếu 400 bước. Điểm mới duy nhất so với báo cáo là ghép mỗi cấu hình chiếu xấp xỉ với lịch sai số ε_k tương ứng của thí nghiệm A, để đường đánh đổi được đọc như minh họa cho định lý: mỗi điểm trên đường là một mức thỏa hiệp giữa tiêu chuẩn sai số và tổng bước nội.

Ba lưu ý trung thực của phần 6 báo cáo được giữ nguyên trong bài: lợi thế đo được là chi phí ở cùng chất lượng, không phải chất lượng, vì phần PSNR nhỉnh hơn ở vài cấu hình là hiệu ứng bán hội tụ; baseline bắt buộc là phép chiếu chính xác có khởi tạo ấm, vì riêng khởi tạo ấm đã tiết kiệm 12 tới 24 lần so với khởi tạo lạnh và phần tiết kiệm này không được gán cho phép chiếu xấp xỉ; mức vi phạm TV(x)/τ được báo cáo kèm, và điểm vận hành chính là m = 2 để đầu ra sát khả thi. Bán kính τ đặt theo thông tin oracle như đã công khai ở phần 3 của báo cáo, điều này được ghi rõ trong bài.

Tiêu chí đặt trước. Giữ nguyên tiêu chí đã thỏa của thí nghiệm thứ hai: chất lượng trong ngưỡng 0,1 dB của phép chiếu chính xác có khởi tạo ấm với tổng bước nội thấp hơn rõ rệt. Thí nghiệm này về bản chất là chạy lại có bổ sung, rủi ro thấp.

### Thí nghiệm C: ví dụ giả đơn điệu nhưng không đơn điệu

Mục tiêu. Định lý phát biểu cho toán tử giả đơn điệu; nếu mọi minh họa số đều dùng toán tử đơn điệu thì phần mở rộng của định lý không có ví dụ chứng thực. Thí nghiệm này dựng một bài toán mà toán tử giả đơn điệu nhưng không đơn điệu, có nghiệm biết trước, và kiểm chứng thuật toán vẫn hội tụ mạnh với tốc độ hội tụ dự đoán.

Toán tử đề xuất, biến thể chiều thấp. Trên H = R^m với tập ràng buộc C là quả cầu đơn vị đóng, xét

F(x) = exp(−‖x‖²) · (x − b),  với b cố định, ‖b‖ > 1.

Tính giả đơn điệu suy trực tiếp từ cấu trúc: x − b đơn điệu và exp(−‖x‖²) là vô hướng dương, nên nếu ⟨F(x), y − x⟩ ≥ 0 thì ⟨x − b, y − x⟩ ≥ 0, do đơn điệu suy ra ⟨y − b, y − x⟩ ≥ 0, nhân với vô hướng dương exp(−‖y‖²) được ⟨F(y), y − x⟩ ≥ 0. Tính không đơn điệu kiểm được tường minh: với m = 1 và b = 2, đạo hàm F′(x) = exp(−x²)(1 − 2x² + 4x) âm tại x = −1, nên tồn tại cặp u, v với ⟨F(u) − F(v), u − v⟩ < 0. Tập nghiệm của bất đẳng thức biến phân trùng tập nghiệm của toán tử x − b, nên nghiệm biết trước ở dạng đóng x* = P_C(b) = b/‖b‖; nhờ đó đo được trực tiếp cả ‖x^k − x*‖ lẫn phần dư biến phân theo bước ngoài. Toán tử Lipschitz trên C vì C bị chặn, thỏa giả thiết định lý.

Biến thể quy mô ảnh. Để minh họa trên đúng hạ tầng của thí nghiệm A, xét toán tử

F(x) = (ρ_min + exp(−‖Bx − y‖²/(σ²n))) · Bᵀ(Bx − y)

trên quả cầu biến phân toàn phần, với ρ_min > 0 nhỏ và n là số điểm ảnh. Lập luận giả đơn điệu giống hệt biến thể chiều thấp vì hệ số trước Bᵀ(Bx − y) là vô hướng dương; tính không đơn điệu không còn dạng đóng nên được chứng thực bằng chứng chỉ số: mã thí nghiệm lấy mẫu ngẫu nhiên các cặp (u, v) trong tập ràng buộc, in ra một cặp cụ thể có ⟨F(u) − F(v), u − v⟩ < 0 kèm giá trị, và chứng chỉ này được đưa vào bài. Nếu việc lấy mẫu không tìm được chứng chỉ với ρ_min và σ đã chọn thì biến thể ảnh bị loại và bài chỉ dùng biến thể chiều thấp; điều kiện loại này được ấn định trước.

Tiêu chí đặt trước. Trên biến thể chiều thấp: ‖x^k − x*‖ giảm về 0 và độ dốc log-log của phần dư biến phân nằm trong dung sai 10 phần trăm của tốc độ lý thuyết, với ít nhất năm giá trị b và ba số chiều m khác nhau; chứng chỉ không đơn điệu được in tự động trong nhật ký chạy. Trên biến thể ảnh: cùng tiêu chí về phần dư biến phân như thí nghiệm A.

### Tái sử dụng mã nguồn và kết quả

| Thành phần | File hoặc lệnh | Mức tái sử dụng |
|---|---|---|
| Phép chiếu lên quả cầu biến phân toàn phần bằng Chambolle-Pock, khởi tạo ấm qua biến đối ngẫu, đếm bước nội tới dung sai | `pie_net/constraints.py` (lớp `TVBallConstraint`, hàm `project`, `iters_to_tol`) | dùng nguyên vẹn cho cả ba thí nghiệm |
| Sơ đồ bốn pha quán tính, chiếu xấp xỉ, hiệu chỉnh phản xạ, độ nhớt | `pie_net/tv_solver.py` (lớp `PIENetTV` với `ZeroG`, ρ = 1) | dùng nguyên vẹn, chỉ nới số bước ngoài và thêm ghi phần dư theo bước |
| Toán tử mờ B, Bᵀ và dữ liệu | `pie_net/operators.py`, `pie_net/data.py` | dùng nguyên vẹn |
| Phần dư biến phân | `pie_net/metrics.py` (hàm `vi_residual`) | dùng có sửa: thay phép chiếu bên trong bằng phép chiếu chính xác 400 bước |
| Thí nghiệm B trọn vẹn | `python quick_test_tv.py --blur gauss` và `python quick_test_tv.py --blur motion`; hình `quick_tv_pareto.png` và số liệu phần 6 của báo cáo | chạy lại nguyên trạng, bổ sung nhãn lịch sai số ε_k |
| Thí nghiệm A | script mới trên khung `quick_test_tv.py`, thêm lịch ε_k = C·k^{−p} và ghi r(x^k) | viết mới phần ghi đo, tái sử dụng toàn bộ hạ tầng |
| Thí nghiệm C | script mới; biến thể chiều thấp độc lập hạ tầng ảnh, biến thể ảnh tái sử dụng `TVBallConstraint` và `PIENetTV` với toán tử F thay mới | viết mới toán tử và chứng chỉ không đơn điệu, khoảng vài trăm dòng |

Khối lượng viết mới ước tính nhỏ: hai script đo và một lớp toán tử, vì toàn bộ phần nặng gồm phép chiếu có khởi tạo ấm, sơ đồ bốn pha và cách đo chi phí trung thực đã có sẵn và đã được kiểm qua năm thí nghiệm của báo cáo.
