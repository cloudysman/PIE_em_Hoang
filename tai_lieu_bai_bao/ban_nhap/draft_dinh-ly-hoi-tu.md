# Định lý hội tụ mạnh và phác thảo chứng minh

Mục này phát biểu định lý chính của bài báo ở dạng dự kiến và trình bày đường chứng minh theo các bổ đề đã biết trong tài liệu. Chúng tôi nói rõ ngay từ đầu: đây là phác thảo, chưa phải chứng minh hoàn chỉnh; các bước được dán nhãn [thường quy] nếu lập luận đã chuẩn hóa trong tài liệu và chỉ cần chép lại có điều chỉnh, hoặc [cần kiểm kỹ] nếu là chỗ mới do việc gộp đồng thời ba thành phần quán tính, độ nhớt và phép chiếu xấp xỉ, nơi các hằng số và số hạng nhiễu phải được rà lại từ đầu.

## Bài toán và giả thiết

Cho $H$ là không gian Hilbert thực, $C \subset H$ là tập ràng buộc đóng, lồi, khác rỗng. Xét bất đẳng thức biến phân: tìm $x^\dagger \in C$ sao cho

$$\langle F(x^\dagger),\, x - x^\dagger \rangle \ge 0 \quad \text{với mọi } x \in C,$$

với tập nghiệm ký hiệu $S$. Các giả thiết làm việc:

- (A1) $S \neq \emptyset$.
- (A2) $F$ giả đơn điệu trên $C$: nếu $\langle F(x), y-x\rangle \ge 0$ thì $\langle F(y), y-x\rangle \ge 0$.
- (A3) $F$ liên tục Lipschitz với hằng số $L$ trên $H$.
- (A4) $F$ liên tục yếu theo dãy trên $C$: $x_k \rightharpoonup x$ kéo theo $F(x_k) \rightharpoonup F(x)$.

Giả thiết (A4) chỉ dùng đúng một lần (bổ đề F dưới đây) và là giả thiết chuẩn của nhánh giả đơn điệu; khả năng nới lỏng (A4) theo một số công trình gần đây được để ở mục vấn đề mở, không đưa vào định lý chính.

## Sơ đồ lặp

Mỗi bước ngoài $k$ dùng đúng một phép chiếu xấp xỉ, gồm bốn pha:

1. Bước quán tính: $w_k = x_k + \alpha_k (x_k - x_{k-1})$.
2. Phép chiếu xấp xỉ: tính $y_k$ thỏa tiêu chuẩn sai số $\|y_k - \bar y_k\| \le \varepsilon_k$, trong đó $\bar y_k = P_C\big(w_k - \lambda F(w_k)\big)$ là phép chiếu chính xác. Trong thực nghiệm, $y_k$ được tính bằng vòng lặp nội kiểu Chambolle–Pock với khởi tạo ấm khi $C$ là quả cầu biến phân toàn phần.
3. Hiệu chỉnh phản xạ (kiểu Tseng): $z_k = y_k - \lambda\big(F(y_k) - F(w_k)\big)$.
4. Bước độ nhớt: $x_{k+1} = \beta_k f(x_k) + (1-\beta_k) z_k$, với $f$ là ánh xạ co hệ số $\kappa \in [0,1)$; trường hợp riêng $f \equiv u$ (điểm neo cố định) cho sơ đồ kiểu Halpern.

Điều kiện tham số:

- (P1) $\lambda \in (0, 1/L)$ (hằng số bước chính xác cho biến thể phản xạ cần kiểm lại, xem điểm khó 4);
- (P2) $\beta_k \in (0,1)$, $\beta_k \to 0$, $\sum_k \beta_k = \infty$;
- (P3) dãy sai số tổng được: $\sum_k \varepsilon_k < \infty$;
- (P4) điều kiện tổng được cho bước quán tính: $\sum_k \alpha_k \|x_k - x_{k-1}\| < \infty$, bảo đảm được trong thực hành bằng quy tắc trực tuyến $\alpha_k \le \min\{\alpha,\, c_k / \|x_k - x_{k-1}\|\}$ với $\sum_k c_k < \infty$.

## Phát biểu định lý chính (dự kiến)

Định lý 1 (dự kiến — chứng minh chưa hoàn chỉnh). Giả sử (A1)–(A4) và (P1)–(P4). Khi đó dãy $(x_k)$ sinh bởi sơ đồ trên hội tụ mạnh tới $x^* \in S$, là điểm bất động duy nhất của $P_S \circ f$, tức nghiệm duy nhất của bất đẳng thức biến phân phụ $\langle (I-f)(x^*),\, x - x^*\rangle \ge 0$ với mọi $x \in S$. Nói riêng, khi $f \equiv u$ thì $x^* = P_S(u)$: dãy lặp hội tụ mạnh tới hình chiếu của điểm neo lên tập nghiệm.

