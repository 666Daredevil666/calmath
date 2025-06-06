import os
os.environ["MPLBACKEND"] = "TkAgg"
import matplotlib.pyplot as plt
from equations import ODES
from ode_methods import euler, rk4, adams_pc4, adaptive
from utils import print_table

def main():
    print("Выберите одно из уравнений:")
    for k, v in ODES.items():
        print(f"{k}: {v[0]}")
    eq = int(input("Номер уравнения: "))
    f = ODES[eq][1]
    exact = ODES[eq][2]
    x0 = float(input("x0: "))
    xn = float(input("xn: "))
    y0 = float(input("y0: "))
    h0 = float(input("Начальный шаг h: "))
    eps = float(input("Точность ε для одношаговых методов: "))
    xs_e, ys_e, h_e, err_e = adaptive(euler, 1, f, x0, y0, xn, h0, eps)
    xs_rk, ys_rk, h_rk, err_rk = adaptive(rk4, 4, f, x0, y0, xn, h0, eps)
    xs_ad, ys_ad = adams_pc4(f, x0, y0, xn, h_rk)
    err_ad = max(abs(ys_ad[i] - exact(xs_ad[i], y0, x0)) for i in range(len(xs_ad)))
    print(f"\nМетод Эйлера: h = {h_e}  |ε| ≈ {err_e}")
    print(f"Рунге-Кутта 4: h = {h_rk} |ε| ≈ {err_rk}")
    print(f"Адамса      : h = {h_rk} |ε| ≈ {err_ad}\n")
    print_table(xs_ad, ys_e, ys_rk, ys_ad, exact, y0, x0)
    plt.plot(xs_e, ys_e, label="Euler")
    plt.plot(xs_rk, ys_rk, label="RK4")
    plt.plot(xs_ad, ys_ad, label="Adams")
    xs_dense = [x0 + i * (xn - x0) / 1000 for i in range(1001)]
    ys_dense = [exact(x, y0, x0) for x in xs_dense]
    plt.plot(xs_dense, ys_dense, label="Exact")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

