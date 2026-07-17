# Chứng minh hội tụ yếu cho phương pháp chiếu phản xạ với phép chiếu xấp xỉ

Cảnh báo, thêm sau vòng phản biện. Bốn bổ đề ở mục 3 và 4 đã được kiểm từng dòng và đều đúng, nhưng mục 5 dựng trên một câu sai và lập luận tính mới ở mục 0 là ngụy biện. Đọc mục 8 trước khi dùng bất cứ phần nào của mục 0 và mục 5.

## 0. Vì sao chọn bài toán này

Bản thảo ở tệp 03 nhắm hội tụ mạnh cho sơ đồ bốn pha và đã sụp: bổ đề một bước của Malitsky đòi một chuỗi phép chiếu liền mạch, trong đó điểm gốc của bước sau chính là đầu ra phép chiếu của bước trước, mà bước quán tính và bước neo cắt đứt chuỗi đó.

Tài liệu này chọn bài toán khác, khả thi hơn hẳn, bằng cách bỏ cả hai thứ gây đứt chuỗi:

- Bỏ bước quán tính. Số liệu đã xác nhận bỏ nó không mất gì (24,3458 dB ở cả hai phiên bản), và tài liệu cho thấy phản xạ cộng quán tính đã có người làm (Journal of Scientific Computing 2022).
- Bỏ bước neo. Khi đó điểm lặp tiếp theo chính là đầu ra phép chiếu, chuỗi liền mạch trở lại. Cái giá là chỉ còn hội tụ yếu thay vì hội tụ mạnh; nhưng với toán tử đơn điệu, hội tụ yếu là kết quả chuẩn của dòng này, đúng như Malitsky 2015.

Tính mới được giữ nhờ chỗ khác: phép chiếu xấp xỉ dùng tiêu chuẩn sai số tương đối, nên sai số phụ thuộc trạng thái và không rút gọn về một dãy nhiễu ngoài cho trước. Nhờ đó định lý không phải hệ quả trực tiếp của định lý bền vững với nhiễu.

Trạng thái: đây là bản thảo do trợ lý soạn, cần người hướng dẫn và người phản biện kiểm từng dòng. Các chỗ cần soi kỹ được đánh dấu.

## 1. Bài toán, sơ đồ và giả thiết

Bài toán: tìm x* thuộc D sao cho ⟨F(x*), x − x*⟩ ≥ 0 với mọi x thuộc D. Tập nghiệm ký hiệu S.

Sơ đồ, với x⁰ và x⁻¹ cho trước trong D:

    rᵏ = 2xᵏ − xᵏ⁻¹                              (điểm phản xạ)
    xᵏ⁺¹ = P_D^{εₖ}( xᵏ − λ F(rᵏ) )              (chiếu xấp xỉ, sai số εₖ)

Ký hiệu điểm chiếu chính xác lý tưởng x̄ᵏ⁺¹ = P_D(xᵏ − λ F(rᵏ)), nên ‖xᵏ⁺¹ − x̄ᵏ⁺¹‖ ≤ εₖ.

Giả thiết.

- A1: D lồi đóng khác rỗng, S khác rỗng.
- A2: F đơn điệu trên H và liên tục Lipschitz với hằng số L trên H. Lưu ý phải là trên H chứ không chỉ trên D, vì điểm phản xạ rᵏ nói chung nằm ngoài D. Trong ứng dụng khôi phục ảnh, F(x) = Bᵀ(Bx − y) đơn điệu và Lipschitz trên toàn H nên giả thiết thỏa.
- A3: λ thuộc khoảng (0, (√2 − 1)/L).
- A4: phép chiếu xấp xỉ trả về điểm KHẢ THI, tức xᵏ thuộc D với mọi k. Cài đặt hiện tại thỏa giả thiết này vì thủ tục chiếu ép khả thi trước khi trả về, và số liệu xác nhận mức vi phạm ràng buộc bằng 1,0000 ở toàn bộ cấu hình. Giả thiết này quan trọng: nó cho phép dùng ⟨F(z), xᵏ − z⟩ ≥ 0 với z thuộc S.
- A5: dãy sai số thỏa tổng các εₖ hữu hạn. Mục 5 bàn cách bảo đảm điều này bằng tiêu chuẩn tương đối.

