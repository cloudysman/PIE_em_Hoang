# Chứng minh đầy đủ định lý hội tụ yếu: phần ghép thế năng mang nhiễu

Tài liệu này viết trọn phần mà bản thảo bài báo và tệp 05 để ở dạng phác thảo: ghép đại lượng thế năng của Malitsky, có mang theo nhiễu do phép chiếu xấp xỉ. Ký hiệu theo bản thảo. Mọi bước được dẫn từ đầu; các chỗ dùng kết quả có sẵn được nêu tên tại chỗ.

## Ký hiệu

Sơ đồ: r^k = 2x^k − x^{k−1}; x^{k+1} thuộc P_D^{ε_k}(x^k − λF(r^k)). Điểm chiếu chính xác lý tưởng x̄^{k+1} = P_D(x^k − λF(r^k)), nên ‖x^{k+1} − x̄^{k+1}‖ ≤ ε_k. Đặt e^k = x^{k+1} − x̄^{k+1}. Cố định z thuộc S và đặt a_j = ⟨F(z), z − x^j⟩. Vì x^j thuộc D (giả thiết khả thi) và z thuộc S, ta có a_j ≤ 0 với mọi j.

Các hằng số: c1 = 1 − λL(1 + √2), c2 = 1 − √2 λL. Theo giả thiết bước nhảy λ < (√2 − 1)/L, cả hai dương. Một đẳng thức sẽ dùng nhiều lần: c2 − λL = 1 − √2λL − λL = 1 − λL(1 + √2) = c1.

## 1. Bất đẳng thức một bước cho điểm chiếu chính xác

Đây là bổ đề chính của Malitsky, áp cho x̄^{k+1}. Cần phân biệt hai vai trò của phép chiếu, vì đây chính là chỗ nhiễu sẽ vào. Việc áp bổ đề cho x̄^{k+1} chỉ đòi phép chiếu HIỆN TẠI chính xác, tức x̄^{k+1} = P_D(x^k − λF(r^k)); điều này đúng theo định nghĩa. Nhưng số hạng λL‖x^k − r^{k−1}‖² trong (1) còn chứa x^{k−2} qua r^{k−1} = 2x^{k−1} − x^{k−2}, và điểm x^{k−2} chỉ đi vào phân tích qua bất đẳng thức chiếu của bước TRƯỚC, vốn chỉ đúng cho phép chiếu chính xác x̄^k. Trong sơ đồ nhiễu x^k khác x̄^k, nên phụ thuộc này sinh sai số ν_k, xử lý ở mục 4. Với mọi z thuộc D:

    ‖x̄^{k+1} − z‖² ≤ ‖x^k − z‖² − c1‖x^k − x^{k−1}‖² + λL‖x^k − r^{k−1}‖²
                    − c2‖x̄^{k+1} − r^k‖² − 2λ⟨F(z), r^k − z⟩.        (1)

Bất đẳng thức (1) chính là Bổ đề 9 của Malitsky với ánh xạ hằng số bước λ; ở đây chỉ đổi ký hiệu y_n thành r^k và x_{n+1} thành x̄^{k+1}. Việc dẫn (1) từ bất đẳng thức một bước cộng tính đơn điệu cộng ước lượng Lipschitz cho số hạng ⟨F(r^k), r^k − x̄^{k+1}⟩ là nội dung Bổ đề onestep, mono và bước ước lượng Lipschitz trong bản thảo; số hạng λL‖x^k − r^{k−1}‖² sinh ra từ chính bước ước lượng đó, và nó dùng bất đẳng thức chiếu của bước TRƯỚC cho điểm chiếu chính xác x̄^k. Đây là chỗ nhiễu điểm gốc sẽ xuất hiện ở mục 3.

## 2. Xử lý số hạng nghiệm bằng telescoping

Từ r^k = 2x^k − x^{k−1} và z − r^k = 2(z − x^k) − (z − x^{k−1}):

    ⟨F(z), z − r^k⟩ = 2a_k − a_{k−1},   nên   −2λ⟨F(z), r^k − z⟩ = 2λ(2a_k − a_{k−1}) = 4λa_k − 2λa_{k−1}.

