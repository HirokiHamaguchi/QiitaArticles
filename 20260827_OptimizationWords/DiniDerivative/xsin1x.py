import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib


sns.set_theme(style="whitegrid", context="talk")
plt.rcParams["text.usetex"] = True


def f(x: np.ndarray) -> np.ndarray:
	"""Return x sin(1/x), excluding the undefined point x=0."""
	return x * np.sin(1 / x)


# Avoid x=0, where sin(1/x) is undefined, while showing both sides of the origin.
x_left = np.linspace(-0.05, -0.0001, 5000)
x_right = np.linspace(0.0001, 0.05, 5000)

fig, ax = plt.subplots(figsize=(6, 5))
ax.set_aspect(aspect="equal", adjustable="box")
ax.plot(x_left, f(x_left), label=r"$x\sin(1/x)$")
ax.plot(x_right, f(x_right))
ax.axvline(0, color="black", linewidth=0.8, alpha=0.5)
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$x\sin(1/x)$")
ax.set_title(r"Graph of $x\sin(1/x)$")
ax.legend()
fig.tight_layout()

plt.savefig(pathlib.Path(__file__).parent / "xsin1x.png", dpi=300)
