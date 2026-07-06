"""CON ĐƯỜNG 2 - PHÉP THỬ QUYẾT ĐỊNH (bước hai): có khoảng cách để học hay không?

Linh hồn: một bài toán đáng theo phải có KHOẢNG CÁCH LỚN giữa prior thủ công tốt
nhất và mức trần mà prior học được đạt được. Nếu khoảng cách nhỏ, dù mô hình tinh
xảo đến đâu cũng không tạo được đóng góp đáng đăng. Vì vậy việc đầu tiên là ĐO
khoảng cách này trên ảnh kết cấu giàu (nơi TV yếu), KHÔNG phải viết mô hình.

Đo ba mức trên cùng tập kiểm tra, cùng cách đo (PSNR ảnh trong [0,1]):
  Mức 1 - prior thủ công TỐT NHẤT: ràng buộc TV giải tới hội tụ, bán kính dò tốt
          nhất theo từng ảnh (oracle) -> đối thủ phải vượt.
  Mức 2 - TRẦN của việc học: một mạng khôi phục học sâu (DnCNN, học phần dư) huấn
          luyện đầu-cuối -> mức trần mà việc học có thể đạt trên bài toán này.
  Mức 3 - đường đáy bắt lỗi đo đạc: ảnh suy biến đầu vào + nghiệm bình phương tối
          thiểu không prior. Thứ tự đúng phải là: đáy <= TV <= học.

TIÊU CHÍ ĐẶT TRƯỚC: gap = PSNR(mức 2) - PSNR(mức 1).
  gap >= GAP_PASS (1.0 dB)  -> ĐẠT: bài toán có chỗ cho đóng góp học được, đi tiếp bước 3.
  gap <  GAP_PASS           -> KHÔNG ĐẠT: đổi bài toán hoặc dừng (đừng viết mô hình).

Chạy:  python pivot_decisive_test.py [--quick] [--device cpu|cuda] [--noise f]
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from statistics import mean, pstdev

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import torch
import torch.nn as nn
import torch.nn.functional as F

from pie_net.constraints import TVBallConstraint, tv_isotropic
from pie_net.data import make_texture_patches, degrade
from pie_net.metrics import psnr, ssim
from pie_net.operators import BlurOperator, gaussian_kernel, motion_kernel

RESULTS = "results"
GAP_PASS = 1.0        # ngưỡng đặt trước (dB): mức 2 phải hơn mức 1 ít nhất chừng này


# --------------------------------------------------------------------------- #
#  Mức 2 - mạng khôi phục học sâu (DnCNN, học phần dư) = trần của việc học      #
# --------------------------------------------------------------------------- #
class DnCNN(nn.Module):
    def __init__(self, ch: int = 64, depth: int = 10):
        super().__init__()
        layers = [nn.Conv2d(1, ch, 3, padding=1), nn.ReLU(inplace=True)]
        for _ in range(depth - 2):
            layers += [nn.Conv2d(ch, ch, 3, padding=1),
                       nn.BatchNorm2d(ch), nn.ReLU(inplace=True)]
        layers += [nn.Conv2d(ch, 1, 3, padding=1)]
        self.net = nn.Sequential(*layers)

    def forward(self, y):
        return y - self.net(y)            # học phần dư: x_hat = y - residual


def train_restoration(blur, x_train, device, seed, noise, epochs, batch=16,
                      lr=1e-3, depth=10):
    torch.manual_seed(seed)
    net = DnCNN(depth=depth).to(device).train()
    x_train = x_train.to(device)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    n = x_train.shape[0]
    for ep in range(epochs):
        perm = torch.randperm(n, device=device)
        for i in range(0, n, batch):
            xb = x_train[perm[i:i + batch]]
            yb = degrade(xb, blur, noise_std=noise)
            loss = F.mse_loss(net(yb), xb)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
    return net.eval()


# --------------------------------------------------------------------------- #
#  Mức 1 - prior thủ công TV tốt nhất (giải tới hội tụ, bán kính dò tốt nhất)  #
# --------------------------------------------------------------------------- #
@torch.no_grad()
def solve_tv(blur, y, tau, K_outer, m_inner, lam=1.0):
    """Chiếu - gradient trên quả cầu TV, giải tới hội tụ (K_outer lớn, chiếu khá
    chính xác m_inner bước, khởi tạo ấm)."""
    cons = TVBallConstraint(tau=tau, box=(0.0, 1.0))
    x = blur.adjoint(y).clamp(0, 1)
    state = None
    for _ in range(K_outer):
        v = x - lam * blur.adjoint(blur(x) - y)
        res = cons.project(v, tol=1e-5, max_inner=m_inner, state=state)
        x, state = res.x, res.state
    return x.clamp(0, 1)


@torch.no_grad()
def best_tv(blur, y, x_clean, fracs, K_outer, m_inner):
    """Dò bán kính tau = frac * TV(ảnh sạch) theo từng ảnh (oracle), lấy frac cho
    PSNR tốt nhất -> prior thủ công MẠNH NHẤT có thể."""
    tv_clean = tv_isotropic(x_clean)
    best = None
    for f in fracs:
        xr = solve_tv(blur, y, f * tv_clean, K_outer, m_inner)
        p = psnr(xr, x_clean)
        if best is None or p > best[1]:
            best = (f, p, xr)
    return best                                   # (frac, psnr, recon)


@torch.no_grad()
def solve_l2(blur, y, steps=80, lam=1.0):
    """Nghiệm bình phương tối thiểu không prior (gradient hạng dữ liệu + chặn hộp)."""
    x = blur.adjoint(y).clamp(0, 1)
    for _ in range(steps):
        x = (x - lam * blur.adjoint(blur(x) - y)).clamp(0, 1)
    return x


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--blur", choices=["gauss", "motion"], default="gauss")
    ap.add_argument("--noise", type=float, default=0.05)
    ap.add_argument("--ksize", type=int, default=7, help="cỡ nhân mờ Gauss")
    ap.add_argument("--sigma", type=float, default=1.0, help="độ rộng mờ Gauss (nhẹ -> giữ kết cấu)")
    args = ap.parse_args()

    os.makedirs(RESULTS, exist_ok=True)
    dev = args.device

    if args.quick:
        patch, n_train, n_test = 64, 80, 8
        epochs, depth, seeds = 15, 6, [0]
        fracs = [0.5, 0.7, 0.9]
        K_outer, m_inner = 120, 30
    else:
        patch, n_train, n_test = 96, 800, 24
        epochs, depth, seeds = 80, 12, [0, 1, 2]
        fracs = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        K_outer, m_inner = 250, 50

    print("=" * 80)
    blur_desc = (f"gauss({args.ksize},{args.sigma})" if args.blur == "gauss"
                 else "motion(9,30)")
    print(f"PHÉP THỬ QUYẾT ĐỊNH (con đường 2) | ảnh kết cấu | device={dev} | "
          f"blur={blur_desc} | noise={args.noise}")
    print(f"  quy mô: patch={patch} n_train={n_train} n_test={n_test} | "
          f"DnCNN depth={depth} epochs={epochs} seeds={seeds}")
    print(f"  TIÊU CHÍ ĐẶT TRƯỚC: ĐẠT nếu PSNR(học) - PSNR(TV tốt nhất) >= {GAP_PASS} dB")
    print("=" * 80)

    x_train, x_test = make_texture_patches(patch=patch, n_train=n_train,
                                           n_test=n_test, seed=1)
    kernel = (gaussian_kernel(args.ksize, args.sigma) if args.blur == "gauss"
              else motion_kernel(9, 30.0))
    blur = BlurOperator(kernel).to(dev)
    x_test = x_test.to(dev)
    y_test = degrade(x_test, blur, noise_std=args.noise, seed=2024)

    # --- Mức 3: đường đáy ---------------------------------------------------- #
    p_degraded = psnr(y_test.clamp(0, 1), x_test)
    x_l2 = solve_l2(blur, y_test)
    p_l2 = psnr(x_l2, x_test)
    print(f"\n[mức 3 - đáy] ảnh suy biến: {p_degraded:.3f} dB | "
          f"bình phương tối thiểu: {p_l2:.3f} dB")

    # --- Mức 1: prior thủ công TV tốt nhất ---------------------------------- #
    t0 = time.time()
    frac, p_tv, x_tv = best_tv(blur, y_test, x_test, fracs, K_outer, m_inner)
    s_tv = ssim(x_tv, x_test)
    print(f"[mức 1 - TV tốt nhất] PSNR {p_tv:.3f} dB | SSIM {s_tv:.3f} | "
          f"bán kính tốt nhất frac={frac} | {time.time()-t0:.1f}s")

    # --- Mức 2: trần của việc học (DnCNN) ----------------------------------- #
    p_learn, s_learn = [], []
    for sd in seeds:
        t0 = time.time()
        net = train_restoration(blur, x_train, dev, sd, args.noise, epochs,
                                depth=depth)
        with torch.no_grad():
            xr = net(y_test).clamp(0, 1)
        p, s = psnr(xr, x_test), ssim(xr, x_test)
        p_learn.append(p); s_learn.append(s)
        print(f"[mức 2 - học] seed={sd}: PSNR {p:.3f} dB | SSIM {s:.3f} | "
              f"{time.time()-t0:.1f}s")
    pl_mean = mean(p_learn); pl_std = pstdev(p_learn) if len(p_learn) > 1 else 0.0
    pl_best = max(p_learn)

    # --- PHÁN QUYẾT --------------------------------------------------------- #
    gap = pl_mean - p_tv
    gap_best = pl_best - p_tv
    passed = gap >= GAP_PASS

    print("\n" + "=" * 80)
    print("KẾT QUẢ")
    print(f"  mức 3 (đáy)            : suy biến {p_degraded:.3f} | L2 {p_l2:.3f} dB")
    print(f"  mức 1 (TV tốt nhất)    : {p_tv:.3f} dB")
    print(f"  mức 2 (trần việc học)  : {pl_mean:.3f} ± {pl_std:.2f} dB "
          f"(tốt nhất {pl_best:.3f})")
    print(f"  KHOẢNG CÁCH học - TV   : {gap:+.3f} dB (theo seed tốt nhất {gap_best:+.3f})")
    # kiểm tra thứ tự đo đạc (bắt lỗi)
    ok_order = p_degraded <= p_tv + 1e-6 and p_l2 <= pl_best + 1e-6
    print(f"  thứ tự đo đạc hợp lệ (đáy <= TV <= học): {'có' if ok_order else 'KHÔNG - kiểm tra lại'}")
    print("=" * 80)

    if passed:
        verdict = (f"ĐẠT - khoảng cách {gap:.2f} dB >= {GAP_PASS} dB: bài toán có chỗ "
                   f"cho prior học được. Đi tiếp bước 3 (xây phần lõi đóng góp).")
    else:
        verdict = (f"KHÔNG ĐẠT - khoảng cách {gap:.2f} dB < {GAP_PASS} dB: bài toán "
                   f"không đủ chỗ cho đóng góp học được. Đổi bài toán hoặc dừng, "
                   f"KHÔNG viết mô hình.")
    print("\n>>> " + verdict)

    with open(f"{RESULTS}/pivot_decisive_{args.blur}.csv", "w", newline="",
              encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["level", "method", "psnr", "note"])
        w.writerow([3, "degraded_input", f"{p_degraded:.4f}", ""])
        w.writerow([3, "least_squares", f"{p_l2:.4f}", ""])
        w.writerow([1, "best_TV", f"{p_tv:.4f}", f"frac={frac}"])
        for sd, p in zip(seeds, p_learn):
            w.writerow([2, "DnCNN", f"{p:.4f}", f"seed={sd}"])
        w.writerow(["", "GAP_learn_minus_TV", f"{gap:.4f}", f"pass={passed}"])
    print(f"-> đã lưu {RESULTS}/pivot_decisive_{args.blur}.csv")


if __name__ == "__main__":
    main()
