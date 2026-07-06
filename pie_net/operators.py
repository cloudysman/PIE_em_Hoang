"""WP1 - Mô hình hóa và chứng nhận toán tử.

Xây dựng toán tử chi phí học được
        F_theta(x) = rho_theta(x) * M_phi(x),
        M_phi(x)   = B^T (B x - y) + G_phi(x).

- Hạng dữ liệu  B^T(Bx - y)  là affine với phần tuyến tính B^T B nửa xác định
  dương  =>  đơn điệu (monotone) một cách chính xác.
- G_phi là mạng nơ-ron được huấn luyện cho đơn điệu (qua hàm phạt Jacobian,
  kiểu Belkouchi-Repetti) -> M_phi là "lớp vỏ đơn điệu".
- rho_theta(x) là *vô hướng* dương học được, chặn trong [rho_min, rho_max].

Mệnh đề 1 (giả đơn điệu theo cấu trúc): vì rho_theta(x) > 0 là vô hướng và
M_phi đơn điệu, F_theta = rho_theta * M_phi là giả đơn điệu (pseudomonotone).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


# --------------------------------------------------------------------------- #
#  Toán tử suy biến tuyến tính B (blur)  và  adjoint B^T                       #
# --------------------------------------------------------------------------- #
class BlurOperator(nn.Module):
    """Toán tử làm mờ B (convolution) cùng adjoint B^T chính xác.

    Dùng zero-padding 'same' với nhân lẻ (odd kernel); khi đó adjoint của
    phép tích chập là tích chập với nhân quay 180 độ (rot180) cùng padding,
    nên ``adjoint`` là B^T *chính xác* và B^T B nửa xác định dương.
    """

    def __init__(self, kernel: torch.Tensor):
        super().__init__()
        assert kernel.dim() == 2, "kernel phải là tensor 2D (kh, kw)"
        kh, kw = kernel.shape
        assert kh % 2 == 1 and kw % 2 == 1, "dùng nhân lẻ để adjoint chính xác"
        k = kernel.to(torch.float32)
        k = k / k.sum().clamp_min(1e-12)                      # chuẩn hóa: sum = 1
        self.register_buffer("k", k.view(1, 1, kh, kw))
        self.register_buffer("k_adj", torch.flip(self.k, dims=(-1, -2)))
        self.pad = (kw // 2, kw // 2, kh // 2, kh // 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:        # B x
        xp = F.pad(x, self.pad, mode="constant", value=0.0)
        return F.conv2d(xp, self.k)

    def adjoint(self, r: torch.Tensor) -> torch.Tensor:        # B^T r
        rp = F.pad(r, self.pad, mode="constant", value=0.0)
        return F.conv2d(rp, self.k_adj)

    def grad_data(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Gradient hạng dữ liệu  B^T (B x - y)  (đơn điệu, gradient của
        1/2||Bx - y||^2)."""
        return self.adjoint(self.forward(x) - y)


def gaussian_kernel(ksize: int = 9, sigma: float = 1.6) -> torch.Tensor:
    ax = torch.arange(ksize, dtype=torch.float32) - (ksize - 1) / 2
    g = torch.exp(-(ax ** 2) / (2 * sigma ** 2))
    k = torch.outer(g, g)
    return k / k.sum()


def motion_kernel(length: int = 9, angle_deg: float = 30.0) -> torch.Tensor:
    """Nhân mờ chuyển động (xấp xỉ một đoạn thẳng)."""
    ksize = length if length % 2 == 1 else length + 1
    k = torch.zeros(ksize, ksize)
    c = ksize // 2
    theta = torch.deg2rad(torch.tensor(angle_deg))
    dx, dy = torch.cos(theta).item(), torch.sin(theta).item()
    for t in torch.linspace(-length / 2, length / 2, steps=ksize * 4):
        x = int(round(c + t.item() * dx))
        y = int(round(c + t.item() * dy))
        if 0 <= x < ksize and 0 <= y < ksize:
            k[y, x] = 1.0
    return k / k.sum().clamp_min(1e-12)


