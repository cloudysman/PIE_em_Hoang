# Kết luận điều hành: định vị lại hướng bài báo từ dự án PIE-Net

Ngày lập: 2026-07-07. Tài liệu này tổng hợp kết quả của một vòng khảo sát tài liệu sâu (năm góc độc lập) và một vòng soạn thảo kèm phản biện đối kháng (năm cấu phần, mỗi cấu phần một người phản biện độc lập). Toàn bộ bản nháp và biên bản phản biện nằm trong hai thư mục con `ban_nhap/` và `phan_bien/`; bảng khảo sát đầy đủ nằm trong `khao_sat_tai_lieu_bang_tong_hop.md` và `khao_sat_tai_lieu_ket_luan_5_goc.md`.

## 1. Kết luận chính

Đánh giá lạc quan ban đầu về điểm mới đã bị lật ngược một phần sau khi khảo sát sâu hơn. Cụ thể:

Điểm mới thứ nhất, tức chứng minh hội tụ mạnh khi thay phép chiếu chính xác bằng phép chiếu xấp xỉ với dãy sai số tổng được cho bất đẳng thức biến phân giả đơn điệu, về cơ bản đã bị chặn trước bởi tài liệu 2024–2025. Hai bài chặn quan trọng nhất:

- Diaz Millan, Ferreira, Ugon, "Extragradient method with feasible inexact projection to variational inequality problem", Computational Optimization and Applications, 2024: phép chiếu xấp xỉ với tiêu chuẩn sai số bị khống chế bởi dãy tổng được, cho toán tử giả đơn điệu.
- Bài "Viscosity inexact projection methods with applications to electricity production models", Communications in Nonlinear Science and Numerical Simulation, 2025 (đã xác minh tồn tại trên ScienceDirect, mã bài S1007570425008809): kết hợp phép chiếu xấp xỉ với độ nhớt và lặp kiểu Mann cho bất đẳng thức biến phân giả đơn điệu, chứng minh hội tụ mạnh. Đây gần như chính là lõi của điểm mới thứ nhất; phần còn thiếu chỉ là bước quán tính và bước hiệu chỉnh.

Ngoài ra, sơ đồ gồm quán tính, độ nhớt, một phép chiếu mỗi bước và hiệu chỉnh kiểu Tseng cho toán tử giả đơn điệu với phép chiếu chính xác đã có sẵn (Tan–Qin 2020, arXiv:2007.11761, và nhiều bài 2019–2025). Phần dư ra của sơ đồ bốn pha chỉ là việc lắp ráp các khối đã biết thành một tổ hợp chưa ai in nguyên trạng. Loại đóng góp này thuộc mức bài ghép kỹ thuật, phù hợp tạp chí hạng trung về tối ưu và giải tích số, không đủ cho nhóm Q1 hàng đầu.

Điểm mới thứ hai, tức mệnh đề nối tiêu chuẩn sai số với chi phí khởi tạo ấm, không bị bài nào phủ nhận trực tiếp trong dòng bất đẳng thức biến phân, và cả năm góc khảo sát đồng thuận đây là mảnh ít bị chiếm nhất. Tuy nhiên nó sát với nguyên lý kinh điển của phương pháp điểm gần kề xấp xỉ (Rockafellar 1976; Salzo–Villa 2012; Schmidt–Le Roux–Bach 2011), nên chỉ bảo vệ được nếu nâng từ nhận xét định tính lên mệnh đề định lượng chặt, và phải sửa một lỗi toán học thực sự được phát hiện ở vòng phản biện (xem mục 3).

## 2. Một phát hiện danh pháp có hệ quả

Vòng phản biện chỉ ra pha thứ ba của sơ đồ, z = y − λ(F(y) − F(w)), là bước hiệu chỉnh kiểu Tseng (forward-backward-forward), không phải bước phản xạ kiểu Malitsky (vốn dùng điểm phản xạ 2x_k − x_{k−1} trong đối số toán tử và chỉ tính toán tử một lần mỗi bước). Cách gọi "hiệu chỉnh phản xạ" trong thuyết minh và báo cáo là sai tên. Hệ quả kép:

