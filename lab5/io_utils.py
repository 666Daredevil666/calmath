import csv
import math
from pathlib import Path
from typing import List, Tuple, Callable

_BUILTIN_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "exp": math.exp,
    "log": math.log,
}

def _read_keyboard() -> Tuple[List[float], List[float]]:
    n = int(input("Сколько узлов? "))
    x, y = [], []
    for i in range(n):
        x.append(float(input(f"x[{i}] = ")))
        y.append(float(input(f"y[{i}] = ")))
    return x, y

def _read_from_file() -> Tuple[List[float], List[float]]:
    name = input("Имя CSV-файла: ").strip()
    p = Path(name).expanduser()
    if not p.is_absolute():
        p = Path("data") / p
    if not p.exists():
        raise FileNotFoundError(f"{p} не найден")
    x, y = [], []
    with p.open(newline="") as f:
        for row in csv.reader(f, delimiter=";"):
            if row:
                x.append(float(row[0].replace(",", ".")))
                y.append(float(row[1].replace(",", ".")))
    return x, y

def _generate_from_function() -> Tuple[List[float], List[float], Callable[[float], float]]:
    f = _BUILTIN_FUNCTIONS[input(f"Функция {list(_BUILTIN_FUNCTIONS)}: ").strip().lower()]
    a = float(input("a = "))
    b = float(input("b = "))
    n = int(input("n ≥ 2: "))
    h = (b - a) / (n - 1)
    xs = [a + i * h for i in range(n)]
    ys = [f(x) for x in xs]
    return xs, ys, f

def acquire_dataset():
    print("1 — клавиатура\n2 — csv-файл\n3 — встроенная функция")
    m = input("Выбор: ").strip()
    if m == "1":
        x, y = _read_keyboard()
        return x, y, None
    if m == "2":
        x, y = _read_from_file()
        return x, y, None
    if m == "3":
        return _generate_from_function()
    raise ValueError("неверный выбор")

def ask_target_x() -> float:
    return float(input("x* = "))
