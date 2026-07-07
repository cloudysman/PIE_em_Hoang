# Bản thảo chứng minh định lý hội tụ mạnh

## 0. Phạm vi và ranh giới trung thực

Tài liệu này soạn bản thảo chứng minh hội tụ mạnh cho sơ đồ phản xạ bốn pha với phép chiếu xấp xỉ đã cài trong `pie_net/reflected_solver.py`. Cần nói thẳng ba điều trước khi vào chi tiết.

Thứ nhất, một chứng minh toán học chỉ được coi là đúng sau khi qua kiểm định độc lập của người hướng dẫn và người phản biện tạp chí. Bản thảo này viết đầy đủ và cố gắng chặt, nhưng không thay thế được khâu kiểm định đó; các bước cần soi kỹ được đánh dấu bằng chữ "cần kiểm".

Thứ hai, chứng minh sạch nhất là cho toán tử đơn điệu. Đây là vì bước phản xạ đánh giá toán tử tại điểm rᵏ nằm ngoài tập ràng buộc, trong khi tính giả đơn điệu chỉ cho thông tin tại các điểm mà nghiệm so được, thường nằm trong tập ràng buộc. Bài toán khôi phục ảnh của dự án dùng toán tử F(x) = Bᵀ(Bx − y), là toán tử đơn điệu, nên trường hợp đơn điệu đã đủ cho ứng dụng. Trường hợp giả đơn điệu được trình bày ở mục 8 như một mở rộng có điều kiện, với chỗ khó nêu rõ.

Thứ ba, chứng minh dựa trên bổ đề một bước của phương pháp chiếu phản xạ (Malitsky 2015) và bổ đề dãy số thực kiểu Xu và Maingé cho hội tụ mạnh của sơ đồ độ nhớt. Các nguồn này được trích dẫn tại chỗ dùng.

## 1. Ký hiệu, giả thiết và điều kiện tham số

Không gian Hilbert thực H, tích vô hướng ⟨·,·⟩, chuẩn ‖·‖. Tập ràng buộc D lồi đóng khác rỗng. Phép chiếu chính xác P_D. Bất đẳng thức biến phân: tìm x* thuộc D sao cho ⟨F(x*), x − x*⟩ ≥ 0 với mọi x thuộc D; tập nghiệm ký hiệu S.

Sơ đồ, với x⁰ = x⁻¹ cho trước và điểm neo qua ánh xạ co f:

    wᵏ = xᵏ + αₖ (xᵏ − xᵏ⁻¹)
    rᵏ = 2 wᵏ − wᵏ⁻¹
    ȳᵏ = P_D( wᵏ − λ F(rᵏ) )                (điểm chiếu chính xác lý tưởng)
    yᵏ = P_D^{εₖ}( wᵏ − λ F(rᵏ) ),  ‖yᵏ − ȳᵏ‖ ≤ εₖ
    xᵏ⁺¹ = βₖ f(xᵏ) + (1 − βₖ) yᵏ

Giả thiết.

- Giả thiết A1: D lồi đóng khác rỗng.
- Giả thiết A2: F đơn điệu trên D, tức ⟨F(u) − F(v), u − v⟩ ≥ 0 với mọi u, v thuộc D; và F liên tục Lipschitz trên H với hằng số L.
- Giả thiết A3: S khác rỗng.
- Giả thiết A5: f là ánh xạ co từ D vào D với hệ số ρ thuộc [0, 1). Trường hợp f là ánh xạ hằng về điểm neo a ứng với ρ = 0.

Điều kiện tham số.

- Điều kiện C1: λ thuộc khoảng (0, (√2 − 1)/L). Đặt c₁ = 1 − λL(1 + √2) > 0 và c₂ = 1 − √2 λL > 0.
- Điều kiện C2: βₖ thuộc (0, 1), βₖ → 0, tổng các βₖ phân kỳ.
- Điều kiện C3: αₖ ≥ 0 và αₖ ‖xᵏ − xᵏ⁻¹‖ ≤ τₖ với τₖ/βₖ → 0. Cài đặt τₖ = βₖ/(k+1) thỏa điều kiện này vì τₖ/βₖ = 1/(k+1) → 0.
- Điều kiện C4: εₖ ≥ 0 và εₖ/βₖ → 0.

