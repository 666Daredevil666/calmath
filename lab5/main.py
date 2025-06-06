from utils.io_utils import acquire_dataset, ask_target_x
from utils.plot_utils import plot_interpolation
from interpolation.lagrange import lagrange
from interpolation.newton_divided import newton_divided
from interpolation.newton_finite import newton_finite, finite_difference_table

def main() -> None:
    x_nodes, y_nodes, intrinsic_f = acquire_dataset()

    print("\nТаблица конечных разностей:")
    fd_table = finite_difference_table(y_nodes)
    for row in fd_table:
        print(" ".join(f"{v:12.6g}" if v is not None else " " * 12 for v in row))

    x_target = ask_target_x()

    approx = {
        "lagrange": lagrange(x_nodes, y_nodes, x_target),
        "newton_divided": newton_divided(x_nodes, y_nodes, x_target),
        "newton_finite": newton_finite(x_nodes, y_nodes, x_target),
    }

    print(f"\n≈ f({x_target})")
    for name, value in approx.items():
        print(f"{name:>15}: {value:.10g}")

    if intrinsic_f is not None:
        exact = intrinsic_f(x_target)
        print(f"{'exact':>15}: {exact:.10g}")
        print(f"{'abs error':>15}: {max(abs(v - exact) for v in approx.values()):.3e}")

    plot_interpolation(x_nodes, y_nodes, intrinsic_f, approx, x_target)

if __name__ == "__main__":
    main()

