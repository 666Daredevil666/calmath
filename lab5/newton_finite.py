from typing import Sequence, List
import numpy as np

def _eq(arr: Sequence[float], tol: float = 1e-9) -> bool:
    a = np.asarray(arr, dtype=float)
    h = a[1] - a[0]
    return np.allclose(np.diff(a), h, atol=tol, rtol=0)

def finite_difference_table(y: Sequence[float]) -> List[List[float]]:
    n = len(y)
    t: List[List[float]] = [[None] * n for _ in range(n)]
    for i, v in enumerate(y):
        t[i][0] = float(v)
    for j in range(1, n):
        for i in range(n - j):
            t[i][j] = t[i + 1][j - 1] - t[i][j - 1]
    return t

def newton_finite(x: Sequence[float], y: Sequence[float], x_target: float) -> float:
    x = np.asarray(x, dtype=float)
    if len(x) < 2 or not _eq(x):
        raise ValueError("non-equidistant nodes")
    h = x[1] - x[0]
    t = (x_target - x[0]) / h
    table = finite_difference_table(y)
    res = table[0][0]
    fact = 1.0
    prod = 1.0
    for k in range(1, len(x)):
        fact *= k
        prod *= (t - (k - 1))
        res += (prod / fact) * table[0][k]
    return float(res)
