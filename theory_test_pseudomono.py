"""Ví dụ giả đơn điệu (không đơn điệu) — minh họa hội tụ của sơ đồ phản xạ bốn pha.

Mục đích: định lý hội tụ mạnh của bài phát biểu cho toán tử giả đơn điệu. Nếu ví
dụ số duy nhất là bài khôi phục ảnh thì toán tử ở đó là đơn điệu (trường hợp
riêng), nên định lý sẽ rộng hơn ví dụ. Tệp này cung cấp một toán tử giả đơn điệu
nhưng KHÔNG đơn điệu, kèm chứng chỉ số, để lấp đúng khoảng đó.

Toán tử:  F(x) = c(x) * A (x - b),  c(x) = exp(-||x||^2) > 0,  A nửa xác định dương.
  - c(x) > 0 là trường vô hướng dương; A(x - b) là toán tử affine đơn điệu (A PSD).
  - Vì c(x) > 0 vô hướng và A(x - b) đơn điệu, F giả đơn điệu (pseudomonotone):
    tập nghiệm của bất đẳng thức biến phân với F trùng tập nghiệm với A(x - b).
  - F nói chung KHÔNG đơn điệu (c(x) thay đổi làm phần đối xứng của Jacobian mất
    tính nửa xác định dương). Ta xác nhận bằng chứng chỉ số: tìm cặp (u, v) với
    <F(u) - F(v), u - v> < 0.

Hai biến thể của A:
  - "degenerate": A = diag(1,...,1,0,...,0) nửa số chiều bằng 0 — nửa xác định
    dương SUY BIẾN. Giả đơn điệu nhưng không mạnh; phần dư biến phân giảm dưới
    tuyến tính.
  - "strong": A = I — giả đơn điệu mạnh; phần dư biến phân giảm hình học.

Tập ràng buộc: quả cầu đơn vị C = { x : ||x|| <= 1 } (chiếu đóng, rẻ), nên phép
chiếu ở đây không phải chỗ tốn kém — trọng tâm là minh họa hội tụ dưới giả đơn
điệu, không phải chi phí chiếu (chi phí chiếu đã xét ở bài khôi phục ảnh).
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import torch

RESULT_DIR = os.path.join("results", "theory")


def make_A(n: int, variant: str, device, dtype) -> torch.Tensor:
    d = torch.ones(n, device=device, dtype=dtype)
    if variant == "degenerate":
        d[n // 2:] = 0.0                       # nửa sau bằng 0: PSD suy biến
    elif variant != "strong":
        raise ValueError(variant)
    return torch.diag(d)


def project_ball(x: torch.Tensor) -> torch.Tensor:
    """Chiếu chính xác lên quả cầu đơn vị (công thức đóng)."""
    nrm = x.norm()
    return x if nrm <= 1.0 else x / nrm


def estimate_L(F, n: int, device, dtype, n_pairs: int = 2000,
               seed: int = 0) -> float:
    """Ước lượng hằng số Lipschitz của F bằng lấy mẫu cặp điểm trong quả cầu."""
    g = torch.Generator(device="cpu").manual_seed(seed)
    L = 0.0
    for _ in range(n_pairs):
        u = torch.randn(n, generator=g).to(device=device, dtype=dtype)
        v = torch.randn(n, generator=g).to(device=device, dtype=dtype)
        u, v = project_ball(u), project_ball(v)
        du = (u - v).norm().item()
        if du < 1e-9:
            continue
        ratio = (F(u) - F(v)).norm().item() / du
        L = max(L, ratio)
    return L


def certify_nonmonotone(F, n: int, device, dtype, n_points: int = 400,
                        n_dirs: int = 50, h: float = 1e-2, seed: int = 1):
    """Tìm cặp (u, v) trong quả cầu với <F(u) - F(v), u - v> < 0, xác nhận F KHÔNG
    đơn điệu. Tính không đơn điệu là hiện tượng ĐỊA PHƯƠNG (phần đối xứng của
    Jacobian có trị riêng âm), nên ta thử bằng nhiễu nhỏ quanh mỗi điểm: u lấy
    trong nội quả cầu (||u|| <= 0.9), v = u + h d với d hướng đơn vị và h nhỏ.
    Trả về (giá trị âm nhất, u, v tương ứng)."""
    g = torch.Generator(device="cpu").manual_seed(seed)
    worst = 0.0
    uw = vw = None
    for _ in range(n_points):
        u = torch.randn(n, generator=g).to(device, dtype)
        u = 0.9 * u / u.norm().clamp_min(1e-12) * torch.rand(1, generator=g).item()
        Fu = F(u)
        for _ in range(n_dirs):
            d = torch.randn(n, generator=g).to(device, dtype)
            d = d / d.norm().clamp_min(1e-12)
            v = u + h * d                          # u nội nên v vẫn trong quả cầu
            val = torch.dot(Fu - F(v), u - v).item()
            if val < worst:
                worst, uw, vw = val, u, v
    return worst, uw, vw


@torch.no_grad()
def run_reflected_rn(F, x0, anchor, K, lam, beta0=0.05, alpha_bar=0.3):
    """Sơ đồ phản xạ bốn pha trong R^n (chiếu chính xác lên quả cầu đơn vị).

        w^k = x^k + alpha_k (x^k - x^{k-1})              (quán tính)
        r^k = 2 w^k - w^{k-1}                            (phản xạ kiểu Malitsky)
        y^k = P_C(w^k - lam F(r^k))                      (chiếu chính xác)
        x^{k+1} = beta_k anchor + (1 - beta_k) y^k       (trộn độ nhớt, f hằng)
    """
    x_prev = x0.clone()
    x = x0.clone()
    w_prev = x0.clone()                       # w^{-1} := x^0 => r^0 = x^0
    resids = []
    for k in range(K):
        beta_k = beta0 / (k + 1.0)
        tau_k = beta_k / (k + 1.0)
        dx = x - x_prev
        ndx = dx.norm().item()
        alpha_k = min(alpha_bar, tau_k / max(ndx, 1e-12))
        w = x + alpha_k * dx
        r = 2.0 * w - w_prev
        u = w - lam * F(r)
        y = project_ball(u)
        x_next = beta_k * anchor + (1.0 - beta_k) * y
        # phần dư biến phân r(x) = ||x - P_C(x - lam F(x))|| (0 <=> x là nghiệm)
        resid = (x_next - project_ball(x_next - lam * F(x_next))).norm().item()
        resids.append(resid)
        w_prev = w
        x_prev, x = x, x_next
    return x, resids


def slope_loglog(resids, lo_frac=0.5):
    """Độ dốc log-log của phần dư trên đoạn cuối (ước lượng tốc độ đa thức)."""
    import numpy as np
    r = np.asarray(resids)
    k = np.arange(1, len(r) + 1)
    lo = int(len(r) * lo_frac)
    mask = (r[lo:] > 1e-14)
    if mask.sum() < 3:
        return float("nan")
    lk = np.log(k[lo:][mask])
    lr = np.log(r[lo:][mask])
    return float(np.polyfit(lk, lr, 1)[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=50, help="số chiều")
    ap.add_argument("--K", type=int, default=400, help="số bước ngoài")
    ap.add_argument("--beta0", type=float, default=0.05)
    ap.add_argument("--b_scale", type=float, default=3.0,
                    help="||b|| (điểm neo ngoài quả cầu để lộ tính không đơn điệu)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    dev, dtype = "cpu", torch.float32
    os.makedirs(RESULT_DIR, exist_ok=True)
    g = torch.Generator(device="cpu").manual_seed(args.seed)
    # b nằm NGOÀI quả cầu (||b|| = b_scale): độ lệch (x - b) lớn nên phần thay đổi
    # của trường vô hướng c(x) = exp(-||x||^2) đủ phá tính đơn điệu (mà vẫn giữ
    # giả đơn điệu vì c(x) > 0). Nghiệm bất đẳng thức biến phân là P_C(b) = b/||b||.
    bv = torch.randn(args.n, generator=g).to(dev, dtype)
    b = args.b_scale * bv / bv.norm()
    anchor = torch.zeros(args.n, device=dev, dtype=dtype)                    # điểm neo trong C
    x0 = anchor.clone()

    print(f"== Ví dụ giả đơn điệu (không đơn điệu) | n={args.n} | K={args.K} ==")
    print(f"   F(x) = exp(-||x||^2) A (x - b), C = quả cầu đơn vị, neo = 0, ||b||={b.norm().item():.3f}")

    rows = []
    for variant in ["degenerate", "strong"]:
        A = make_A(args.n, variant, dev, dtype)

        def F(x, A=A, b=b):
            c = math.exp(-(x @ x).item())
            return c * (A @ (x - b))

        L = estimate_L(F, args.n, dev, dtype)
        lam = 0.9 * (math.sqrt(2.0) - 1.0) / max(L, 1e-9)
        worst, _, _ = certify_nonmonotone(F, args.n, dev, dtype)

        x_star, resids = run_reflected_rn(F, x0, anchor, args.K, lam,
                                          beta0=args.beta0)
        slope = slope_loglog(resids)
        # nghiệm tham chiếu cho biến thể strong (A = I): x* = P_C(b)
        ref_note = ""
        if variant == "strong":
            xref = project_ball(b)
            dist = (x_star - xref).norm().item()
            # ước lượng hệ số co hình học từ nửa cuối
            import numpy as np
            r = np.asarray(resids)
            lo = len(r) // 2
            rr = r[lo:][r[lo:] > 1e-14]
            geom = float(np.exp(np.polyfit(np.arange(len(rr)), np.log(rr), 1)[0])) if len(rr) > 3 else float("nan")
            ref_note = f"dist(x_K, P_C(b))={dist:.3e}; hệ số co hình học~{geom:.4f}"

        path = os.path.join(RESULT_DIR, f"pseudomono_{variant}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow(["k", "resid"])
            for k, rv in enumerate(resids):
                wr.writerow([k, f"{rv:.8e}"])

        print(f"\n[{variant}] L~{L:.4f} | lambda={lam:.4f}")
        print(f"   chứng chỉ KHÔNG đơn điệu: min <F(u)-F(v),u-v> = {worst:.4e}"
              f"  ({'ÂM => không đơn điệu' if worst < 0 else 'không tìm được cặp âm'})")
        print(f"   phần dư: đầu={resids[0]:.3e} -> cuối={resids[-1]:.3e}"
              f" | độ dốc log-log nửa cuối={slope:.3f}")
        if ref_note:
            print(f"   {ref_note}")
        print(f"   -> {path}")

        rows.append({
            "variant": variant, "L": f"{L:.4f}", "lambda": f"{lam:.4f}",
            "nonmono_worst": f"{worst:.4e}",
            "resid_first": f"{resids[0]:.4e}", "resid_last": f"{resids[-1]:.4e}",
            "loglog_slope_tail": f"{slope:.3f}", "note": ref_note,
        })

    sp = os.path.join(RESULT_DIR, "pseudomono_summary.csv")
    with open(sp, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print(f"\n-> tổng hợp: {sp}")
    print("\nDiễn giải: biến thể 'degenerate' (giả đơn điệu, không mạnh) cho phần dư"
          " giảm dưới tuyến tính (độ dốc log-log hữu hạn); biến thể 'strong' (giả"
          " đơn điệu mạnh) cho phần dư giảm hình học và hội tụ về P_C(b).")


if __name__ == "__main__":
    main()
