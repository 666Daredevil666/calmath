import pathlib
from typing import Tuple, List, Callable
#import matplotlib
#matplotlib.use("TkAgg")
import numpy as np
import pandas as pd

from approximations import ModelResult


#ввод точек
def read_csv(path: pathlib.Path) -> Tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(path, header=None, names=["x", "y"])
    if df.shape[1] != 2:
        raise ValueError("CSV должен содержать ровно 2 столбца (x,y)")
    return df["x"].to_numpy(float), df["y"].to_numpy(float)


def read_console() -> Tuple[np.ndarray, np.ndarray]:
    print("Введите пары x y (пустая строка — конец ввода):")
    pts = []
    while True:
        line = input()
        if not line.strip():
            break
        try:
            pts.append(tuple(map(float, line.split())))
        except Exception:
            print("Неверный формат строки. Повторите.")
    if not pts:
        raise ValueError("Точки не введены")
    x, y = zip(*pts)
    return np.array(x, float), np.array(y, float)


def validate_points(x: np.ndarray, y: np.ndarray, min_n=8, max_n=12):
    if not (min_n <= len(x) <= max_n):
        raise ValueError(f"Нужно от {min_n} до {max_n} точек, сейчас {len(x)}")


#результаты
def save_report(path: pathlib.Path,
                x: np.ndarray,
                y: np.ndarray,
                models: List[ModelResult],
                best_name: str,
                r2_interpreter: Callable[[float], str]):
    with open(path, "w", encoding="utf-8") as f:
        print("Аппроксимация методом наименьших квадратов", file=f)
        print("=" * 60, file=f)

        # краткая сводка
        for m in models:
            msg = r2_interpreter(m.r2)
            line = (f"{m.name:<16} σ={m.sigma:.6g}  R²={m.r2:.6g} "
                    f"({msg})  coef=[{m.coef_str()}]")
            if "Pearson r" in m.extra:
                line += f"  r={m.extra['Pearson r']:.6g}"
            print(line, file=f)

        print("-" * 60, file=f)
        print(f"Лучшее приближение → {best_name}", file=f)

        # развёрнутые таблицы для каждой модели
        for m in models:
            print("\n" + m.name, file=f)
            print(" i      x_i        y_i      φ(x_i)       ε_i", file=f)
            eps = y - m.y_hat
            for i, (xi, yi, fi, ei) in enumerate(zip(x, y, m.y_hat, eps), 1):
                print(f"{i:2d}  {xi:9.5g}  {yi:9.5g}  {fi:11.5g}  {ei:11.5g}",
                      file=f)

    print(f"Отчёт сохранён в {path.resolve()}")