## 2. Công cụ

Bổ đề B1 (đặc trưng phép chiếu). Với v thuộc H và z thuộc D: ⟨v − P_D(v), z − P_D(v)⟩ ≤ 0.

Bổ đề B2 (đẳng thức phân cực). 2⟨a, b⟩ = ‖a‖² + ‖b‖² − ‖a − b‖².

Bổ đề B3 (tựa Fejér, Combettes 2001). Nếu {sₖ} không âm và sₖ₊₁ ≤ sₖ + δₖ với tổng các δₖ hữu hạn, thì {sₖ} hội tụ.

Bổ đề B4 (Opial). Trong không gian Hilbert, nếu {xᵏ} bị chặn, mọi điểm tụ yếu của nó thuộc S, và ‖xᵏ − z‖ hội tụ với mọi z thuộc S, thì {xᵏ} hội tụ yếu về một phần tử của S.

## 3. Bổ đề một bước, dẫn từ đầu

Đây là phần thay cho việc mượn nguyên bổ đề của Malitsky; bản thảo trước sụp đúng vì mượn nguyên khối.

Bổ đề 1 (bất đẳng thức cơ bản của bước chiếu). Với mọi z thuộc D:

    ‖x̄ᵏ⁺¹ − z‖² ≤ ‖xᵏ − z‖² − ‖xᵏ − x̄ᵏ⁺¹‖² + 2λ ⟨F(rᵏ), z − x̄ᵏ⁺¹⟩.

Chứng minh. Áp Bổ đề B1 cho v = xᵏ − λF(rᵏ), điểm chiếu x̄ᵏ⁺¹ và z thuộc D:

    ⟨xᵏ − λF(rᵏ) − x̄ᵏ⁺¹, z − x̄ᵏ⁺¹⟩ ≤ 0,
    tức ⟨xᵏ − x̄ᵏ⁺¹, z − x̄ᵏ⁺¹⟩ ≤ λ ⟨F(rᵏ), z − x̄ᵏ⁺¹⟩.

Áp Bổ đề B2 cho vế trái với a = xᵏ − x̄ᵏ⁺¹ và b = z − x̄ᵏ⁺¹:

    2⟨xᵏ − x̄ᵏ⁺¹, z − x̄ᵏ⁺¹⟩ = ‖xᵏ − x̄ᵏ⁺¹‖² + ‖z − x̄ᵏ⁺¹‖² − ‖xᵏ − z‖².

Thay vào và chuyển vế được điều phải chứng minh. Đây là bước thường quy.

Bổ đề 2 (xử lý số hạng toán tử bằng tính đơn điệu). Với z thuộc S:

    2λ ⟨F(rᵏ), z − x̄ᵏ⁺¹⟩ ≤ 2λ ⟨F(z), z − rᵏ⟩ + 2λ ⟨F(rᵏ), rᵏ − x̄ᵏ⁺¹⟩.

Chứng minh. Tách ⟨F(rᵏ), z − x̄ᵏ⁺¹⟩ = ⟨F(rᵏ), z − rᵏ⟩ + ⟨F(rᵏ), rᵏ − x̄ᵏ⁺¹⟩. Với số hạng đầu, dùng tính đơn điệu của F tại cặp (rᵏ, z): ⟨F(rᵏ) − F(z), rᵏ − z⟩ ≥ 0, tức ⟨F(rᵏ), z − rᵏ⟩ ≤ ⟨F(z), z − rᵏ⟩. Đây là chỗ duy nhất dùng tính đơn điệu, và nó cần F đơn điệu tại một cặp mà rᵏ nằm ngoài D, nên giả thiết A2 phải phát biểu trên H.

