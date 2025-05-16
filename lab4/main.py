import argparse
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np

import approximations as appr
import io_utils as io


#вспомогательное пояснение R²
def interpret_r2(r2: float) -> str:
    if np.isnan(r2):
        return "R² не определён"
    if r2 >= 0.9:
        return "отличное согласие"
    if r2 >= 0.75:
        return "хорошее согласие"
    if r2 >= 0.5:
        return "удовлетворительное согласие"
    return "слабое согласие"


#построение графика
def _plot_models(x, y, models):
    xmin, xmax = x.min(), x.max()
    dx = 0.05 * (xmax - xmin)   #запас
    xs = np.linspace(xmin - dx, xmax + dx, 400)

    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, c="black", label="исходные точки")

    for m in models:
        if m.name == "Экспоненциальная":
            ys = m.coef[0] * np.exp(m.coef[1] * xs)
        elif m.name == "Логарифмическая":
            ys = m.coef[0] + m.coef[1] * np.log(xs)
            ys[np.isinf(ys) | np.isnan(ys)] = np.nan
        elif m.name == "Степенная":
            ys = m.coef[0] * xs ** m.coef[1]
        elif m.name.startswith("Полином 3"):
            a, b, c, d = m.coef
            ys = a + b*xs + c*xs**2 + d*xs**3
        elif m.name.startswith("Полином 2"):
            a, b, c = m.coef
            ys = a + b*xs + c*xs**2
        else:  # линейная
            a, b = m.coef
            ys = a + b*xs
        plt.plot(xs, ys, label=f"{m.name} (σ={m.sigma:.3g})")

    plt.title("Аппроксимация (МНК)")
    plt.xlabel("x"), plt.ylabel("y")
    plt.grid(True), plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="ЛР-4: аппроксимация МНК (6 моделей)")
    parser.add_argument("-i", "--input", help="CSV-файл с точками x,y")
    parser.add_argument("-o", "--output", default="results.txt",
                        help="файл текстового отчёта (по умолчанию results.txt)")
    args = parser.parse_args()

    #ввод точек
    try:
        if args.input:
            x, y = io.read_csv(pathlib.Path(args.input))
        else:
            x, y = io.read_console()
        io.validate_points(x, y)
    except Exception as e:
        sys.exit(f"Ошибка ввода точек: {e}")

    print(f"Принято {len(x)} точек.")

    #аппроксимация
    models = appr.fit_all_models(x, y)
    if not models:
        sys.exit("Ни одна модель не применима к этим данным.")

    best = appr.choose_best(models)

    #вывод (коэффициенты + интерпретация R²)
    print("\nРезультаты:")
    for m in models:
        r2_msg = interpret_r2(m.r2)
        line = (f"{m.name:<16} σ={m.sigma:.6g}  R²={m.r2:.6g} "
                f"({r2_msg})  coef=[{m.coef_str()}]")
        if "Pearson r" in m.extra:
            line += f"  r={m.extra['Pearson r']:.6g}"
        print(line)
    print(f"\nЛучшее приближение → {best.name}")

    # --- полный отчёт в файл (с массивами φ(x_i) и ε_i)
    try:
        io.save_report(pathlib.Path(args.output), x, y, models, best.name,
                       r2_interpreter=interpret_r2)
    except Exception as e:
        print(f"Не удалось сохранить отчёт: {e}")

    #график
    _plot_models(x, y, models)


if __name__ == "__main__":
    main()
