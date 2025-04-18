# main.py

from functions import (
    func1, func2, func3,   # «обычные»
    func4, func5, func6    # с разрывами
)
from methods import (
    left_rect_method, right_rect_method, mid_rect_method,
    trapezoid_method, simpson_method,
    integrate_with_precision, improper_integral
)

def choose_function():
    print("Функции:")
    print("1) -x^3 - x^2 - 2x + 1")
    print("2) x^2")
    print("3) sin(x)")
    print("4) ln(x)/sqrt(x)            (разрыв в a)")
    print("5) 1/sqrt(1-x)              (разрыв в b)")
    print("6) 1/sqrt(|x-0.5|)          (разрыв внутри)")
    while True:
        try:
            k = int(input("Выберите номер функции: ").strip())
            if k == 1:
                return func1
            if k == 2:
                return func2
            if k == 3:
                return func3
            if k == 4:
                return func4
            if k == 5:
                return func5
            if k == 6:
                return func6
            raise ValueError
        except ValueError:
            print("Неверный ввод.")

def choose_method():
    print("\nМетоды:")
    print("1) Левые прямоугольники")
    print("2) Правые прямоугольники")
    print("3) Средние прямоугольники")
    print("4) Трапеции")
    print("5) Симпсон")
    while True:
        try:
            k = int(input("Номер метода: ").strip())
            if k == 1:
                return left_rect_method, 1, "Левые прямоугольники"
            elif k == 2:
                return right_rect_method, 1, "Правые прямоугольники"
            elif k == 3:
                return mid_rect_method,   2, "Средние прямоугольники"
            elif k == 4:
                return trapezoid_method,  2, "Метод трапеций"
            elif k == 5:
                return simpson_method,    4, "Метод Симпсона"
            raise ValueError
        except ValueError:
            print("Неверный ввод.")

def main():
    print("=== Численное интегрирование (включая несобственные) ===\n")

    f = choose_function()

    while True:
        try:
            a = float(input("\nНижний предел a: ").strip())
            b = float(input("Верхний предел b: ").strip())
            if a == b:
                raise ValueError
            break
        except ValueError:
            print("Введите два различных числа.")

    while True:
        try:
            eps = float(input("Требуемая точность eps (например 1e-6): ").strip())
            if eps <= 0:
                raise ValueError
            break
        except ValueError:
            print("eps должно быть положительным числом.")

    method, p_order, method_name = choose_method()

    impro = input("\nНесобственный интеграл? (y/N) ").strip().lower() == 'y'

    if impro:
        res, n_tot = improper_integral(f, a, b, eps, method, p_order, n_start=4)
        if res is None:
            print("\n>>> Интеграл не существует (расходится).")
            return
        algo_used = "несобственный (с усечением хвоста)"
    else:
        res, n_tot = integrate_with_precision(method, f, a, b, eps, p_order, n_start=4)
        algo_used = "обычный"

    print("\n-------- Результаты --------")
    print(f"Метод:           {method_name}")
    print(f"Алгоритм:        {algo_used}")
    print(f"Интервал:        [{a}, {b}]")
    print(f"eps:             {eps}")
    print(f"Значение I:      {res}")
    print(f"Разбиений n:     {n_tot}")
    print("----------------------------\n")

if __name__ == "__main__":
    main()