Bổ đề 3 (telescoping số hạng nghiệm). Đặt aₖ = ⟨F(z), z − xᵏ⟩. Vì z thuộc S và xᵏ thuộc D theo giả thiết A4, ta có aₖ ≤ 0. Hơn nữa, do rᵏ = 2xᵏ − xᵏ⁻¹,

    ⟨F(z), z − rᵏ⟩ = 2aₖ − aₖ₋₁.

Chứng minh. ⟨F(z), z − 2xᵏ + xᵏ⁻¹⟩ = 2⟨F(z), z − xᵏ⟩ − ⟨F(z), z − xᵏ⁻¹⟩ = 2aₖ − aₖ₋₁, dùng z − 2xᵏ + xᵏ⁻¹ = 2(z − xᵏ) − (z − xᵏ⁻¹).

Nhận xét quan trọng về vai trò của giả thiết A4. Nếu phép chiếu xấp xỉ trả về điểm không khả thi thì aₖ ≤ 0 không còn đúng và toàn bộ telescoping mất dấu. Đây là lý do thủ tục chiếu phải ép khả thi, và là chỗ mà thiết kế cài đặt gặp lý thuyết: mức vi phạm bằng 1,0000 trong thực nghiệm không phải chi tiết kỹ thuật mà là điều kiện của định lý.

Cần kiểm: bước ghép ba bổ đề trên thành một đại lượng Lyapunov giảm, tức chỗ Malitsky dùng để thu hệ số 1 − λL(1 + √2) và 1 − √2λL. Cụ thể phải ước lượng ⟨F(rᵏ), rᵏ − x̄ᵏ⁺¹⟩ qua tính Lipschitz và tách rᵏ − x̄ᵏ⁺¹ = (xᵏ − x̄ᵏ⁺¹) + (xᵏ − xᵏ⁻¹), rồi gộp 2λ(2aₖ − aₖ₋₁) vào một hàm thế năng dạng φₖ = ‖xᵏ − z‖² − 2λaₖ₋₁ + (số hạng bình phương). Đây là phần kỹ thuật nặng nhất và chưa được viết đầy đủ ở đây.

## 4. Nhiễu do phép chiếu xấp xỉ

Bổ đề 4 (nhiễu đều). Với mọi z:

    ‖xᵏ⁺¹ − z‖ ≤ ‖x̄ᵏ⁺¹ − z‖ + εₖ,
    ‖xᵏ⁺¹ − z‖² ≤ ‖x̄ᵏ⁺¹ − z‖² + 2εₖ‖x̄ᵏ⁺¹ − z‖ + εₖ².

Chứng minh: bất đẳng thức tam giác và khai triển bình phương, dùng ‖xᵏ⁺¹ − x̄ᵏ⁺¹‖ ≤ εₖ.

Điểm mấu chốt so với bản thảo trước: ở đây nhiễu là ĐỀU, bị chặn bởi εₖ và không phụ thuộc trạng thái ở số hạng bậc nhất khi dãy bị chặn. Bản thảo trước vấp phải nhiễu phụ thuộc trạng thái vì đã tách sai chỗ.

Cần kiểm: bổ đề một bước của Malitsky đòi điểm gốc xᵏ là đầu ra phép chiếu CHÍNH XÁC của bước trước, trong khi ở đây xᵏ là đầu ra phép chiếu XẤP XỈ, tức xᵏ = x̄ᵏ + eᵏ⁻¹ với ‖eᵏ⁻¹‖ ≤ εₖ₋₁. Do đó khi dẫn bổ đề một bước phải mang theo tường minh nhiễu này ở điểm gốc, sinh thêm các số hạng chéo bậc nhất theo εₖ₋₁ nhân với các đại lượng bị chặn. Vì dãy sai số tổng được, các số hạng này tổng được và bị hấp thụ vào Bổ đề B3. Đây là chỗ khác biệt thực chất so với chứng minh gốc và phải viết đầy đủ; đây cũng là phần công việc mới của bài, không mượn được.

