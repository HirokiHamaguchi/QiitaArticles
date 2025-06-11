import glob
import os

import pymupdf


def pdf2png(pdf_file):
    doc = pymupdf.open(pdf_file)
    assert len(doc) == 1

    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=300)  # type: ignore[no-untyped-call]
    output_file = f"{os.path.splitext(pdf_file)[0]}.png"
    pix.save(output_file)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for pdf_file in glob.glob("*.pdf"):
        pdf2png(pdf_file)
        print(f"Converted {pdf_file} to png")


if __name__ == "__main__":
    main()
