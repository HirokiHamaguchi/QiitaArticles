import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import fitz  # type: ignore
import pyperclip  # type: ignore

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "failed_examples"
PNG_WIDTH = 1024


@dataclass
class CompileMethod:
    name: str
    tex_file: str
    steps: List[str]


TOOL_DEFINITIONS: Dict[str, List[str]] = {
    "pdflatex": [
        "pdflatex",
        "-interaction=nonstopmode",
        "-synctex=1",
        "-file-line-error",
        "--shell-escape",
        "%DOC%",
    ],
    "lualatex": [
        "lualatex",
        "-file-line-error",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "%DOC%",
    ],
    "xelatex": [
        "xelatex",
        "-file-line-error",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "%DOC%",
    ],
    "xelatex (no-pdf)": [
        "xelatex",
        "-no-pdf",
        "-file-line-error",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "%DOC%",
    ],
    "xdvipdfmx": [
        "xdvipdfmx",
        "%DOCFILE%.xdv",
    ],
    "platex": [
        "platex",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-synctex=1",
        "%DOC%",
    ],
    "uplatex": [
        "uplatex",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-synctex=1",
        "%DOC%",
    ],
    "dvipdfmx": [
        "dvipdfmx",
        "%DOCFILE%",
    ],
    "ptex2pdf (platex)": [
        "ptex2pdf",
        "-interaction=nonstopmode",
        "-l",
        "-ot",
        "-kanji=utf8 -synctex=1 -file-line-error",
        "%DOC%",
    ],
    "ptex2pdf (uplatex)": [
        "ptex2pdf",
        "-interaction=nonstopmode",
        "-u",
        "-l",
        "-ot",
        "-kanji=utf8 -synctex=1 -file-line-error",
        "%DOC%",
    ],
    "latexmk (pdflatex)": [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-synctex=1",
        "-file-line-error",
        "%DOC%",
    ],
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def build_step_command(step_name: str, tex_name: str, docfile: str) -> List[str]:
    template = TOOL_DEFINITIONS[step_name]
    return [
        token.replace("%DOC%", tex_name).replace("%DOCFILE%", docfile)
        for token in template
    ]


def run_compile_method(method: CompileMethod) -> Path | None:
    tex_stem = Path(method.tex_file).stem
    tex_name = Path(method.tex_file).name
    docfile = tex_stem
    method_slug = slugify(method.name)

    required_commands = [
        TOOL_DEFINITIONS[step_name][0]
        for step_name in method.steps
        if step_name in TOOL_DEFINITIONS
    ]
    for command_name in sorted(set(required_commands)):
        if not command_exists(command_name):
            raise RuntimeError(
                f"Required command not found: {command_name} (needed for method: {method.name})"
            )

    print(f"[RUN ] {method.name}")
    for step_name in method.steps:
        command = build_step_command(step_name, tex_name, docfile)
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            text=True,
            capture_output=True,
        )
        if result.stdout.strip():
            print(result.stdout[:3000] + ("..." if len(result.stdout) > 3000 else ""))
        if result.stderr.strip():
            print(result.stderr[:3000] + ("..." if len(result.stderr) > 3000 else ""))
        if result.returncode != 0:
            print(f"[FAIL] {method.name}: {' '.join(command)}")
            return None

    generated_pdf = SCRIPT_DIR / f"{tex_stem}.pdf"
    if not generated_pdf.exists():
        print(f"[FAIL] {method.name}: PDF not found: {tex_stem}.pdf")
        return None

    output_pdf = OUTPUT_DIR / f"{tex_stem}__{method_slug}.pdf"
    shutil.copy2(generated_pdf, output_pdf)
    print(f"[ OK ] saved PDF: {output_pdf}")
    return output_pdf


def annotate_and_convert_pdf_to_png(pdf_file: Path) -> Path | None:
    doc = fitz.open(str(pdf_file))
    if len(doc) == 0:
        print(f"[SKIP] empty PDF: {pdf_file.name}")
        doc.close()
        return None

    page = doc.load_page(0)

    links = page.get_links()
    shape = page.new_shape()
    for link in links:
        rect = link.get("from")
        kind = link.get("kind")
        if rect:
            if kind == 2:
                color = (1, 0, 0)  # red
            elif kind == 4:
                color = (0, 1, 1)  # aqua
            else:
                color = (0, 1, 0)  # green
            shape.draw_rect(rect)
            shape.finish(color=color, width=2)
            shape.commit()
            shape = page.new_shape()  # reset for next rect

    page_width = page.rect.width
    assert page_width > 0, "Page width must be positive"
    zoom = PNG_WIDTH / page_width
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    output_png = pdf_file.with_suffix(".png")
    pix.save(str(output_png))
    doc.close()
    print(f"[ OK ] saved PNG: {output_png}")
    return output_png