Nhận xét về tính đặt đúng của giới hạn. Phát biểu trên chỉ có nghĩa nếu $P_S$ xác định, tức $S$ đóng và lồi. Với $F$ giả đơn điệu và liên tục, tập nghiệm Stampacchia trùng tập nghiệm Minty (lập luận kiểu Cottle–Yao), mà tập nghiệm Minty luôn đóng và lồi; do đó $S$ đóng, lồi và $P_S \circ f$ là ánh xạ co trên $H$, có điểm bất động duy nhất theo nguyên lý Banach. Bước này là [thường quy] nhưng bắt buộc phải ghi tường minh, vì với toán tử giả đơn điệu tính lồi của $S$ không hiển nhiên như trường hợp đơn điệu.

## Phác thảo chứng minh qua chuỗi bổ đề

Công cụ chính gồm: bổ đề dãy số thực của Xu (2002, J. London Math. Soc.) cho hồi quy $s_{k+1} \le (1-\beta_k) s_k + \beta_k b_k + c_k$; kỹ thuật hai trường hợp của Maingé (2008, Set-Valued Anal.) cho dãy không đơn điệu; phân tích quasi-Fejér với nhiễu tổng được theo Combettes (2001); và cách xử lý tiêu chuẩn sai số của nhánh chiếu xấp xỉ, gần nhất là bài "Extragradient method with feasible inexact projection" (Comput. Optim. Appl., 2024).

Bổ đề B (bất đẳng thức một bước) [cần kiểm kỹ]. Với mọi $p \in S$, mục tiêu là

$$\|z_k - p\|^2 \le \|w_k - p\|^2 - (1 - \lambda^2 L^2)\,\|\bar y_k - w_k\|^2 + \eta_k,$$

trong đó $\eta_k$ gom các số hạng nhiễu sinh bởi phép chiếu xấp xỉ, cỡ $O\big(\varepsilon_k (\|w_k - p\| + \|F(w_k)\| + 1)\big)$. Với phép chiếu chính xác ($\varepsilon_k = 0$) đây là bất đẳng thức chuẩn của sơ đồ Tseng và là [thường quy]. Hai chỗ phải kiểm kỹ: (i) tính giả đơn điệu chỉ áp dụng được cho điểm thuộc $C$, trong khi $y_k$ có thể nằm ngoài $C$; lập luận phải đi qua điểm chiếu chính xác $\bar y_k \in C$ rồi ước lượng phần chênh $\|y_k - \bar y_k\| \le \varepsilon_k$ — đây là khác biệt bản chất so với trường hợp đơn điệu, nơi bất đẳng thức đặc trưng của phép chiếu đủ dùng trực tiếp; (ii) mọi hằng số trong $\eta_k$ phải tường minh vì bước sau cần tính tổng được của $\eta_k$.

Bổ đề C (kiểm soát bước quán tính) [thường quy]. Từ định nghĩa $w_k$: $\|w_k - p\|^2 \le \|x_k - p\|^2 + \theta_k$ với $\theta_k$ cỡ $\alpha_k \|x_k - x_{k-1}\| (\|x_k - p\| + \|x_k - x_{k-1}\|)$; điều kiện (P4) làm $\sum_k \theta_k < \infty$ một khi dãy bị chặn. Lập luận này đã chuẩn hóa trong nhánh quán tính.

Bổ đề D (tính bị chặn của dãy lặp) [cần kiểm kỹ]. Ghép B, C với bước độ nhớt: $\|x_{k+1} - p\| \le (1-\beta_k)\|z_k - p\| + \beta_k \|f(x_k) - p\|$ và tính co của $f$ cho hồi quy kiểu $s_{k+1} \le \max\{s_k, M\} + \xi_k$. Chỗ tinh vi: $\eta_k$ và $\theta_k$ phụ thuộc $\|w_k - p\|$, $\|x_k - x_{k-1}\|$ — các đại lượng chưa biết bị chặn — nên nếu lập luận không cẩn thận sẽ luẩn quẩn (dùng tính bị chặn để chứng minh tính bị chặn). Lối ra đã biết là bổ đề quasi-Fejér với nhiễu tổng được (Combettes, 2001) hoặc quy nạp với chặn đều tường minh; việc chọn lối nào và viết trọn vẹn là một trong những phần việc chính còn lại.

Bổ đề E (phần dư biến phân triệt tiêu) [thường quy sau khi có D]. Khi dãy đã bị chặn, cộng dồn bất đẳng thức một bước cho $(1-\lambda^2 L^2) \sum \text{(trên dãy con thích hợp)}\, \|\bar y_k - w_k\|^2$ hữu hạn, suy ra phần dư biến phân $r(w_k) = \|w_k - P_C(w_k - \lambda F(w_k))\|$ tiến về $0$ trên dãy con đó. Việc "dãy con thích hợp" là toàn dãy hay dãy con $\tau(k)$ tùy thuộc trường hợp của Maingé ở bổ đề G.