# --------------------------------------------------------------------------- #
#  G_phi : mạng regularizer học được, được huấn luyện cho đơn điệu            #
# --------------------------------------------------------------------------- #
class MonotoneNet(nn.Module):
    """Mạng CNN G_phi. Đơn điệu KHÔNG ép bằng kiến trúc mà được *chứng nhận*
    qua hàm phạt directional-Jacobian (xem ``monotonicity_penalty``), đúng tinh
    thần Belkouchi-Repetti (2024). Dùng activation trơn (ELU) để Jacobian xác
    định tốt theo từng điểm.
    """

    def __init__(self, channels: int = 32, depth: int = 3):
        super().__init__()
        layers = [nn.Conv2d(1, channels, 3, padding=1)]
        for _ in range(depth - 1):
            layers += [nn.ELU(), nn.Conv2d(channels, channels, 3, padding=1)]
        layers += [nn.ELU(), nn.Conv2d(channels, 1, 3, padding=1)]
        self.net = nn.Sequential(*layers)
        # khởi tạo nhỏ để G_phi ban đầu gần 0 (M_phi do hạng dữ liệu chi phối,
        # nên đơn điệu ngay từ đầu huấn luyện).
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.normal_(m.weight, std=1e-2)
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

    def monotonicity_penalty(self, x: torch.Tensor, n_dirs: int = 1,
                             h: float = 1e-2) -> torch.Tensor:
        """Hàm phạt đơn điệu (chứng nhận). Ước lượng v^T J_G v theo sai phân
        hữu hạn cho các hướng ngẫu nhiên v và phạt phần âm:
            penalty = mean( relu( - <G(x + h v) - G(x), v> / h ) ).
        Đạt 0 khi G_phi đơn điệu (J đối xứng nửa xác định dương) theo các hướng.
        """
        gx = self(x)
        pen = x.new_zeros(())
        for _ in range(n_dirs):
            v = torch.randn_like(x)
            v = v / v.flatten(1).norm(dim=1).clamp_min(1e-12).view(-1, 1, 1, 1)
            gxv = self(x + h * v)
            dd = ((gxv - gx) * v).flatten(1).sum(dim=1) / h   # ~ v^T J v
            pen = pen + F.relu(-dd).mean()
        return pen / n_dirs


# --------------------------------------------------------------------------- #
#  rho_theta : trường VÔ HƯỚNG dương học được (preconditioner phụ thuộc x)     #
# --------------------------------------------------------------------------- #
class RhoNet(nn.Module):
    """rho_theta(x) -> vô hướng dương cho mỗi ảnh, chặn trong [rho_min, rho_max].

    Vô hướng (không phải trường theo điểm ảnh) để Mệnh đề 1 đúng: chỉ một số
    dương nhân với toán tử đơn điệu mới bảo toàn tính giả đơn điệu.
    """

    def __init__(self, channels: int = 16, rho_min: float = 0.3,
                 rho_max: float = 3.0):
        super().__init__()
        self.rho_min, self.rho_max = rho_min, rho_max
        self.body = nn.Sequential(
            nn.Conv2d(1, channels, 3, padding=1), nn.ELU(),
            nn.Conv2d(channels, channels, 3, padding=1), nn.ELU(),
            nn.AdaptiveAvgPool2d(1),
        )
        self.head = nn.Linear(channels, 1)
        nn.init.zeros_(self.head.weight)
        # khởi tạo rho ~ 1.0 (bằng với ConstantRho) để so sánh công bằng
        t = (1.0 - rho_min) / (rho_max - rho_min)
        t = min(max(t, 1e-4), 1 - 1e-4)
        nn.init.constant_(self.head.bias, float(torch.log(torch.tensor(t / (1 - t)))))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        s = self.body(x).flatten(1)
        s = self.head(s)                                       # (B, 1)
        rho = self.rho_min + (self.rho_max - self.rho_min) * torch.sigmoid(s)
        return rho.view(-1, 1, 1, 1)                           # vô hướng/ảnh


class ConstantRho(nn.Module):
    """rho hằng số (một tham số học được, chặn trong [rho_min, rho_max]).

    Dùng cho thí nghiệm then chốt: rho_theta học được vs rho HẰNG được tinh
    chỉnh tốt (cùng được huấn luyện đầu-cuối)."""

    def __init__(self, rho_min: float = 0.3, rho_max: float = 3.0,
                 init: float = 1.0):
        super().__init__()
        self.rho_min, self.rho_max = rho_min, rho_max
        # nghịch đảo sigmoid để khởi tạo đúng giá trị init
        t = (init - rho_min) / (rho_max - rho_min)
        t = min(max(t, 1e-4), 1 - 1e-4)
        s0 = torch.log(torch.tensor(t / (1 - t)))
        self.s = nn.Parameter(s0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rho = self.rho_min + (self.rho_max - self.rho_min) * torch.sigmoid(self.s)
        return rho.view(1, 1, 1, 1).expand(x.shape[0], 1, 1, 1)


# --------------------------------------------------------------------------- #
#  F_theta = rho_theta * M_phi                                                #
# --------------------------------------------------------------------------- #
class CostOperator(nn.Module):
    """Toán tử chi phí F_theta(x) = rho_theta(x) * (B^T(Bx - y) + G_phi(x))."""

    def __init__(self, blur: BlurOperator, G: MonotoneNet, rho: nn.Module):
        super().__init__()
        self.blur, self.G, self.rho = blur, G, rho

    def shell(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """Lớp vỏ đơn điệu M_phi(x) = B^T(Bx - y) + G_phi(x)."""
        return self.blur.grad_data(x, y) + self.G(x)

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return self.rho(x) * self.shell(x, y)
