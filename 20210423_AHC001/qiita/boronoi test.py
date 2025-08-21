from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import cv2
import numpy as np

img = cv2.imread("boronoi.jpeg")

h, w = img.shape[:2]
print(h, w)

pts = [
    [1508, 990],
    [710, 1687],
    [2120, 1639],
    [1667, 813],
    [2238, 1701],
    [1362, 267],
    [1751, 1371],
    [1864, 918],
    [1648, 611],
    [2148, 735],
    [1397, 936],
    [1866, 797],
    [2015, 1337],
    [1394, 1330],
    [1586, 1128],
    [890, 1314],
    [1645, 1285],
    [127, 1851],
    [947, 1782],
    [1568, 1325],
    [1347, 653],
    [868, 1679],
    [2172, 1436],
    [1981, 1215],
    [1914, 556],
    [1624, 1616],
    [1352, 1174],
    [994, 1902],
    [1645, 1405],
    [1699, 661],
    [300, 1914],
    [920, 1976],
    [167, 1445],
    [1055, 1018],
    [2224, 536],
    [245, 1886],
    [1745, 869],
    [247, 1459],
    [2142, 1546],
    [1517, 593],
    [2103, 1028],
    [1309, 1269],
    [547, 1522],
    [2123, 837],
    [1025, 228],
    [493, 1794],
    [1564, 1787],
    [2275, 1125],
    [1973, 1523],
    [1754, 547],
    [1539, 785],
    [1760, 1686],
    [1612, 495],
    [636, 1625],
    [1006, 1595],
    [1890, 1015],
    [2018, 414],
]
pts = [[p[1], h - p[0]] for p in pts]

tri = Delaunay(pts)
fig = delaunay_plot_2d(tri)
vor = Voronoi(pts)

fig = voronoi_plot_2d(vor)
fig.savefig("scipy_matplotlib_voronoi.png")

fig, ax = plt.subplots()
voronoi_plot_2d(vor, ax)

for region, c in zip([r for r in vor.regions if -1 not in r and r], ["yellow", "pink"]):
    ax.fill(vor.vertices[region][:, 0], vor.vertices[region][:, 1], color=c)

fig.savefig("scipy_matplotlib_voronoi_fill.png")

fig, ax = plt.subplots(figsize=(w / 500, h / 500))
# delaunay_plot_2d(tri, ax)
voronoi_plot_2d(vor, ax, show_vertices=False)

ax.set_xlim(0, w)
ax.set_ylim(0, h)

fig.savefig("scipy_matplotlib_delaunay_voronoi.png")