## 5. Tiêu chuẩn sai số tương đối và tính tổng được

Thay vì áp một lịch sai số cho trước, đặt

    εₖ = c · dₖ₋₁,  với dₖ = ‖x̄ᵏ⁺¹ − xᵏ‖ là dịch chuyển của bước chiếu,

và c dương đủ nhỏ. Đây là tiêu chuẩn tương đối: sai số cho phép tỉ lệ với mức dịch chuyển mà bước chiếu tạo ra, nên tự nới khi còn xa nghiệm và tự siết khi đã gần.

Vì sao chọn dịch chuyển của bước chiếu chứ không phải dịch chuyển của dãy lặp: trong sơ đồ có neo, dịch chuyển của dãy lặp chứa số hạng neo cỡ βₖ, mà tổng các βₖ phân kỳ theo đúng điều kiện của phương pháp neo; chọn nó sẽ làm dãy sai số không tổng được. Dịch chuyển của bước chiếu không chứa số hạng đó. Ở sơ đồ không neo của tài liệu này hai đại lượng trùng nhau, nhưng ghi lại vì nó quyết định khi mở rộng sang trường hợp có neo.

Điều cần chứng minh: tổng các dₖ hữu hạn, khi đó tổng các εₖ hữu hạn và giả thiết A5 thỏa.

Bằng chứng số hiện có, chưa phải chứng minh. Lượt đo dài với 3000 bước ngoài trên GPU cho kết quả quyết định, và nó khác hẳn lượt ngắn:

| cấu hình | độ dốc log-log của dịch chuyển bước chiếu | tổng tích lũy, nửa quãng và cuối | kết luận |
|---|---|---|---|
| có neo, mờ chuyển động | −1,011 | 13,9732 và 14,2359 | sát ngưỡng, không dựa được |
| tắt neo, mờ Gauss | −2,342 | 11,7212 và 11,7973 | tổng được rõ ràng |
| tắt neo, mờ chuyển động | −2,838 | 12,7002 và 12,7033 | tổng được rõ ràng |

Điểm quan trọng nhất: khi có neo, độ dốc tụt về −1,011, tức sát ngưỡng phân kỳ. Ở lượt ngắn 600 bước, độ dốc đo được là −1,479 và trông an toàn; phải chạy tới 3000 bước mới lộ ra rằng nó đang tiến về −1. Đây đúng là lo ngại ban đầu: bước neo áp đặt dịch chuyển cỡ nghịch đảo số bước, mà chuỗi đó phân kỳ. Bài học: đừng kết luận tính tổng được từ quỹ đạo ngắn.

Ngược lại, khi tắt neo, tức đúng sơ đồ của tài liệu này, độ dốc là −2,3 đến −2,8 và tổng bão hòa dứt khoát, tỉ lệ 1,000 đến 1,006. Tổng được ở đây là thật.

Hệ quả cho thiết kế: quyết định bỏ bước neo đúng ở cả hai mặt cùng lúc. Nó vừa nối lại chuỗi phép chiếu để bổ đề một bước dùng được, vừa cứu chính tính tổng được. Nếu giữ neo, giả thiết tổng được sẽ nằm ngay ranh giới phân kỳ và không thể dựa vào. Đây là lập luận nên đưa vào bài để biện minh cho việc chọn sơ đồ không neo, thay vì để người phản biện hỏi tại sao không nhắm hội tụ mạnh.

Hướng chứng minh dự kiến: từ bổ đề một bước, sau khi ghép Lyapunov, thu được bất đẳng thức dạng φₖ₊₁ ≤ φₖ − c′ dₖ² + (số hạng nhiễu tổng được). Cộng dồn cho tổng các dₖ² hữu hạn. Từ tổng bình phương hữu hạn KHÔNG suy ra ngay tổng dₖ hữu hạn; cần thêm lập luận, ví dụ một điều kiện chặn sai số quanh tập nghiệm, hoặc thay tiêu chuẩn thành εₖ = c·dₖ₋₁² hay εₖ = c·dₖ₋₁·γₖ với dãy γₖ tổng được. Cần kiểm: đây là mắt xích còn thiếu và là chỗ quan trọng nhất cần người hướng dẫn quyết định.

