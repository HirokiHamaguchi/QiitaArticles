import os
from PIL import Image


def combine_images():
    numbers = [1, 5, 10, 50, 100, 500]

    for number in numbers:
        img = Image.open(f"original/yen/{number}.jpg")
        img = img.resize((150, 150))
        img.save(f"imgs/yen/{number}.jpg")

    numbers = [1, 2, 5]

    for number in numbers:
        img = Image.open(f"original/cent/{number}.png")
        img = img.resize((250, 250))

        baseImg = Image.new("RGB", (250, 250), (255, 255, 255))
        baseImg.paste(img, (0, 0), img)
        baseImg.save(f"imgs/cent/{number}.jpg")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    combine_images()