Nhận xét về vai trò của điều kiện C3 và C4: cả sai lệch do quán tính (cỡ τₖ) lẫn sai số chiếu (cỡ εₖ) đều phải nhỏ hơn hệ số độ nhớt βₖ theo nghĩa chia cho βₖ thì tiến về không. Đây chính là điều kiện mà mục 7 chỉ ra là cần thiết cho nhánh không đơn điệu của bổ đề dãy số thực.

## 2. Công cụ

Bổ đề A (bổ đề dãy số thực kiểu Xu và Maingé; xem Tan và Qin 2020, Bổ đề 2.2; Maingé 2008). Cho {pₖ} dãy số thực không âm, {σₖ} nằm trong (0, 1) với tổng các σₖ phân kỳ, và {qₖ} dãy số thực sao cho

    pₖ₊₁ ≤ (1 − σₖ) pₖ + σₖ qₖ  với mọi k.

Nếu với mọi dãy con {p_{kⱼ}} thỏa liminf (p_{kⱼ+1} − p_{kⱼ}) ≥ 0 ta có limsup q_{kⱼ} ≤ 0, thì pₖ → 0.

Bổ đề này gộp hai nhánh (dãy đơn điệu và không đơn điệu) vào một phát biểu, nên tránh được việc xử lý riêng nhánh không đơn điệu bằng dãy chỉ số của Maingé. Cần kiểm: khi áp dụng, phải kiểm đúng giả thiết về dãy con, đây là chỗ điều kiện C4 và C3 được dùng.

Bổ đề B (tính chất phép chiếu). Với mọi v thuộc H và u thuộc D: ⟨v − P_D(v), u − P_D(v)⟩ ≤ 0, và ‖P_D(u) − P_D(v)‖ ≤ ‖u − v‖.

Bổ đề C (đẳng thức chuẩn). Với mọi a, b thuộc H và t thuộc [0, 1]:
‖t a + (1 − t) b‖² = t‖a‖² + (1 − t)‖b‖² − t(1 − t)‖a − b‖².

## 3. Bổ đề 1: kiểm soát sai số chiếu xấp xỉ

Theo định nghĩa phép chiếu xấp xỉ, ‖yᵏ − ȳᵏ‖ ≤ εₖ. Do đó với mọi z thuộc H:

    ‖yᵏ − z‖ ≤ ‖ȳᵏ − z‖ + εₖ,
    ‖yᵏ − z‖² ≤ ‖ȳᵏ − z‖² + 2εₖ‖ȳᵏ − z‖ + εₖ².

Đây là dạng nhiễu đều: sai lệch bị chặn bởi εₖ, không phụ thuộc trạng thái ngoài qua chuẩn ‖ȳᵏ − z‖ ở số hạng bậc nhất. Khi dãy bị chặn (Bổ đề 3), số hạng 2εₖ‖ȳᵏ − z‖ + εₖ² là O(εₖ).

## 4. Bổ đề 2: bất đẳng thức một bước cho điểm chiếu chính xác

Áp dụng bổ đề một bước của phương pháp chiếu phản xạ (Malitsky 2015, Bổ đề 9) cho biến wᵏ với điểm phản xạ rᵏ = 2wᵏ − wᵏ⁻¹ và điểm chiếu ȳᵏ = P_D(wᵏ − λF(rᵏ)). Với mọi z thuộc S:

    ‖ȳᵏ − z‖² ≤ ‖wᵏ − z‖² − c₁ ‖wᵏ − wᵏ⁻¹‖² + λL ‖wᵏ − rᵏ⁻¹‖²
                − c₂ ‖ȳᵏ − rᵏ‖² − 2λ ⟨F(z), rᵏ − z⟩,

với c₁ = 1 − λL(1 + √2) và c₂ = 1 − √2 λL, cả hai dương nhờ điều kiện C1.

Xử lý số hạng cuối bằng tính đơn điệu. Vì z thuộc S và ȳᵏ thuộc D, ta có ⟨F(z), ȳᵏ − z⟩ ≥ 0. Viết

    − 2λ ⟨F(z), rᵏ − z⟩ = − 2λ ⟨F(z), ȳᵏ − z⟩ − 2λ ⟨F(z), rᵏ − ȳᵏ⟩
                        ≤ − 2λ ⟨F(z), rᵏ − ȳᵏ⟩.

Số hạng − 2λ⟨F(z), rᵏ − ȳᵏ⟩ được hấp thụ vào lược đồ Lyapunov theo đúng cách của Malitsky: nó ghép với các số hạng ‖wᵏ − rᵏ⁻¹‖² và ‖ȳᵏ − rᵏ‖² để tạo một đại lượng Lyapunov Γₖ giảm. Cụ thể, đặt

    Γₖ = ‖wᵏ − z‖² + λL ‖wᵏ − wᵏ⁻¹‖² + 2λ ⟨F(z), wᵏ⁻¹ − z⟩ + (hằng số),

