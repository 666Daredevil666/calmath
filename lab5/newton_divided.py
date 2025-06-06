from typing import Sequence, List
import numpy as np

def _dup(x: Sequence[float]) -> None:
    a = np.asarray(x, dtype=float)
    if np.any(np.isclose(np.diff(np.sort(a)), 0.0, atol=1e-12, rtol=0)):
        raise ValueError("duplicate x")

def _table(x: Sequence[float], y: Sequence[float]) -> List[List[float]]:
    _dup(x)
    n = len(x)
    t = [[0.0] * n for _ in range(n)]
    for i in range(n):
        t[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - j):
            t[i][j] = (t[i + 1][j - 1] - t[i][j - 1]) / (x[i + j] - x[i])
    return t

def newton_divided(x: Sequence[float], y: Sequence[float], x_target: float) -> float:
    x = np.asarray(x, dtype=float)
    tab = _table(x, y)
    n = len(x)
    res = tab[0][0]
    prod = 1.0
    for k in range(1, n):
        prod *= (x_target - x[k - 1])
        res += tab[0][k] * prod
    return float(res)
