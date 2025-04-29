import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 頂点と面の定義
vertices = [
    (-1, -1, -1),  # v0
    (-1, -1, 1),  # v1
    (-1, 1, 1),  # v2
    (1, 1, 1),  # v3
]
faces = [
    (0, 1, 2),  # x1 = -1 面
    (1, 2, 3),  # x3 =  1 面
    (0, 1, 3),  # x1 = x2 面
    (0, 2, 3),  # x2 = x3 面
]

# Numpy 配列に変換
v = np.array(vertices)

# プロット
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_trisurf(
    v[:, 0],
    v[:, 1],
    v[:, 2],
    triangles=faces,
    linewidth=0.5,
    antialiased=True,
    alpha=0.6,
)

# 軸範囲とラベル
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

ax.xaxis.labelpad = -10
ax.yaxis.labelpad = -10
ax.zaxis.labelpad = -10
ax.set_xlabel("$x_1$", fontsize=20)
ax.set_ylabel("$x_2$", fontsize=20)
ax.set_zlabel("$x_3$", fontsize=20)
ax.set_box_aspect([1, 1, 1])

plt.savefig(
    os.path.join(os.path.dirname(__file__), "constraints_3d.png"),
    bbox_inches="tight",
    dpi=300,
)
