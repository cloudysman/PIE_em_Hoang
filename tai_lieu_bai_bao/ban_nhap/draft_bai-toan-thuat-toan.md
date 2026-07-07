## 2. Phát biểu bài toán, giả thiết và thuật toán

### 2.1. Bài toán bất đẳng thức biến phân trên tập ràng buộc

Cho $H$ là không gian Hilbert thực với tích vô hướng $\langle \cdot,\cdot\rangle$ và chuẩn $\|\cdot\|$, $D \subset H$ là tập ràng buộc và $F: H \to H$ là toán tử chi phí. Bài toán bất đẳng thức biến phân, ký hiệu $\mathrm{VI}(F, D)$, được phát biểu như sau: tìm $x^* \in D$ sao cho

$$\langle F(x^*),\, x - x^* \rangle \ \ge\ 0 \qquad \forall x \in D. \tag{2.1}$$

Tập nghiệm của (2.1) được ký hiệu là $\Omega$. Phép chiếu chính xác lên $D$ là ánh xạ $P_D(v) = \operatorname{argmin}_{u \in D} \|u - v\|$, xác định duy nhất khi $D$ lồi đóng khác rỗng. Khoảng cách từ một điểm tới nghiệm được đo bằng phần dư biến phân tự nhiên

$$r(x) \ =\ \bigl\| x - P_D\bigl(x - F(x)\bigr) \bigr\|, \tag{2.2}$$

với tính chất $r(x) = 0$ khi và chỉ khi $x \in \Omega$; đại lượng này vừa là thước đo hội tụ trong phân tích lý thuyết, vừa là tiêu chí dừng trong tính toán.

Bài toán (2.1) bao trùm mô hình khôi phục ảnh mà chúng tôi quan tâm. Với bài toán ngược $y = Bx + \varepsilon$, trong đó $B$ là toán tử suy biến tuyến tính đã biết và $\varepsilon$ là nhiễu, toán tử chi phí có cấu trúc tích

$$F(x) \ =\ \rho(x)\, M(x), \qquad M(x) \ =\ B^{\top}(Bx - y) + G(x), \tag{2.3}$$

trong đó $B^{\top}(Bx - y)$ là gradient của hạng dữ liệu $\tfrac{1}{2}\|Bx - y\|^2$ (đơn điệu vì $B^{\top}B$ nửa xác định dương), $G$ là thành phần chính quy hóa đơn điệu, và $\rho(x)$ là hệ số vô hướng dương bị chặn trong $[\rho_{\min}, \rho_{\max}] \subset (0, \infty)$. Vì $\rho$ là vô hướng dương và $M$ đơn điệu, toán tử $F$ giả đơn điệu theo cấu trúc nhưng nói chung không đơn điệu; đồng thời tập nghiệm của $\mathrm{VI}(F, D)$ trùng với tập nghiệm của $\mathrm{VI}(M, D)$. Hai lớp tập ràng buộc điển hình là hộp giá trị điểm ảnh $D = [0,1]^n$, nơi phép chiếu chính xác có công thức đóng (cắt giá trị từng tọa độ), và quả cầu biến phân toàn phần $D = \{x : \mathrm{TV}(x) \le \tau\}$, nơi phép chiếu chính xác không có công thức đóng và phải giải bằng vòng lặp nội (chẳng hạn thuật toán Chambolle-Pock). Trường hợp thứ hai là động cơ trực tiếp của phép chiếu xấp xỉ ở mục 2.3.

### 2.2. Giả thiết

Xuyên suốt bài báo, chúng tôi làm việc dưới các giả thiết chuẩn sau.

(A1) $D \subset H$ là tập ràng buộc lồi, đóng, khác rỗng.

(A2) $F$ giả đơn điệu trên $D$: với mọi $x, y \in D$,
$$\langle F(x),\, y - x\rangle \ge 0 \ \Longrightarrow\ \langle F(y),\, y - x\rangle \ge 0.$$

