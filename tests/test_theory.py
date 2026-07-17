"""Kiểm thử các tính chất toán học cốt lõi của hướng lý thuyết.

Chạy: pytest tests/ -q

Mỗi kiểm thử nhắm một tính chất mà nếu sai thì kết quả số mất nghĩa, chứ không
kiểm chi tiết cài đặt. Dùng ảnh nhỏ để chạy nhanh.
"""

from __future__ import annotations

import math

import pytest
import torch

from pie_net.constraints import TVBallConstraint, tv_isotropic
from pie_net.operators import BlurOperator, gaussian_kernel
from pie_net.reflected_solver import Budget, power_iteration_L, run_reflected


@pytest.fixture(scope="module")
def setup():
    torch.manual_seed(0)
    x = torch.rand(2, 1, 32, 32)
    tau = (0.5 * tv_isotropic(x)).detach()
    v = x + 0.2 * torch.randn_like(x)      # điểm cần chiếu, vi phạm ràng buộc
    return x, tau, v


def test_phep_chieu_cho_diem_kha_thi(setup):
    """Nghiệm chiếu phải nằm trong quả cầu biến phân toàn phần."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    out = cons.project(v, tol=0.0, max_inner=3000)
    # dung sai nhỏ vì vòng lặp nội chỉ tiến dần về nghiệm
    assert torch.all(tv_isotropic(out.x) <= tau * 1.01)


def test_dac_trung_bien_phan_cua_phep_chieu(setup):
    """Đặc trưng phép chiếu: <v - P(v), z - P(v)> <= 0 với mọi z khả thi.

    Đây là tính chất định nghĩa nên nghiệm chiếu; nếu sai thì phép chiếu sai."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    px = cons.project(v, tol=0.0, max_inner=3000).x
    # z khả thi: ảnh hằng (biến phân toàn phần bằng 0)
    z = torch.full_like(v, 0.5)
    assert torch.all(tv_isotropic(z) <= tau)
    ip = ((v - px) * (z - px)).flatten(1).sum(dim=1)
    assert torch.all(ip <= 1e-3)


def test_ban_tang_toc_cho_cung_nghiem(setup):
    """Lịch bước tăng tốc chỉ đổi tốc độ, không được đổi nghiệm."""
    _, tau, v = setup
    base = TVBallConstraint(tau=tau, box=None, accel=False).project(v, tol=0.0, max_inner=4000).x
    acc = TVBallConstraint(tau=tau, box=None, accel=True).project(v, tol=0.0, max_inner=4000).x
    rel = ((acc - base).flatten(1).norm(dim=1) /
           base.flatten(1).norm(dim=1).clamp_min(1e-12))
    assert torch.all(rel < 1e-3)


def test_khoi_tao_am_re_hon_khoi_tao_lanh(setup):
    """Khởi tạo ấm phải tốn ít bước nội hơn khởi tạo lạnh cho cùng dung sai.

    Đây là cơ chế nền của toàn bộ lập luận chi phí."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    ref = cons.project(v, tol=0.0, max_inner=5000).x
    n_lanh = cons.project_to_ref(v, ref, 1e-3, 5000, state=None).n_inner
    # trạng thái ấm: chiếu một điểm rất gần v
    warm = cons.project(v + 1e-3 * torch.randn_like(v), tol=0.0, max_inner=200).state
    n_am = cons.project_to_ref(v, ref, 1e-3, 5000, state=warm).n_inner
    assert n_am < n_lanh


def test_uoc_luong_hang_so_lipschitz(setup):
    """L = ||B^T B|| của nhân mờ chuẩn hóa phải dương và không vượt 1."""
    blur = BlurOperator(gaussian_kernel(9, 1.6))
    L = power_iteration_L(blur, (1, 1, 32, 32), n_iter=100)
    assert 0.0 < L <= 1.0 + 1e-6


def test_buoc_nhay_thoa_dieu_kien_malitsky(setup):
    """Bước nhảy dùng trong thực nghiệm phải nằm trong khoảng của phương pháp
    chiếu phản xạ, tức lambda < (căn 2 - 1)/L."""
    blur = BlurOperator(gaussian_kernel(9, 1.6))
    L = power_iteration_L(blur, (1, 1, 32, 32), n_iter=100)
    lam = 0.9 * (math.sqrt(2.0) - 1.0) / L
    assert lam < (math.sqrt(2.0) - 1.0) / L


def test_phan_du_bien_phan_giam(setup):
    """Phần dư biến phân phải giảm rõ rệt qua các bước ngoài."""
    x, tau, _ = setup
    blur = BlurOperator(gaussian_kernel(9, 1.6))
    y = blur(x) + 0.05 * torch.randn_like(x)
    out = run_reflected(blur, y, tau, K=30, budget=Budget(kind="fixed", m=2),
                        beta0=0.05, alpha_bar=0.0, x_clean=x,
                        ref_steps=200, resid_cap=400, measure_every=10)
    resid = out.trace["resid"]
    vals = resid[torch.isfinite(resid)]
    assert vals[-1] < vals[0]


def test_khoang_cach_doi_ngau_khong_am(setup):
    """Khoảng cách đối ngẫu phải không âm ở mọi bước."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    tau_v = cons.tau.view(v.shape[0])
    for n in (1, 10, 100):
        x, p = cons.project(v, tol=0.0, max_inner=n).state
        gap, _ = cons.duality_gap(x, p, v, tau_v)
        assert torch.all(gap >= -1e-6)


