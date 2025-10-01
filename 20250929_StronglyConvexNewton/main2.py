from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return np.sqrt(1 + x**2)


def df(x):
    return x / np.sqrt(1 + x**2)


def d2f(x):
    return 1 / (1 + x**2) ** (3 / 2)


def vis(x0):
    xs = [x0]
    for _ in range(3):
        x_next = xs[-1] - df(xs[-1]) / d2f(xs[-1])
        xs.append(x_next)

    f_points = f(np.array(xs))
    abs_max = max(abs(np.array(xs)))
    x = np.linspace(-abs_max * 1.2, abs_max * 1.2, 400)
    fx = f(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, fx, label=r"$f(x)=\sqrt{1+x^2}$")
    plt.title(rf"Graph of $f(x)$ with $x_0$={x0}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)

    plt.scatter(xs, f_points, color="red", label="Newton steps")
    for i in range(len(xs) - 1):
        plt.annotate(
            "",
            xy=(xs[i + 1], f_points[i + 1]),
            xytext=(xs[i], f_points[i]),
            arrowprops=dict(arrowstyle="->", color="red", lw=1.5, mutation_scale=30),
        )

    plt.legend(loc="upper center")
    plt.savefig(Path(__file__).parent / f"sqrt_function_{x0}.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    for x0 in [1.1]:
        vis(x0)
