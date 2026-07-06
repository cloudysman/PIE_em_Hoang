"""Sơ đồ PIE-Net trên QUẢ CẦU TV - dùng cho phép thử ba mốc.

Tái dùng:
  - sơ đồ 4 pha của ``solver.PIENet`` (quán tính -> chiếu xấp xỉ -> hiệu chỉnh
    phản xạ -> trộn độ nhớt);
  - toán tử ``operators.CostOperator``  F_theta = rho_theta * (B^T(Bx - y) + G_phi);
  - phép chiếu lên quả cầu TV ``constraints.TVBallConstraint`` (Chambolle-Pock,
    khởi tạo ấm, ngân sách m bước nội, có đếm số bước nội).

Khác ``solver.PIENet`` ở ba điểm cần thiết cho phép thử:
  1. chiếu lên quả cầu TV  D = {x : TV(x) <= tau}  thay vì hộp [0,1];
  2. truyền (thread) trạng thái khởi tạo ấm qua các bước ngoài;
  3. trả về TỔNG số bước nội để đo chi phí trung thực.

Cấu hình headline (đúng sơ đồ đã chạy ở ``quick_test_tv.py``): quán tính, hiệu
chỉnh phản xạ và độ nhớt đều TẮT, nên một bước ngoài rút về chiếu - gradient
    x_{k+1} = P_D( x_k - lambda_k F_theta(x_k) ).
Khi đó đầu ra x^K là một phép chiếu nên KHẢ THI (TV <= tau) tới sai số nội.
Ba pha còn lại vẫn cài sẵn (bật qua TVSchedules) để dùng về sau nếu cần.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torch.nn as nn

from .constraints import TVBallConstraint, tv_isotropic
from .operators import CostOperator


class ZeroG(nn.Module):
    """G_phi = 0: mốc không học không có regularizer học được.

    Có ``monotonicity_penalty`` trả về 0 để dùng chung vòng huấn luyện với mốc
    có học (vốn phạt đơn điệu cho G_phi)."""

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.zeros_like(x)

    def monotonicity_penalty(self, x: torch.Tensor, n_dirs: int = 1,
                             h: float = 1e-2) -> torch.Tensor:
        return x.new_zeros(())


@dataclass
class TVSchedules:
    """Lịch tham số. Mặc định = sơ đồ chiếu - gradient (đúng cái đã chạy)."""
    K: int = 12                  # số bước ngoài
    m: int = 2                   # ngân sách bước nội của chiếu xấp xỉ
    lam0: float = 1.0            # bước lambda khởi tạo (~ giá trị thật sau softplus)
    learn_lambda: bool = True    # lambda_k học được (deep unfolding) - cấp cho CẢ HAI mốc
    alpha: float = 0.0           # quán tính (0 = tắt)
    beta0: float = 0.0           # hệ số độ nhớt beta_k = beta0/(k+1) (0 = tắt)
    delta: float = 0.5           # hằng co của ánh xạ độ nhớt (chỉ dùng khi beta0>0)
    use_reflection: bool = False # hiệu chỉnh phản xạ (tắt = chiếu - gradient thuần)


class PIENetTV(nn.Module):
    """PIE-Net trên quả cầu TV: unroll K bước, chiếu xấp xỉ TV có khởi tạo ấm."""

    def __init__(self, cost: CostOperator, sched: TVSchedules,
                 box: Optional[Tuple[float, float]] = (0.0, 1.0)):
        super().__init__()
        self.cost = cost
        self.s = sched
        self.box = box
        # khởi tạo để softplus(lam_raw) ~ lam0 (lambda > 0)
        lam_raw0 = math.log(math.expm1(max(sched.lam0, 1e-3)))
        if sched.learn_lambda:
            self.lam_raw = nn.Parameter(torch.full((sched.K,), float(lam_raw0)))
        else:
            self.register_buffer("lam_raw", torch.full((sched.K,), float(lam_raw0)))

    def _lambda(self, k: int) -> torch.Tensor:
        return torch.nn.functional.softplus(self.lam_raw[k]).clamp(1e-3, 2.0)

    def _viscosity(self, x, anchor):
        d = self.s.delta
        return d * x + (1.0 - d) * anchor

    def forward(self, y: torch.Tensor, tau: torch.Tensor, x0=None,
                return_cost: bool = False):
        """y: (B,1,H,W) ảnh quan sát. tau: (B,) bán kính quả cầu TV (oracle =
        frac * TV(ảnh sạch)). Trả về x^K, hoặc (x^K, tổng_bước_nội)."""
        cons = TVBallConstraint(tau=tau.detach(), box=self.box)
        if x0 is None:
            x0 = self.cost.blur.adjoint(y)
            if self.box is not None:
                x0 = x0.clamp(self.box[0], self.box[1])
        anchor = x0
        x_prev = x = x0
        state = None
        total_inner = 0

        for k in range(self.s.K):
            lam = self._lambda(k)
            # (1) quán tính
            w = x + self.s.alpha * (x - x_prev) if self.s.alpha > 0 else x
            Fw = self.cost(w, y)
            # (2) chiếu xấp xỉ lên quả cầu TV (m bước nội, khởi tạo ấm qua state)
            res = cons.project(w - lam * Fw, tol=0.0, max_inner=self.s.m, state=state)
            yk = res.x
            state = res.state
            total_inner += res.n_inner
            # (3) hiệu chỉnh phản xạ (tùy chọn)
            if self.s.use_reflection:
                Fy = self.cost(yk, y)
                z = yk - lam * (Fy - Fw)
            else:
                z = yk
            # (4) trộn độ nhớt (tùy chọn)
            if self.s.beta0 > 0:
                beta = self.s.beta0 / (k + 1.0)
                x_next = beta * self._viscosity(x, anchor) + (1.0 - beta) * z
            else:
                x_next = z
            x_prev, x = x, x_next

        if return_cost:
            return x, total_inner
        return x

    @torch.no_grad()
    def feasibility(self, x: torch.Tensor, tau: torch.Tensor) -> float:
        """Độ khả thi trung bình TV(x)/tau (<= 1 nghĩa là không vi phạm)."""
        return (tv_isotropic(x) / tau.to(x.device)).mean().item()
