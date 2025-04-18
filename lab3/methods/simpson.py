def simpson_method(f, a, b, n):
    if n % 2 != 0:
        n += 1  # делаем n чётным

    h = (b - a) / n
    s1 = 0.0  #sum нечётные индексы
    s2 = 0.0 #четные
    for i in range(1, n):
        x_i = a + i*h
        if i % 2 == 0:
            s2 += f(x_i)
        else:
            s1 += f(x_i)
    return (h/3) * (f(a) + 4*s1 + 2*s2 + f(b))
