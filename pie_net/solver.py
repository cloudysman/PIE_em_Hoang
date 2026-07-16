"""WP2/WP3 - Thuật toán PIE-Net (rời rạc hóa VAPA/MVAPA của Paper 81).

Một bước lặp gồm 4 pha:
    (1) quán tính        w^k = x^k + alpha_k (x^k - x^{k-1})
    (2) chiếu xấp xỉ     y^k = P_D^{eps_k}( w^k - lambda_k F_theta(w^k) )
    (3) hiệu chỉnh Tseng  z^k = y^k - lambda_k ( F_theta(y^k) - F_theta(w^k) )
    (4) trộn độ nhớt     x^{k+1} = beta_k f(x^k) + (1 - beta_k) z^k

với f là ánh xạ co (viscosity), {beta_k} -> 0 và không khả tổng, {alpha_k} quán
tính, {lambda_k} bước, {eps_k} sai số chiếu. Biến thể L-free thay bước cố định
bằng linesearch kiểu Tseng (không cần hằng số Lipschitz của mạng).

Lưu ý danh pháp: pha (3) là hiệu chỉnh kiểu Tseng (forward-backward-forward, tính
toán tử HAI lần), KHÔNG phải bước phản xạ kiểu Malitsky (dùng điểm phản xạ
2x^k - x^{k-1} và chỉ tính toán tử một lần). Các tài liệu trước của đề tài gọi
nhầm pha này là "hiệu chỉnh phản xạ"; sơ đồ phản xạ đúng nghĩa nằm ở
``reflected_solver.py``.

Về phần dư biến phân r(x) = || x - P_D( x - F_theta(x) ) ||: thực nghiệm chỉ cho
thấy r giảm theo bước lặp (từ 2.48 xuống 0.199 qua 200 bước, giảm KHÔNG đơn điệu),
KHÔNG chứng minh r tiến về 0. Mọi khẳng định mạnh hơn mức này là quá lời so với số
liệu (xem ``forward(..., return_history=True)``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import torch
import torch.nn as nn

from .operators import CostOperator
from .projection import inexact_project_box, exact_project_box


@dataclass
class Schedules:
    """Lịch tham số cho K bước lặp."""
    K: int = 12
    alpha: float = 0.3          # hệ số quán tính (inertial)
    beta0: float = 0.5          # beta_k = beta0 / (k + 1)  -> 0, không khả tổng
    lam0: float = 0.5           # bước lambda khởi tạo
    eps0: float = 5e-2          # eps_k = eps0 / (k + 1)  (dung sai chiếu)
    delta: float = 0.5          # hằng co của ánh xạ viscosity f
    n_inner: int = 4            # số bước nội tối đa của chiếu xấp xỉ
    gamma: float = 0.6          # hệ số relaxed của chiếu xấp xỉ
    learn_lambda: bool = True   # lambda_k học được (deep unfolding)
    use_inertial: bool = True
    use_viscosity: bool = True
    inexact_proj: bool = True   # True: chiếu xấp xỉ ; False: chiếu chính xác
    tseng_linesearch: bool = False   # biến thể L-free


class PIENet(nn.Module):
    """Mạng cân bằng PIE-Net: unroll K bước thuật toán bất đẳng thức biến phân.

    Đầu vào: y (dữ liệu quan sát), x0 (khởi tạo, mặc định = clamp(B^T y)).
    Đầu ra : x^K (ảnh khôi phục) - điểm-lặp-cuối.
    """

    def __init__(self, cost: CostOperator, sched: Schedules,
                 lo: float = 0.0, hi: float = 1.0,
                 f_anchor: Optional[Callable] = None):
        super().__init__()
        self.cost = cost
        self.s = sched
        self.lo, self.hi = lo, hi
        # f(x) = delta * x + (1 - delta) * anchor  -> ánh xạ co (Lipschitz delta).
        # Mặc định anchor là khởi tạo x0 (Halpern-viscosity hướng về x0).
        self.f_anchor = f_anchor
        if sched.learn_lambda:
            # lambda_k > 0 qua softplus, mỗi bước một tham số (deep unfolding).
            self.lam_raw = nn.Parameter(torch.full((sched.K,), float(sched.lam0)))
        else:
            self.register_buffer("lam_raw", torch.full((sched.K,), float(sched.lam0)))

    # ------------------------------------------------------------------ #
    def _lambda(self, k: int) -> torch.Tensor:
        if self.s.learn_lambda:
            return torch.nn.functional.softplus(self.lam_raw[k]).clamp(1e-3, 2.0)
        return self.lam_raw[k]

    def _project(self, v, eps):
        if self.s.inexact_proj:
            u, rel, n = inexact_project_box(v, self.lo, self.hi,
                                            self.s.n_inner, self.s.gamma, eps)
            return u, rel, n
        return exact_project_box(v, self.lo, self.hi), v.new_zeros(v.shape[0]), 1

    def _viscosity(self, x, anchor):
        d = self.s.delta
        return d * x + (1.0 - d) * anchor

    def vi_residual(self, x, y):
        """Phần dư VI tự nhiên: || x - P_D(x - F_theta(x)) || (norm trung bình/ảnh)."""
        with torch.no_grad():
            r = x - (x - self.cost(x, y)).clamp(self.lo, self.hi)
            return r.flatten(1).norm(dim=1).mean()

    # ------------------------------------------------------------------ #
    def forward(self, y, x0=None, return_history: bool = False, ref=None):
        if x0 is None:
            x0 = self.cost.blur.adjoint(y).clamp(self.lo, self.hi)
        anchor = x0 if self.f_anchor is None else self.f_anchor
        x_prev = x0
        x = x0
        hist = {"vi": [], "proj_err": [], "psnr_step": []} if return_history else None

        for k in range(self.s.K):
            lam = self._lambda(k)
            beta = self.s.beta0 / (k + 1.0)
            eps = self.s.eps0 / (k + 1.0)

            # (1) quán tính
            if self.s.use_inertial:
                w = x + self.s.alpha * (x - x_prev)
            else:
                w = x

            Fw = self.cost(w, y)

            # (2) chiếu xấp xỉ  y^k = P_D( w - lambda F(w) )  (có thể linesearch)
            if self.s.tseng_linesearch:
                lam = self._tseng_step(w, Fw, y, lam)
            yk, rel, _ = self._project(w - lam * Fw, eps)

            # (3) hiệu chỉnh phản xạ
            Fy = self.cost(yk, y)
            z = yk - lam * (Fy - Fw)

            # (4) trộn độ nhớt
            if self.s.use_viscosity:
                x_next = beta * self._viscosity(x, anchor) + (1.0 - beta) * z
            else:
                x_next = z

            x_prev, x = x, x_next

            if return_history:
                hist["vi"].append(self.vi_residual(x, y).item())
                hist["proj_err"].append(float(rel.mean()))
                if ref is not None:
                    with torch.no_grad():
                        mse = (x - ref).pow(2).flatten(1).mean(dim=1).clamp_min(1e-12)
                        hist["psnr_step"].append((10 * torch.log10(1.0 / mse)).mean().item())

        if return_history:
            return x, hist
        return x

    # ------------------------------------------------------------------ #
    def _step(self, x, x_prev, y, k, lam, use_tseng, anchor):
        """Một bước lặp 4 pha với bước vô hướng lam (dùng cho chế độ cân bằng)."""
        beta = self.s.beta0 / (k + 1.0)
        eps = self.s.eps0 / (k + 1.0)
        w = x + self.s.alpha * (x - x_prev) if self.s.use_inertial else x
        Fw = self.cost(w, y)
        lam_k = self._tseng_step(w, Fw, y, lam) if use_tseng else torch.as_tensor(
            lam, device=w.device, dtype=w.dtype)
        yk, _, _ = self._project(w - lam_k * Fw, eps)
        Fy = self.cost(yk, y)
        z = yk - lam_k * (Fy - Fw)
        x_next = (beta * self._viscosity(x, anchor) + (1 - beta) * z
                  if self.s.use_viscosity else z)
        return x_next, x

    def forward_equilibrium(self, y, n_warm: int = 15, n_grad: int = 6,
                            lam: float = 0.3, use_tseng: bool = False, x0=None):
        """Chế độ MẠNG CÂN BẰNG (DEQ-style): chạy n_warm bước KHÔNG gradient để
        tiến về điểm bất động, rồi n_grad bước CÓ gradient ở đuôi. Huấn luyện ở
        chế độ này ép *điểm bất động* của F_theta trở thành ảnh khôi phục tốt
        (đúng tinh thần 'đầu ra là điểm bất động'), thay vì chỉ tốt ở bước cắt."""
        if x0 is None:
            x0 = self.cost.blur.adjoint(y).clamp(self.lo, self.hi)
        anchor = x0
        x_prev = x = x0
        with torch.no_grad():
            for k in range(n_warm):
                x, x_prev = self._step(x, x_prev, y, k, lam, use_tseng, anchor)
        for k in range(n_warm, n_warm + n_grad):
            x, x_prev = self._step(x, x_prev, y, k, lam, use_tseng, anchor)
        return x

    # ------------------------------------------------------------------ #
    @torch.no_grad()
    def solve_long(self, y, K_long: int = 200, lam: float = 0.4,
                   use_tseng: bool = True, x0=None, ref=None):
        """Quan sát hành vi dài hạn: lấy toán tử F_theta ĐÃ HUẤN LUYỆN và chạy
        *thuật toán thuần* (không phải unroll cắt ngắn) trong nhiều bước với
        bước Tseng. Trả về (x, history).

        Trung thực về điều quan sát được: trong 200 bước, phần dư biến phân giảm
        từ 2.48 xuống 0.199 và giảm không đơn điệu; đây KHÔNG phải bằng chứng
        phần dư tiến về 0. Đồng thời PSNR đạt đỉnh quanh bước 26 rồi giảm còn
        6.77 dB ở bước 200 — hiện tượng bán hội tụ kinh điển của bài toán đặt
        không chỉnh: nghiệm chính xác của F_theta bám dữ liệu có nhiễu."""
        if x0 is None:
            x0 = self.cost.blur.adjoint(y).clamp(self.lo, self.hi)
        anchor = x0
        x_prev = x = x0
        hist = {"vi": [], "psnr_step": []}
        for k in range(K_long):
            beta = self.s.beta0 / (k + 1.0)
            eps = self.s.eps0 / (k + 1.0)
            w = x + self.s.alpha * (x - x_prev) if self.s.use_inertial else x
            Fw = self.cost(w, y)
            lam_k = self._tseng_step(w, Fw, y, lam) if use_tseng else torch.as_tensor(lam)
            yk, _, _ = self._project(w - lam_k * Fw, eps)
            Fy = self.cost(yk, y)
            z = yk - lam_k * (Fy - Fw)
            x_next = (beta * self._viscosity(x, anchor) + (1 - beta) * z
                      if self.s.use_viscosity else z)
            x_prev, x = x, x_next
            hist["vi"].append(self.vi_residual(x, y).item())
            if ref is not None:
                mse = (x - ref).pow(2).flatten(1).mean(dim=1).clamp_min(1e-12)
                hist["psnr_step"].append((10 * torch.log10(1.0 / mse)).mean().item())
        return x, hist

    # ------------------------------------------------------------------ #
    def _tseng_step(self, w, Fw, y, lam0, mu: float = 0.7, shrink: float = 0.7,
                    max_bt: int = 6):
        """Linesearch kiểu Tseng (L-free): tìm lambda lớn nhất sao cho
        lambda * ||F(y) - F(w)|| <= mu * ||y - w||, với y = P_D(w - lambda F(w)).
        Không cần biết hằng số Lipschitz của mạng."""
        lam = float(lam0) if not torch.is_tensor(lam0) else lam0.item()
        for _ in range(max_bt):
            yk = (w - lam * Fw).clamp(self.lo, self.hi)
            Fy = self.cost(yk, y)
            lhs = lam * (Fy - Fw).flatten(1).norm(dim=1)
            rhs = mu * (yk - w).flatten(1).norm(dim=1).clamp_min(1e-12)
            if torch.all(lhs <= rhs):
                break
            lam *= shrink
        return torch.as_tensor(lam, device=w.device, dtype=w.dtype)
