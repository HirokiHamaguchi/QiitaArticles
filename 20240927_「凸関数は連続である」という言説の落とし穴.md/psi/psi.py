import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"


def psi(g, gamma):
    psi_values = np.zeros_like(gamma)
    mask = gamma > 0
    psi_values[mask] = g[mask] ** 2 / (2 * gamma[mask])
    return psi_values


for gamma_min in [0.05, 0.03, 0.01]:
    g_vals = np.linspace(-3, 3, 1000)
    gamma_vals = np.linspace(gamma_min, 3, 1000)
    G, Gamma = np.meshgrid(g_vals, gamma_vals)
    Psi = psi(G, Gamma)

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d", computed_zorder=False)
    ax.plot_surface(
        G,
        Gamma,
        Psi,
        cmap="viridis",
        edgecolor="none",
        lw=0.01,
        rcount=1000,
        ccount=100,
    )

    ax.plot(
        g_vals,
        np.full_like(g_vals, gamma_min),
        psi(g_vals, np.full_like(g_vals, gamma_min)),
        linestyle="dashed",
        color="black",
        linewidth=3,
    )
    ax.scatter(0, 0, 0, color="blue", s=300, zorder=10)

    g = 6
    gamma = []
    _gamma = gamma_min
    while True:
        gamma.append(_gamma)
        _gamma += 0.035
        if _gamma > (3 / 6) ** 2:
            break
    gamma = np.array(gamma)
    ax.scatter(
        np.sqrt(gamma) * g,
        gamma,
        psi(np.sqrt(gamma) * g, gamma),
        color="red",
        alpha=1,
        zorder=10,
        s=50,
    )

    ax.set_xlabel("$g$", fontsize=30)
    ax.set_ylabel("$\gamma$", fontsize=30)
    ax.set_zlabel("$\psi(g, \gamma)$", fontsize=30)
    ax.set_zlim(0, 50)
    ax.set_title(f"$\psi(g, \gamma)$ with $\gamma > {gamma_min}$", fontsize=40, pad=20)
    ax.view_init(20, 120)

    plt.tight_layout()
    plt.savefig(f"psi/psi_{gamma_min}.png")
    plt.close()

images = [cv2.imread(f"psi/psi_{gamma_min}.png") for gamma_min in [0.05, 0.03, 0.01]]
combined = cv2.hconcat(images)
cv2.imwrite("psi/psi.png", combined)
