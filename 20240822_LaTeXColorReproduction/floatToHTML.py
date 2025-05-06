import matplotlib
import numpy as np
from typing import Tuple


def floatsToHTML(floats: Tuple[float, float, float]) -> str:
    return "".join(list(map(lambda x: f"{int(x * 255):02x}", floats)))


def floatsToRGB(floats: Tuple[float, float, float]) -> str:
    return ",".join(list(map(lambda x: str(int(x * 255)), floats)))


def floatsToLaTeX(color: Tuple[float, float, float], idx: int, method: str) -> str:
    if method == "RGB":
        return "\\definecolor{c" + str(idx) + "}{RGB}{" + floatsToRGB(color) + "}"
    elif method == "HTML":
        return "\\definecolor{c" + str(idx) + "}{HTML}{" + floatsToHTML(color) + "}"
    else:
        raise ValueError("Invalid method")


def main():
    # 好みのカラーマップ
    cmap = matplotlib.colormaps.get_cmap("viridis")
    # 色を取得したい任意の値
    values = [+1, +1 / np.sqrt(2), +1 / 2, -1 / 2, -1 / np.sqrt(2)]
    # 値の範囲
    vMax, vMin = +1, -1

    for idx, value in enumerate(values):
        color = cmap((value - vMin) / (vMax - vMin))
        assert color[-1] == 1  # alpha channel
        print(floatsToLaTeX(color[:3], idx, "RGB"))


if __name__ == "__main__":
    main()
