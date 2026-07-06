"""WP4 - Chỉ số đánh giá: PSNR, SSIM, phần dư VI."""

from __future__ import annotations

import torch
from skimage.metrics import structural_similarity as _ssim


@torch.no_grad()
def psnr(x: torch.Tensor, ref: torch.Tensor, data_range: float = 1.0) -> float:
    """PSNR trung bình trên batch (ảnh trong [0, data_range])."""
    mse = (x - ref).clamp(-data_range, data_range).pow(2).flatten(1).mean(dim=1)
    mse = mse.clamp_min(1e-12)
    return (10.0 * torch.log10(data_range ** 2 / mse)).mean().item()


@torch.no_grad()
def ssim(x: torch.Tensor, ref: torch.Tensor, data_range: float = 1.0) -> float:
    """SSIM trung bình trên batch (dùng skimage cho từng ảnh)."""
    xx = x.clamp(0, data_range).cpu().numpy()
    rr = ref.clamp(0, data_range).cpu().numpy()
    vals = []
    for b in range(xx.shape[0]):
        vals.append(_ssim(rr[b, 0], xx[b, 0], data_range=data_range))
    return float(sum(vals) / len(vals))


@torch.no_grad()
def vi_residual(net, x: torch.Tensor, y: torch.Tensor) -> float:
    """Phần dư VI || x - P_D(x - F_theta(x)) || trung bình/ảnh."""
    return net.vi_residual(x, y).item()
