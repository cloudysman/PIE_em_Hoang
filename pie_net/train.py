"""WP4 - Huấn luyện đầu-cuối (end-to-end) PIE-Net.

Mất mát = MSE(x^K, x_gt)  +  mu * hàm_phạt_đơn_điệu(G_phi).
Gradient qua lớp chiếu xấp xỉ được tính bằng trải vòng lặp (unroll) - phương án
(a) trong WP2, chắc chắn nhất cho gradient không thiên lệch.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F

from .data import degrade
from .metrics import psnr, ssim
from .solver import PIENet


@dataclass
class TrainCfg:
    epochs: int = 40
    batch: int = 8
    lr: float = 2e-3
    mu_mono: float = 1.0        # trọng số phạt đơn điệu cho G_phi
    noise_std: float = 0.01
    log_every: int = 10
    seed: int = 0


def train(net: PIENet, blur, x_train: torch.Tensor, cfg: TrainCfg,
          device: str = "cpu", verbose: bool = True, forward_fn=None):
    """forward_fn(net, y) -> xhat. Mặc định net(y) (deep unfolding). Truyền
    lambda net, y: net.forward_equilibrium(y, ...) để huấn luyện chế độ cân bằng."""
    if forward_fn is None:
        forward_fn = lambda net, y: net(y)
    torch.manual_seed(cfg.seed)
    net.to(device).train()
    x_train = x_train.to(device)
    opt = torch.optim.Adam(net.parameters(), lr=cfg.lr)
    n = x_train.shape[0]
    history = []

    for ep in range(cfg.epochs):
        perm = torch.randperm(n, device=device)
        tot, tot_mono = 0.0, 0.0
        nb = 0
        for i in range(0, n, cfg.batch):
            idx = perm[i:i + cfg.batch]
            xb = x_train[idx]
            yb = degrade(xb, blur, noise_std=cfg.noise_std)

            xhat = forward_fn(net, yb)
            loss_rec = F.mse_loss(xhat, xb)
            # hàm phạt đơn điệu (chứng nhận) cho G_phi, lấy mẫu tại ảnh khôi phục
            loss_mono = net.cost.G.monotonicity_penalty(xb.detach())
            loss = loss_rec + cfg.mu_mono * loss_mono

            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 5.0)
            opt.step()

            tot += loss_rec.item(); tot_mono += loss_mono.item(); nb += 1

        history.append((tot / nb, tot_mono / nb))
        if verbose and (ep % cfg.log_every == 0 or ep == cfg.epochs - 1):
            with torch.no_grad():
                yb = degrade(x_train[:cfg.batch], blur,
                             noise_std=cfg.noise_std, seed=123)
                xhat = forward_fn(net, yb)
                p = psnr(xhat, x_train[:cfg.batch])
            print(f"  epoch {ep:3d} | rec {tot/nb:.4e} | mono {tot_mono/nb:.3e} "
                  f"| PSNR(train) {p:5.2f} dB")
    return history
