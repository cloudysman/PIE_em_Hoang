"""CON ĐƯỜNG 2 - PHÉP THỬ QUYẾT ĐỊNH v2: sơ đồ chiếu của nhóm THÊM GÌ so với
Plug-and-Play mạnh?

Bài học trước: "prior học thắng TV" không mới (mạng end-to-end đã làm), và "một
prior dùng cho nhiều suy biến" cũng không mới (đó là lời rao của Plug-and-Play).
Nên đối thủ ở đây KHÔNG phải mạng học trực tiếp, mà là Plug-and-Play mạnh. Phần
delta phải là thứ Plug-and-Play thường KHÔNG có: ràng buộc cứng nhất quán dữ liệu
giải bằng vòng lặp nội, cộng kiểm soát vi phạm.

Hai phương pháp dùng CHUNG một denoiser học được D (huấn luyện một lần, khử nhiễu
mức sigma0). Khác nhau ở cách ép dữ liệu:
  Plug-and-Play (dữ liệu MỀM):  x <- D( x - lam * B^T(Bx - y) )
  Của nhóm (dữ liệu CỨNG)    :  x <- P_C( D(x) ),  C = { x : ||Bx - y|| <= eps }
  với P_C giải bằng vòng lặp nội (bisection theo mu + CG, chiếu XẤP XỈ).

Đo ở HAI chế độ:
  khớp : nhiễu test = sigma0 (denoiser đúng cỡ).
  lệch : nhiễu test > sigma0 (denoiser sai cỡ) - nơi dữ liệu cứng có cửa thắng.

TIÊU CHÍ ĐẶT TRƯỚC: của nhóm phải hơn Plug-and-Play >= MARGIN dB (cùng chi phí)
ít nhất ở chế độ lệch, HOẶC đạt cùng PSNR với vi phạm dữ liệu nhỏ hơn rõ rệt.
Nếu không -> lùi về phương án hai (kết quả tầm vừa), không cố lên tạp chí lớn.

Chạy:  python pivot_pnp_test.py [--quick] [--device cpu|cuda]
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import torch
import torch.nn.functional as F

from pie_net.data import make_texture_patches, degrade
from pie_net.metrics import psnr, ssim
from pie_net.operators import BlurOperator, gaussian_kernel
from pivot_decisive_test import DnCNN          # tái dùng kiến trúc denoiser

RESULTS = "results"
MARGIN_DB = 0.3


# --------------------------------------------------------------------------- #
#  prior học được: denoiser Gauss (huấn luyện MỘT lần, không phụ thuộc B)       #
# --------------------------------------------------------------------------- #
def train_denoiser(x_train, device, seed, sigma0, epochs, batch=16, lr=1e-3,
                   depth=12):
    torch.manual_seed(seed)
    net = DnCNN(depth=depth).to(device).train()
    x_train = x_train.to(device)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    n = x_train.shape[0]
    for _ in range(epochs):
        perm = torch.randperm(n, device=device)
        for i in range(0, n, batch):
            xb = x_train[perm[i:i + batch]]
            yb = xb + sigma0 * torch.randn_like(xb)         # nhiễu trắng mức sigma0
            loss = F.mse_loss(net(yb), xb)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
    return net.eval()


# --------------------------------------------------------------------------- #
#  Plug-and-Play mạnh (dữ liệu mềm): forward-backward + denoiser               #
# --------------------------------------------------------------------------- #
@torch.no_grad()
def pnp_pgd(D, blur, y, lam, beta, K=30):
    """Plug-and-Play forward-backward CÓ GIÃN (relaxation) beta để không áp
    denoiser hết cỡ mỗi vòng (tránh oversmooth) - cho đối thủ mạnh, công bằng."""
    x = blur.adjoint(y).clamp(0, 1)
    for _ in range(K):
        step = D(x - lam * blur.adjoint(blur(x) - y))
        x = (x + beta * (step - x)).clamp(0, 1)
    return x


# --------------------------------------------------------------------------- #
#  Của nhóm (dữ liệu cứng): denoiser + chiếu xấp xỉ lên quả cầu nhất quán       #
#  C = { x : ||Bx - y|| <= eps },  P_C giải bằng bisection(mu) + CG (vòng nội). #
# --------------------------------------------------------------------------- #
def _cg(A_apply, b, x0, iters):
    """Giải A x = b bằng CG (iters bước). A đối xứng xác định dương."""
    x = x0
    r = b - A_apply(x)
    p = r.clone()
    rs = (r * r).flatten(1).sum(1).view(-1, 1, 1, 1)
    for _ in range(iters):
        Ap = A_apply(p)
        pAp = (p * Ap).flatten(1).sum(1).view(-1, 1, 1, 1).clamp_min(1e-12)
        a = rs / pAp
        x = x + a * p
        r = r - a * Ap
        rs_new = (r * r).flatten(1).sum(1).view(-1, 1, 1, 1)
        p = r + (rs_new / rs.clamp_min(1e-12)) * p
        rs = rs_new
    return x


@torch.no_grad()
def proj_data_ball(v, blur, y, eps, mu_steps=8, cg_iters=5):
    """Chiếu XẤP XỈ v lên C = {x: ||Bx-y|| <= eps}. Nghiệm có dạng
    x(mu) = (I + mu B^T B)^{-1} (v + mu B^T y); tăng mu tới khi ||Bx-y|| <= eps
    (||Bx(mu)-y|| giảm đơn điệu theo mu). Trả về (x, số_bước_nội)."""
    res0 = (blur(v) - y).flatten(1).norm(dim=1)
    if torch.all(res0 <= eps):
        return v, 0
    mus = torch.logspace(-2, 3, mu_steps)
    x = v
    chosen = v.clone()
    done = res0 <= eps
    used = 0
    for mu in mus:
        mu = float(mu)
        A = lambda z: z + mu * blur.adjoint(blur(z))
        b = v + mu * blur.adjoint(y)
        x = _cg(A, b, x, cg_iters)                          # warm-start qua các mu
        used += cg_iters
        res = (blur(x) - y).flatten(1).norm(dim=1)
        newly = (res <= eps) & (~done)
        if torch.any(newly):
            chosen[newly] = x[newly]
            done = done | newly
        if torch.all(done):
            break
    chosen[~done] = x[~done]                                 # ảnh chưa đạt: lấy mu lớn nhất
    return chosen.clamp(0, 1), used


@torch.no_grad()
def ours(D, blur, y, eps, beta, K=30, mu_steps=8, cg_iters=5):
    """Cùng denoiser, cùng giãn beta như Plug-and-Play; khác DUY NHẤT: dữ liệu ép
    CỨNG bằng chiếu lên quả cầu nhất quán thay vì gradient mềm."""
    x = blur.adjoint(y).clamp(0, 1)
    total_inner = 0
    for _ in range(K):
        step = D(x)
        u = (x + beta * (step - x)).clamp(0, 1)             # bước prior (cùng giãn)
        x, used = proj_data_ball(u, blur, y, eps, mu_steps, cg_iters)  # dữ liệu cứng
        total_inner += used
    return x, total_inner


# --------------------------------------------------------------------------- #
@torch.no_grad()
def data_violation(x, blur, y, eps):
    """Mức vi phạm nhất quán dữ liệu trung bình ||Bx-y|| / eps (<=1 là khả thi)."""
    return ((blur(x) - y).flatten(1).norm(dim=1) / eps).mean().item()


def eval_regime(D, blur, x_test, sigma_test, lam_grid, beta_grid, K, mu_steps,
                cg_iters):
    y = degrade(x_test, blur, noise_std=sigma_test, seed=2024)
    eps = sigma_test * (x_test.shape[2] * x_test.shape[3]) ** 0.5   # Morozov: ||noise||
    eps_t = torch.full((x_test.shape[0],), eps, device=x_test.device)

    # Plug-and-Play: dò (lam, beta) tốt nhất -> cho đối thủ cơ hội MẠNH nhất
    best = None
    for lam in lam_grid:
        for beta in beta_grid:
            xp = pnp_pgd(D, blur, y, lam, beta, K)
            p = psnr(xp, x_test)
            if best is None or p > best[1]:
                best = ((lam, beta), p, xp)
    (lam, beta_p), p_pnp, xp = best
    pnp = {"psnr": p_pnp, "ssim": ssim(xp, x_test), "cfg": (lam, beta_p),
           "viol": data_violation(xp, blur, y, eps_t)}

    # Của nhóm: dò beta tốt nhất (cùng quyền chỉnh denoiser như Plug-and-Play)
    best_o = None
    for beta in beta_grid:
        xo, inner = ours(D, blur, y, eps_t, beta, K, mu_steps, cg_iters)
        p = psnr(xo, x_test)
        if best_o is None or p > best_o[1]:
            best_o = (beta, p, xo, inner)
    beta_o, p_o, xo, inner = best_o
    ours_r = {"psnr": p_o, "ssim": ssim(xo, x_test), "cfg": beta_o,
              "viol": data_violation(xo, blur, y, eps_t), "inner": inner}
    return pnp, ours_r


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--sigma0", type=float, default=0.05, help="mức nhiễu denoiser được huấn luyện")
    args = ap.parse_args()

    os.makedirs(RESULTS, exist_ok=True)
    dev = args.device

    if args.quick:
        patch, n_train, n_test = 64, 120, 8
        epochs, depth, seeds = 12, 6, [0]
        K, mu_steps, cg_iters = 20, 6, 4
        lam_grid, beta_grid = [0.5, 1.0], [0.3, 1.0]
    else:
        patch, n_train, n_test = 96, 800, 24
        epochs, depth, seeds = 60, 12, [0, 1, 2]
        K, mu_steps, cg_iters = 30, 8, 5
        lam_grid, beta_grid = [0.3, 0.5, 0.7, 1.0, 1.5], [0.2, 0.4, 0.7, 1.0]

    sigma0 = args.sigma0
    sigma_stress = 2.0 * sigma0
    print("=" * 84)
    print(f"PHÉP THỬ QUYẾT ĐỊNH v2 (đối thủ = Plug-and-Play mạnh) | device={dev}")
    print(f"  ảnh kết cấu | mờ Gauss(7,1.0) | denoiser huấn luyện ở sigma0={sigma0}")
    print(f"  chế độ khớp: nhiễu={sigma0} | chế độ lệch: nhiễu={sigma_stress}")
    print(f"  quy mô: patch={patch} n_train={n_train} n_test={n_test} | "
          f"depth={depth} epochs={epochs} seeds={seeds} | K={K}")
    print(f"  TIÊU CHÍ: của nhóm hơn Plug-and-Play >= {MARGIN_DB} dB (cùng chi phí) ở "
          f"chế độ lệch, HOẶC cùng PSNR với vi phạm dữ liệu nhỏ hơn rõ rệt")
    print("=" * 84)

    x_train, x_test = make_texture_patches(patch=patch, n_train=n_train,
                                           n_test=n_test, seed=1)
    blur = BlurOperator(gaussian_kernel(7, 1.0)).to(dev)
    x_test = x_test.to(dev)

    rows = []
    agg = {}   # (regime) -> list of (pnp,ours) theo seed
    for regime, sigma in [("khớp", sigma0), ("lệch", sigma_stress)]:
        agg[regime] = []
    for sd in seeds:
        D = train_denoiser(x_train, dev, sd, sigma0, epochs, depth=depth)
        for regime, sigma in [("khớp", sigma0), ("lệch", sigma_stress)]:
            pnp, ourr = eval_regime(D, blur, x_test, sigma, lam_grid, beta_grid,
                                    K, mu_steps, cg_iters)
            agg[regime].append((pnp, ourr))
            print(f"  [seed {sd}] {regime:5s} nhiễu={sigma:.3f} | "
                  f"PnP {pnp['psnr']:.3f} dB (viol {pnp['viol']:.2f}) | "
                  f"nhóm {ourr['psnr']:.3f} dB (viol {ourr['viol']:.2f}) | "
                  f"chênh {ourr['psnr']-pnp['psnr']:+.3f} | nội {ourr['inner']}")

    # tổng hợp
    from statistics import mean, pstdev
    def m(regime, who, key):
        vals = [r[0 if who == "pnp" else 1][key] for r in agg[regime]]
        return mean(vals), (pstdev(vals) if len(vals) > 1 else 0.0)

    print("\n" + "=" * 84)
    print("KẾT QUẢ (trung bình theo seed)")
    print(f"{'chế độ':6} | {'PnP PSNR':>10} {'nhóm PSNR':>10} {'chênh':>8} | "
          f"{'PnP viol':>9} {'nhóm viol':>10}")
    print("-" * 84)
    gaps = {}
    for regime in ("khớp", "lệch"):
        pp, sp = m(regime, "pnp", "psnr")
        po, so = m(regime, "ours", "psnr")
        vp = m(regime, "pnp", "viol")[0]
        vo = m(regime, "ours", "viol")[0]
        gaps[regime] = (po - pp, sp + so, vp, vo)
        print(f"{regime:6} | {pp:7.3f}±{sp:.2f} {po:7.3f}±{so:.2f} {po-pp:>+8.3f} | "
              f"{vp:9.2f} {vo:10.2f}")
    print("=" * 84)

    # PHÁN QUYẾT
    g_str, n_str, vp_str, vo_str = gaps["lệch"]
    win_psnr = g_str >= MARGIN_DB and g_str >= max(n_str, 1e-9)
    # thắng "cùng PSNR, vi phạm nhỏ hơn": chênh PSNR không âm đáng kể VÀ vi phạm thấp hơn nhiều
    win_viol = g_str >= -0.1 and vo_str <= 0.5 * vp_str and vp_str > 1.0
    passed = win_psnr or win_viol

    print("\nPHÁN QUYẾT (trọng tâm: chế độ lệch)")
    print(f"  hơn PSNR ở chế độ lệch: {g_str:+.3f} dB (dao động ±{n_str:.2f}) -> "
          f"{'ĐẠT' if win_psnr else 'KHÔNG'}")
    print(f"  cùng PSNR + vi phạm dữ liệu nhỏ hơn rõ rệt: nhóm {vo_str:.2f} vs "
          f"PnP {vp_str:.2f} -> {'ĐẠT' if win_viol else 'KHÔNG'}")
    if passed:
        verdict = ("ĐẠT - sơ đồ chiếu của nhóm có delta đo được so với Plug-and-Play "
                   "(dữ liệu cứng giúp khi denoiser lệch). Đi tiếp xây phần lõi + lý thuyết.")
    else:
        verdict = ("KHÔNG ĐẠT - không tách được khỏi Plug-and-Play. Lùi về phương án "
                   "hai (kết quả tầm vừa, trung thực), không nhắm tạp chí lớn.")
    print("\n>>> " + verdict)

    with open(f"{RESULTS}/pivot_pnp.csv", "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["regime", "method", "psnr_mean", "psnr_std", "violation"])
        for regime in ("khớp", "lệch"):
            w.writerow([regime, "PnP", f"{m(regime,'pnp','psnr')[0]:.4f}",
                        f"{m(regime,'pnp','psnr')[1]:.4f}", f"{m(regime,'pnp','viol')[0]:.4f}"])
            w.writerow([regime, "ours", f"{m(regime,'ours','psnr')[0]:.4f}",
                        f"{m(regime,'ours','psnr')[1]:.4f}", f"{m(regime,'ours','viol')[0]:.4f}"])
    print(f"-> đã lưu {RESULTS}/pivot_pnp.csv")


if __name__ == "__main__":
    main()