Thay vào (1):

    ‖x̄^{k+1} − z‖² ≤ ‖x^k − z‖² − c1‖x^k − x^{k−1}‖² + λL‖x^k − r^{k−1}‖²
                    − c2‖x̄^{k+1} − r^k‖² + 4λa_k − 2λa_{k−1}.        (2)

## 3. Đại lượng thế năng và bước ghép, trường hợp chiếu chính xác

Định nghĩa thế năng

    φ_k = ‖x^k − z‖² + λL‖x^k − r^{k−1}‖² − 2λa_{k−1}.        (3)

Ba số hạng đều không âm: hai số hạng đầu hiển nhiên, số hạng thứ ba vì a_{k−1} ≤ 0. Do đó φ_k ≥ 0, và ‖x^k − z‖² ≤ φ_k.

Trước hết xét trường hợp chiếu chính xác, tức x^{k+1} = x̄^{k+1}, để làm rõ cơ chế. Khi đó φ_{k+1} = ‖x^{k+1} − z‖² + λL‖x^{k+1} − r^k‖² − 2λa_k. Cộng λL‖x̄^{k+1} − r^k‖² − 2λa_k vào hai vế của (2):

    φ_{k+1} = ‖x̄^{k+1} − z‖² + λL‖x̄^{k+1} − r^k‖² − 2λa_k
            ≤ [‖x^k − z‖² + λL‖x^k − r^{k−1}‖² − 2λa_{k−1}]
              − c1‖x^k − x^{k−1}‖² + (λL − c2)‖x̄^{k+1} − r^k‖² + 2λa_k
            = φ_k − c1‖x^k − x^{k−1}‖² − c1‖x̄^{k+1} − r^k‖² + 2λa_k,        (4)

trong đó ở dòng cuối dùng λL − c2 = −c1. Vì a_k ≤ 0, bất đẳng thức (4) cho φ_{k+1} ≤ φ_k. Đây là chứng minh đầy đủ cho trường hợp chiếu chính xác, và nó khép kín: φ giảm, bị chặn dưới bởi 0, nên hội tụ; các số hạng âm cộng dồn hữu hạn.

## 4. Thêm nhiễu chiếu xấp xỉ

Bây giờ x^{k+1} = x̄^{k+1} + e^k với ‖e^k‖ ≤ ε_k. Nhiễu vào theo hai đường.

Đường thứ nhất, ở vế trái của (4), khi thay x̄^{k+1} bằng x^{k+1} trong φ_{k+1}. Có

    ‖x^{k+1} − z‖² = ‖x̄^{k+1} − z‖² + 2⟨e^k, x̄^{k+1} − z⟩ + ‖e^k‖²
                   ≤ ‖x̄^{k+1} − z‖² + 2ε_k‖x̄^{k+1} − z‖ + ε_k²,
    ‖x^{k+1} − r^k‖² ≤ ‖x̄^{k+1} − r^k‖² + 2ε_k‖x̄^{k+1} − r^k‖ + ε_k².

Do đó φ_{k+1} thực (dùng x^{k+1}) không vượt φ_{k+1} lý tưởng (dùng x̄^{k+1}) cộng một lượng

    μ_k = 2ε_k‖x̄^{k+1} − z‖ + (1 + λL)ε_k² + 2λL ε_k‖x̄^{k+1} − r^k‖.

Đường thứ hai, ở vế phải: số hạng λL‖x^k − r^{k−1}‖² của (2) đến từ bất đẳng thức chiếu của bước trước áp cho x̄^k, nhưng biến thực của sơ đồ là x^k = x̄^k + e^{k−1}. Bất đẳng thức chiếu chính xác của bước k−1 là: với mọi y thuộc D,

    ⟨x^{k−1} − λF(r^{k−1}) − x̄^k, y − x̄^k⟩ ≤ 0.

Khi bất đẳng thức này được dùng để chặn số hạng toán tử, việc thay x̄^k = x^k − e^{k−1} sinh các số hạng chéo bậc nhất theo e^{k−1}. Gộp lại, đường thứ hai đóng góp một lượng

    ν_k ≤ C ε_{k−1},

