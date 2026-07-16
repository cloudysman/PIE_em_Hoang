"""Tập ràng buộc cần vòng lặp nội để chiếu (cốt lõi của hướng 2).

Khẳng định DUY NHẤT đang kiểm chứng:
    Trên một tập ràng buộc mà chiếu CHÍNH XÁC đòi hỏi một vòng lặp nội tốn kém,
    thay chiếu chính xác bằng chiếu XẤP XỈ với sai số e_k có kiểm soát đạt CÙNG
    chất lượng ảnh nhưng tốn ÍT chi phí hơn rõ rệt (tổng số bước nội + thời gian),
    trong khi vẫn giữ hội tụ.

Để phép thử có nghĩa, tập ràng buộc phải THẬT SỰ cần vòng lặp nội. Quả cầu l1 bị
loại vì có chiếu chính xác nhanh bằng sắp xếp (không có đánh đổi). Ta dùng:

    QUẢ CẦU TV (chính):  D = { x : TV(x) <= tau }.
    Chiếu lên D không có công thức đóng. Ta giải
        P_D(v) = argmin_x  1/2||x - v||^2   s.t.  ||grad x||_{2,1} <= tau
    bằng Chambolle-Pock (primal-dual), MỘT vòng lặp nội có dung sai dừng,
    KHỞI TẠO ẤM được qua biến đối ngẫu p, KHÔNG lồng (khác bisection x FGP).

Giao diện ``Constraint`` tổng quát để lớp chiếu xấp xỉ (solver) gọi đồng nhất cho
mọi tập ràng buộc và đếm số bước nội thực sự đã dùng.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional, Tuple

import torch


# --------------------------------------------------------------------------- #
#  Toán tử gradient rời rạc và adjoint (divergence)                            #
#  Forward difference, biên Neumann (đạo hàm = 0 ở biên xa).                   #
#  Quy ước Chambolle: div = -grad^T  =>  <grad x, p> = -<x, div p>.            #
# --------------------------------------------------------------------------- #
def grad2d(x: torch.Tensor) -> torch.Tensor:
    """grad x : (B,1,H,W) -> (B,2,H,W) = (gx_ngang, gy_doc)."""
    gx = torch.zeros_like(x)
    gy = torch.zeros_like(x)
    gx[..., :, :-1] = x[..., :, 1:] - x[..., :, :-1]      # đạo hàm theo chiều rộng
    gy[..., :-1, :] = x[..., 1:, :] - x[..., :-1, :]      # đạo hàm theo chiều cao
    return torch.cat([gx, gy], dim=1)


def div2d(p: torch.Tensor) -> torch.Tensor:
    """divergence : (B,2,H,W) -> (B,1,H,W), thỏa <grad x, p> = -<x, div p>."""
    px = p[:, 0:1]
    py = p[:, 1:2]
    dpx = torch.zeros_like(px)
    dpx[..., :, 1:-1] = px[..., :, 1:-1] - px[..., :, 0:-2]
    dpx[..., :, 0] = px[..., :, 0]
    dpx[..., :, -1] = -px[..., :, -2]
    dpy = torch.zeros_like(py)
    dpy[..., 1:-1, :] = py[..., 1:-1, :] - py[..., 0:-2, :]
    dpy[..., 0, :] = py[..., 0, :]
    dpy[..., -1, :] = -py[..., -2, :]
    return dpx + dpy


def tv_isotropic(x: torch.Tensor) -> torch.Tensor:
    """TV đẳng hướng theo từng ảnh trong batch: sum_pixel ||(grad x)_pixel||_2.
    Trả về tensor (B,)."""
    g = grad2d(x)
    nrm = torch.sqrt((g ** 2).sum(dim=1) + 1e-12)        # (B,H,W) chuẩn l2 theo 2 kênh
    return nrm.flatten(1).sum(dim=1)


# --------------------------------------------------------------------------- #
#  Chiếu lên quả cầu l1 (theo từng ảnh, vector không âm) - dùng cho bước       #
#  prox của chiếu l2,1-ball bên trong Chambolle-Pock.                          #
# --------------------------------------------------------------------------- #
def _project_l1_ball_nonneg(r: torch.Tensor, tau: torch.Tensor) -> torch.Tensor:
    """Chiếu vector KHÔNG ÂM r (B,N) lên quả cầu l1 bán kính tau (B,) hoặc vô
    hướng: tìm ngưỡng theta sao cho sum max(r - theta, 0) = tau (sắp xếp,
    Duchi 2008). Hàng nào sum(r) <= tau giữ nguyên."""
    B, N = r.shape
    if not torch.is_tensor(tau):
        tau = r.new_full((B,), float(tau))
    tau = tau.view(B)
    out = r.clone()
    s = r.sum(dim=1)
    need = s > tau                                        # chỉ xử lý hàng vượt cầu
    if not torch.any(need):
        return out
    rr = r[need]
    tt = tau[need]
    u, _ = torch.sort(rr, dim=1, descending=True)
    cssv = torch.cumsum(u, dim=1) - tt.view(-1, 1)
    ind = torch.arange(1, N + 1, device=r.device, dtype=r.dtype).view(1, N)
    cond = (u - cssv / ind) > 0
    rho = cond.to(r.dtype).sum(dim=1).clamp_min(1.0)      # số phần tử active
    theta = cssv.gather(1, (rho.long() - 1).view(-1, 1)).squeeze(1) / rho
    out[need] = torch.clamp(rr - theta.view(-1, 1), min=0.0)
    return out


def _project_l21_ball(z: torch.Tensor, tau: torch.Tensor) -> torch.Tensor:
    """Chiếu trường gradient z (B,2,H,W) lên quả cầu l2,1 bán kính tau:
    { z : sum_pixel ||z_pixel||_2 <= tau }.

    = chiếu vector chuẩn-nhóm (theo điểm ảnh) lên quả cầu l1, rồi co lại."""
    B = z.shape[0]
    nrm = torch.sqrt((z ** 2).sum(dim=1, keepdim=True) + 1e-12)   # (B,1,H,W)
    r = nrm.flatten(1)                                            # (B,N)
    r_hat = _project_l1_ball_nonneg(r, tau).view_as(nrm)
    scale = r_hat / nrm                                           # <= 1
    return z * scale


# --------------------------------------------------------------------------- #
#  Giao diện ràng buộc tổng quát                                               #
# --------------------------------------------------------------------------- #
@dataclass
class ProjResult:
    x: torch.Tensor                 # điểm chiếu (xấp xỉ hoặc chính xác)
    n_inner: int                    # SỐ BƯỚC NỘI thực sự đã dùng (đếm chi phí)
    state: object                   # trạng thái nội để KHỞI TẠO ẤM bước ngoài sau
    feas: torch.Tensor              # giá trị ràng buộc TV(x) (để kiểm tra khả thi)


class Constraint:
    """Giao diện: project(v, tol, max_inner, state) -> ProjResult.

    - tol      : dung sai dừng nội (sai số e_k); nhỏ -> chiếu chính xác.
    - max_inner: trần số bước nội; nhỏ -> chiếu xấp xỉ.
    - state    : trạng thái nội của bước ngoài trước (khởi tạo ấm); None = lạnh.
    Dừng khi đạt tol HOẶC chạm max_inner; LUÔN trả số bước nội thực dùng.
    """

    def project(self, v: torch.Tensor, tol: float, max_inner: int,
                state=None) -> ProjResult:                       # pragma: no cover
        raise NotImplementedError

    def value(self, x: torch.Tensor) -> torch.Tensor:           # pragma: no cover
        raise NotImplementedError


class BoxConstraint(Constraint):
    """Hộp [lo,hi]: chiếu chính xác = clamp trong 1 bước. Dùng để kiểm tra
    rằng tập TẦM THƯỜNG không tạo đánh đổi (n_inner luôn = 1)."""

    def __init__(self, lo: float = 0.0, hi: float = 1.0):
        self.lo, self.hi = lo, hi

    def project(self, v, tol=0.0, max_inner=1, state=None) -> ProjResult:
        x = v.clamp(self.lo, self.hi)
        return ProjResult(x, 1, None, x.new_zeros(v.shape[0]))

    def value(self, x):
        return x.new_zeros(x.shape[0])


class TVBallConstraint(Constraint):
    """Quả cầu TV  D = { x : TV(x) <= tau }  (TV đẳng hướng).

    Chiếu  P_D(v) = argmin_x 1/2||x-v||^2  s.t. ||grad x||_{2,1} <= tau
    giải bằng Chambolle-Pock:
        min_x  G(x) + F(K x),  G(x)=1/2||x-v||^2,  K=grad,  F=ind_{l2,1<=tau}.
        p^{n+1} = prox_{sigma F*}(p^n + sigma K xbar^n)
                = q - sigma * proj_l21( q/sigma ),   q = p + sigma grad(xbar)
        x^{n+1} = prox_{t G}(x^n - t K* p^{n+1}) = (x + t div(p) + t v)/(1+t)
        xbar    = 2 x^{n+1} - x^n
    với sigma*t*||K||^2 <= 1, ||grad||^2 <= 8. Khởi tạo ấm = (x, p) bước trước.
    """

    def __init__(self, tau: torch.Tensor, box: Optional[Tuple[float, float]] = (0.0, 1.0),
                 accel: bool = False):
        # tau: (B,) bán kính TV theo từng ảnh (ví dụ = TV ảnh sạch, oracle).
        self.tau = tau
        self.box = box                                  # ràng buộc hộp phụ (tùy chọn)
        self.L = (8.0) ** 0.5                            # ||grad||
        self.sigma = 1.0 / self.L
        self.t = 1.0 / self.L
        # accel=True: lịch bước TĂNG TỐC (Chambolle-Pock 2011, thuật toán 2) khai
        # thác việc G(x)=1/2||x-v||^2 LỒI MẠNH với tham số gamma=1, cho tốc độ
        # O(1/N^2) thay vì O(1/N). Lịch (t_n, sigma_n) được ĐẶT LẠI ở mỗi lần gọi
        # project vì mỗi bước ngoài là một bài toán chiếu mới; khởi tạo ấm vẫn giữ
        # nguyên qua biến (x, p).
        self.accel = accel
        self.gamma = 1.0                                 # G lồi mạnh tham số 1

    def value(self, x):
        return tv_isotropic(x)

    def _init(self, v, state):
        """Khởi tạo (x, p) — ấm nếu có state của bước ngoài trước, lạnh nếu None."""
        if state is not None:
            x, p = state
            return x.detach().clone(), p.detach().clone()
        B = v.shape[0]
        x = v.clone()
        p = torch.zeros(B, 2, v.shape[2], v.shape[3],
                        device=v.device, dtype=v.dtype)
        return x, p

    def _cp_step(self, x, xbar, p, v, tau):
        """MỘT bước Chambolle-Pock cho phép chiếu lên quả cầu TV."""
        sigma, t = self.sigma, self.t
        x_prev = x
        q = p + sigma * grad2d(xbar)                    # đối ngẫu: prox F* (l2,1-ball)
        p = q - sigma * _project_l21_ball(q / sigma, tau)
        x = (x + t * div2d(p) + t * v) / (1.0 + t)      # nguyên thủy: prox G (bậc hai)
        if self.box is not None:
            x = x.clamp(self.box[0], self.box[1])
        xbar = 2.0 * x - x_prev
        return x, xbar, p

    def _cp_step_accel(self, x, xbar, p, v, tau, t, sigma):
        """MỘT bước Chambolle-Pock TĂNG TỐC (thuật toán 2), khai thác G lồi mạnh.

        Khác bản cơ bản ở chỗ (t, sigma) thay đổi theo bước và hệ số ngoại suy
        theta không còn bằng 1:
            theta = 1/sqrt(1 + 2 gamma t),  t <- theta t,  sigma <- sigma/theta,
            xbar  = x + theta (x - x_prev).
        Tích sigma*t*||K||^2 <= 1 được bảo toàn vì t giảm đúng bằng phần sigma tăng.
        """
        x_prev = x
        q = p + sigma * grad2d(xbar)                    # đối ngẫu: prox F* (l2,1-ball)
        p = q - sigma * _project_l21_ball(q / sigma, tau)
        x = (x + t * div2d(p) + t * v) / (1.0 + t)      # nguyên thủy: prox G (bậc hai)
        if self.box is not None:
            x = x.clamp(self.box[0], self.box[1])
        theta = 1.0 / math.sqrt(1.0 + 2.0 * self.gamma * t)
        xbar = x + theta * (x - x_prev)
        return x, xbar, p, theta * t, sigma / theta

    def _step(self, x, xbar, p, v, tau, t, sigma):
        """Một bước nội, chọn bản cơ bản hay bản tăng tốc theo cờ ``accel``."""
        if self.accel:
            return self._cp_step_accel(x, xbar, p, v, tau, t, sigma)
        x, xbar, p = self._cp_step(x, xbar, p, v, tau)
        return x, xbar, p, t, sigma

    def project(self, v, tol: float = 0.0, max_inner: int = 200,
                state=None) -> ProjResult:
        """Chạy CP tối đa max_inner bước (tol=0 -> đúng max_inner bước, dùng cho
        chiếu xấp xỉ ngân sách cố định). tol>0 dừng sớm theo thay đổi nguyên thủy
        — LƯU Ý: tiêu chí này kích hoạt sớm; để đo 'chính xác' dùng iters_to_tol."""
        tau = self.tau.to(v.device).view(v.shape[0])
        x, p = self._init(v, state)
        xbar = x.clone()
        t, sig = self.t, self.sigma          # đặt lại lịch bước cho bài toán chiếu này
        n_used = 0
        for it in range(max_inner):
            x_prev = x
            x, xbar, p, t, sig = self._step(x, xbar, p, v, tau, t, sig)
            n_used = it + 1
            if tol > 0.0:
                rel = ((x - x_prev).flatten(1).norm(dim=1) /
                       x_prev.flatten(1).norm(dim=1).clamp_min(1e-12))
                if torch.all(rel < tol):
                    break
        return ProjResult(x, n_used, (x, p), tv_isotropic(x))

    def project_to_ref(self, v, x_ref, tol_rel: float, cap: int,
                       state=None) -> ProjResult:
        """Chiếu với SAI SỐ ĐO ĐƯỢC: chạy CP (khởi tạo ấm nếu có state) tới khi
        sai số tương đối so với nghiệm tham chiếu x_ref <= tol_rel, chặn ở cap.

        Khác ``iters_to_tol`` ở hai điểm: (i) trả về CẢ iterate lẫn state (dùng
        được làm bước chiếu thật trong chế độ 'chiếu chính xác' / 'eps hằng'),
        (ii) kiểm tra TRƯỚC bước đầu — khởi tạo ấm đã đạt tol thì tốn 0 bước
        (đếm chi phí trung thực). Đồng bộ batch: dừng khi MỌI ảnh đạt tol."""
        tau = self.tau.to(v.device).view(v.shape[0])
        x, p = self._init(v, state)
        xbar = x.clone()
        t, sig = self.t, self.sigma          # đặt lại lịch bước cho bài toán chiếu này
        ref_norm = x_ref.flatten(1).norm(dim=1).clamp_min(1e-12)
        rel = (x - x_ref).flatten(1).norm(dim=1) / ref_norm
        n_used = 0
        while not torch.all(rel <= tol_rel) and n_used < cap:
            x, xbar, p, t, sig = self._step(x, xbar, p, v, tau, t, sig)
            n_used += 1
            rel = (x - x_ref).flatten(1).norm(dim=1) / ref_norm
        return ProjResult(x, n_used, (x, p), tv_isotropic(x))

    def iters_to_tol(self, v, x_ref, delta: float, cap: int, state=None) -> int:
        """Số bước CP để đạt sai số tương đối <= delta so với nghiệm chiếu HỘI TỤ
        x_ref (thước đo chi phí TRUNG THỰC của 'chiếu chính xác'). Đồng bộ batch:
        trả về bước đầu tiên mà MỌI ảnh đều đạt delta (chặn ở cap)."""
        tau = self.tau.to(v.device).view(v.shape[0])
        x, p = self._init(v, state)
        xbar = x.clone()
        ref_norm = x_ref.flatten(1).norm(dim=1).clamp_min(1e-12)
        for it in range(1, cap + 1):
            x, xbar, p = self._cp_step(x, xbar, p, v, tau)
            rel = (x - x_ref).flatten(1).norm(dim=1) / ref_norm
            if torch.all(rel <= delta):
                return it
        return cap