Nhận xét về tính mới: nếu chọn εₖ = c·dₖ₋₁·γₖ với γₖ tổng được cho trước, dãy sai số vẫn phụ thuộc trạng thái qua dₖ₋₁, nên không rút gọn về một dãy nhiễu ngoài cho trước, và định lý không phải hệ quả của định lý bền vững. Đây là cách giữ tính mới mà vẫn có tính tổng được gần như hiển nhiên, vì dₖ bị chặn. Đây có thể là lối thoát sạch nhất và nên thử trước.

## 6. Định lý và đường chứng minh

Định lý (dự kiến). Dưới các giả thiết A1 đến A5, dãy {xᵏ} sinh bởi sơ đồ hội tụ yếu về một phần tử của S.

Đường chứng minh: (i) từ bổ đề một bước có nhiễu, thu bất đẳng thức tựa Fejér φₖ₊₁ ≤ φₖ + δₖ với tổng các δₖ hữu hạn; (ii) Bổ đề B3 cho φₖ hội tụ, suy ra {xᵏ} bị chặn và ‖xᵏ − z‖ hội tụ với mọi z thuộc S; (iii) từ phần âm của bất đẳng thức, suy ra dịch chuyển tiến về không, do đó rᵏ − xᵏ tiến về không; (iv) mọi điểm tụ yếu thuộc S, dùng đặc trưng phép chiếu, tính Lipschitz và tính đơn điệu qua bổ đề Minty; (v) Bổ đề B4 kết thúc.

## 7. Trạng thái trung thực và việc cần làm

Đã viết đầy đủ và tin được: Bổ đề 1, 2, 3, 4 (các bước thường quy, dẫn từ đầu, không mượn nguyên khối), cùng nhận xét rằng giả thiết khả thi A4 là điều kiện thật của định lý chứ không phải chi tiết cài đặt.

Chưa viết đầy đủ, cần người hướng dẫn:

1. Ghép Lyapunov để thu các hệ số của Malitsky, có mang theo nhiễu ở điểm gốc. Đây là phần kỹ thuật nặng nhất.
2. Mắt xích từ tổng bình phương dịch chuyển hữu hạn sang tổng dịch chuyển hữu hạn, hoặc chọn dạng tiêu chuẩn tương đối tránh được mắt xích này (xem đề xuất εₖ = c·dₖ₋₁·γₖ ở mục 5).
3. Bước chuyển giới hạn yếu ở phần (iv).

Điều đã đạt so với bản thảo trước: bài toán được thu về một sơ đồ hai dòng với chuỗi phép chiếu liền mạch, thay vì sơ đồ bốn pha bị cắt đứt chuỗi ở hai chỗ. Đây là lý do bản này có cơ hội khép lại, còn bản trước thì không.

## 8. Biên bản phản biện và hướng đi đã được xác định lại

Vòng phản biện bốn tác nhân độc lập cho kết quả vừa khẳng định vừa bác. Ghi đầy đủ vì đây là chỉ dẫn kỹ thuật quan trọng nhất mà dự án nhận được.

### 8.1. Những gì đã được xác nhận là đúng

Bổ đề 1, 2, 3, 4 đều đúng, kiểm từng dấu và từng hệ số. Cụ thể: Bổ đề 1 đúng cả dấu lẫn hệ số 2λ; Bổ đề 2 dùng tính đơn điệu đúng một chỗ và giả thiết A2 trên toàn không gian là đúng chỗ, không dư không thiếu, giống hệt lý do Malitsky cũng đòi đơn điệu trên toàn không gian; Bổ đề 3 đúng về đại số.