Bổ đề F (điểm tụ yếu thuộc tập nghiệm) [thường quy, dựa vào (A4)]. Từ $r(w_k) \to 0$ và $\lambda$ tách khỏi $0$, mọi điểm tụ yếu $\bar x$ của $(w_k)$ thỏa bất đẳng thức Minty $\langle F(x), x - \bar x\rangle \ge 0$ với mọi $x \in C$; kết hợp tính liên tục và giả đơn điệu suy ra $\bar x \in S$. Đây là chỗ duy nhất dùng (A4); lập luận theo mẫu đã có của nhánh giả đơn điệu, nhưng cần kiểm rằng sai số $\varepsilon_k \to 0$ không phá vỡ bước qua giới hạn (dự kiến không, vì $\varepsilon_k$ tổng được nên $\varepsilon_k \to 0$).

Bổ đề G (kết thúc bằng bổ đề dãy số) [thường quy]. Đặt $s_k = \|x_k - x^*\|^2$. Khai triển bước độ nhớt cho

$$s_{k+1} \le \big(1 - (1-\kappa)\beta_k\big) s_k + (1-\kappa)\beta_k\, b_k + c_k,$$

với $b_k$ chứa $\langle f(x^*) - x^*,\, x_{k+1} - x^*\rangle$ (sai khác hằng số) và $c_k$ gom $\eta_k$, $\theta_k$ tổng được. Hai trường hợp theo Maingé (2008): nếu $s_k$ đơn điệu giảm từ một lúc nào đó, bổ đề E và F trên toàn dãy cùng đặc trưng của phép chiếu $P_S$ cho $\limsup_k b_k \le 0$, rồi bổ đề Xu (2002) kết luận $s_k \to 0$, tức hội tụ mạnh; nếu không, xét dãy chỉ số $\tau(k) = \max\{j \le k : s_j < s_{j+1}\}$ và lặp lại lập luận dọc $\tau(k)$ theo đúng khuôn của Maingé. Cả hai nhánh là [thường quy] một khi các bổ đề B–F đã đứng vững.

## Những điểm khó phải kiểm kỹ trước khi viết chứng minh đầy đủ

1. Lựa chọn tiêu chuẩn sai số. Có hai họ: sai số theo khoảng cách tới phép chiếu chính xác (điểm $y_k$ có thể nằm ngoài $C$, như phát biểu ở trên) và sai số khả thi ($y_k \in C$, theo hướng của bài Comput. Optim. Appl. 2024). Với toán tử giả đơn điệu, họ thứ hai thuận cho bổ đề B và F hơn nhưng đòi hỏi vòng lặp nội trả về điểm khả thi — điều sơ đồ Chambolle–Pock trên quả cầu biến phân toàn phần không tự nhiên bảo đảm. Quyết định này ảnh hưởng dây chuyền tới cả mệnh đề chi phí khởi tạo ấm và phải chốt trước tiên.
2. Nhiễu phụ thuộc trạng thái trong bổ đề D: tránh lập luận vòng khi $\eta_k$ chứa chuẩn của chính dãy lặp.
3. Tương tác ba thành phần. Từng cặp {quán tính, độ nhớt}, {độ nhớt, chiếu xấp xỉ} đã có tiền lệ; gộp cả ba đồng thời là phần mới của bài. Không được mượn nguyên văn hằng số từ các bài chỉ gộp từng cặp; mọi bất đẳng thức trung gian phải dẫn lại.
4. Hằng số bước cho hiệu chỉnh phản xạ: biên $\lambda < 1/L$ đúng cho dạng Tseng; nếu chuyển sang biến thể phản xạ khác (kiểu Malitsky), biên sẽ khác và ảnh hưởng hệ số trước $\|\bar y_k - w_k\|^2$. Cần cố định một biến thể và kiểm biên tương ứng.
5. Quan hệ giữa (P3) và (P2): dãy sai số tổng được đủ cho hội tụ mạnh (vào vị trí $c_k$ trong bổ đề Xu); nhưng nếu về sau muốn phát biểu tốc độ hội tụ, nhiều khả năng cần điều kiện mạnh hơn kiểu $\varepsilon_k = o(\beta_k)$ — để ở mục tùy chọn, không cài vào định lý chính.

## Tuyên bố trung thực

Toàn bộ mục này là phác thảo đường chứng minh, chưa phải chứng minh. Các bổ đề A, C, E, F, G có khuôn mẫu sẵn trong tài liệu và chúng tôi đánh giá rủi ro thấp; bổ đề B và D là nơi tính mới tập trung và cũng là nơi rủi ro kỹ thuật cao nhất, đặc biệt điểm khó 1 và 2. Chừng nào hai bổ đề này chưa được viết trọn và kiểm tra độc lập, định lý 1 phải được coi là phát biểu dự kiến.