(A3) $F$ liên tục Lipschitz trên $H$ với hằng số $L > 0$:
$$\|F(x) - F(y)\| \ \le\ L\,\|x - y\| \qquad \forall x, y \in H.$$

(A4) Tập nghiệm $\Omega$ của (2.1) khác rỗng.

(A5) $f: H \to H$ là ánh xạ co với hằng số $\delta \in [0, 1)$, tức $\|f(x) - f(y)\| \le \delta \|x - y\|$ với mọi $x, y \in H$.

Vài nhận xét về phạm vi của các giả thiết. Thứ nhất, mọi toán tử đơn điệu đều giả đơn điệu, nên (A2) rộng hơn hẳn lớp đơn điệu; toán tử cấu trúc (2.3) là một ví dụ giả đơn điệu tự nhiên nằm ngoài lớp đơn điệu. Thứ hai, trong không gian vô hạn chiều, phân tích hội tụ cho toán tử giả đơn điệu thường cần thêm điều kiện liên tục yếu theo dãy của $F$; trong không gian ảnh hữu hạn chiều $\mathbb{R}^n$, điều kiện này được thỏa tự động nhờ (A3), nên chúng tôi không phát biểu thành giả thiết riêng. Thứ ba, hằng số $L$ trong (A3) có thể không biết trước hoặc khó ước lượng khi $F$ chứa thành phần học được; biến thể linesearch ở mục 2.4 được đưa vào chính để xử lý tình huống này.

### 2.3. Phép chiếu xấp xỉ và tiêu chuẩn sai số

Khi tập ràng buộc là quả cầu biến phân toàn phần, mỗi lần gọi phép chiếu chính xác đòi hỏi giải một bài toán tối ưu con tới hội tụ, và chi phí này lặp lại ở mọi bước ngoài. Phép chiếu xấp xỉ thay thế yêu cầu đó bằng một điểm gần điểm chiếu với sai số được kiểm soát.

Định nghĩa 2.1 (phép chiếu xấp xỉ). Cho $v \in H$ và $\epsilon \ge 0$. Một điểm $u \in H$ được gọi là phép chiếu xấp xỉ của $v$ lên $D$ với dung sai $\epsilon$, ký hiệu $u = P_D^{\epsilon}(v)$, nếu

$$\|u - P_D(v)\| \ \le\ \epsilon. \tag{2.4}$$

Khi $\epsilon = 0$, định nghĩa trên thu về phép chiếu chính xác. Bất đẳng thức (2.4) là tiêu chuẩn sai số dạng tuyệt đối; trong cài đặt số, chúng tôi dùng dạng tương đối $\|u - P_D(v)\| \le \epsilon\, \|P_D(v)\|$, tương đương (2.4) với một hằng số tỉ lệ trên miền ảnh bị chặn. Cần nhấn mạnh rằng điểm $u$ trong định nghĩa 2.1 không buộc phải thuộc $D$: đầu ra của phép chiếu xấp xỉ có thể vi phạm ràng buộc ở mức bị chặn bởi $\epsilon$, và mức vi phạm này phải được theo dõi cùng với chất lượng nghiệm.