với C là hằng số phụ thuộc λ và chặn của dãy và của F, độc lập k. Vì ∑ε_{k−1} hữu hạn, ν_k tổng được, và đó là tất cả những gì cần cho hội tụ.

Ghi chú trung thực về hệ số, đã sửa sau vòng phản biện. Bản trước của tài liệu này khẳng định hằng số C chứa nghịch đảo bước nhảy 1/λ, và gọi đó là đóng góp mới của bài. Khẳng định đó chưa được thiết lập: bất đẳng thức chiếu tuy chia cho λ, nhưng khi được dùng trong lược đồ giảm nó thường bị nhân lại với một thừa số λ có sẵn trên các số hạng toán tử, nên hệ số 1/λ có thể triệt tiêu thành bậc một. Chưa kiểm cái nào đúng. Vì hội tụ chỉ cần ν_k tổng được, không cần biết hệ số chính xác, ta phát biểu ν_k ≤ Cε_{k−1} và để việc xác định C có chứa 1/λ hay không cho bước viết đầy đủ; nếu C thật sự chứa 1/λ thì đó mới là điểm phân biệt của bài, còn nếu không thì đóng góp thu về đúng phần hợp nhất phản xạ với chiếu xấp xỉ.

Kết hợp, bất đẳng thức (4) trở thành

    φ_{k+1} ≤ φ_k − c1‖x^k − x^{k−1}‖² − c1‖x̄^{k+1} − r^k‖² + 2λa_k + δ_k,        (5)

với δ_k = μ_k + ν_k. Lưu ý ν_k tổng được ngay, nhưng μ_k chứa các thừa số chuẩn ‖x̄^{k+1} − z‖ và ‖x̄^{k+1} − r^k‖ chưa bị chặn tiên nghiệm, nên δ_k CHƯA tổng được trực tiếp; tính bị chặn của quỹ đạo lại là một phần của kết luận, nên phải xử lý μ_k bằng nhân tính hóa ở mục 5, không được viết tổng δ_k hữu hạn vô điều kiện ở đây.

## 5. Tính tổng được của δ_k và đóng vòng

Trong δ_k, các số hạng ‖x̄^{k+1} − z‖ và ‖x̄^{k+1} − r^k‖ cần được chặn để δ_k tổng được. Đây là chỗ dùng dạng nhân tính hóa quen thuộc: với mọi số dương t,

    2ε_k‖x̄^{k+1} − z‖ ≤ ε_k(1 + ‖x̄^{k+1} − z‖²) ≤ ε_k(1 + φ_{k+1}^{≤}) ,

trong đó φ_{k+1}^{≤} là vế trên. Điều này biến (5) thành truy hồi tựa Fejér loại nhân tính

    φ_{k+1} ≤ (1 + α_k) φ_k − c1(‖x^k − x^{k−1}‖² + ‖x̄^{k+1} − r^k‖²) + 2λa_k + β_k,        (6)

với ∑α_k < ∞ và ∑β_k < ∞, cả hai suy từ ∑ε_k < ∞ và ∑ε_{k−1} < ∞ cùng tính bị chặn của F trên quỹ đạo. Cần kiểm: bước nhân tính hóa phải làm cẩn thận để không nuốt mất phần âm −c1(...); chuẩn của việc này là bổ đề tựa Fejér loại II của Combettes 2001, phát biểu chính xác cho truy hồi dạng (6).

Áp bổ đề tựa Fejér loại nhân tính cho {φ_k}: vì ∑α_k, ∑β_k hữu hạn và a_k ≤ 0, dãy {φ_k} hội tụ, {x^k} bị chặn, và cộng dồn phần âm cho

    ∑_k ‖x^k − x^{k−1}‖² < ∞,   ∑_k ‖x̄^{k+1} − r^k‖² < ∞,   ∑_k (−a_k) < ∞.

