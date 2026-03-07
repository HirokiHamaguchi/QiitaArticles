"""PDF to PNG conversion utilities."""

from pathlib import Path

import fitz


def convert_pdf_to_png(current_dir: Path) -> None:
    """Convert all PDF files in current_dir to PNG.

    Uses PyMuPDF to convert PDFs.

    Args:
        current_dir: Directory containing PDF files to convert
    """

    pdf_files = list(current_dir.glob("**/**.pdf"))
    print(f"Found {len(pdf_files)} PDF files to convert.")
    for pdf_file in pdf_files:
        if pdf_file.parent.name == "main" and any(
            pdf_file.stem.startswith(str(i)) for i in range(1, 5)
        ):
            continue

        png_file = pdf_file.with_suffix(".png")
        try:
            doc = fitz.open(str(pdf_file))
            page = doc[0]
            if "sixhump" in pdf_file.name:
                continue
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            pix.save(str(png_file))
            doc.close()
            print(f"Converted {pdf_file.name} to {png_file.name}")
        except Exception as e:
            print(f"Error converting {pdf_file.name}: {e}")
