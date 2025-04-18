import math
from .runge import integrate_with_precision


def _is_finite(value):
    return math.isfinite(value)

def _safe_eval(f, x):
    try:
        return f(x)
    except Exception:
        return float("inf")

def detect_singularity(f, a, b, n_test=10):
    # край a
    if not _is_finite(_safe_eval(f, a + 1e-12)):
        return "left", a
    # край b
    if not _is_finite(_safe_eval(f, b - 1e-12)):
        return "right", b
    # поиск внутреннего
    h = (b - a) / (n_test + 1)
    for i in range(1, n_test + 1):
        x = a + i*h
        if not _is_finite(_safe_eval(f, x)):
            return "inner", x
    return None, None

def improper_integral(f, a, b, eps, method, p, n_start=4):
    kind, c = detect_singularity(f, a, b)
    if kind is None:
        return integrate_with_precision(method, f, a, b, eps, p, n_start)

    max_iter = 20
    delta    = 1e-3
    tail_val = 0.0
    for _ in range(max_iter):
        if kind == "left":
            tail_val = method(f, a, a+delta, n_start)
        elif kind == "right":
            tail_val = method(f, b-delta, b, n_start)
        else:  # "inner"
            tail_val = (
                method(f, c-delta, c,   n_start) +
                method(f, c,       c+delta, n_start)
            )
        if math.isfinite(tail_val) and abs(tail_val) < eps/2:
            break
        delta /= 2.0
    else:
        return None, None

    if kind == "left":
        I_main, n_main = integrate_with_precision(
            method, f, a+delta, b, eps/2, p, n_start)
    elif kind == "right":
        I_main, n_main = integrate_with_precision(
            method, f, a, b-delta, eps/2, p, n_start)
    else:
        I1, n1 = integrate_with_precision(
            method, f, a,     c-delta, eps/4, p, n_start)
        I2, n2 = integrate_with_precision(
            method, f, c+delta, b,     eps/4, p, n_start)
        I_main = I1 + I2
        n_main = n1 + n2

    return I_main + tail_val, n_main