Về mặt tính toán, $P_D^{\epsilon}(v)$ được hiện thực bằng một vòng lặp nội hội tụ về $P_D(v)$, dừng theo một trong hai chế độ. Chế độ kiểm soát sai số chạy bước nội cho tới khi tiêu chuẩn sai số với dung sai $\epsilon_k$ được thỏa. Chế độ ngân sách chạy đúng $m$ bước nội mỗi bước ngoài, với khởi tạo ấm: trạng thái nội (biến đối ngẫu) của phép chiếu ở bước ngoài trước được dùng làm điểm xuất phát cho phép chiếu ở bước ngoài sau, nhờ đó phép chiếu được hoàn thiện dần dọc theo quỹ đạo ngoài và sai số thực đạt đóng vai trò $\epsilon_k$. Hai vòng lặp nội cụ thể được dùng là: trên hộp $[l, h]^n$, phép lặp giãn $u_{t+1} = (1 - \gamma)\,u_t + \gamma\, \Pi_{[l,h]}(u_t)$ với $u_0 = v$ và hệ số giãn $\gamma \in (0, 1]$, trong đó $\gamma = 1$ cho phép chiếu chính xác sau một bước; trên quả cầu biến phân toàn phần, thuật toán Chambolle-Pock trên bài toán đối ngẫu với khởi tạo ấm qua biến đối ngẫu. Khi sơ đồ được trải phẳng thành mạng và huấn luyện đầu cuối, gradient qua phép chiếu xấp xỉ được lấy bằng cách trải chính vòng lặp nội đã thực hiện, nên không chịu thiên lệch của xấp xỉ hàm ẩn tại điểm dừng sớm.

### 2.4. Thuật toán bốn pha với phép chiếu xấp xỉ

Thuật toán đề xuất ghép bốn cơ chế trong mỗi bước lặp: bước quán tính để tăng tốc, phép chiếu xấp xỉ thay cho phép chiếu chính xác, hiệu chỉnh phản xạ kiểu Tseng để xử lý tính giả đơn điệu với đúng hai lần tính $F$ mỗi bước ngoài, và trộn độ nhớt để bảo đảm hội tụ mạnh của điểm lặp cuối.

Thuật toán 2.1. Chọn $x^0 \in H$, đặt $x^{-1} = x^0$; chọn ánh xạ co $f$ thỏa (A5) và các dãy tham số $\{\alpha_k\}$, $\{\beta_k\}$, $\{\lambda_k\}$, $\{\epsilon_k\}$ thỏa các điều kiện (C1)–(C4) dưới đây. Tại bước $k = 0, 1, 2, \ldots$ thực hiện:

$$
\begin{aligned}
&\text{pha 1 (quán tính):} && w^k = x^k + \alpha_k \,(x^k - x^{k-1}); \\[2pt]
&\text{pha 2 (chiếu xấp xỉ):} && y^k = P_D^{\epsilon_k}\bigl(w^k - \lambda_k F(w^k)\bigr); \\[2pt]
&\text{pha 3 (hiệu chỉnh phản xạ):} && z^k = y^k - \lambda_k \bigl(F(y^k) - F(w^k)\bigr); \\[2pt]
&\text{pha 4 (trộn độ nhớt):} && x^{k+1} = \beta_k\, f(x^k) + (1 - \beta_k)\, z^k.
\end{aligned}
\tag{2.5}
$$

Các dãy tham số chịu các điều kiện sau.

(C1) Hệ số quán tính: $0 \le \alpha_k \le \bar{\alpha} < 1$ với mọi $k$, và
$$\lim_{k \to \infty} \frac{\alpha_k}{\beta_k}\, \|x^k - x^{k-1}\| = 0.$$

(C2) Hệ số độ nhớt: $\beta_k \in (0, 1)$, $\displaystyle\lim_{k \to \infty} \beta_k = 0$ và $\displaystyle\sum_{k=0}^{\infty} \beta_k = \infty$.

(C3) Bước nhảy: $0 < \underline{\lambda} \le \lambda_k \le \bar{\lambda} < 1/L$ với mọi $k$, trong đó $L$ là hằng số Lipschitz ở (A3).

(C4) Dãy sai số: $\{\epsilon_k\}$ là dãy sai số tổng được, $\displaystyle\sum_{k=0}^{\infty} \epsilon_k < \infty$.

Khi hằng số $L$ không biết trước, điều kiện (C3) được thay bằng biến thể linesearch kiểu Tseng: tại bước $k$, lấy $\lambda_k$ là giá trị lớn nhất trong dãy $\{\lambda\, \gamma_{\mathrm{ls}}^{\,j} : j = 0, 1, \ldots\}$, với $\gamma_{\mathrm{ls}} \in (0,1)$ cố định, sao cho

