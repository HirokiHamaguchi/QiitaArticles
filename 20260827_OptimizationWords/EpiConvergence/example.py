"""
Side-by-side examples of epi-convergence.

Requirements:
- seaborn styling
- same n values on both panels: n = 1, 5, 20, 100
- same color assigned to the same n in both panels
- LaTeX rendering
- black coordinate axes
- shared overall title: "Example of Epi-Convergence"
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# ---------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------
SNS_STYLE = "whitegrid"
PALETTE_NAME = "colorblind"
N_VALUES = [2, 10, 20]

sns.set_theme(
    style=SNS_STYLE,
    context="paper",
    font_scale=2,
)

plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "axes.edgecolor": "black",
        "axes.labelcolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)

# Same n -> same color in both panels.
N_COLORS = dict(zip(N_VALUES, sns.color_palette(PALETTE_NAME, n_colors=len(N_VALUES))))

# Limit function is drawn in a separate neutral color.
LIMIT_COLOR = "black"


# ---------------------------------------------------------------------
# Function families
# ---------------------------------------------------------------------
def oscillatory_fn(x, n):
    r"""f_n(x) = x^2 + sin(nx) + 1."""
    return x**2 + np.sin(n * x) + 1


def oscillatory_limit(x):
    r"""Epi-limit: f(x) = x^2."""
    return x**2


def double_well_fn(x, n):
    r"""f_n(x) = (x^2 - 1)^2 + (x + 1)^2 / n."""
    return (x**2 - 1) ** 2 + (x + 1) ** 2 / n


def double_well_limit(x):
    r"""Limit: f(x) = (x^2 - 1)^2."""
    return (x**2 - 1) ** 2


# ---------------------------------------------------------------------
# Shared plotting utilities
# ---------------------------------------------------------------------
def style_axis(ax, xlim, ylim):
    """Apply common styling to a panel."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f_n(x)$")

    # Coordinate axes in black.
    ax.axhline(0, color="black", linewidth=0.9, zorder=0)
    ax.axvline(0, color="black", linewidth=0.9, zorder=0)

    # Black frame and ticks.
    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(0.9)

    ax.tick_params(axis="both", colors="black", direction="out")

    # Keep seaborn grid subtle.
    ax.grid(True, alpha=0.25, linewidth=0.6)
    ax.set_axisbelow(True)


def plot_family(
    ax,
    x,
    fn,
    limit_fn,
    title,
    xlim,
    ylim,
):
    """Plot one epi-convergent family using the shared n/color mapping."""
    for n in N_VALUES:
        ax.plot(
            x,
            fn(x, n),
            color=N_COLORS[n],
            linewidth=1.6,
            label=rf"$f_{{n={n}}}$",
        )

    ax.plot(
        x,
        limit_fn(x),
        color=LIMIT_COLOR,
        linewidth=2.6,
        linestyle="--",
        label=r"$f$",
    )

    ax.set_title(title, pad=10)
    style_axis(ax, xlim=xlim, ylim=ylim)

    ax.legend(
        loc="upper center",
        frameon=True,
        fancybox=True,
        framealpha=0.95,
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    x_left = np.linspace(-2.1, 2.1, 6000)
    x_right = np.linspace(-1.7, 1.7, 5000)

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(14, 5.6),
        constrained_layout=False,
    )

    plot_family(
        ax=axes[0],
        x=x_left,
        fn=oscillatory_fn,
        limit_fn=oscillatory_limit,
        title=r"$f_n(x)=x^2+\sin(nx)+1,\qquad f(x)=x^2$",
        xlim=(-2.1, 2.1),
        ylim=(-0.15, 5.2),
    )

    plot_family(
        ax=axes[1],
        x=x_right,
        fn=double_well_fn,
        limit_fn=double_well_limit,
        title=(
            r"$f_n(x)=(x^2-1)^2+\frac{(x+1)^2}{n},"
            r"\qquad f(x)=(x^2-1)^2$"
        ),
        xlim=(-1.7, 1.7),
        ylim=(-0.08, 2.5),
    )

    fig.suptitle(
        r"\textbf{Example of Epi-Convergence}",
        fontsize=18,
        y=0.98,
    )

    fig.subplots_adjust(
        left=0.07,
        right=0.985,
        bottom=0.13,
        top=0.84,
        wspace=0.20,
    )

    output_path = Path(__file__).with_name("epi_convergence_examples.png")
    fig.savefig(output_path, dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
