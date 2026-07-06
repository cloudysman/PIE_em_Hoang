"""WP2 - Lớp chiếu xấp xỉ khả vi (differentiable inexact projection).

Tập ràng buộc vật lý là hộp giá trị điểm ảnh D = [lo, hi] (mặc định [0, 1]).
Phép chiếu *chính xác* lên hộp là clamp. Để hiện thực hóa cơ chế "chiếu xấp xỉ"
(Procedure 2.1 của Paper 81) với sai số được kiểm soát, ta dùng một vòng lặp nội
relaxed (giãn) hội tụ tới phép chiếu chính xác:

        u_{t+1} = (1 - gamma) * u_t + gamma * clamp(u_t, lo, hi),   u_0 = v.

- gamma = 1            -> chiếu CHÍNH XÁC ngay sau 1 bước (clamp).
- 0 < gamma < 1        -> chiếu XẤP XỈ; dừng sớm ở dung sai eps_k -> sai số > 0.

Vấn đề mấu chốt (xem WP2/Rủi ro 3): khi dừng sớm, điểm trả về không thỏa điều
kiện tối ưu chính xác, nên gradient theo định lý hàm ẩn sẽ bị thiên lệch. Phương
án (a) - chắc chắn nhất - là *trải vòng lặp nội* (unroll) và để autograd tính
đúng gradient của chính phép tính đã thực hiện. Hàm dưới đây unroll nên tương
thích autograd trực tiếp.
"""

from __future__ import annotations

from typing import Tuple

import torch


def inexact_project_box(
    v: torch.Tensor,
    lo: float = 0.0,
    hi: float = 1.0,
    n_inner: int = 4,
    gamma: float = 0.6,
    eps: float = 1e-3,
) -> Tuple[torch.Tensor, torch.Tensor, int]:
    """Chiếu xấp xỉ lên hộp [lo, hi] bằng vòng lặp nội relaxed, có dừng sớm.

    Trả về (u, rel_err, n_used):
        u        : điểm chiếu xấp xỉ (khả vi qua autograd nhờ unroll).
        rel_err  : sai số tương đối ||u - clamp(v)|| / ||clamp(v)|| (đo lường e_k).
        n_used   : số bước nội thực sự đã dùng.
    """
    exact = v.clamp(lo, hi)                      # phép chiếu chính xác (tham chiếu)
    denom = exact.flatten(1).norm(dim=1).clamp_min(1e-12)
    u = v
    n_used = 0
    for t in range(n_inner):
        u = (1.0 - gamma) * u + gamma * u.clamp(lo, hi)
        n_used = t + 1
        rel = (u - exact).flatten(1).norm(dim=1) / denom
        if torch.all(rel < eps):
            break
    rel_err = (u - exact).flatten(1).norm(dim=1) / denom
    return u, rel_err.detach(), n_used


def exact_project_box(v: torch.Tensor, lo: float = 0.0,
                      hi: float = 1.0) -> torch.Tensor:
    """Phép chiếu chính xác lên hộp (clamp) - dùng cho ablation exact vs inexact."""
    return v.clamp(lo, hi)