thì lập luận của Malitsky cho

    ‖ȳᵏ − z‖² ≤ Γₖ − Γₖ₊₁' − c ‖ȳᵏ − rᵏ‖² + (số hạng đơn điệu không dương),

trong đó c > 0. Cần kiểm: bước ghép các số hạng phản xạ thành đại lượng Lyapunov Γₖ phải viết lại đầy đủ cho biến wᵏ của sơ đồ này, vì ở đây wᵏ liên hệ với xᵏ qua quán tính chứ không phải là biến lặp trực tiếp như trong Malitsky. Đây là một trong hai chỗ kỹ thuật nặng nhất của bản thảo.

Kết quả rút gọn dùng cho các bước sau: tồn tại hằng số c > 0 và một dãy {Aₖ} không âm với

    ‖ȳᵏ − z‖² ≤ ‖wᵏ − z‖² − c ‖ȳᵏ − wᵏ‖² + (Aₖ − Aₖ₊₁),   (∗)

trong đó Aₖ tổng hợp các số hạng phản xạ và đơn điệu; tính không âm và tính giảm tổng của {Aₖ} là nội dung cần kiểm của Bổ đề 2.

## 5. Bổ đề 3: dãy lặp bị chặn

Từ quán tính, ‖wᵏ − xᵏ‖ = αₖ‖xᵏ − xᵏ⁻¹‖ ≤ τₖ, và τₖ → 0 nên bị chặn. Do đó ‖wᵏ − z‖ ≤ ‖xᵏ − z‖ + τₖ.

Từ (∗) và Bổ đề 1, với z thuộc S:

    ‖yᵏ − z‖ ≤ ‖ȳᵏ − z‖ + εₖ ≤ ‖wᵏ − z‖ + (Aₖ − Aₖ₊₁ ở dạng đã lấy căn) + εₖ
             ≤ ‖xᵏ − z‖ + τₖ + εₖ + (số hạng phản xạ).

Bước độ nhớt và tính co của f:

    ‖xᵏ⁺¹ − z‖ = ‖βₖ (f(xᵏ) − z) + (1 − βₖ)(yᵏ − z)‖
               ≤ βₖ ‖f(xᵏ) − f(z)‖ + βₖ ‖f(z) − z‖ + (1 − βₖ) ‖yᵏ − z‖
               ≤ βₖ ρ ‖xᵏ − z‖ + βₖ ‖f(z) − z‖ + (1 − βₖ) ‖yᵏ − z‖.

Thế cận của ‖yᵏ − z‖ và dùng τₖ, εₖ → 0 cùng βₖ → 0, thu được truy hồi dạng

    ‖xᵏ⁺¹ − z‖ ≤ (1 − βₖ(1 − ρ)) ‖xᵏ − z‖ + βₖ(1 − ρ) · M_k,

với M_k bị chặn (do các số hạng phụ chia cho βₖ đều bị chặn nhờ C3, C4). Bằng quy nạp, {xᵏ} bị chặn. Cần kiểm: kiểm soát số hạng phản xạ trong bước lấy căn để truy hồi trên đúng dạng co; đây là chỗ dùng tính giảm tổng của {Aₖ}.

## 6. Bổ đề 4: các đại lượng tiệm cận triệt tiêu

Từ (∗), bước độ nhớt và Bổ đề C, thiết lập bất đẳng thức cho sₖ = ‖xᵏ − z‖²:

    sₖ₊₁ ≤ (1 − βₖ(1 − ρ)) sₖ − (1 − βₖ) c ‖ȳᵏ − wᵏ‖² + βₖ(1 − ρ) ξₖ + ηₖ,

trong đó ξₖ chứa các số hạng dạng ⟨f(z) − z, xᵏ⁺¹ − z⟩ và ηₖ = O(εₖ) + O(τₖ) + (Aₖ − Aₖ₊₁). Vì εₖ, τₖ đều là o(βₖ) theo C3, C4, ta có ηₖ/βₖ → 0.

Xét hai khả năng theo Bổ đề A.

