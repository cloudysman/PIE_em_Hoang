"""WP4 - Dữ liệu và mô hình suy biến  y = B x + eps.

Dùng ảnh thật có sẵn trong scikit-image (không cần Internet) để tạo các mảnh
ảnh (patch) huấn luyện/kiểm tra. Bài toán: khử mờ (Gauss / chuyển động) + nhiễu.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
import torch
from skimage import color, data, transform


def _load_gray_images() -> List[np.ndarray]:
    """Một số ảnh xám chuẩn trong skimage, giá trị trong [0, 1]."""
    imgs = []
    for name in ["camera", "coins", "moon", "page", "text", "checkerboard"]:
        try:
            im = getattr(data, name)()
        except Exception:
            continue
        if im.ndim == 3:
            im = color.rgb2gray(im)
        im = im.astype(np.float32)
        im = (im - im.min()) / (im.max() - im.min() + 1e-8)
        imgs.append(im)
    # thêm ảnh màu chuyển xám để đa dạng kết cấu
    for name in ["astronaut", "chelsea", "coffee"]:
        try:
            im = getattr(data, name)()
            im = color.rgb2gray(im).astype(np.float32)
            im = (im - im.min()) / (im.max() - im.min() + 1e-8)
            imgs.append(im)
        except Exception:
            pass
    return imgs


def make_patches(patch: int = 64, n_train: int = 64, n_test: int = 8,
                 seed: int = 0) -> Tuple[torch.Tensor, torch.Tensor]:
    """Trích các patch ngẫu nhiên; tách ảnh nguồn cho train/test (không rò rỉ)."""
    rng = np.random.default_rng(seed)
    imgs = _load_gray_images()
    assert len(imgs) >= 2
    split = max(1, len(imgs) - 2)
    train_src, test_src = imgs[:split], imgs[split:]

    def sample(srcs, n):
        out = []
        for _ in range(n):
            im = srcs[rng.integers(len(srcs))]
            H, W = im.shape
            if H < patch or W < patch:
                im = transform.resize(im, (max(H, patch), max(W, patch)),
                                      anti_aliasing=True)
                H, W = im.shape
            i = rng.integers(0, H - patch + 1)
            j = rng.integers(0, W - patch + 1)
            out.append(im[i:i + patch, j:j + patch])
        arr = np.stack(out)[:, None].astype(np.float32)        # (n,1,P,P)
        return torch.from_numpy(arr)

    return sample(train_src, n_train), sample(test_src, n_test)


def degrade(x: torch.Tensor, blur, noise_std: float = 0.01,
            seed: int | None = None) -> torch.Tensor:
    """Sinh dữ liệu quan sát y = B x + eps."""
    if seed is not None:
        g = torch.Generator(device=x.device).manual_seed(seed)
        eps = torch.randn(x.shape, generator=g, device=x.device) * noise_std
    else:
        eps = torch.randn_like(x) * noise_std
    return blur(x) + eps


# --------------------------------------------------------------------------- #
#  Ảnh KẾT CẤU GIÀU - dùng cho con đường 2 (nơi prior thủ công TV yếu nhất).   #
# --------------------------------------------------------------------------- #
def load_texture_images() -> List[np.ndarray]:
    """Ảnh kết cấu lặp, chi tiết tần số cao (brick/grass/gravel của skimage).
    Đây là lớp ảnh mà ràng buộc TV làm phẳng kết cấu thành mảng trơn -> prior
    thủ công yếu, để prior học được có chỗ chứng minh lợi thế."""
    imgs = []
    for name in ["brick", "grass", "gravel"]:
        try:
            im = getattr(data, name)()
        except Exception:
            continue
        if im.ndim == 3:
            im = color.rgb2gray(im)
        im = im.astype(np.float32)
        im = (im - im.min()) / (im.max() - im.min() + 1e-8)
        imgs.append(im)
    assert len(imgs) >= 2, "cần ít nhất 2 ảnh kết cấu"
    return imgs


def make_texture_patches(patch: int = 96, n_train: int = 200, n_test: int = 24,
                         seed: int = 0, split_row: float = 0.6
                         ) -> Tuple[torch.Tensor, torch.Tensor]:
    """Trích patch từ ảnh kết cấu, tách train/test theo VÙNG KHÔNG GỐI trên cùng
    ảnh: phần trên (split_row) cho train, phần dưới cho test (không rò rỉ pixel)."""
    rng = np.random.default_rng(seed)
    imgs = load_texture_images()
    train_reg = [im[:int(im.shape[0] * split_row)] for im in imgs]
    test_reg = [im[int(im.shape[0] * split_row):] for im in imgs]

    def sample(regions, n):
        out = []
        while len(out) < n:
            im = regions[rng.integers(len(regions))]
            H, W = im.shape
            if H < patch or W < patch:
                continue
            i = rng.integers(0, H - patch + 1)
            j = rng.integers(0, W - patch + 1)
            out.append(im[i:i + patch, j:j + patch])
        arr = np.stack(out)[:, None].astype(np.float32)
        return torch.from_numpy(arr)

    return sample(train_reg, n_train), sample(test_reg, n_test)
