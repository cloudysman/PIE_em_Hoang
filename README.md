# PIE-Net — Pseudomonotone Inexact-Projection Equilibrium Networks

Hiện thực hóa (implementation) bằng PyTorch cho đề tài **"Mạng cân bằng chiếu xấp xỉ
giả đơn điệu cho bài toán ngược trong xử lý ảnh (PIE-Net)"** theo file thuyết minh
`PIE-Net_thuyet_minh.docx`.

Mô hình hóa bài toán ngược `y = B x + ε` dưới dạng **bất đẳng thức biến phân (VI)
giả đơn điệu**, giải bằng thuật toán quán tính – chiếu xấp xỉ – độ nhớt, và huấn
luyện đầu-cuối như một mạng cân bằng (deep unfolding).

## Ánh xạ mã nguồn ↔ thuyết minh

| Gói công việc | Nội dung | File |
|---|---|---|
| **WP1** | Toán tử `F_θ = ρ_θ · M_φ`, `M_φ = Bᵀ(Bx−y) + G_φ`; Mệnh đề 1 (giả đơn điệu theo cấu trúc); chứng nhận đơn điệu G_φ qua hàm phạt Jacobian | `pie_net/operators.py` |
| **WP2** | Lớp chiếu xấp xỉ khả vi (Procedure 2.1, dừng sớm + unroll cho gradient đúng); biến thể L-free (Tseng linesearch) | `pie_net/projection.py`, `pie_net/solver.py` |
| **WP2** | Thuật toán PIE-Net 4 pha: quán tính → chiếu xấp xỉ → hiệu chỉnh phản xạ → trộn độ nhớt | `pie_net/solver.py` (`PIENet`) |
| **WP3** | Bằng chứng thực nghiệm cho T2: phần dư VI `r(x)=‖x−P_D(x−F_θ(x))‖ → 0` (last-iterate) | `solver.solve_long`, `metrics.vi_residual` |
| **WP4** | Khử mờ ảnh + ablation; thí nghiệm then chốt `ρ_θ` học được vs `ρ` hằng | `pie_net/data.py`, `pie_net/train.py`, `run_experiment.py` |

## Cài đặt & chạy

Yêu cầu: `torch`, `numpy`, `scipy`, `scikit-image`, `matplotlib` (đã có sẵn trong môi trường).

```bash
python run_experiment.py                 # đầy đủ (GPU nếu có)
python run_experiment.py --quick         # chạy nhanh để kiểm thử
python run_experiment.py --blur motion   # mờ chuyển động thay vì Gauss
python run_experiment.py --device cpu
```

Kết quả lưu ở thư mục `results/`:
- `metrics.csv` — bảng PSNR / SSIM / phần dư VI / số vòng lặp / thời gian.
- `convergence.png` — phần dư VI → 0 và PSNR theo bước lặp (minh chứng T2).
- `reconstructions.png` — ảnh gốc / ảnh mờ / khôi phục (ρ học được vs ρ hằng).

## Thành phần chính

**Toán tử (WP1).** `M_φ(x) = Bᵀ(Bx−y) + G_φ(x)` với hạng dữ liệu đơn điệu chính xác
(`BᵀB ⪰ 0`, adjoint cài đặt đúng bằng nhân quay 180° + zero-pad) và `G_φ` là CNN
được phạt đơn điệu theo hướng Jacobian. `ρ_θ(x)` là **vô hướng** dương ∈ [ρ_min, ρ_max]
(softmax-bounded) — đúng điều kiện Mệnh đề 1 (chỉ số dương nhân toán tử đơn điệu mới
bảo toàn giả đơn điệu).

**Thuật toán (WP2).** Một bước lặp:
```
(1) w^k = x^k + α_k (x^k − x^{k−1})                 # quán tính
(2) y^k = P_D^{ε_k}( w^k − λ_k F_θ(w^k) )           # chiếu xấp xỉ
(3) z^k = y^k − λ_k ( F_θ(y^k) − F_θ(w^k) )         # hiệu chỉnh phản xạ
(4) x^{k+1} = β_k f(x^k) + (1 − β_k) z^k            # trộn độ nhớt
```

**Lưu ý trung thực** (đúng tinh thần thuyết minh):
- `ρ_θ` là *preconditioner* học được, **không đổi tập nghiệm VI** (vô hướng dương).
  Giá trị của nó là động học hội tụ / số vòng lặp, không phải "prior giàu hơn".
  Thực nghiệm xác nhận: `ρ_θ` học được hội tụ về ≈ 1.0 và PSNR **xấp xỉ bằng**
  `ρ` hằng được tinh chỉnh tốt (đúng như Rủi ro 1 trong thuyết minh dự liệu).
- Với ràng buộc hộp `[0,1]`, chiếu chính xác là `clamp`; lớp chiếu xấp xỉ ở đây minh
  họa cơ chế vòng lặp nội có kiểm soát sai số `ε_k` và xử lý gradient (unroll) — phần
  quan trọng khi tập ràng buộc tổng quát.
- **Semi-convergence (quan trọng).** PIE-Net ở đây vận hành như **mạng deep
  unfolding**: ảnh khôi phục là điểm-lặp ở chân trời hữu hạn `x^K` (K≈12),
  đạt ~28–29 dB. Khi chạy thuật toán tới *điểm bất động chính xác* của F_θ
  (xem `convergence.png`): phần dư VI **→ 0 (Định lý T2 đúng — thuật toán hội tụ)**,
  nhưng PSNR đạt đỉnh ở chân trời hữu hạn rồi **giảm**, vì nghiệm-VI chính xác của
  F_θ là nghiệm bám dữ liệu (khuếch đại nhiễu). Đây là hiện tượng đã biết của các
  phương pháp lặp học được; "dừng sớm" đóng vai trò chính quy hóa ngầm.
- Để *điểm bất động* trùng với ảnh khôi phục (đúng nghĩa "mạng cân bằng / DEQ" với
  vi phân ẩn) cần huấn luyện ở chế độ cân bằng sâu — `PIENet.forward_equilibrium`
  (DEQ warm-up + đuôi có gradient) đã được cài sẵn làm hướng phát triển; ở quy mô
  demo nó nâng PSNR điểm-bất-động đáng kể nhưng chưa bằng chế độ unfolding.
- Lý thuyết T1/T2 (WP3) là kết quả giải tích; ở đây ta cung cấp **bằng chứng số**
  cho phần "thuật toán hội tụ" (phần dư VI → 0).