def _display_label_from_png_name(png_name: str) -> str:
    stem = Path(png_name).stem
    if "__" not in stem:
        return stem
    _, method_part = stem.split("__", 1)
    return method_part.replace("_", " ")


def build_markdown_table(caption: str, png_files: List[Path]) -> str:
    assert len(png_files) > 0, f"No PNG files for table: {caption}"
    headers = [_display_label_from_png_name(path.name) for path in png_files]
    rel_paths = [f"failed_examples/{path.name}" for path in png_files]

    header_row = "| " + " | ".join(headers) + " |"
    align_row = "| " + " | ".join([":---:"] * len(headers)) + " |"
    image_row = (
        "| "
        + " | ".join(
            [
                f"![{rel_path.replace('failed_examples/', '').replace('.png', '')}]({rel_path})"
                for rel_path in rel_paths
            ]
        )
        + " |"
    )
    return "\n".join(
        [
            f"Table: {caption}",
            "",
            header_row,
            align_row,
            image_row,
        ]
    )


def build_and_copy_tables(generated_pngs: List[Path]) -> str:
    raw_pngs = sorted(
        [
            path
            for path in generated_pngs
            if path.name.startswith("failed_examples_raw__")
        ]
    )
    dvipdfmx_pngs = sorted(
        [
            path
            for path in generated_pngs
            if path.name.startswith("failed_examples_dvipdfmx__")
        ]
    )

    raw_table = build_markdown_table("Raw engine outputs", raw_pngs)
    dvipdfmx_table = build_markdown_table("DVI-to-PDF workflow outputs", dvipdfmx_pngs)
    tables_text = f"{raw_table}\n\n{dvipdfmx_table}"
    pyperclip.copy(tables_text)
    return tables_text


def get_compile_methods() -> List[CompileMethod]:
    return [
        CompileMethod(
            name="pdflatex",
            tex_file="failed_examples_raw.tex",
            steps=["pdflatex", "pdflatex"],
        ),
        CompileMethod(
            name="lualatex",
            tex_file="failed_examples_raw.tex",
            steps=["lualatex", "lualatex"],
        ),
        CompileMethod(
            name="xelatex",
            tex_file="failed_examples_raw.tex",
            steps=["xelatex", "xelatex"],
        ),
        CompileMethod(
            name="xelatex -> xdvipdfmx",
            tex_file="failed_examples_raw.tex",
            steps=["xelatex (no-pdf)", "xelatex (no-pdf)", "xdvipdfmx"],
        ),
        CompileMethod(
            name="platex -> dvipdfmx",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=["platex", "platex", "dvipdfmx"],
        ),
        CompileMethod(
            name="uplatex -> dvipdfmx",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=["uplatex", "uplatex", "dvipdfmx"],
        ),
        CompileMethod(
            name="ptex2pdf (platex)",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=["ptex2pdf (platex)", "ptex2pdf (platex)"],
        ),
        CompileMethod(
            name="ptex2pdf (uplatex)",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=["ptex2pdf (uplatex)", "ptex2pdf (uplatex)"],
        ),
        CompileMethod(
            name="latexmk (pdflatex)",
            tex_file="failed_examples_raw.tex",
            steps=["latexmk (pdflatex)"],
        ),
    ]


def main() -> None:
    os.chdir(SCRIPT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    legacy_build_dir = OUTPUT_DIR / "_build"
    if legacy_build_dir.exists() and legacy_build_dir.is_dir():
        shutil.rmtree(legacy_build_dir)

    methods = get_compile_methods()
    generated_pdfs: List[Path] = []
    generated_pngs: List[Path] = []

    for method in methods:
        pdf_path = run_compile_method(method)
        assert pdf_path is not None
        generated_pdfs.append(pdf_path)

    for item in SCRIPT_DIR.iterdir():
        if item.is_file() and item.suffix in {
            ".aux",
            ".out",
            ".log",
            ".gz",
            ".dvi",
            ".xdv",
            ".fls",
            ".fdb_latexmk",
            ".toc",
            ".pdf",
        }:
            item.unlink()

    for pdf_file in generated_pdfs:
        png_path = annotate_and_convert_pdf_to_png(pdf_file)
        if png_path is not None:
            generated_pngs.append(png_path)

    tables_text = build_and_copy_tables(generated_pngs)
    print("\nCopied tables to clipboard:\n")
    print(tables_text)

    print(f"Done. Generated {len(generated_pdfs)} PDF(s) and PNG(s) in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
