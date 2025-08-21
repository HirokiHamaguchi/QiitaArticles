import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def f(x):
    return 0.1 * np.pow(np.abs(x - 0.5), 2.5)


def grad_f(x):
    return 0.25 * np.sign(x - 0.5) * np.pow(np.abs(x - 0.5), 1.5)


def g(x, lam):
    return lam * np.abs(x)


def prox_g(x, lam):
    """Proximal operator for g(x) = lambda * |x| (soft thresholding)."""
    return np.sign(x) * np.maximum(np.abs(x) - lam, 0)


def proximal_gradient_operator(x, ell, lam):
    return prox_g(x - (1 / ell) * grad_f(x), lam / ell)


def gradient_mapping(x, ell, lam):
    return ell * (x - proximal_gradient_operator(x, ell, lam))


def main():
    sns.set()
    plt.rcParams["axes.labelsize"] = 14
    plt.rcParams["xtick.labelsize"] = 14
    plt.rcParams["ytick.labelsize"] = 14

    plt.rcParams["text.usetex"] = True
    plt.rcParams["font.family"] = "serif"

    ell = 2.0
    lam = 0.5
    xs_all = np.linspace(-2.1, 2.6, 100)
    ys_all = [f(x) + g(x, lam) for x in xs_all]
    plt.plot(xs_all, ys_all)

    xs = [-1, 0, 1.5]
    colors = ["red", "green", "blue"]
    for x, color in zip(xs, colors):
        y = f(x) + g(x, lam)
        plt.scatter(x, y, color=color, marker="o", s=100, label=None, zorder=3)

        # proximal_gradient_operator
        x_pgo = proximal_gradient_operator(x, ell, lam)
        y_pgo = f(x_pgo) + g(x_pgo, lam)
        plt.plot(x_pgo, y_pgo, color=color, marker="*", ms=10, zorder=2)
        print(x_pgo, y_pgo)
        if color == "red":
            plt.text(
                x_pgo + 0.2,
                y_pgo + 0.4,
                r"$T_L^{f,g}(x)$",
                color=color,
                ha="center",
                va="center",
                fontsize=24,
            )
        elif color == "blue":
            plt.text(
                x_pgo - 0.2,
                y_pgo + 0.4,
                r"$T_L^{f,g}(x)$",
                color=color,
                ha="center",
                va="center",
                fontsize=24,
            )

        # gradient_mapping
        x_gm = gradient_mapping(x, ell, lam)
        plt.arrow(x, y, x_gm, 0, color=color, head_width=0.2, length_includes_head=True)
        if color == "red":
            plt.text(
                x + x_gm + 0.2,
                y - 0.3,
                r"$\mathcal{G}_L^{f,g}(x)$",
                color=color,
                ha="center",
                va="center",
                fontsize=24,
            )
        elif color == "blue":
            plt.text(
                x + x_gm - 0.2,
                y - 0.3,
                r"$\mathcal{G}_L^{f,g}(x)$",
                color=color,
                ha="center",
                va="center",
                fontsize=24,
            )

        if color == "green":
            plt.text(
                x_pgo,
                -0.35,
                r"$\mathcal{G}_L^{f,g}(x)=0$, $T_L^{f,g}(x)=0$",
                color=color,
                ha="center",
                fontsize=24,
            )

    plt.title(r"$f(x) + g(x)$ $(g(x)=\lambda |x|)$", fontsize=24)
    plt.ylim(-0.5, 2.2)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "gradientMapping.png"), dpi=300)


if __name__ == "__main__":
    main()
