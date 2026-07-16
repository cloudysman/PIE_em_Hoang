# PIE-Net — mạng chiếu xấp xỉ giả đơn điệu cho bài toán ngược trong xử lý ảnh

Mã nguồn, thực nghiệm và tài liệu của đề tài "Mạng cân bằng chiếu xấp xỉ giả đơn điệu cho bài toán ngược trong xử lý ảnh". Bài toán ngược y = Bx + ε được đặt dưới dạng bất đẳng thức biến phân trên một tập ràng buộc, và giải bằng một sơ đồ chiếu có quán tính và độ nhớt.

Kho này gồm hai giai đoạn: giai đoạn thực nghiệm ban đầu, đã kết thúc với kết quả âm tính được ghi nhận đầy đủ; và giai đoạn lý thuyết hiện tại, tập trung vào tính chất hội tụ và chi phí của bản thân sơ đồ lặp.

## Trạng thái và kết quả trung thực

Giai đoạn thực nghiệm kiểm bốn khẳng định của thiết kế ban đầu qua năm thí nghiệm, mỗi thí nghiệm có tiêu chí đạt hay không đạt đặt trước khi chạy. Kết quả: chỉ một khẳng định đạt.

- Hệ số vô hướng học được không cải thiện chất lượng khôi phục so với hệ số hằng được tinh chỉnh tốt (28,31 so với 28,91 dB), và tự hội tụ về hằng số xấp xỉ 1. Điều này có tính cấu trúc: một vô hướng dương nhân với toán tử không làm thay đổi tập nghiệm của bất đẳng thức biến phân.
- Thành phần học được không vượt phiên bản không học trên quả cầu biến phân toàn phần, kể cả sau khi được cho điều kiện huấn luyện tốt hơn.
- Ràng buộc cứng nhất quán dữ liệu thua phương pháp Plug-and-Play ở cả hai chế độ (thua 0,59 dB khi khớp mức nhiễu và 0,88 dB khi lệch), vì ép nghiệm bám quả cầu quanh dữ liệu quan sát chính là nạp nhiễu trở lại.
- Khẳng định duy nhất đứng vững là lợi thế chi phí của phép chiếu xấp xỉ có khởi tạo ấm.

Vì các kết quả âm tính có tính cấu trúc chứ không do lỗi cài đặt hay thiếu tinh chỉnh, hướng thực nghiệm đã được đóng lại. Trọng tâm chuyển sang một đóng góp lý thuyết về sơ đồ lặp, trong đó mã nguồn đóng vai trò minh họa số. Chi tiết trong `Bao_cao_thuc_nghiem_PIE-Net.docx` và thư mục `tai_lieu_bai_bao/`.

Lưu ý về một khẳng định đã được sửa: các phiên bản trước của tài liệu này nói phần dư biến phân tiến về không. Số liệu chỉ chứng minh phần dư giảm từ 2,48 xuống 0,199 qua 200 bước và giảm không đơn điệu, nên khẳng định cũ vượt quá điều số liệu cho phép và đã được gỡ.

## Cấu trúc mã nguồn

Phần lý thuyết, dùng cho hướng hiện tại:

| Tệp | Nội dung |
|---|---|
| `pie_net/constraints.py` | Phép chiếu lên quả cầu biến phân toàn phần bằng Chambolle-Pock, khởi tạo ấm qua biến đối ngẫu, đếm bước nội. Có chế độ lịch bước tăng tốc khai thác tính lồi mạnh của bài toán chiếu. |
| `pie_net/reflected_solver.py` | Sơ đồ phản xạ với phép chiếu xấp xỉ: bước phản xạ kiểu Malitsky (toán tử chỉ tính một lần mỗi bước ngoài), độ nhớt, và bốn chế độ ngân sách bước nội. Đo sai số chiếu và phần dư biến phân tách khỏi chi phí thuật toán. |
| `theory_test_reflected.py` | Chạy lưới cấu hình theo loại mờ và chế độ ngân sách, ghi vết đầy đủ. |
| `theory_test_pseudomono.py` | Ví dụ giả đơn điệu nhưng không đơn điệu, kèm chứng chỉ số. |
| `analyze_theory.py` | Tính độ dốc, tính tổng được của sai số chiếu, và bảng chi phí. |
| `tests/` | Kiểm thử các tính chất toán học cốt lõi. |

Phần thực nghiệm ban đầu, giữ lại làm hồ sơ:

| Tệp | Nội dung |
|---|---|
| `pie_net/operators.py` | Toán tử chi phí dạng tích của một vô hướng dương học được với một toán tử đơn điệu. |
| `pie_net/solver.py`, `pie_net/tv_solver.py` | Sơ đồ bốn pha: quán tính, chiếu xấp xỉ, hiệu chỉnh kiểu Tseng, trộn độ nhớt. Lưu ý pha thứ ba là hiệu chỉnh kiểu Tseng, không phải bước phản xạ; các tài liệu trước gọi sai tên. |
| `run_experiment.py`, `quick_test_tv.py`, `milestone_test.py`, `steelman_m2.py`, `pivot_decisive_test.py`, `pivot_pnp_test.py` | Năm thí nghiệm của báo cáo. |

## Cách chạy

Yêu cầu: torch, numpy, scikit-image, matplotlib.

Phần lý thuyết:

```bash
python theory_test_reflected.py --K 150 --size 64 --measure_every 5   # lưới đầy đủ
python theory_test_reflected.py --alpha_bar 0                         # tắt quán tính
python theory_test_pseudomono.py                                      # ví dụ giả đơn điệu
python analyze_theory.py                                              # bảng độ dốc và chi phí
pytest tests/ -q                                                      # kiểm thử
```

Phần thực nghiệm ban đầu, các lệnh tái lập nằm ở mục 13.2 của báo cáo.

## Kết quả số của hướng lý thuyết

Đo trên ảnh xám cạnh 64 điểm ảnh, 150 bước ngoài, thuần suy diễn, không có thành phần học.

Lợi thế đo được là chi phí, không phải chất lượng khôi phục. Để đạt cùng một mức phần dư biến phân, phép chiếu xấp xỉ với ngân sách bước nội nhỏ tốn ít hơn phép chiếu chính xác có khởi tạo ấm khoảng 2,5 đến 2,8 lần trên mờ Gauss, và khoảng 4 đến 7 lần trên mờ chuyển động, nơi bài toán chiếu khó hơn. Đây là một hệ số hằng, không phải khác biệt bậc.

Ví dụ giả đơn điệu xác nhận toán tử thực sự không đơn điệu (tìm được cặp điểm với tích vô hướng âm) trong khi thuật toán vẫn hội tụ, nên định lý phát biểu cho lớp giả đơn điệu không rộng hơn ví dụ minh họa.

## Tài liệu

Thư mục `tai_lieu_bai_bao/` chứa: kết luận điều hành và định vị so với tài liệu, khung bài báo, báo cáo số liệu, bản thảo chứng minh kèm biên bản phản biện, và lộ trình chứng minh. Đọc `00_ket_luan_dieu_hanh.md` trước.