$$\lambda_k\, \bigl\| F\bigl(y^k(\lambda_k)\bigr) - F(w^k) \bigr\| \ \le\ \mu\, \bigl\| y^k(\lambda_k) - w^k \bigr\|, \qquad \mu \in (0, 1), \tag{2.6}$$

trong đó $y^k(\lambda) = P_D^{\epsilon_k}\bigl(w^k - \lambda F(w^k)\bigr)$. Biến thể này không cần hằng số Lipschitz của $F$, đổi lại mỗi lần lùi bước tốn thêm một lần tính $F$ và một phép chiếu xấp xỉ.

Vài nhận xét về thuật toán 2.1. Thứ nhất, khi $\epsilon_k \equiv 0$, sơ đồ (2.5) thu về phương pháp bốn pha với phép chiếu chính xác; đóng góp của bài báo nằm ở việc giữ nguyên các kết luận hội tụ khi phép chiếu chính xác được thay bằng phép chiếu xấp xỉ dưới điều kiện (C4). Thứ hai, do phép chiếu xấp xỉ, các điểm $y^k$ và do đó $x^{k+1}$ có thể nằm ngoài $D$; điều kiện dãy sai số tổng được bảo đảm tổng mức lệch khỏi tập ràng buộc là hữu hạn, và khi cần đầu ra khả thi thì điểm lặp cuối được ép về $D$ bằng một phép chiếu chính xác duy nhất. Thứ ba, vai trò của pha trộn độ nhớt là chọn nghiệm: dưới (C2), điểm giới hạn kỳ vọng là nghiệm duy nhất $\hat{x} \in \Omega$ của bất đẳng thức biến phân $\langle (I - f)\hat{x},\, x - \hat{x}\rangle \ge 0$ với mọi $x \in \Omega$, và sự hội tụ của $\{x^k\}$ tới $\hat{x}$ là hội tụ mạnh, không chỉ hội tụ yếu như ở các sơ đồ không có độ nhớt. Trong cài đặt, ánh xạ co được lấy dạng $f(x) = \delta x + (1 - \delta)\, x^0$ với $\delta \in [0,1)$, tức kéo nhẹ về điểm khởi tạo theo kiểu Halpern. Thứ tư, về chi phí, mỗi bước ngoài của (2.5) cần hai lần tính $F$ (tại $w^k$ và $y^k$) và một phép chiếu xấp xỉ gồm $m$ bước nội có khởi tạo ấm; so với sơ đồ dùng phép chiếu chính xác, toàn bộ phần tiết kiệm nằm ở việc cắt ngắn vòng lặp nội. Thứ năm, về lịch tham số, cài đặt số dùng $\alpha_k \equiv \alpha \in [0, 1)$, $\beta_k = \beta_0 / (k+1)$ (thỏa (C2)) và $\lambda_k$ trong khoảng $[\underline{\lambda}, \bar{\lambda}]$ cố định hoặc học được theo từng bước khi sơ đồ được trải phẳng với số bước ngoài hữu hạn $K$; ở chân trời hữu hạn, dung sai được đặt giảm dần $\epsilon_k = \epsilon_0/(k+1)$, còn phân tích tiệm cận đòi hỏi đúng điều kiện tổng được (C4), chẳng hạn $\epsilon_k = O\bigl(1/k^{1+\nu}\bigr)$ với $\nu > 0$.

Mục tiêu lý thuyết của bài báo là hai kết luận cho thuật toán 2.1 dưới các giả thiết (A1)–(A5) và điều kiện (C1)–(C4): sự hội tụ mạnh của điểm lặp cuối $x^k$ tới $\hat{x}$, và tốc độ hội tụ của phần dư biến phân $r(x^k)$ theo (2.2). Hai kết luận này được phát biểu và chứng minh ở mục sau.
