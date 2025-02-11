# 3d  plot of the Huber2 function

import numpy as np
import matplotlib.pyplot as plt
import os

# use latex
plt.rc("text", usetex=True)
plt.rc("font", family="serif")


def Huber2(x, delta):
    assert len(x) == 2
    return np.sum(
        np.where(np.abs(x) <= delta, 0.5 * x**2, delta * (np.abs(x) - 0.5 * delta))
    )


X, Y = np.meshgrid(np.linspace(-2, 2, 100), np.linspace(-2, 2, 100))
W = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        W[i, j] = Huber2(np.array([X[i, j], Y[i, j]]), 1e-3)
Z = np.zeros_like(X)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = Huber2(np.array([X[i, j], Y[i, j]]), 1)

fig = plt.figure()
ax = fig.add_subplot(121, projection="3d")
ax.plot_surface(X, Y, W, cmap="viridis")
ax.set_xlabel("$x_1$", fontsize=16)
ax.set_ylabel("$x_2$", fontsize=16)
ax.set_title(r"$\delta=10^{-3}$", fontsize=16)

ax = fig.add_subplot(122, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis")
ax.set_xlabel("$x_1$", fontsize=16)
ax.set_ylabel("$x_2$", fontsize=16)
ax.set_title(r"$\delta=1$", fontsize=16)

# eliminate white space
fig.subplots_adjust(left=0, right=0.95, bottom=0, top=1)
bbox = fig.bbox_inches.from_bounds(0, 0.65, 6.4, 3.5)
plt.savefig(os.path.join(os.path.dirname(__file__), "Huber2.png"), bbox_inches=bbox)
