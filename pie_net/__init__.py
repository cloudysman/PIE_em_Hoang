"""PIE-Net: Pseudomonotone Inexact-Projection Equilibrium Networks
for Image Inverse Problems.

Hiện thực hóa (implementation) theo thuyết minh đề tài:
  - WP1 (operators.py): toán tử học được F_theta = rho_theta * M_phi,
    với M_phi(x) = B^T(Bx - y) + G_phi(x) là "lớp vỏ đơn điệu",
    rho_theta là trường vô hướng dương học được  ->  Mệnh đề 1 (giả đơn điệu).
  - WP2 (projection.py, solver.py): thuật toán PIE-Net 4 pha
    (quán tính - chiếu xấp xỉ - hiệu chỉnh kiểu Tseng - trộn độ nhớt) và
    lớp chiếu xấp xỉ khả vi (differentiable inexact projection).
  - WP3 (metrics.py + solver.py): phần dư biến phân (VI residual) dùng để
    quan sát hành vi hội tụ; số liệu chỉ cho thấy phần dư GIẢM, không chứng
    minh phần dư tiến về 0.
  - WP4 (data.py, train.py, run_experiment.py): khử mờ ảnh + ablation,
    thí nghiệm then chốt rho_theta học được vs rho hằng số.

Hướng lý thuyết hiện tại (reflected_solver.py, constraints.py): sơ đồ phản xạ
kiểu Malitsky với phép chiếu xấp xỉ lên quả cầu biến phân toàn phần. Xem README
và thư mục tai_lieu_bai_bao/ để biết trạng thái và các kết quả âm tính đã ghi nhận.
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