Từ đó ‖x^k − x^{k−1}‖ → 0, ‖x̄^{k+1} − r^k‖ → 0, và a_k → 0. Vì ‖x^{k+1} − x̄^{k+1}‖ ≤ ε_k → 0, cũng có ‖x^{k+1} − r^k‖ → 0. Kết hợp r^k = 2x^k − x^{k−1} và ‖x^k − x^{k−1}‖ → 0 cho ‖x^{k+1} − x^k‖ → 0.

Vì {φ_k} hội tụ và λL‖x^k − r^{k−1}‖² → 0 cùng a_{k−1} → 0, từ (3) suy ra ‖x^k − z‖² hội tụ, với mọi z thuộc S.

## 6. Điểm tụ yếu thuộc tập nghiệm và kết luận

Do {x^k} bị chặn, có dãy con hội tụ yếu về x̂. Vì ‖x^k − x^{k−1}‖ → 0, các điểm r^k trên dãy con cũng hội tụ yếu về x̂; và ‖x̄^{k+1} − r^k‖ → 0 với ‖x^{k+1} − x̄^{k+1}‖ → 0 nên x^{k+1} hội tụ yếu về x̂ trên dãy con. Từ định nghĩa x̄^{k+1} = P_D(x^k − λF(r^k)) và đặc trưng phép chiếu, với mọi y thuộc D:

    ⟨x^k − λF(r^k) − x̄^{k+1}, y − x̄^{k+1}⟩ ≤ 0.

Chia cho λ, dùng ‖x^k − x̄^{k+1}‖ → 0 (suy từ ‖x^k − x^{k−1}‖ → 0 và ‖x̄^{k+1} − r^k‖ → 0), chuyển qua giới hạn yếu, và dùng tính đơn điệu Lipschitz của F qua bổ đề Minty, thu được ⟨F(y), y − x̂⟩ ≥ 0 với mọi y thuộc D, tức x̂ thuộc S theo Minty.

Cuối cùng, vì ‖x^k − z‖ hội tụ với mọi z thuộc S và mọi điểm tụ yếu thuộc S, bổ đề Opial cho {x^k} hội tụ yếu về một phần tử của S. Kết thúc.

## 7. Trạng thái và các chỗ cần kiểm

Đã dẫn đầy đủ, tin được: mục 1 đến 3, tức bước ghép thế năng cho chiếu chính xác, kể cả đẳng thức then chốt c2 − λL = c1 làm hai số hạng âm gộp lại với cùng hệ số. Đây là phần mà bản thảo trước để ở dạng phác thảo.

Cần kiểm kỹ, và là chỗ đóng góp thật của bài:

1. Hằng số C1, C2 trong ν_k ở mục 4. Việc dẫn chính xác chúng đòi viết ra tường minh chỗ Malitsky dùng bất đẳng thức chiếu bước trước, rồi thay x̄^k = x^k − e^{k−1} và gom số hạng chứa 1/λ. Bản thảo này chỉ khẳng định dạng, chưa viết ra từng hằng số.
2. Bước nhân tính hóa ở mục 5 phải kiểm không nuốt phần âm −c1(...); dùng đúng phát biểu bổ đề tựa Fejér loại nhân tính của Combettes.
3. Bước chuyển giới hạn yếu ở mục 6 dùng tính đơn điệu và Minty; trong không gian hữu hạn chiều của phần thực nghiệm là thường quy, trong không gian vô hạn chiều cần tính liên tục yếu theo dãy của F.

So với bản thảo trước, mục 1 đến 3 đã chuyển từ phác thảo thành chứng minh đầy đủ. Phần còn thiếu thu hẹp về đúng ba mục trên.

## 7bis. Dẫn xuất đầy đủ hằng số ν_k, và câu trả lời cho câu hỏi hệ số 1/λ

Đây là chỗ được đánh dấu là quyết định: hằng số C trong ν_k ≤ Cε_{k−1} có chứa nghịch đảo bước nhảy hay không. Ta dẫn xuất từ đầu, dùng đúng công thức (11) của Malitsky.

