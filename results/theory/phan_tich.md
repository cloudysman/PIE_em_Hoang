# Phân tích số liệu — sơ đồ phản xạ bốn pha với chiếu xấp xỉ

## Ví dụ giả đơn điệu (không đơn điệu)

| biến thể | chứng chỉ không đơn điệu | phần dư đầu -> cuối | dốc log-log | ghi chú |
|---|---|---|---|---|
| degenerate | -5.5949e-06 | 5.0000e-02 -> 1.2512e-04 | -1.000 |  |
| strong | -2.5037e-06 | 5.0000e-02 -> 1.2505e-04 | -1.000 | dist(x_K, P_C(b))=1.251e-04; hệ số co hình học~0.9966 |

## Mờ gauss

### Độ dốc log-log (nửa cuối quỹ đạo)

| chế độ | dốc delta_k | dốc e_k | dốc phần dư | phần dư cuối | tổng bước nội |
|---|---|---|---|---|---|
| epsconst | -1.974 | 0.010 | -0.001 | 1.018e-01 | 111 |
| exact | -2.194 | 0.086 | -0.035 | 2.902e-02 | 387 |
| m1 | -1.203 | -1.299 | -1.283 | 2.655e-02 | 150 |
| m2 | -1.278 | -1.335 | -1.277 | 1.242e-02 | 300 |
| m5 | -1.522 | -1.503 | -1.467 | 5.920e-03 | 750 |
| mlog | -1.662 | -2.182 | -1.579 | 4.615e-03 | 1428 |

### Tổng tích lũy sai số chiếu e_k (trên điểm đo)

| chế độ | tổng e_k (điểm đo) | số điểm | e_k cuối |
|---|---|---|---|
| epsconst | 2.964 | 31 | 1.010e-01 |
| exact | 0.735 | 31 | 2.822e-02 |
| m1 | 4.966 | 31 | 2.056e-02 |
| m2 | 2.181 | 31 | 6.476e-03 |
| m5 | 0.631 | 31 | 1.190e-03 |
| mlog | 1.890 | 31 | 1.409e-04 |

### Bảng chi phí: tổng bước nội để đạt phần dư <= 3.047e-02

| chế độ | tổng bước nội tới mục tiêu | hệ số so exact |
|---|---|---|
| epsconst | không đạt trong K | - |
| exact | 382 | 1.00x rẻ hơn |
| m1 | 136 | 2.81x rẻ hơn |
| m2 | 152 | 2.51x rẻ hơn |
| m5 | 230 | 1.66x rẻ hơn |
| mlog | 289 | 1.32x rẻ hơn |

## Mờ motion

### Độ dốc log-log (nửa cuối quỹ đạo)

| chế độ | dốc delta_k | dốc e_k | dốc phần dư | phần dư cuối | tổng bước nội |
|---|---|---|---|---|---|
| epsconst | -1.981 | 0.007 | -0.001 | 1.403e-01 | 442 |
| exact | -8.404 | 0.296 | -0.119 | 2.916e-02 | 1688 |
| m1 | -0.626 | -0.739 | -0.760 | 1.225e-01 | 150 |
| m2 | -1.463 | -0.994 | -1.079 | 2.232e-02 | 300 |
| m5 | -1.658 | -1.494 | -1.516 | 9.028e-03 | 750 |
| mlog | -1.820 | -3.021 | -1.925 | 5.159e-03 | 1428 |

### Tổng tích lũy sai số chiếu e_k (trên điểm đo)

| chế độ | tổng e_k (điểm đo) | số điểm | e_k cuối |
|---|---|---|---|
| epsconst | 4.017 | 31 | 1.395e-01 |
| exact | 0.752 | 31 | 2.830e-02 |
| m1 | 10.532 | 31 | 1.159e-01 |
| m2 | 3.428 | 31 | 1.589e-02 |
| m5 | 1.318 | 31 | 4.130e-03 |
| mlog | 2.537 | 31 | 7.000e-04 |

### Bảng chi phí: tổng bước nội để đạt phần dư <= 3.062e-02

| chế độ | tổng bước nội tới mục tiêu | hệ số so exact |
|---|---|---|
| epsconst | không đạt trong K | - |
| exact | 1684 | 1.00x rẻ hơn |
| m1 | không đạt trong K | - |
| m2 | 232 | 7.26x rẻ hơn |
| m5 | 330 | 5.10x rẻ hơn |
| mlog | 426 | 3.95x rẻ hơn |
