def print_table(xs, ys_e, ys_rk, ys_ad, exact_func, y0, x0):
    header = f"{'x':>10}{'Euler':>15}{'RK4':>15}{'Adams':>15}{'Exact':>15}"
    print(header)
    for i in range(len(xs)):
        x = xs[i]
        y_exact = exact_func(x, y0, x0)
        y_e = ys_e[i] if i < len(ys_e) else float('nan')
        y_rk = ys_rk[i] if i < len(ys_rk) else float('nan')
        y_ad = ys_ad[i]
        print(f"{x:10.6f}{y_e:15.6f}{y_rk:15.6f}{y_ad:15.6f}{y_exact:15.6f}")
