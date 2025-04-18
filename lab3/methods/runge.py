def integrate_with_precision(method, f, a, b, eps, p, n_start=4):
    """
    Итерационное вычисление интеграла с заданной точностью eps по правилу Рунге:

        Δ = |I_{2n} - I_n| / (2^p - 1), где p — порядок метода (1, 2 или 4).
    Возвращает кортеж (v, n),
    где:
      - v — найденное приближение интеграла,
      - n — число разбиений, при котором достигнута точность.
    """
    n = n_start
    while True:
        i_n = method(f, a, b, n)
        i_2n = method(f, a, b, 2 * n)
        delta = abs(i_2n - i_n) / (2 ** p - 1)
        if delta < eps:
            return i_2n, 2 * n
        else:
            n *= 2
