import math

def euler(f, x0, y0, xn, h):
    xs = [x0]
    ys = [y0]
    x = x0
    y = y0
    while x < xn - 1e-12:
        y += h * f(x, y)
        x += h
        xs.append(x)
        ys.append(y)
    return xs, ys

def rk4(f, x0, y0, xn, h):
    xs = [x0]
    ys = [y0]
    x = x0
    y = y0
    while x < xn - 1e-12:
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h * k1 / 2)
        k3 = f(x + h / 2, y + h * k2 / 2)
        k4 = f(x + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
        xs.append(x)
        ys.append(y)
    return xs, ys

def adams_pc4(f, x0, y0, xn, h):
    xs, ys = rk4(f, x0, y0, x0 + 3 * h, h)
    x = xs[-1]
    while x < xn - 1e-12:
        i = len(xs) - 1
        f0 = f(xs[i], ys[i])
        f1 = f(xs[i - 1], ys[i - 1])
        f2 = f(xs[i - 2], ys[i - 2])
        f3 = f(xs[i - 3], ys[i - 3])
        y_pred = ys[i] + h * (55 * f0 - 59 * f1 + 37 * f2 - 9 * f3) / 24
        x_next = x + h
        f_pred = f(x_next, y_pred)
        y_corr = ys[i] + h * (9 * f_pred + 19 * f0 - 5 * f1 + f2) / 24
        x = x_next
        xs.append(x)
        ys.append(y_corr)
    return xs, ys

def runge_error(method, p, f, x0, y0, xn, h):
    _, y1 = method(f, x0, y0, xn, h)
    _, y2 = method(f, x0, y0, xn, h / 2)
    return abs(y2[-1] - y1[-1]) / (2 ** p - 1)

def adaptive(method, p, f, x0, y0, xn, h, eps,
             max_halvings=20, max_steps=200_000):
    for _ in range(max_halvings):
        err = runge_error(method, p, f, x0, y0, xn, h)
        steps = int((xn - x0) / h) + 1
        if err <= eps or steps > max_steps:
            xs, ys = method(f, x0, y0, xn, h)
            return xs, ys, h, err
        h /= 2
    print(f"⚠️  adaptive: точность {eps} не достигнута после {max_halvings} делений; "
          f"err ≈ {err:e}, h = {h:e}")
    xs, ys = method(f, x0, y0, xn, h)
    return xs, ys, h, err

