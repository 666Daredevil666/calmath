import os
import matplotlib
if os.environ.get("PYCHARM_HOSTED") == "1":
    matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
from typing import Sequence, Callable, Mapping
from interpolation.lagrange import lagrange

def plot_interpolation(
    x_nodes: Sequence[float],
    y_nodes: Sequence[float],
    intrinsic_f: Callable[[float], float] | None,
    approx_f_values: Mapping[str, float],
    x_target: float
) -> None:
    xs = np.linspace(min(x_nodes), max(x_nodes), 400)

    plt.figure()
    if intrinsic_f is not None:
        plt.plot(xs, [intrinsic_f(x) for x in xs], label="f(x)")

    plt.plot(xs, [lagrange(x_nodes, y_nodes, xi) for xi in xs], label="interpolant")
    plt.scatter(x_nodes, y_nodes, color="black", zorder=5, label="nodes")

    for name, y_val in approx_f_values.items():
        plt.scatter([x_target], [y_val], label=f"{name} @ {x_target:.3g}")

    plt.title("Интерполяция")
    plt.legend()
    plt.grid(True)
    plt.show()
