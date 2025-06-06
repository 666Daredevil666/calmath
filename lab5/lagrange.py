from typing import Sequence
import numpy as np

def lagrange(x: Sequence[float], y: Sequence[float], x_target: float) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    idx = np.where(np.isclose(x_target, x, atol=1e-12, rtol=0))[0]
    if idx.size:
        return float(y[idx[0]])
    n = len(x)
    res = 0.0
    for i in range(n):
        li = 1.0
        for j in range(n):
            if i != j:
                li *= (x_target - x[j]) / (x[i] - x[j])
        res += y[i] * li
    return float(res)