Khả năng thứ nhất, {sₖ} cuối cùng đơn điệu giảm. Khi đó sₖ hội tụ, hiệu sₖ − sₖ₊₁ → 0, và vì βₖ → 0 với hệ số c > 0, suy ra ‖ȳᵏ − wᵏ‖ → 0.

Khả năng thứ hai, {sₖ} không đơn điệu. Dùng dãy con {s_{kⱼ}} với liminf (s_{kⱼ+1} − s_{kⱼ}) ≥ 0. Từ bất đẳng thức trên, trên dãy con này (1 − β_{kⱼ}) c ‖ȳ^{kⱼ} − w^{kⱼ}‖² ≤ s_{kⱼ} − s_{kⱼ+1} + β_{kⱼ}(1 − ρ) ξ_{kⱼ} + η_{kⱼ}, mà vế phải có limsup không dương sau khi chia cho hằng số dương, nên ‖ȳ^{kⱼ} − w^{kⱼ}‖ → 0 trên dãy con.

Trong cả hai khả năng, ‖ȳᵏ − wᵏ‖ → 0 trên dãy thích hợp. Kết hợp ‖yᵏ − ȳᵏ‖ ≤ εₖ → 0 và ‖wᵏ − xᵏ‖ ≤ τₖ → 0, thu được ‖yᵏ − xᵏ‖ → 0 và ‖xᵏ⁺¹ − xᵏ‖ → 0 (số hạng cuối vì bước độ nhớt dịch chuyển cỡ βₖ cộng ‖yᵏ − xᵏ‖).

## 7. Bổ đề 5 và định lý chính (trường hợp đơn điệu)

Bổ đề 5 (điểm tụ yếu thuộc tập nghiệm). Do {xᵏ} bị chặn, tồn tại dãy con hội tụ yếu về một điểm x̂. Từ Bổ đề 4, các điểm wᵏ, rᵏ, ȳᵏ trên dãy con cũng hội tụ yếu về x̂. Vì ‖ȳᵏ − wᵏ‖ → 0 và ȳᵏ = P_D(wᵏ − λF(rᵏ)), dùng bất đẳng thức đặc trưng của phép chiếu (Bổ đề B) và tính đơn điệu Lipschitz của F, chuyển qua giới hạn yếu thu được ⟨F(x̂), x − x̂⟩ ≥ 0 với mọi x thuộc D, tức x̂ thuộc S. Cần kiểm: bước chuyển giới hạn yếu qua toán tử dùng tính liên tục yếu theo dãy của F, tự động thỏa trong không gian hữu hạn chiều của phần thực nghiệm.

Định lý (hội tụ mạnh, trường hợp đơn điệu). Dưới các giả thiết A1, A2, A3, A5 và các điều kiện C1, C2, C3, C4, dãy {xᵏ} hội tụ mạnh về x* = P_S(f(x*)), là nghiệm duy nhất của bất đẳng thức biến phân ⟨(I − f)(x*), x − x*⟩ ≥ 0 với mọi x thuộc S. Khi f là ánh xạ hằng về điểm neo a, x* = P_S(a).

Chứng minh. Áp dụng Bổ đề A với pₖ = ‖xᵏ − x*‖², σₖ = βₖ(1 − ρ), và

    qₖ = [2 ⟨f(x*) − x*, xᵏ⁺¹ − x*⟩ + ηₖ/βₖ] / (1 − ρ).

Bất đẳng thức Bổ đề 4 cho pₖ₊₁ ≤ (1 − σₖ) pₖ + σₖ qₖ (cần kiểm: gom đúng các số hạng, dùng bước độ nhớt và tính co của f để ra hệ số 1 − ρ). Với mọi dãy con {p_{kⱼ}} thỏa liminf (p_{kⱼ+1} − p_{kⱼ}) ≥ 0, Bổ đề 4 cho ‖ȳ^{kⱼ} − w^{kⱼ}‖ → 0, nên dãy con này có điểm tụ yếu thuộc S (Bổ đề 5); do x* = P_S(f(x*)) và tính chất phép chiếu, limsup ⟨f(x*) − x*, x^{kⱼ+1} − x*⟩ ≤ 0. Cùng với ηₖ/βₖ → 0 (đây là chỗ điều kiện C3 và C4 được dùng), suy ra limsup q_{kⱼ} ≤ 0. Bổ đề A cho pₖ → 0, tức xᵏ → x* mạnh. Kết thúc chứng minh.

