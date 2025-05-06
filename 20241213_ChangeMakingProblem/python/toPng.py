# convert pdf to png

import os
from pdf2image import convert_from_path


def png2pdf():
    for number in range(1, 6 + 1):
        pathIn = f"figs/fig{number}.pdf"
        pathOut = f"figs/fig{number}.png"
        images = convert_from_path(pathIn, dpi=400 if number == 4 else 300)
        for image in images:
            image.save(pathOut, "PNG")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    png2pdf()
