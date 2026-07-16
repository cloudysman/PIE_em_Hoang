"""Sơ đồ PHẢN XẠ BỐN PHA với chiếu xấp xỉ lên quả cầu TV — bản LÝ THUYẾT.

Thuần suy diễn (KHÔNG học): rho = 1, G = 0, F(x) = B^T(B x - y). Một bước ngoài:

    w^k = x^k + alpha_k (x^k - x^{k-1})                      (quán tính)
    r^k = 2 w^k - w^{k-1}                                    (điểm phản xạ kiểu Malitsky;
                                                              F tính MỘT lần / bước, tại r^k)
    y^k = P_D^{eps_k}( w^k - lambda F(r^k) )                 (chiếu XẤP XỈ lên D={TV<=tau},
                                                              Chambolle-Pock, khởi tạo ấm đối ngẫu)
    x^{k+1} = beta_k f(x^k) + (1 - beta_k) y^k               (trộn độ nhớt; f = ánh xạ HẰNG
                                                              về điểm neo x_anchor = ảnh quan sát)

Ràng buộc tham số (theo phản biện):
  - lambda = 0.9 (sqrt(2)-1) / L,  L = ||B^T B|| ước lượng bằng power iteration
    (kernel chuẩn hóa nên L <= 1 nhưng vẫn PHẢI ước lượng, không gán bừa).
  - alpha_k = min(alpha_bar, tau_k / max(||x^k - x^{k-1}||, 1e-12)),
    tau_k = beta_k/(k+1), alpha_bar = 0.3   (bảo đảm alpha_k ||dx|| / beta_k -> 0).
  - beta_k = beta0/(k+1), beta0 mặc định 0.05 (cho phép 0 để ablation).

Chế độ ngân sách bước nội (eps_k điều khiển gián tiếp):
  - "fixed"    : m bước CP cố định (m ∈ {1,2,5}), khởi tạo ấm.
  - "log"      : m_k = ceil(1 + 2 ln(k+1)) — ngân sách tăng CHẬM theo log
                 (điều kiện tổng được sửa đúng, không 'tự động tổng được').
  - "exact"    : ĐỐI CHỨNG chiếu chính xác khởi tạo ấm — chạy vòng nội tới khi
                 sai số ĐO ĐƯỢC so với chiếu tham chiếu <= delta (delta=1e-3).
  - "epsconst" : eps HẰNG (không giảm) — minh họa MỨC SÀN sai số/hội tụ.

Đo đạc mỗi bước ngoài (mọi phép đo tách khỏi chi phí thuật toán):
  - e_k = ||y^k - P_ref(u^k)||, P_ref = Chambolle-Pock ``ref_steps`` (mặc định
    1500) bước, khởi tạo ấm trên luồng trạng thái RIÊNG; kiểm định ổn định:
    tại 3 mốc k đối chiếu 1500 vs 3000 bước, ghi chênh lệch (cột ref_check).
  - delta_k = ||x^{k+1} - x^k|| (dịch chuyển do bước k tạo ra).
  - phần dư biến phân r(x^{k+1}) = ||x^{k+1} - P_hiacc(x^{k+1} - lambda F(x^{k+1}))||
    với P_hiacc có độ chính xác THÍCH NGHI: đích tham chiếu <= (phần dư nhỏ nhất
    đã quan sát)/10 — tránh sàn sai số tham chiếu làm phẳng độ dốc.
  - PSNR (theo từng ảnh), số bước nội của bước k + cộng dồn, TV(y^k)/tau.

Quy mô CPU laptop: ảnh 64–96 px, K=300 (độ dốc) / K=40 (bảng chi phí), float32,
toàn bộ trong torch.no_grad(). BẮT BUỘC box=None (chạy lý thuyết, không kẹp hộp).
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import torch

from .constraints import TVBallConstraint, tv_isotropic
from .operators import BlurOperator


# --------------------------------------------------------------------------- #
#  L = ||B^T B|| bằng power iteration (không gán bừa L=1)                       #
# --------------------------------------------------------------------------- #
@torch.no_grad()
def power_iteration_L(blur: BlurOperator, shape, n_iter: int = 100,
                      device: str = "cpu", dtype=torch.float32,
                      seed: int = 0) -> float:
    """Ước lượng L = ||B^T B|| (chuẩn phổ) trên ảnh kích thước ``shape``
    = (1, 1, H, W). B^T B đối xứng PSD nên power iteration hội tụ về trị riêng
    lớn nhất."""
    g = torch.Generator(device="cpu").manual_seed(seed)
    x = torch.randn(shape, generator=g).to(device=device, dtype=dtype)
    x = x / x.flatten().norm().clamp_min(1e-12)
    L = 1.0
    for _ in range(n_iter):
        z = blur.adjoint(blur(x))
        L = z.flatten().norm().item()
        if L < 1e-20:
            return 1e-20
        x = z / L
    return L


# --------------------------------------------------------------------------- #
#  Chế độ ngân sách bước nội                                                    #
# --------------------------------------------------------------------------- #
@dataclass
class Budget:
    """kind: 'fixed' (m cố định) | 'log' (m_k = ceil(1+2 ln(k+1))) |
    'exact' (chiếu chính xác khởi tạo ấm, sai số đo được <= delta) |
    'epsconst' (eps hằng, không giảm — minh họa mức sàn)."""
    kind: str = "fixed"
    m: int = 2                    # cho kind='fixed'
    delta: float = 1e-3           # cho kind='exact' (sai số tương đối đo được)
    eps_const: float = 5e-3       # cho kind='epsconst' (sai số tương đối HẰNG)
    cap: int = 3000               # trần bước nội cho exact/epsconst

    def label(self) -> str:
        if self.kind == "fixed":
            return f"m{self.m}"
        if self.kind == "log":
            return "mlog"
        if self.kind == "exact":
            return "exact"
        if self.kind == "epsconst":
            return "epsconst"
        raise ValueError(self.kind)

    def fixed_budget_at(self, k: int) -> int:
        """Ngân sách bước nội tại bước ngoài k (0-based) cho fixed/log."""
        if self.kind == "fixed":
            return self.m
        if self.kind == "log":
            return int(math.ceil(1.0 + 2.0 * math.log(k + 1)))
        raise ValueError("chỉ dùng cho kind='fixed'/'log'")


# --------------------------------------------------------------------------- #
#  Chiếu tham chiếu độ chính xác cao THÍCH NGHI (đo phần dư)                    #
# --------------------------------------------------------------------------- #
@torch.no_grad()
def _hiacc_project(cons: TVBallConstraint, v: torch.Tensor, state,
                   target: float, chunk: int = 100, cap: int = 6000):
    """P_hiacc(v): chạy CP theo khối ``chunk`` bước (khởi tạo ấm) tới khi thay
    đổi giữa hai mốc khối liên tiếp <= 0.1*target (mọi ảnh) hoặc chạm cap.
    ``target`` do người gọi đặt = (phần dư nhỏ nhất đã quan sát)/10 — bảo đảm
    sai số tham chiếu nhỏ hơn ÍT NHẤT 10 lần đại lượng cần đo."""
    res = cons.project(v, tol=0.0, max_inner=chunk, state=state)
    x_prev, st, used = res.x, res.state, chunk
    while used < cap:
        res = cons.project(v, tol=0.0, max_inner=chunk, state=st)
        st, used = res.state, used + chunk
        diff = (res.x - x_prev).flatten(1).norm(dim=1).max().item()
        if diff <= 0.1 * target:
            break
        x_prev = res.x
    return res.x, st, used


def _per_image_norm(t: torch.Tensor) -> torch.Tensor:
    return t.flatten(1).norm(dim=1)


def _per_image_psnr(x: torch.Tensor, ref: torch.Tensor) -> torch.Tensor:
    mse = (x.clamp(0, 1) - ref).pow(2).flatten(1).mean(dim=1).clamp_min(1e-12)
    return 10.0 * torch.log10(1.0 / mse)


# --------------------------------------------------------------------------- #
#  Bộ giải phản xạ bốn pha                                                      #
# --------------------------------------------------------------------------- #
@dataclass
class ReflectedResult:
    trace: Dict[str, torch.Tensor]     # mỗi mục: tensor (K, B) — vết theo bước x ảnh
    x_final: torch.Tensor
    lam: float
    L: float
    total_inner: int
    time_alg: float                    # thời gian THUẬT TOÁN (không tính đo đạc)
    time_total: float


@torch.no_grad()
def run_reflected(blur: BlurOperator, y: torch.Tensor, tau: torch.Tensor,
                  K: int, budget: Budget, beta0: float = 0.05,
                  alpha_bar: float = 0.3, lam: Optional[float] = None,
                  x_clean: Optional[torch.Tensor] = None,
                  ref_steps: int = 1000, ref_check_steps: int = 2000,
                  ref_check_ks: Optional[List[int]] = None,
                  resid_chunk: int = 100, resid_cap: int = 3000,
                  resid_target0: float = 1e-3, measure_every: int = 1,
                  accel: bool = False,
                  verbose: bool = False) -> ReflectedResult:
    """Chạy K bước ngoài của sơ đồ phản xạ bốn pha trên quả cầu TV.

    y: (B,1,H,W) ảnh quan sát; tau: (B,) bán kính TV (oracle). x0 = anchor = y.
    BẮT BUỘC box=None trong TVBallConstraint (chạy lý thuyết)."""
    dev, dtype = y.device, y.dtype
    B = y.shape[0]
    # KHÔNG kẹp hộp (chạy lý thuyết).
    # cons: phép chiếu của THUẬT TOÁN. accel=True dùng lịch bước tăng tốc khai thác
    #   tính lồi mạnh của bài toán chiếu; áp cho MỌI chế độ ngân sách, kể cả chiếu
    #   chính xác khởi tạo ấm, nên so sánh chi phí vẫn công bằng.
    # cons_ref: phép chiếu dùng để ĐO (tham chiếu và phần dư), LUÔN dùng bản cơ bản.
    #   Lý do: lịch tăng tốc làm bước nguyên thủy co về không nên ở độ chính xác cao
    #   nó chậm hơn bản cơ bản; phép đo cần độ chính xác cao nên không dùng tăng tốc.
    cons = TVBallConstraint(tau=tau.detach(), box=None, accel=accel)
    cons_ref = TVBallConstraint(tau=tau.detach(), box=None, accel=False)

    if lam is None:
        L = power_iteration_L(blur, (1, 1, y.shape[2], y.shape[3]),
                              n_iter=100, device=dev, dtype=dtype)
        lam = 0.9 * (math.sqrt(2.0) - 1.0) / max(L, 1e-12)
    else:
        L = float("nan")

    if ref_check_ks is None:
        ref_check_ks = sorted({1, max(K // 2, 1), K - 1})

    def F(x):
        return blur.adjoint(blur(x) - y)

    anchor = y.clone()
    x_prev = y.clone()
    x = y.clone()
    w_prev = y.clone()          # w^{-1} := x^0  =>  r^0 = x^0
    alg_state = None            # luồng ấm của phép chiếu THUẬT TOÁN
    ref_state = None            # luồng ấm RIÊNG của chiếu tham chiếu P_ref (đo e_k)
    resid_state = None          # luồng ấm RIÊNG của P_hiacc (đo phần dư)

    total_inner = 0
    r_min_seen = float("inf")   # phần dư nhỏ nhất đã quan sát (điều khiển target)
    keys = ["e_abs", "e_rel", "delta", "resid", "psnr", "inner_k",
            "inner_cum", "tv_ratio", "ref_check", "alpha", "beta", "m_k"]
    tr: Dict[str, List[torch.Tensor]] = {k: [] for k in keys}
    t_alg = 0.0
    t0_total = time.perf_counter()

    for k in range(K):
        beta_k = beta0 / (k + 1.0)
        tau_k = beta_k / (k + 1.0)

        # ------------------- THUẬT TOÁN (tính vào chi phí) ------------------- #
        t0 = time.perf_counter()
        dx = x - x_prev
        ndx = _per_image_norm(dx)                                     # (B,)
        alpha_k = torch.clamp(tau_k / ndx.clamp_min(1e-12), max=alpha_bar)
        w = x + alpha_k.view(B, 1, 1, 1) * dx                         # quán tính
        r = 2.0 * w - w_prev                                          # phản xạ Malitsky
        Fr = F(r)                                                     # F MỘT lần/bước
        u = w - lam * Fr
        t_alg += time.perf_counter() - t0

        # Các phép ĐO ĐẠC đắt (chiếu tham chiếu, chiếu độ chính xác cao) chỉ
        # chạy ở bước đo, TRỪ khi chế độ ngân sách cần x_ref làm đích thuật toán.
        do_measure = (k % measure_every == 0) or (k == K - 1)
        need_ref = budget.kind in ("exact", "epsconst") or do_measure

        # ------------- ĐO ĐẠC: chiếu tham chiếu P_ref(u^k) (e_k) ------------- #
        ref_check = torch.full((B,), float("nan"), device=dev, dtype=dtype)
        x_ref = None
        if need_ref:
            res_ref = cons_ref.project(u, tol=0.0, max_inner=ref_steps, state=ref_state)
            x_ref = res_ref.x
            ref_state = res_ref.state
            if k in ref_check_ks:
                # kiểm định ổn định: chạy tiếp tới ref_check_steps, ghi chênh lệch
                extra = cons_ref.project(u, tol=0.0,
                                         max_inner=ref_check_steps - ref_steps,
                                         state=res_ref.state)
                ref_check = _per_image_norm(extra.x - x_ref)

        # -------------------- THUẬT TOÁN: chiếu xấp xỉ y^k -------------------- #
        t0 = time.perf_counter()
        if budget.kind in ("fixed", "log"):
            m_k = budget.fixed_budget_at(k)
            res = cons.project(u, tol=0.0, max_inner=m_k, state=alg_state)
        elif budget.kind == "exact":
            res = cons.project_to_ref(u, x_ref, budget.delta, budget.cap,
                                      state=alg_state)
            m_k = res.n_inner
        elif budget.kind == "epsconst":
            res = cons.project_to_ref(u, x_ref, budget.eps_const, budget.cap,
                                      state=alg_state)
            m_k = res.n_inner
        else:
            raise ValueError(budget.kind)
        yk = res.x
        alg_state = res.state
        total_inner += res.n_inner
        x_next = beta_k * anchor + (1.0 - beta_k) * yk    # trộn độ nhớt (f hằng)
        t_alg += time.perf_counter() - t0

        # ----------------------------- ĐO ĐẠC ----------------------------- #
        nan_b = torch.full((B,), float("nan"), device=dev, dtype=dtype)
        delta_k = _per_image_norm(x_next - x)                      # rẻ: đo mọi bước
        if do_measure:
            e_abs = _per_image_norm(yk - x_ref)
            e_rel = e_abs / _per_image_norm(x_ref).clamp_min(1e-12)
            # phần dư biến phân tại x^{k+1}, tham chiếu THÍCH NGHI
            target = max(min(resid_target0, r_min_seen / 10.0), 5e-7)
            v_res = x_next - lam * F(x_next)
            p_hi, resid_state, _ = _hiacc_project(cons_ref, v_res, resid_state,
                                                  target, resid_chunk, resid_cap)
            resid = _per_image_norm(x_next - p_hi)
            r_min_seen = min(r_min_seen, resid.min().item())
        else:
            e_abs = e_rel = resid = nan_b
        psnr_i = (_per_image_psnr(x_next, x_clean) if x_clean is not None
                  else nan_b)
        tv_ratio = res.feas / tau.to(dev).view(B)

        tr["e_abs"].append(e_abs)
        tr["e_rel"].append(e_rel)
        tr["delta"].append(delta_k)
        tr["resid"].append(resid)
        tr["psnr"].append(psnr_i)
        tr["inner_k"].append(torch.full((B,), float(res.n_inner)))
        tr["inner_cum"].append(torch.full((B,), float(total_inner)))
        tr["tv_ratio"].append(tv_ratio)
        tr["ref_check"].append(ref_check)
        tr["alpha"].append(alpha_k)
        tr["beta"].append(torch.full((B,), beta_k))
        tr["m_k"].append(torch.full((B,), float(m_k)))

        # ------------------------ cập nhật trạng thái ------------------------ #
        w_prev = w
        x_prev, x = x, x_next

        if verbose and (k % max(K // 10, 1) == 0 or k == K - 1):
            print(f"    k={k:4d} | e_k={e_abs.mean().item():.3e} | "
                  f"resid={resid.mean().item():.3e} | "
                  f"PSNR={psnr_i.mean().item():.2f} dB | "
                  f"inner_k={res.n_inner} | cum={total_inner}")

    trace = {kk: torch.stack([t.detach().cpu().float() for t in vv])
             for kk, vv in tr.items()}
    return ReflectedResult(trace=trace, x_final=x, lam=lam, L=L,
                           total_inner=total_inner, time_alg=t_alg,
                           time_total=time.perf_counter() - t0_total)
