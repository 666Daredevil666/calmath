def left_rect_method(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    x = a
    for _ in range(n):
        s += f(x)
        x += h
    return s * h

def right_rect_method(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    x = a + h
    for _ in range(n):
        s += f(x)
        x += h
    return s * h

def mid_rect_method(f, a, b, n):
    h = (b - a) / n
    s = 0.0
    x = a + h/2
    for _ in range(n):
        s += f(x)
        x += h
    return s * h