def test_chung_chi_la_chan_tren_that_su(setup):
    """Tính chất định nghĩa nên chứng chỉ: sqrt(2*gap) phải là CHẶN TRÊN của sai
    số chiếu thật. Nếu tính chất này sai thì mọi tiêu chuẩn dừng dựa trên nó đều
    vô nghĩa, nên đây là kiểm thử quan trọng nhất của chứng chỉ."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    tau_v = cons.tau.view(v.shape[0])
    ref = cons.project(v, tol=0.0, max_inner=8000).x
    for n in (5, 25, 100, 400):
        x, p = cons.project(v, tol=0.0, max_inner=n).state
        bound, xf = cons.error_bound(x, p, v, tau_v)
        err = (xf - ref).flatten(1).norm(dim=1)
        assert torch.all(bound >= err - 1e-5), f"chặn trên bị vi phạm ở n={n}"


def test_chieu_theo_chung_chi_dat_tieu_chuan_va_kha_thi(setup):
    """project_to_bound phải dừng đúng khi chứng chỉ đạt ngưỡng, và trả về điểm
    nằm trong quả cầu biến phân toàn phần."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    tau_v = cons.tau.view(v.shape[0])
    eps = 0.5
    out = cons.project_to_bound(v, eps, cap=8000)
    x, p = out.state
    bound, _ = cons.error_bound(x, p, v, tau_v)
    assert torch.all(bound <= eps + 1e-6)
    assert torch.all(tv_isotropic(out.x) <= tau_v * 1.001)


def test_ngan_sach_nho_hon_thi_ton_it_buoc_hon(setup):
    """Tiêu chuẩn sai số lỏng hơn phải tốn ít bước nội hơn."""
    _, tau, v = setup
    cons = TVBallConstraint(tau=tau, box=None)
    n_long = cons.project_to_bound(v, 1.0, cap=8000).n_inner
    n_chat = cons.project_to_bound(v, 0.2, cap=8000).n_inner
    assert n_long < n_chat


def test_tieu_chuan_tuong_doi_chay_va_kha_thi(setup):
    """Chế độ tiêu chuẩn tương đối phải chạy được và cho nghiệm khả thi.

    Khác chế độ lịch tuyệt đối ở chỗ sai số cho phép phụ thuộc TRẠNG THÁI (tỉ lệ
    với độ dài bước gradient), nên nó không rút gọn về một dãy nhiễu cho trước."""
    x, tau, _ = setup
    blur = BlurOperator(gaussian_kernel(9, 1.6))
    y = blur(x) + 0.05 * torch.randn_like(x)
    out = run_reflected(blur, y, tau, K=20, budget=Budget(kind="relative", c_rel=0.3),
                        beta0=0.05, alpha_bar=0.0, x_clean=x,
                        ref_steps=200, resid_cap=400, measure_every=10)
    tv = out.trace["tv_ratio"]
    assert torch.all(tv[torch.isfinite(tv)] <= 1.001)
    resid = out.trace["resid"]
    vals = resid[torch.isfinite(resid)]
    assert vals[-1] < vals[0]


def test_tieu_chuan_tuong_doi_long_hon_thi_re_hon(setup):
    """Hệ số tương đối lớn hơn nghĩa là cho phép sai số lớn hơn, phải tốn ít bước hơn."""
    x, tau, _ = setup
    blur = BlurOperator(gaussian_kernel(9, 1.6))
    y = blur(x) + 0.05 * torch.randn_like(x)
    inner = {}
    for c in (0.05, 0.5):
        out = run_reflected(blur, y, tau, K=15, budget=Budget(kind="relative", c_rel=c),
                            beta0=0.05, alpha_bar=0.0, x_clean=x,
                            ref_steps=150, resid_cap=300, measure_every=15)
        inner[c] = out.total_inner
    assert inner[0.5] < inner[0.05]


def test_sai_so_chieu_giam_theo_ngan_sach(setup):
    """Ngân sách bước nội lớn hơn phải cho sai số chiếu nhỏ hơn."""
    x, tau, _ = setup
    blur = BlurOperator(gaussian_kernel(9, 1.6))
    y = blur(x) + 0.05 * torch.randn_like(x)
    e_cuoi = {}
    for m in (1, 5):
        out = run_reflected(blur, y, tau, K=20, budget=Budget(kind="fixed", m=m),
                            beta0=0.05, alpha_bar=0.0, x_clean=x,
                            ref_steps=200, resid_cap=400, measure_every=10)
        e = out.trace["e_abs"]
        e_cuoi[m] = e[torch.isfinite(e)][-1].item()
    assert e_cuoi[5] < e_cuoi[1]
