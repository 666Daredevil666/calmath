import math
import numpy as np

def sign_changes_count(f, a, b, steps=2000):
    xs = np.linspace(a, b, steps+1)
    prev_sign = None
    count = 0
    for x in xs:
        val = f(x)
        s = 1 if val>0 else (-1 if val<0 else 0)
        if prev_sign is not None and s*prev_sign<0:
            count += 1
        if s != 0:
            prev_sign = s
    return count

def check_interval_for_root(f, a, b):
    c = sign_changes_count(f, a, b)
    return c

def bisection(f, a, b, eps=1e-3, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa*fb > 0:
        raise ValueError("На [a,b] нет гарантии одного корня (f(a)*f(b)>0).")

    it = 0
    while it < max_iter and abs(b - a) > eps:
        it += 1
        x = (a + b)/2
        fx = f(x)
        if fa*fx <= 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx
    return ((a + b)/2, it)

def secant(f, a, b, eps=1e-3, max_iter=100):
    x0, x1 = a, b
    for i in range(max_iter):
        fx0, fx1 = f(x0), f(x1)
        denom = fx1 - fx0
        if abs(denom) < 1e-15:
            raise ZeroDivisionError("Секущая выродилась.")
        x2 = x1 - fx1*(x1 - x0)/denom
        if abs(x2 - x1) < eps:
            return (x2, i+1)
        x0, x1 = x1, x2
    return (x1, max_iter)

def newton_method(f, df, x0, eps=1e-3, max_iter=100):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-15:
            raise ZeroDivisionError("Производная ~0 возле x=%.5f" % x)
        x_new = x - fx/dfx
        if abs(x_new - x) < eps:
            return (x_new, i+1)
        x = x_new
    return (x, max_iter)


def phi_simple(x, f, alpha=0.01):
    return x - alpha*f(x)

def simple_iteration(f, df, a, b, x0, eps=1e-3, max_iter=100, alpha=0.01):
    x = x0
    for i in range(max_iter):
        x_new = phi_simple(x, f, alpha=alpha)
        if abs(x_new - x) < eps:
            return (x_new, i+1)
        x = x_new
    return (x, max_iter)

def check_single_iter_convergence(f, df, a, b, alpha=0.01, steps=100):
    """
    Проверяем достаточное условие сходимости для
    phi(x)= x - alpha*f(x), т.е. phi'(x)= 1 - alpha*f'(x).
    Проверяем max|1 - alpha*f'(x)|<1 на [a,b].
    Возвращаем (ok, max_val).
    """
    xs = np.linspace(a, b, steps+1)
    max_val = 0.0
    for xx in xs:
        dphi = 1 - alpha*df(xx)
        val = abs(dphi)
        if val > max_val:
            max_val = val
    is_ok = (max_val < 1)
    return (is_ok, max_val)
