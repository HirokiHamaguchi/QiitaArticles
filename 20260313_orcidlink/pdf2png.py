import glob
import os

from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    # Get all PNG files starting with _test
    png_files = glob.glob("_test*.png")

    for png_file in png_files:
        # Open the image
        img = Image.open(png_file)
        width, height = img.size

        # Calculate crop boundaries (top, left, right, bottom)
        top = int(height * 0.13)
        left = int(width * 0.25)
        right = int(width * (1 - 0.21))
        bottom = int(height * (1 - 0.03))

        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))

        # Generate output filename (remove leading underscore)
        output_filename = png_file[1:]

        # Save the cropped image
        cropped_img.save(output_filename)
        print(f"Saved: {output_filename}")


if __name__ == "__main__":
    main()
