import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import fitz  # type: ignore

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIRS = {
    "failed": SCRIPT_DIR / "examples_failed",
    "succeeded": SCRIPT_DIR / "examples_succeeded",
}
TABLE_FILES = {
    "failed": SCRIPT_DIR / "examples_failed_table.txt",
    "succeeded": SCRIPT_DIR / "examples_succeeded_table.txt",
}
RAW_GITHUB_BASE_URL = (
    "https://raw.githubusercontent.com/"
    "HirokiHamaguchi/QiitaArticles/main/20260313_orcidlink"
)

TOOL_DEFINITIONS = {
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

METHOD_SPECS = [
    ("pdflatex", "raw", ["pdflatex", "pdflatex"]),
    ("lualatex", "raw", ["lualatex", "lualatex"]),
    ("xelatex", "raw", ["xelatex", "xelatex"]),
    (
        "xelatex -> xdvipdfmx",
        "raw",
        ["xelatex (no-pdf)", "xelatex (no-pdf)", "xdvipdfmx"],
    ),
    ("platex -> dvipdfmx", "dvipdfmx", ["platex", "platex", "dvipdfmx"]),
    ("uplatex -> dvipdfmx", "dvipdfmx", ["uplatex", "uplatex", "dvipdfmx"]),
    (
        "ptex2pdf (platex)",
        "dvipdfmx",
        ["ptex2pdf (platex)", "ptex2pdf (platex)"],
    ),
    (
        "ptex2pdf (uplatex)",
        "dvipdfmx",
        ["ptex2pdf (uplatex)", "ptex2pdf (uplatex)"],
    ),
    ("latexmk (pdflatex)", "raw", ["latexmk (pdflatex)"]),
]


@dataclass
class CompileMethod:
    name: str
    tex_file: str
    steps: list[str]


def run_compile_method(method: CompileMethod) -> Path | None:
    tex_path = Path(method.tex_file)
    tex_name = tex_path.name
    tex_stem = tex_path.stem
    missing_commands = sorted(
        {
            TOOL_DEFINITIONS[step_name][0]
            for step_name in method.steps
            if shutil.which(TOOL_DEFINITIONS[step_name][0]) is None
        }
    )
    if missing_commands:
        raise RuntimeError(
            f"Required command(s) not found for {method.name}: {', '.join(missing_commands)}"
        )

    print(f"[RUN ] {method.name}")
    for step_name in method.steps:
        command = [
            token.replace("%DOC%", tex_name).replace("%DOCFILE%", tex_stem)
            for token in TOOL_DEFINITIONS[step_name]
        ]
        result = subprocess.run(
            command,
            cwd=SCRIPT_DIR,
            text=True,
            capture_output=True,
        )
        for output in (result.stdout, result.stderr):
            if output.strip():
                print(output[:3000] + ("..." if len(output) > 3000 else ""))
        if result.returncode != 0:
            print(f"[FAIL] {method.name}: {' '.join(command)}")
            return None

    generated_pdf = SCRIPT_DIR / f"{tex_stem}.pdf"
    if not generated_pdf.exists():
        print(f"[FAIL] {method.name}: PDF not found: {tex_stem}.pdf")
        return None

    output_dir = OUTPUT_DIRS[
        "succeeded" if tex_stem.startswith("examples_succeeded_") else "failed"
    ]
    output_pdf = output_dir / (
        f"{tex_stem}__{re.sub(r'[^a-z0-9]+', '_', method.name.lower()).strip('_')}.pdf"
    )
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
    shape = page.new_shape()
    for link in page.get_links():
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

    assert page.rect.width > 0, "Page width must be positive"
    zoom = 2
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
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


def build_markdown_table(caption: str, png_files: list[Path]) -> str:
    assert len(png_files) > 0, f"No PNG files for table: {caption}"
    headers = [_display_label_from_png_name(path.name) for path in png_files]
    image_urls = [
        f"{RAW_GITHUB_BASE_URL}/{path.parent.name}/{path.name}" for path in png_files
    ]

    header_row = "| " + " | ".join(headers) + " |"
    align_row = "| " + " | ".join([":---:"] * len(headers)) + " |"
    images = [
        f"![{Path(image_url).name.replace('.png', '')}]({image_url})"
        for image_url in image_urls
    ]
    image_row = "| " + " | ".join(images) + " |"
    return "\n".join([f"Table: {caption}", "", header_row, align_row, image_row])


def save_tables(generated_pngs: list[Path]) -> list[Path]:
    saved_files = []
    for status, output_path in TABLE_FILES.items():
        status_tables = []
        for variant, caption in (
            ("raw", "Raw engine outputs"),
            ("dvipdfmx", "DVI-to-PDF workflow outputs"),
        ):
            prefix = f"examples_{status}_{variant}__"
            png_files = sorted(
                path for path in generated_pngs if path.name.startswith(prefix)
            )
            status_tables.append(build_markdown_table(caption, png_files))
        output_path.write_text("\n\n".join(status_tables) + "\n", encoding="utf-8")
        saved_files.append(output_path)
    return saved_files


def get_compile_methods() -> list[CompileMethod]:
    return [
        CompileMethod(
            name=f"{name}{'' if prefix == 'failed' else ' (succeeded)'}",
            tex_file=f"examples_{prefix}_{variant}.tex",
            steps=steps,
        )
        for prefix in ("failed", "succeeded")
        for name, variant, steps in METHOD_SPECS
    ]


def prepare_raw_tex_from_dvipdfmx_tex() -> None:
    source_path = SCRIPT_DIR / "examples_failed_dvipdfmx.tex"
    if not source_path.exists():
        raise FileNotFoundError(
            "Could not find source TeX file: examples_failed_dvipdfmx.tex"
        )
    text = source_path.read_text(encoding="utf-8")

    old_include = ",dvipdfmx]"
    if old_include not in text:
        raise ValueError(
            f"Expected string not found in {source_path.name}: {old_include}"
        )
    text = text.replace(old_include, "]")

    old_recipe = "% !LW recipe=platex"
    if old_recipe not in text:
        raise ValueError(
            f"Expected string not found in {source_path.name}: {old_recipe}"
        )
    text = text.replace(old_recipe, "% !LW recipe=pdflatex")

    (SCRIPT_DIR / "examples_failed_raw.tex").write_text(text, encoding="utf-8")


def prepare_succeeded_tex_from_failed_tex() -> None:
    for source_name, target_name in (
        ("examples_failed_raw.tex", "examples_succeeded_raw.tex"),
        ("examples_failed_dvipdfmx.tex", "examples_succeeded_dvipdfmx.tex"),
    ):
        source_path = SCRIPT_DIR / source_name
        target_path = SCRIPT_DIR / target_name
        text = source_path.read_text(encoding="utf-8")

        old_macro = r"\XeTeXLinkBox"
        if old_macro not in text:
            raise ValueError(
                f"Expected string not found in {source_path.name}: {old_macro}"
            )
        text = text.replace(old_macro, r"\HyperrefLinkBox")
        text = text.replace(r"\usepackage{orcidlink}", r"\usepackage{myorcidlink}")
        target_path.write_text(text, encoding="utf-8")


def main() -> None:
    prepare_raw_tex_from_dvipdfmx_tex()
    prepare_succeeded_tex_from_failed_tex()
    for output_dir in OUTPUT_DIRS.values():
        output_dir.mkdir(parents=True, exist_ok=True)
        build_dir = output_dir / "_build"
        if build_dir.exists() and build_dir.is_dir():
            shutil.rmtree(build_dir)

    generated_pdfs = []
    for method in get_compile_methods():
        pdf_path = run_compile_method(method)
        if pdf_path is None:
            raise RuntimeError(f"Compilation failed: {method.name}")
        generated_pdfs.append(pdf_path)

    unnecessary_suffixes = [
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
    ]
    for item in SCRIPT_DIR.iterdir():
        if item.is_file() and item.suffix in unnecessary_suffixes:
            item.unlink()

    generated_pngs = [
        png_path
        for pdf_file in generated_pdfs
        for png_path in [annotate_and_convert_pdf_to_png(pdf_file)]
        if png_path is not None
    ]

    table_files = save_tables(generated_pngs)
    print("\nSaved tables:\n")
    for table_file in table_files:
        print(table_file)

    print(
        "Done. Generated "
        f"{len(generated_pdfs)} PDF(s) and PNG(s) in: "
        f"{OUTPUT_DIRS['failed']} and {OUTPUT_DIRS['succeeded']}"
    )


if __name__ == "__main__":
    main()