- Gọi đúng tên thì sơ đồ bốn pha gần trùng với Tan–Qin 2020 (chỉ khác ở phép chiếu xấp xỉ), làm mỏng thêm điểm mới thứ nhất.
- Ngược lại, mảnh thực sự còn trống trong tài liệu (theo góc khảo sát C) là kết hợp bước phản xạ kiểu Malitsky đúng nghĩa với phép chiếu xấp xỉ; chưa ai ghép cặp này. Đây là cơ hội nếu chấp nhận sửa thuật toán.

## 3. Các lỗi kỹ thuật phải sửa nếu viết bài (từ vòng phản biện)

Những điểm sau do các tác nhân phản biện độc lập phát hiện; chi tiết và cách sửa nằm trong thư mục `phan_bien/`. Đây là phần có giá trị nhất của vòng làm việc này, vì nó tránh cho bài bị bác ở khâu phản biện thật.

1. Lỗi nặng nhất, ở mệnh đề chi phí: khẳng định "ngân sách bước nội cố định cộng khởi tạo ấm tự động cho dãy sai số tổng được" là sai trong trường hợp tổng quát. Lý do: bước trộn độ nhớt tự nó làm dịch chuyển giữa hai bước ngoài cỡ β_k, mà điều kiện hội tụ mạnh đòi tổng các β_k phân kỳ, nên dãy dịch chuyển không tổng được, kéo theo dãy sai số dưới ngân sách cố định cũng không tổng được. Cách sửa khả thi: thay ngân sách cố định bằng ngân sách tăng chậm m_k cỡ log k, khi đó sai số đạt mức o(β_k) và tổng chi phí bước nội cỡ K log K, vẫn gần tuyến tính; hoặc giới hạn mệnh đề vào lớp bài toán có chặn sai số (error bound) với phát biểu giả thiết tường minh.
2. Điểm bất động của vòng lặp Chambolle-Pock cho phép chiếu lên quả cầu biến phân toàn phần không duy nhất ở biến đối ngẫu (toán tử phân kỳ có hạch không tầm thường), nên giả thiết co rút về một điểm là bất khả thi; phải phát biểu lại theo khoảng cách tới tập điểm bất động và tính chính quy dưới mêtric.
3. Vòng lặp Chambolle-Pock cơ bản trên bài chiếu này chỉ hội tụ với tốc độ O(1/t), không phải tuyến tính, nên câu chuyện sai số giảm hình học cần dùng biến thể tăng tốc (bài chiếu có phần gốc lồi mạnh) hoặc thêm giả thiết, và phải nói rõ.
4. Tiêu chuẩn sai số dạng khoảng cách tới phép chiếu chính xác không tính được trong thực thi; phải thay bằng chứng chỉ sai số tính được, ví dụ qua khoảng cách đối ngẫu của bài chiếu lồi mạnh.
5. Toán tử dạng tích ρ(x)·M(x) với ρ không hằng nói chung không Lipschitz toàn cục, mâu thuẫn với giả thiết nếu phát biểu trên toàn không gian; cần hạn chế trên tập bị chặn hoặc đổi tham số hóa.
6. Lịch quán tính hằng cộng độ nhớt giảm như trong mã hiện tại không thỏa điều kiện của các định lý hội tụ mạnh; cần quy tắc quán tính thích nghi chuẩn (α_k bị chặn theo dịch chuyển và o(β_k)).
7. Trong phác thảo chứng minh, nhánh hai của kỹ thuật Maingé không khép được nếu chỉ giả thiết sai số tổng được; khả năng phải cần điều kiện ε_k/β_k tiến về không — đây là chỗ kỹ thuật thật sự cần thầy hướng dẫn kiểm.
8. Lợi thế của phép chiếu xấp xỉ so với phép chiếu chính xác có khởi tạo ấm là hệ số hằng (cỡ 8 lần theo số liệu), không phải khác biệt bị chặn so với không bị chặn; mọi phát biểu phải giữ đúng mức này.

