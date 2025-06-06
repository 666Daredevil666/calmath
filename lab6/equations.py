import math

def f1(x, y):
    return x + y

def exact1(x, y0, x0):
    return (y0 + x0 + 1) * math.exp(x - x0) - x - 1

def f2(x, y):
    return y - x ** 2 + 1

def exact2(x, y0, x0):
    return (y0 - (x0 ** 2 - 2 * x0 + 2)) * math.exp(x - x0) + x ** 2 - 2 * x + 2

def f3(x, y):
    return x * y

def exact3(x, y0, x0):
    return y0 * math.exp((x ** 2 - x0 ** 2) / 2)

ODES = {
    1: ("y' = x + y", f1, exact1, 1),
    2: ("y' = y - x^2 + 1", f2, exact2, 1),
    3: ("y' = x·y", f3, exact3, 1),
}
