"""PHÉP KIỂM THÉP - cho mốc 2 (có học) cơ hội tốt nhất để vượt mốc 1.

Chỉ chạy ở m=5 (điểm vận hành ổn định nhất trong phép thử full), với learning
rate thấp hơn (5e-4) và nhiều epoch hơn (40) để loại bỏ khả năng mốc 2 thua chỉ
vì huấn luyện mất ổn định, không phải vì bản chất không thêm giá trị.

Nếu steelman vẫn không cho mốc 2 vượt mốc 1 quá +0.3 dB -> FAIL được chốt chắc.
"""

from __future__ import annotations

import statistics
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import torch

from milestone_test import (build_milestone, train_milestone, eval_milestone,
                            TrainCfg, MARGIN_DB)
from pie_net.data import make_patches
from pie_net.operators import BlurOperator, gaussian_kernel, motion_kernel
from pie_net.tv_solver import TVSchedules

dev = "cuda" if torch.cuda.is_available() else "cpu"
patch, n_train, n_test, K, m = 96, 40, 6, 12, 5
tau_frac, noise = 0.55, 0.05
LR, EPOCHS, SEEDS = 5e-4, 40, [0, 1, 2]

print(f"PHÉP KIỂM THÉP | mốc 2 @ m={m} | lr={LR} epochs={EPOCHS} seeds={SEEDS} "
      f"| device={dev}")
print(f"ngưỡng thắng: mốc 2 phải vượt mốc 1 quá +{MARGIN_DB} dB\n")

for blur_kind in ("gauss", "motion"):
    x_train, x_test = make_patches(patch=patch, n_train=n_train,
                                   n_test=n_test, seed=1)
    kernel = gaussian_kernel(9, 1.6) if blur_kind == "gauss" else motion_kernel(9, 30.0)
    blur = BlurOperator(kernel).to(dev)
    sched = TVSchedules(K=K, m=m, lam0=1.0, learn_lambda=True)

    # mốc 1 tham chiếu (ổn định, 1 hạt giống là đủ)
    net1 = build_milestone(blur, sched, 1, dev)
    train_milestone(net1, blur, x_train, tau_frac,
                    TrainCfg(epochs=20, lr=2e-3, noise_std=noise), dev, 0)
    p1 = eval_milestone(net1, blur, x_test, tau_frac, noise, dev)["psnr"]

    # mốc 2 steelman
    cfg2 = TrainCfg(epochs=EPOCHS, lr=LR, noise_std=noise)
    p2 = []
    for sd in SEEDS:
        net2 = build_milestone(blur, sched, 2, dev)
        train_milestone(net2, blur, x_train, tau_frac, cfg2, dev, sd)
        ev = eval_milestone(net2, blur, x_test, tau_frac, noise, dev)
        p2.append(ev["psnr"])
        print(f"  [{blur_kind}] mốc 2 seed={sd}: PSNR {ev['psnr']:.3f} | "
              f"TV/tau {ev['feas_pol']:.3f}")

    mean2 = statistics.mean(p2)
    std2 = statistics.pstdev(p2) if len(p2) > 1 else 0.0
    best2 = max(p2)
    win = best2 - p1 >= MARGIN_DB
    print(f"  [{blur_kind}] mốc 1 = {p1:.3f} | mốc 2 = {mean2:.3f}±{std2:.2f} "
          f"(tốt nhất {best2:.3f}) | chênh trung bình {mean2-p1:+.3f}, "
          f"chênh tốt nhất {best2-p1:+.3f} -> {'VƯỢT' if win else 'KHÔNG VƯỢT'}\n")

print("DONE")