Vai trò của điều kiện sai số chia hệ số độ nhớt tiến về không. Trong biểu thức qₖ có số hạng ηₖ/βₖ, với ηₖ gồm O(εₖ) và O(τₖ). Nếu chỉ giả thiết dãy sai số tổng được mà không giả thiết εₖ/βₖ → 0 và τₖ/βₖ → 0, thì trên nhánh không đơn điệu (khả năng thứ hai của Bổ đề A), không bảo đảm được limsup của ηₖ/βₖ dọc dãy con bằng không, nên không kết luận được limsup q_{kⱼ} ≤ 0. Đây đúng là lỗ hổng mà vòng phản biện đã chỉ ra, và điều kiện C4 (cùng C3) là cách vá đúng: nó bảo đảm số hạng nhiễu nhỏ hơn hẳn so với lực kéo độ nhớt trên mọi dãy con.

## 8. Mở rộng cho toán tử giả đơn điệu

Với F giả đơn điệu thay cho đơn điệu, chỗ hỏng nằm ở Bổ đề 2. Ở đó ta dùng ⟨F(z), ȳᵏ − z⟩ ≥ 0 (đúng cho mọi toán tử vì z là nghiệm và ȳᵏ thuộc D) rồi bước tiếp cần một dạng đơn điệu để hấp thụ số hạng phản xạ. Tính giả đơn điệu chỉ cho ⟨F(z), u − z⟩ ≥ 0 suy ra ⟨F(u), u − z⟩ ≥ 0 với u thuộc D; nhưng toán tử trong sơ đồ được đánh giá tại rᵏ nằm ngoài D, nên không áp trực tiếp được.

Một đường cứu có điều kiện. Giả thiết thêm F giả đơn điệu và liên tục Lipschitz trên toàn H. Viết F(rᵏ) = F(ȳᵏ) + (F(rᵏ) − F(ȳᵏ)), với ‖F(rᵏ) − F(ȳᵏ)‖ ≤ L‖rᵏ − ȳᵏ‖. Áp tính giả đơn điệu tại ȳᵏ thuộc D: từ ⟨F(z), ȳᵏ − z⟩ ≥ 0 suy ra ⟨F(ȳᵏ), ȳᵏ − z⟩ ≥ 0. Phần chênh do đánh giá tại rᵏ thay vì ȳᵏ bị chặn bởi L‖rᵏ − ȳᵏ‖ nhân một đại lượng bị chặn, và ‖rᵏ − ȳᵏ‖ → 0 theo Bổ đề 4, nên số hạng chênh này triệt tiêu tiệm cận. Cần kiểm: phải kiểm rằng số hạng chênh này thực sự hấp thụ được vào lược đồ Lyapunov mà không phá dấu của các số hạng phản xạ, và rằng tốc độ ‖rᵏ − ȳᵏ‖ → 0 đủ nhanh so với các số hạng còn lại. Đây là chỗ khó nhất và chưa được kiểm đầy đủ trong bản thảo này; nó là lý do trường hợp giả đơn điệu được để như một mở rộng có điều kiện, không phải kết quả đã hoàn tất.

Hệ quả cho định vị bài báo: nếu chỉ chứng minh được cho đơn điệu, bài vẫn đứng được vì ứng dụng khôi phục ảnh dùng toán tử đơn điệu; nhưng phần bán được về giả đơn điệu sẽ yếu đi. Nếu chứng minh được đầy đủ cho giả đơn điệu qua đường cứu trên, đóng góp mạnh hơn. Quyết định phạm vi nên bàn với người hướng dẫn.

## 9. Tổng kết trạng thái

Trường hợp đơn điệu: bản thảo đi trọn từ bổ đề một bước tới hội tụ mạnh, với hai chỗ cần kiểm nặng là việc ghép đại lượng Lyapunov cho biến quán tính wᵏ trong Bổ đề 2 và việc gom số hạng trong truy hồi của định lý chính. Điều kiện then chốt để nhánh không đơn điệu của bổ đề dãy số thực khép lại là sai số chiếu và sai lệch quán tính đều nhỏ hơn hệ số độ nhớt theo nghĩa chia cho hệ số đó thì tiến về không.

Trường hợp giả đơn điệu: còn một chỗ khó thực sự ở việc hấp thụ chênh lệch do đánh giá toán tử ngoài tập ràng buộc; để như mở rộng có điều kiện.

Việc cần người hướng dẫn: kiểm hai chỗ cần kiểm ở trường hợp đơn điệu, và quyết định có theo đuổi trường hợp giả đơn điệu đầy đủ hay giới hạn bài ở đơn điệu.
