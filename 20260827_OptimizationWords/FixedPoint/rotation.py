import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

# Parameters
theta_deg = 30
theta = np.deg2rad(theta_deg)
n_iter = 30

# Initial point
x0 = np.array([-1.0, 0.0])

# Rotation map T(x) = R_theta x
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

def T(x):
    return R @ x

# ------------------------------------------------------------
# 1. Banach / Picard iteration
#    x_{k+1} = T(x_k)
# ------------------------------------------------------------
banach = [x0.copy()]
x = x0.copy()

for k in range(n_iter):
    x = T(x)
    banach.append(x.copy())

banach = np.array(banach)

# ------------------------------------------------------------
# 2. Krasnosel'skii-Mann iteration
#    x_{k+1} = x_k + alpha_k (T(x_k) - x_k)
# ------------------------------------------------------------
alpha_km = 0.5

km = [x0.copy()]
x = x0.copy()

for k in range(n_iter):
    x = x + alpha_km * (T(x) - x)
    km.append(x.copy())

km = np.array(km)

# ------------------------------------------------------------
# 3. Halpern iteration
#    x_{k+1} = T(x_k) + alpha_k (x_0 - T(x_k))
#    alpha_k = 1 / (k + 2)
# ------------------------------------------------------------
halpern = [x0.copy()]
x = x0.copy()

for k in range(n_iter):
    alpha_k = 1.0 / (k + 2)
    Tx = T(x)
    x = Tx + alpha_k * (x0 - Tx)
    halpern.append(x.copy())

halpern = np.array(halpern)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 5))

ax.plot(
    banach[:, 0], banach[:, 1],
    marker="o", markersize=3, linewidth=1.2,
    label="Banach"
)

ax.plot(
    km[:, 0], km[:, 1],
    marker="s", markersize=3, linewidth=1.2,
    label=rf"Krasnosel'skii-Mann ($\alpha_k={alpha_km}$)"
)

ax.plot(
    halpern[:, 0], halpern[:, 1],
    marker="^", markersize=3, linewidth=1.2,
    label=r"Halpern ($\alpha_k=1/(k+2)$)"
)

# Fixed point and initial point
ax.scatter(0, 0, marker="*", s=150, label="fixed point (0,0)")
ax.scatter(x0[0], x0[1], marker="x", s=80, label="start (-1,0)")

ax.set_aspect("equal", adjustable="box")
ax.set_xlabel(r"$x_1$")
ax.set_ylabel(r"$x_2$")
ax.set_title(
    rf"Fixed-point iterations"
    rf"($\theta={theta_deg}^\circ$, {n_iter} iterations)"
)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")
fig.tight_layout()

fig.savefig(Path(__file__).parent / "rotation.png", dpi=300, bbox_inches="tight")
