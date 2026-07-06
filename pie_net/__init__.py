"""PIE-Net: Pseudomonotone Inexact-Projection Equilibrium Networks
for Image Inverse Problems.

Hiện thực hóa (implementation) theo thuyết minh đề tài:
  - WP1 (operators.py): toán tử học được F_theta = rho_theta * M_phi,
    với M_phi(x) = B^T(Bx - y) + G_phi(x) là "lớp vỏ đơn điệu",
    rho_theta là trường vô hướng dương học được  ->  Mệnh đề 1 (giả đơn điệu).
  - WP2 (projection.py, solver.py): thuật toán PIE-Net 4 pha
    (quán tính - chiếu xấp xỉ - hiệu chỉnh phản xạ - trộn độ nhớt) và
    lớp chiếu xấp xỉ khả vi (differentiable inexact projection).
  - WP3 (metrics.py + solver.py): phần dư VI (VI residual) làm bằng chứng
    thực nghiệm cho hội tụ điểm-lặp-cuối (last-iterate, Định lý T2).
  - WP4 (data.py, train.py, run_experiment.py): khử mờ ảnh + ablation,
    thí nghiệm then chốt rho_theta học được vs rho hằng số.
"""

from .operators import BlurOperator, MonotoneNet, RhoNet, ConstantRho, CostOperator
from .projection import inexact_project_box
from .solver import PIENet, Schedules
from .metrics import psnr, ssim, vi_residual

__all__ = [
    "BlurOperator",
    "MonotoneNet",
    "RhoNet",
    "ConstantRho",
    "CostOperator",
    "inexact_project_box",
    "PIENet",
    "Schedules",
    "psnr",
    "ssim",
    "vi_residual",
]
