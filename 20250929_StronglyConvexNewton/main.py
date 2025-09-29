from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def f(x):
    return np.log(1 + np.exp(x)) - x / 2 + (mu / 2) * x**2


def df(x):
    return np.exp(x) / (1 + np.exp(x)) - 0.5 + mu * x


def d2f(x):
    return np.exp(x) / (1 + np.exp(x)) ** 2 + mu


def vis(mu, x0):
    xs = [x0]
    for _ in range(30):
        x_next = xs[-1] - df(xs[-1]) / d2f(xs[-1])
        xs.append(x_next)

    f_points = (
        np.log(1 + np.exp(np.array(xs)))
        - np.array(xs) / 2
        + (mu / 2) * np.array(xs) ** 2
    )

    abs_max = max(abs(np.array(xs)))
    x = np.linspace(-abs_max * 1.2, abs_max * 1.2, 400)
    fx = f(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, fx, label=r"$f(x)=\log(1+e^x)-x/2 + \mu x^2/2$")
    plt.title(rf"Graph of $f(x)$ with $\mu$={mu} and $x_0$={x0}")
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
    plt.scatter(xs, f_points, color="red", label="Newton steps")

    # グラフ描画
    plt.legend()
    plt.savefig(
        Path(__file__).parent / f"strongly_convex_function_{mu}_{x0}.png", dpi=300
    )
    plt.close()


if __name__ == "__main__":
    for mu, x0 in [(0.1, -4), (0.01, -4)]:
        vis(mu, x0)
