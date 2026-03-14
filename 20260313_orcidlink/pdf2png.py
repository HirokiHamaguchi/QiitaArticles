import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz  # type: ignore

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "failed_examples"
BUILD_DIR = OUTPUT_DIR / "_build"


@dataclass
class CompileMethod:
    name: str
    tex_file: str
    steps: List[List[str]]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def copy_compile_inputs(work_dir: Path):
    work_dir.mkdir(parents=True, exist_ok=True)
    for source in SCRIPT_DIR.iterdir():
        if source.is_file() and source.suffix.lower() in {
            ".tex",
            ".sty",
            ".cls",
            ".png",
            ".jpg",
            ".jpeg",
            ".pdf",
            ".bib",
        }:
            shutil.copy2(source, work_dir / source.name)


def run_compile_method(method: CompileMethod) -> Path | None:
    method_slug = slugify(method.name)
    work_dir = BUILD_DIR / method_slug
    if work_dir.exists():
        shutil.rmtree(work_dir)
    copy_compile_inputs(work_dir)

    tex_stem = Path(method.tex_file).stem
    tex_name = Path(method.tex_file).name
    docfile = tex_stem

    required_commands = {step[0] for step in method.steps if step}
    missing = [cmd for cmd in sorted(required_commands) if not command_exists(cmd)]
    if missing:
        print(f"[SKIP] {method.name}: missing command(s): {', '.join(missing)}")
        return None

    print(f"[RUN ] {method.name}")
    for step in method.steps:
        command = [
            token.replace("%DOC%", tex_name).replace("%DOCFILE%", docfile)
            for token in step
        ]
        result = subprocess.run(
            command,
            cwd=work_dir,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print(f"[FAIL] {method.name}: {' '.join(command)}")
            if result.stdout.strip():
                print(result.stdout[-4000:])
            if result.stderr.strip():
                print(result.stderr[-4000:])
            return None

    generated_pdf = work_dir / f"{tex_stem}.pdf"
    if not generated_pdf.exists():
        print(f"[FAIL] {method.name}: PDF not found: {generated_pdf.name}")
        return None

    output_pdf = OUTPUT_DIR / f"{tex_stem}__{method_slug}.pdf"
    shutil.copy2(generated_pdf, output_pdf)
    print(f"[ OK ] saved PDF: {output_pdf}")
    return output_pdf


def annotate_and_convert_pdf_to_png(pdf_file: Path):
    doc = fitz.open(str(pdf_file))
    if len(doc) == 0:
        print(f"[SKIP] empty PDF: {pdf_file.name}")
        doc.close()
        return

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

    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    output_png = pdf_file.with_suffix(".png")
    pix.save(str(output_png))
    doc.close()
    print(f"[ OK ] saved PNG: {output_png}")


def get_compile_methods() -> List[CompileMethod]:
    return [
        CompileMethod(
            name="pdflatex",
            tex_file="failed_examples_raw.tex",
            steps=[
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-synctex=1",
                    "-file-line-error",
                    "--shell-escape",
                    "%DOC%",
                ],
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-synctex=1",
                    "-file-line-error",
                    "--shell-escape",
                    "%DOC%",
                ],
            ],
        ),
        CompileMethod(
            name="lualatex",
            tex_file="failed_examples_raw.tex",
            steps=[
                [
                    "lualatex",
                    "-file-line-error",
                    "-synctex=1",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "%DOC%",
                ],
                [
                    "lualatex",
                    "-file-line-error",
                    "-synctex=1",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "%DOC%",
                ],
            ],
        ),
        CompileMethod(
            name="xelatex (extra)",
            tex_file="failed_examples_raw.tex",
            steps=[
                [
                    "xelatex",
                    "-file-line-error",
                    "-synctex=1",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "%DOC%",
                ],
                [
                    "xelatex",
                    "-file-line-error",
                    "-synctex=1",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "%DOC%",
                ],
            ],
        ),
        CompileMethod(
            name="platex -> dvipdfmx",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=[
                [
                    "platex",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-synctex=1",
                    "%DOC%",
                ],
                [
                    "platex",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-synctex=1",
                    "%DOC%",
                ],
                ["dvipdfmx", "%DOCFILE%"],
            ],
        ),
        CompileMethod(
            name="uplatex -> dvipdfmx (extra)",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=[
                [
                    "uplatex",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-synctex=1",
                    "%DOC%",
                ],
                [
                    "uplatex",
                    "-interaction=nonstopmode",
                    "-file-line-error",
                    "-synctex=1",
                    "%DOC%",
                ],
                ["dvipdfmx", "%DOCFILE%"],
            ],
        ),
        CompileMethod(
            name="ptex2pdf (platex)",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=[
                [
                    "ptex2pdf",
                    "-interaction=nonstopmode",
                    "-l",
                    "-ot",
                    "-kanji=utf8 -synctex=1 -file-line-error",
                    "%DOC%",
                ],
                [
                    "ptex2pdf",
                    "-interaction=nonstopmode",
                    "-l",
                    "-ot",
                    "-kanji=utf8 -synctex=1 -file-line-error",
                    "%DOC%",
                ],
            ],
        ),
        CompileMethod(
            name="ptex2pdf (uplatex)",
            tex_file="failed_examples_dvipdfmx.tex",
            steps=[
                [
                    "ptex2pdf",
                    "-interaction=nonstopmode",
                    "-u",
                    "-l",
                    "-ot",
                    "-kanji=utf8 -synctex=1 -file-line-error",
                    "%DOC%",
                ],
                [
                    "ptex2pdf",
                    "-interaction=nonstopmode",
                    "-u",
                    "-l",
                    "-ot",
                    "-kanji=utf8 -synctex=1 -file-line-error",
                    "%DOC%",
                ],
            ],
        ),
        CompileMethod(
            name="latexmk (pdflatex extra)",
            tex_file="failed_examples_raw.tex",
            steps=[
                [
                    "latexmk",
                    "-pdf",
                    "-interaction=nonstopmode",
                    "-synctex=1",
                    "-file-line-error",
                    "%DOC%",
                ]
            ],
        ),
    ]


def main():
    os.chdir(SCRIPT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    methods = get_compile_methods()
    generated_pdfs: List[Path] = []

    for method in methods:
        pdf_path = run_compile_method(method)
        if pdf_path is not None:
            generated_pdfs.append(pdf_path)

    if not generated_pdfs:
        print("No PDFs were generated.")
        return

    for pdf_file in generated_pdfs:
        annotate_and_convert_pdf_to_png(pdf_file)

    print(f"Done. Generated {len(generated_pdfs)} PDF(s) and PNG(s) in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
