def trapezoid_method(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    for i in range(1, n):
        x_i = a + i*h
        s += f(x_i)
    return (h / 2) * (f(a) + 2*s + f(b))