Quan trọng nhất, phản biện xác nhận trực giác cốt lõi: giả thiết khả thi thật sự cứu đúng chỗ mà bản thảo ở tệp 03 chết. Lý do có tính cấu trúc: số hạng telescoping chỉ đụng các điểm nằm trong tập ràng buộc, không đụng điểm phản xạ nằm ngoài. Ở tệp 03, điểm quán tính nằm ngoài tập ràng buộc nên mất dấu và toàn bộ sụp.

Ngoài ra, hàm thế năng dự đoán ở mục 3 trùng khớp với năng lượng thật của Malitsky, và điều kiện bước nhảy A3 khớp đúng chặn của ông. Lộ trình là đúng hướng.

### 8.2. Lỗi mức chặn thứ nhất: lập luận tính mới là ngụy biện

Mục 0 và mục 5 khẳng định rằng vì sai số phụ thuộc trạng thái nên định lý không phải hệ quả của định lý bền vững với nhiễu. Đây là ngụy biện. Định lý bền vững chỉ đòi tổng sai số hữu hạn dọc quỹ đạo thực sự sinh ra; nó không quan tâm sai số được chọn trước hay chọn thích nghi. Vì dịch chuyển bị chặn bởi một hằng số, sai số bị trầm bởi một dãy tổng được cho trước, nên định lý vẫn là hệ quả trực tiếp.

Hệ quả: đề xuất đặt sai số bằng tích của dịch chuyển với một dãy tổng được, vốn được gọi ở mục 5 là lối thoát sạch nhất, thực ra là lối thoát ra khỏi chính tính mới.

Thêm vào đó, bài Díaz Millán, Ferreira và Ugon (Computational Optimization and Applications, 2024) đã làm đúng hai thành phần được gọi là mới ở đây: phép chiếu xấp xỉ khả thi và tiêu chuẩn sai số tương đối, cho lớp toán tử còn rộng hơn.

### 8.3. Lỗi mức chặn thứ hai: tiêu chuẩn ở mục 5 không tính được, và một câu sai hẳn

Đại lượng dịch chuyển của bước chiếu được định nghĩa qua điểm chiếu chính xác, tức chính thứ mà theo giả thiết ta không tính được. Nên tiêu chuẩn ở mục 5 không kiểm tra được, nó là một điều kiện ẩn.

Nặng hơn, câu ở mục 5 nói rằng ở sơ đồ không neo, dịch chuyển của bước chiếu và dịch chuyển của dãy lặp trùng nhau là sai: chúng lệch nhau đúng bằng sai số chiếu, và chỉ trùng khi phép chiếu chính xác, tức đúng trường hợp bị loại trừ. Toàn bộ mục 5 dựng trên câu sai này.

### 8.4. Lỗi mức chặn thứ ba, và đây là chẩn đoán kiến trúc quan trọng nhất

Mô hình sai số kiểu quả cầu ở Bổ đề 4 đúng nhưng đặt sai chỗ, và chính nó ép ra giả thiết tổng được. Lý do: bất đẳng thức tam giác đưa nhiễu vào ở bậc nhất, nhân với một đại lượng cỡ hằng số, trong khi phần âm duy nhất để hấp thụ lại ở bậc hai theo dịch chuyển. Bậc nhất không bị bậc hai nuốt, nên buộc phải giả thiết tổng sai số hữu hạn, và đó là lý do tính mới chết.

Cách đúng, theo đúng cách Díaz Millán định nghĩa: dùng phép chiếu xấp xỉ khả thi qua bất đẳng thức chiếu nới lỏng, trong đó điểm trả về nằm trong tập ràng buộc và thỏa bất đẳng thức đặc trưng với một sai số bậc hai theo dịch chuyển. Khi đó sai số vào chứng minh ở bậc hai, hấp thụ được thẳng, và cho phép dung sai tương đối là một hằng số nhỏ hơn một nửa thay vì một dãy tiến về không. Bổ đề 2 và 3 sống nguyên vẹn vì chúng không dùng điểm chiếu chính xác ở chỗ nào không thay được.

