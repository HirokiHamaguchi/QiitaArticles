import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ---- Sample 3 points on 2x + y + z = 1 ----
np.random.seed(0)
points = np.column_stack(([0, 0.5, 0], [0, 0, 0.7], [0.6, 0, 0])) + 0.1

# ---- Figure and axes ----
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection="3d")
ax2 = fig.add_subplot(122, projection="3d")

# Fixed camera parameters
elev = 20
azim = 30

for ax in [ax1, ax2]:
    # Fixed viewpoint
    ax.view_init(elev=elev, azim=azim)

    # Fix limits (common scale and framing)
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(-0.5, 1.5)

    # Equal aspect ratio
    ax.set_box_aspect([1, 1, 1])

    # Black coordinate axes (arrows)
    ax.quiver(0, 0, 0, 1, 0, 0, color="black", arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 1, 0, color="black", arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 1, color="black", arrow_length_ratio=0.1)

    # Black points
    ax.scatter(
        points[:, 0], points[:, 1], points[:, 2], c="black", s=150, depthshade=False
    )

    # Hide axes completely
    ax.set_axis_off()

# ---- Affine hull: plane ----
xx, yy = np.meshgrid(np.linspace(-0.2, 1.2, 30), np.linspace(-0.2, 1.2, 30))
zz = 1 - xx / 2 - yy / 2

ax1.plot_surface(
    xx, yy, zz, color=plt.get_cmap("tab10")(0), alpha=0.8, linewidth=0, shade=False
)

ax1.set_title("Affine Hull")

# ---- Convex hull: triangle ----
triangle = Poly3DCollection(
    [points], facecolor=plt.get_cmap("tab10")(1), alpha=0.8, edgecolor=None
)
ax2.add_collection3d(triangle)

ax2.set_title("Convex Hull")

plt.tight_layout()
plt.show()
