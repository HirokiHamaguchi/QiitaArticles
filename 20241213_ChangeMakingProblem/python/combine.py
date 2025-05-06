import os
from PIL import Image


def combine_images():
    numbers = [1, 5, 10, 50, 100, 500]
    images = []

    for number in numbers:
        img = Image.open(f"imgs/yen/{number}.jpg")
        assert img.size == (150, 150)
        images.append(img)

    combined_image = Image.new("RGB", (450, 300))

    # Paste images into the combined image
    for i, img in enumerate(images):
        x = (i % 3) * 150
        y = (i // 3) * 150
        combined_image.paste(img, (x, y))

    # Save the combined image
    combined_image.save("combined.jpg")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    combine_images()