Hai cảnh báo đi kèm: dung sai này trừ trực tiếp vào lề an toàn của điều kiện bước nhảy, nên A3 phải siết lại; và việc chuyển từ chứng chỉ qua khoảng cách đối ngẫu sang tiêu chuẩn nới lỏng không tự động, vì quả cầu biến phân toàn phần không bị chặn trong không gian nền (mọi ảnh hằng có biến phân toàn phần bằng không), nên cận trên theo mọi điểm của tập ràng buộc không tầm thường. Phải kiểm bộ giải nội có xuất được trực tiếp bất đẳng thức nới lỏng hay không.

### 8.5. Lỗi mức nặng về cơ chế

Phác thảo ghép Lyapunov ở mục 3 sai cơ chế: tính Lipschitz không chặn được chuẩn của toán tử, nó chỉ chặn hiệu hai giá trị. Malitsky không làm như vậy; ông lấy hiệu giữa hai giá trị toán tử ở hai bước liên tiếp để ra bậc hai, rồi xử lý phần còn lại bằng bất đẳng thức chiếu của bước trước. Đây chính là chuỗi phép chiếu liền mạch đã nói ở mục 0 nhưng bị quên ở mục 3.

Hệ quả dây chuyền: khi điểm gốc là đầu ra chiếu xấp xỉ chứ không phải chiếu chính xác, số hạng chéo đi kèm hệ số nghịch đảo bước nhảy, vì bất đẳng thức chiếu chia cho bước nhảy. Với bước nhảy nhỏ, đây là hệ số lớn, không phải nhiễu vô hại như mục 4 gợi ý.

Ngoài ra, bước suy từ hàm thế năng hội tụ sang khoảng cách tới nghiệm hội tụ ở mục 6 là ngụy biện, vì hàm thế năng có ba thành phần không âm. Tin tốt: phản biện chỉ ra cả hai mắt xích còn thiếu đều ra được, và giả thiết khả thi còn cho thêm một món nữa chưa được khai thác — tổng các giá trị đó hữu hạn, không chỉ dấu.

### 8.6. Tính mới thật nằm ở đâu

Không phải ở phép chiếu xấp xỉ với tiêu chuẩn tương đối, vì Díaz Millán đã làm. Cũng không phải ở lập luận không rút gọn về nhiễu ngoài, vì lập luận đó sai.

Cái chưa ai làm là: phép chiếu xấp xỉ khả thi trên sơ đồ phản xạ, nơi điểm gốc vừa là đầu ra phép chiếu xấp xỉ của bước trước vừa sinh ra điểm phản xạ để đánh giá toán tử bên ngoài tập ràng buộc. Do đó sai số ở điểm gốc bị khuếch đại hệ số hai bởi bước phản xạ, và đi vào chứng minh qua bất đẳng thức chiếu của bước trước với hệ số nghịch đảo bước nhảy. Đây đúng là chỗ mục 4 tự đánh dấu là cần kiểm rồi bỏ qua.

Kết luận của phản biện, viết nguyên ý: viết chỗ đó, đừng quảng cáo chỗ khác.

### 8.7. Việc cần làm, theo thứ tự

1. Thay mô hình sai số quả cầu ở Bổ đề 4 bằng bất đẳng thức chiếu nới lỏng kiểu Díaz Millán, để sai số vào ở bậc hai. Xóa mục 5 và giả thiết A5.
2. Kiểm bộ giải nội có xuất được trực tiếp bất đẳng thức nới lỏng không, lưu ý quả cầu biến phân toàn phần không bị chặn.
3. Siết lại điều kiện bước nhảy A3 để chừa lề cho dung sai.
4. Viết đầy đủ phần khuếch đại sai số gốc qua bước phản xạ với hệ số nghịch đảo bước nhảy. Đây là đóng góp thật của bài.
5. Vá hai mắt xích ở mục 6.