Nguồn của số hạng phụ thuộc bước trước. Trong chứng minh Malitsky, số hạng toán tử được tách F(r^k) = [F(r^k) − F(r^{k−1})] + F(r^{k−1}), và phần F(r^{k−1}) được chặn bằng bất đẳng thức chiếu của bước trước, tức đặc trưng của x^k = P_D(x^{k−1} − λF(r^{k−1})):

    ⟨x^{k−1} − λF(r^{k−1}) − x^k, y − x^k⟩ ≤ 0   với mọi y thuộc D.        (P)

Điểm cần chú ý: trong (P), toán tử xuất hiện dưới dạng λF(r^{k−1}), tức đã nhân sẵn với λ; không có phép chia cho λ ở bất kỳ đâu.

Trong sơ đồ chiếu xấp xỉ, đặc trưng (P) chỉ đúng cho phép chiếu chính xác x̄^k, không cho điểm thực x^k = x̄^k + e^{k−1}. Vậy bất đẳng thức đúng là

    ⟨x^{k−1} − λF(r^{k−1}) − x̄^k, y − x̄^k⟩ ≤ 0.        (P')

Đặt A = x^{k−1} − λF(r^{k−1}) − x̄^k. Thay x̄^k = x^k − e^{k−1} vào (P'), tức A = (x^{k−1} − λF(r^{k−1}) − x^k) + e^{k−1} và y − x̄^k = (y − x^k) + e^{k−1}:

    ⟨A_0 + e^{k−1}, (y − x^k) + e^{k−1}⟩ ≤ 0,   với A_0 = x^{k−1} − λF(r^{k−1}) − x^k.

Khai triển:

    ⟨A_0, y − x^k⟩ ≤ − ⟨A_0, e^{k−1}⟩ − ⟨e^{k−1}, y − x^k⟩ − ‖e^{k−1}‖².

Vế trái ⟨A_0, y − x^k⟩ là chính số hạng mà Malitsky dùng cho bản chiếu chính xác. Ba số hạng bên phải là nhiễu. Tính từng cái, với A_0 = −(x^k − x^{k−1}) − λF(r^{k−1}):

    − ⟨A_0, e^{k−1}⟩ = ⟨x^k − x^{k−1}, e^{k−1}⟩ + λ⟨F(r^{k−1}), e^{k−1}⟩ .

Do đó, tổng nhiễu ν_k, sau khi nhân với thừa số 2 mà công thức (11) mang theo, bị chặn bởi

    ν_k ≤ 2\bigl| ⟨x^k − x^{k−1}, e^{k−1}⟩ \bigr|
        + 2λ\bigl| ⟨F(r^{k−1}), e^{k−1}⟩ \bigr|
        + 2\bigl| ⟨e^{k−1}, y − x^k⟩ \bigr|
        + 2‖e^{k−1}‖² .

Chặn từng số hạng bằng Cauchy-Schwarz và ‖e^{k−1}‖ ≤ ε_{k−1}, dùng tính bị chặn của quỹ đạo (đặt M = sup_k ‖x^k − x^{k−1}‖, M_F = sup_k ‖F(r^k)‖, M' = sup ‖y − x^k‖ với y là điểm được chọn trong (11), tất cả hữu hạn vì dãy bị chặn):

    ν_k ≤ 2M ε_{k−1} + 2λ M_F ε_{k−1} + 2M' ε_{k−1} + 2ε_{k−1}²
        = \bigl( 2M + 2λ M_F + 2M' + 2ε_{k−1} \bigr) ε_{k−1}
        ≤ \bigl( 2M + 2λ M_F + 2M' + 2ε_0 \bigr) ε_{k−1}
        =: C ε_{k−1} ,

trong đó dùng ε_{k−1} ≤ ε_0 để C là hằng số cố định, độc lập với chỉ số k.

## 7ter. Câu trả lời, và hệ quả cho định vị bài

Hằng số C = 2M + 2λ M_F + 2M' + 2ε_0 KHÔNG chứa nghịch đảo bước nhảy. Ngược lại, bước nhảy λ xuất hiện ở một số hạng dưới dạng thừa số NHÂN, tức làm số hạng đó nhỏ đi khi λ nhỏ, chứ không phóng đại. Lý do có tính cấu trúc: trong bất đẳng thức chiếu (P), toán tử đã đi kèm sẵn thừa số λ, nên khi sai số điểm gốc e^{k−1} tương tác với số hạng toán tử, nó nhận thừa số λ chứ không phải 1/λ.

Đây là câu trả lời trung thực, và nó đóng lại hy vọng về một điểm phân biệt lý thuyết ở chỗ này. Khẳng định ban đầu của tôi rằng sai số điểm gốc bị khuếch đại bởi 1/λ là sai; phản biện nghi ngờ đúng. Vì hằng số chỉ là O(M, M_F, M') và bị chặn khi λ nằm trong khoảng cho phép, số hạng nhiễu điểm gốc không có gì đặc biệt hơn nhiễu điểm cuối: cả hai đều bậc nhất theo sai số và tổng được.

Hệ quả cho định vị: định lý hội tụ của bài là một MỞ RỘNG, đúng như đã thừa nhận trong ghi chú định vị của bản thảo. Việc thêm phản xạ vào khung chiếu xấp xỉ không tạo ra một số hạng nhiễu mới về bản chất; nó chỉ là kiểm rằng cơ chế bền vững với nhiễu vẫn chạy qua bước phản xạ, điều mà bây giờ ta đã kiểm và thấy đúng. Do đó bài KHÔNG có đóng góp lý thuyết đủ mới để nhắm Q1 ở phần định lý.

Điều này KHÔNG làm bài mất giá trị, mà xác định đúng giá trị của nó. Đóng góp bán được nằm ở nơi bản thảo đã đặt: chứng chỉ sai số tính được qua khoảng cách đối ngẫu, ngân sách thích nghi, và phân tích chi phí kèm thực nghiệm. Đó là đóng góp thực nghiệm và thuật toán, phù hợp một bài Q2, và nó không phụ thuộc vào việc định lý có mới hay không. Kết luận: theo đúng con đường Q2 đã chọn, và không cố nâng lên Q1 bằng phần định lý, vì phần đó đã được chứng minh là mở rộng chứ không phải cơ chế mới.

## 8. Kết quả phản biện, đã tích hợp

Ba tác nhân phản biện độc lập tự tính lại từng phép đại số. Kết quả:

Mục 1 đến 3, trường hợp chiếu chính xác: cả ba xác nhận đúng hoàn toàn, không lỗi dấu, hệ số hay chỉ số. Đẳng thức then chốt c2 − λL = c1 và bước ghép thế năng được kiểm từng số hạng. Đây là lần đầu một khối của chứng minh đứng vững trước phản biện; phần này coi như khép kín.

Mục 4, đường nhiễu thứ nhất qua khai triển bình phương: xác nhận đúng đến từng hệ số, kể cả hệ số (1 + λL) của ε_k².

Hai lỗi đã sửa ở mục 4, cả hai do phản biện chỉ ra và đều đúng:

- Mâu thuẫn nội tại ở mục 1: câu cũ nói bổ đề áp đúng bất kể điểm gốc có phải phép chiếu hay không, mâu thuẫn với việc mục 4 dựa vào phụ thuộc phép chiếu bước trước. Đã sửa mục 1 để phân biệt rõ hai vai trò của phép chiếu.
- Khẳng định hệ số 1/λ ở đường nhiễu thứ hai là nói quá: hệ số đó có thể triệt tiêu do bị nhân lại với thừa số λ trên số hạng toán tử. Đã hạ xuống ν_k ≤ Cε_{k−1} và ghi rõ việc xác định C có chứa 1/λ hay không là để cho bước viết đầy đủ; đây cũng là chỗ quyết định bài có điểm phân biệt hay chỉ là hợp nhất.

Chỗ còn phải viết đầy đủ, thu hẹp lại: hằng số C ở ν_k, phát biểu chính xác bổ đề tựa Fejér loại nhân tính ở mục 5, và bước Minty cùng Opial ở mục 6 cho không gian vô hạn chiều. Trong không gian hữu hạn chiều của phần thực nghiệm, hai mục cuối là thường quy.