## 4. Ba con đường và khuyến nghị

Con đường thứ nhất, an toàn: bài hợp nhất cộng mệnh đề chi phí đã sửa. Giữ sơ đồ bốn pha hiện có (gọi đúng tên hiệu chỉnh kiểu Tseng), định vị trung thực là hợp nhất các khối đã biết, trích dẫn thẳng hai bài chặn 2024–2025, dồn giá trị vào mệnh đề chi phí định lượng với lịch m_k cỡ log k và chứng chỉ sai số tính được. Mức tạp chí thực tế: Optimization, Journal of Computational and Applied Mathematics, hoặc Numerical Algorithms nếu may. Xác suất đăng cao, giá trị vừa.

Con đường thứ hai, tham vọng hơn và là cửa Q1 thật còn lại: đổi pha thứ ba thành bước phản xạ kiểu Malitsky đúng nghĩa, thành phương pháp chiếu phản xạ có quán tính và độ nhớt với phép chiếu xấp xỉ. Cặp phản xạ cộng chiếu xấp xỉ là mảnh khảo sát xác nhận chưa ai ghép; bước phản xạ chỉ tính toán tử một lần mỗi bước nên cộng hưởng tự nhiên với câu chuyện chi phí. Cái giá: phương pháp phản xạ không có tính đơn điệu Fejér nên phân tích khó thật sự (Maingé 2018 mới xử lý được phản xạ cộng neo với phép chiếu chính xác); thêm quán tính và sai số chiếu vào đó là công việc toán mới, rủi ro cao, bắt buộc có thầy hướng dẫn tham gia chứng minh.

Con đường thứ ba, bổ trợ: hồ sơ kết quả âm tính hiện có dùng làm phần động cơ của bài lý thuyết, hoặc gửi dạng workshop về kết quả âm tính; không đứng được thành bài chính độc lập.

Khuyến nghị: theo con đường thứ hai với con đường thứ nhất làm phương án lùi, vì hai con đường dùng chung phần lớn vật liệu (mệnh đề chi phí đã sửa, tổng quan tài liệu, bộ mã chiếu lên quả cầu biến phân toàn phần có khởi tạo ấm, kế hoạch thực nghiệm). Quyết định cuối thuộc về thầy hướng dẫn, đặc biệt ở điểm 7 mục 3 và ở lựa chọn giữa hai con đường.

## 5. Danh mục tệp kèm theo

- `khao_sat_tai_lieu_bang_tong_hop.md`: bảng khảo sát đầy đủ năm góc, từng bài kèm thuộc tính và đường dẫn.
- `khao_sat_tai_lieu_ket_luan_5_goc.md`: kết luận của từng góc về điểm mới.
- `ban_nhap/`: năm bản nháp cấu phần (bài toán và thuật toán; định lý hội tụ; mệnh đề chi phí; kế hoạch thực nghiệm; tổng quan tài liệu). Lưu ý: các bản nháp này được viết trước vòng phản biện, phải đọc kèm biên bản phản biện tương ứng, không dùng nguyên trạng.
- `phan_bien/`: năm biên bản phản biện đối kháng, mỗi biên bản liệt kê lỗi theo mức chặn, nặng, nhẹ kèm cách sửa cụ thể.

## 6. Ghi chú trung thực

Các kết luận về tài liệu trong hồ sơ này dựa trên tìm kiếm và đọc trên web tại thời điểm lập; hai bài chặn chính đã được xác minh tồn tại, nhưng trước khi viết bài cần đọc toàn văn cả hai (đặc biệt bài Communications in Nonlinear Science and Numerical Simulation 2025) để đối chiếu giả thiết và kỹ thuật chứng minh từng dòng. Không loại trừ khả năng còn bài chặn khác chưa tìm thấy.
