"""Converter functions for LaTeX to Markdown conversion."""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# Ensure imports work from doc/study directory
sys.path.insert(0, str(Path(__file__).parent))

from config import ENV_DISPLAY_NAMES, GITHUB_RAW_URL_BASE, USE_GITHUB_URL
from utils import extract_braced_content


def convert_cref(line: str, label_map: Dict[str, tuple]) -> str:
    r"""Convert \cref{label} to appropriate reference format.

    Args:
        line: The line containing \cref commands
        label_map: Map of label names to their (type, number) tuples

    Returns:
        Line with \cref commands converted
    """

    def cref_replace(match: re.Match[str]) -> str:
        labels = [label.strip() for label in match.group(1).split(",") if label.strip()]
        if not labels:
            return match.group(0)

        converted: List[str] = []
        for label in labels:
            if label not in label_map:
                return match.group(0)
            label_type, label_num = label_map[label]
            display_name = ENV_DISPLAY_NAMES.get(label_type)
            if not display_name:
                return match.group(0)
            converted.append(f"{display_name} {label_num}")

        return ", ".join(converted)

    return re.sub(r"\\[Cc]ref\{([^}]+)\}", cref_replace, line)


def convert_section_commands(line: str) -> str:
    """Convert LaTeX section commands to Markdown headers."""
    section_mappings = [
        ("section", "##"),
        ("subsection", "###"),
        ("subsubsection", "####"),
        ("paragraph", "#####"),
        ("subparagraph", "######"),
    ]
    for cmd, heading in section_mappings:
        pattern = rf"\\{cmd}\{{([^}}]*)\}}"
        replacement = rf"{heading} \1"
        line = re.sub(pattern, replacement, line)
    return line


def convert_nested_itemize_enumerate(content: str) -> str:
    """Convert nested itemize and enumerate environments within content.

    This function handles itemize/enumerate blocks that appear inside other
    environments (e.g., theorem, proposition).

    Args:
        content: The content string potentially containing itemize/enumerate blocks

    Returns:
        Content with itemize/enumerate blocks converted to Markdown
    """
    result = []
    i = 0
    lines = content.split("\n")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check for beginning of itemize or enumerate
        if stripped.startswith("\\begin{itemize}"):
            # Collect the entire itemize block
            block_lines = [line]
            i += 1
            while i < len(lines):
                block_lines.append(lines[i])
                if lines[i].strip().startswith("\\end{itemize}"):
                    i += 1
                    break
                i += 1
            # Convert and add
            converted = convert_itemize_to_md("\n".join(block_lines))
            if converted:
                result.append(converted.rstrip())
        elif stripped.startswith("\\begin{enumerate}"):
            # Collect the entire enumerate block
            block_lines = [line]
            i += 1
            while i < len(lines):
                block_lines.append(lines[i])
                if lines[i].strip().startswith("\\end{enumerate}"):
                    i += 1
                    break
                i += 1
            # Convert and add
            converted = convert_enumerate_to_md("\n".join(block_lines))
            if converted:
                result.append(converted.rstrip())
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def convert_href_to_md(content: str) -> str:
    r"""Convert \href{url}{alt} to Markdown [alt](url)."""

    def href_replace(match: re.Match[str]) -> str:
        url = match.group(1)
        alt = match.group(2)
        return f"[{alt}]({url})"

    return re.sub(r"\\href\{([^}]+)\}\{([^}]+)\}", href_replace, content)


def convert_subfile_to_md(content: str) -> str:
    r"""Convert \subfile{filename.tex} to ![filename](filename.png)."""
    from pathlib import Path

    def subfile_replace(match: re.Match[str]) -> str:
        filepath = match.group(1)
        # Extract filename without extension
        filename = Path(filepath).stem
        # Build image path
        image_path = filename + ".png"
        if USE_GITHUB_URL:
            url = f"{GITHUB_RAW_URL_BASE}doc/study/{image_path}"
        else:
            url = image_path
        return f"![{filename}]({url})"

    return re.sub(r"\\subfile\{([^}]+)\}", subfile_replace, content)


def convert_equation_environments(block: str) -> str:
    r"""Convert LaTeX equation environments to Markdown $$ format.

    Converts \begin{equation}...\end{equation} and similar environments
    to $$\n...\n$$ format for Markdown rendering.

    Handles: equation, equation*, align, align*
    """
    lines = block.split("\n")
    result_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check for begin of equation environments
        if re.match(r"\\begin\{(equation\*?|align\*?)\}", stripped):
            # Add newline and $$ before the environment
            result_lines.append("")
            result_lines.append("$$")
            result_lines.append(line)
        # Check for end of equation environments
        elif re.match(r"\\end\{(equation\*?|align\*?)\}", stripped):
            # Add $$ and newline after the environment
            result_lines.append(line)
            result_lines.append("$$")
            result_lines.append("")
        else:
            result_lines.append(line)

    return "\n".join(result_lines)


def convert_itemize_to_md(block: str) -> str:
    """Convert \\item lines to Markdown bullet points."""
    lines = block.split("\n")
    converted = []
    depth = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("\\begin{itemize}"):
            depth += 1
        elif stripped.startswith("\\end{itemize}"):
            depth -= 1
        elif stripped.startswith("\\item"):
            content = stripped[5:].strip()
            indent = "  " * (depth - 1)
            converted.append(f"{indent}- {content}")
        elif not stripped.startswith("\\"):
            if converted and stripped:
                converted[-1] += " " + stripped

    return "\n".join(converted)


def convert_enumerate_to_md(block: str) -> str:
    """Convert \\item lines to Markdown numbered list."""
    lines = block.split("\n")
    converted = []
    depth = 0
    counters = {}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("\\begin{enumerate}"):
            depth += 1
            counters[depth] = 0
        elif stripped.startswith("\\end{enumerate}"):
            depth -= 1
        elif stripped.startswith("\\item"):
            content = stripped[5:].strip()
            counters[depth] = counters.get(depth, 0) + 1
            indent = "  " * (depth - 1)
            converted.append(f"{indent}{counters[depth]}. {content}")
        elif not stripped.startswith("\\"):
            if converted and stripped:
                converted[-1] += " " + stripped

    return "\n".join(converted)


def convert_proof_to_md(block: str, is_japanese_mode: bool) -> str:
    """Convert proof environment to Markdown with italic 'Proof'.

    Removes \\begin{proof}...\\end{proof} lines and replaces with italic text.
    """
    lines = block.split("\n")
    converted = []
    for line in lines:
        stripped = line.strip()
        if stripped == "\\begin{proof}":
            converted.append(
                f"<details><summary>{'証明' if is_japanese_mode else 'Proof'}</summary>\n"
            )
        elif stripped == "\\end{proof}":
            converted.append(
                f"({'証明終わり' if is_japanese_mode else 'End of proof'})\n\n</details>"
            )
        else:
            converted.append(line)
    return "\n".join(converted).strip()


def convert_math_env_to_md(block: str, env_name: str, counter: int) -> str:
    """Convert math environment (theorem, lemma, etc.) to Markdown.

    Formats as:
    **[Environment Name] [counter]**
    content...
    """
    display_name = ENV_DISPLAY_NAMES.get(env_name, env_name)
    lines = block.split("\n")
    first_line = f"**{display_name} {counter}**"

    line_zero = lines[0].strip()
    if line_zero.startswith(f"\\begin{{{env_name}}}["):
        # Extract optional argument for environment (e.g., theorem name)
        opt_arg_match = line_zero[line_zero.find("[") + 1 : line_zero.rfind("]")]
        if opt_arg_match:
            if opt_arg_match.startswith("{") and opt_arg_match.endswith("}"):
                opt_arg = opt_arg_match[1:-1].strip()
            else:
                opt_arg = opt_arg_match.strip()
            if opt_arg:
                print(opt_arg)
                first_line += f" ({opt_arg})"

    result_lines = [first_line]

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith(
            f"\\begin{{{env_name}}}"
        ) and not stripped.startswith(f"\\end{{{env_name}}}"):
            result_lines.append(line)

    return "\n".join(result_lines)


def add_version_query(image_path: str, url: str) -> str:
    with open(Path(__file__).parent / "image_versions.json", "rb") as f:
        image_versions = json.load(f)
    print(image_path)
    image_version = image_versions.get(image_path, 0)
    if image_version:
        url += f"?v={image_version}"
    return url


def convert_figure_to_md(block: str, counter: int) -> str:
    r"""Convert LaTeX figure block to Markdown.

    Converts \includegraphics paths to GitHub raw content URLs and PDF to PNG.
    Extracts caption and adds it below the figure.
    """
    image_entries = extract_figure_images(block)
    if not image_entries:
        return ""

    if len(image_entries) == 1:
        image_path = image_entries[0]["path"].replace(".pdf", ".png")
        if USE_GITHUB_URL:
            assert image_path.startswith("../")
            url = f"{GITHUB_RAW_URL_BASE}doc/{image_path.replace('../', '')}"
            url = add_version_query(image_path, url)
        else:
            url = image_path
        result = f"![{image_path}]({url})\n"
    else:
        img_tags = []
        for entry in image_entries:
            image_path = entry["path"].replace(".pdf", ".png")
            if USE_GITHUB_URL:
                assert image_path.startswith("../")
                url = f"{GITHUB_RAW_URL_BASE}doc/{image_path.replace('../', '')}"
                url = add_version_query(image_path, url)
            else:
                url = image_path
            width = entry.get("width_percent")
            if width is not None:
                if "modified_secant/trial" in image_path:
                    width = "100"
                img_tags.append(f'<img width="{width}%" src="{url}" />')
            else:
                img_tags.append(f'<img src="{url}" />')
        result = "".join(img_tags) + "\n"

    caption_texts = extract_braced_content(block, "caption")
    if caption_texts:
        assert len(caption_texts) == 1
        caption_text = caption_texts[0].replace("\n", " ").strip()
        result += f"\n({ENV_DISPLAY_NAMES['figure']} {counter} {caption_text})\n"

    return result


def extract_figure_images(block: str) -> List[Dict[str, str]]:
    r"""Extract image paths and widths from figure blocks.

    Supports simplified patterns with minipage widths like 0.5\textwidth or 0.33\textwidth.
    Returns a list of dicts with keys: path, width_percent (optional).
    """
    images: List[Dict[str, str]] = []

    # Find minipage blocks with includegraphics inside
    minipage_pattern = re.compile(
        r"\\begin\{minipage\}\{([0-9.]+)\\textwidth\}(.*?)\\end\{minipage\}",
        re.DOTALL,
    )
    include_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")

    for match in minipage_pattern.finditer(block):
        width_str = match.group(1)
        inner = match.group(2)
        img_match = include_pattern.search(inner)
        if not img_match:
            continue
        path = img_match.group(1)
        width_percent = str(round(float(width_str) * 100))
        images.append({"path": path, "width_percent": width_percent})

    # Find standalone includegraphics
    if not images:
        for match in include_pattern.finditer(block):
            path = match.group(1)
            images.append({"path": path, "width_percent": "100"})

    return images


def convert_table_to_md(block: str, counter: int) -> str:
    """Convert LaTeX table to Markdown.

    Extracts tabular content and formats as Markdown table.
    Adds caption below the table.
    """
    # Extract tabular block
    tabular_match = re.search(
        r"\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}", block, re.DOTALL
    )
    if not tabular_match:
        return ""

    content = tabular_match.group(2)

    # Parse table rows and cells
    lines = [line.strip() for line in content.split("\n") if line.strip()]

    # Split by \\ to get rows
    rows = []
    current_row = []
    for line in lines:
        cells = [
            cell.strip().replace("\\\\", "").replace(" ", "")
            for cell in line.split("&")
        ]
        cells = [c for c in cells if c != "\\hline"]
        if len(cells) == 0:
            continue
        current_row.extend(cells)
        if "\\\\" in line:
            rows.append(current_row)
            current_row = []

    if current_row:
        rows.append(current_row)

    if not rows:
        return ""

    # Build Markdown table
    result_lines = []

    # Header row
    result_lines.append("| " + " | ".join(rows[0]) + " |")

    # Separator row
    col_count = len(rows[0])
    result_lines.append("|" + "|".join([" --- " for _ in range(col_count)]) + "|")

    # Data rows
    for row in rows[1:]:
        result_lines.append("| " + " | ".join(row) + " |")

    result = "\n".join(result_lines) + "\n"

    # Add caption
    caption_texts = extract_braced_content(block, "caption")
    if caption_texts:
        assert len(caption_texts) == 1
        caption_text = caption_texts[0].replace("\n", " ").strip()
        result += f"\n({ENV_DISPLAY_NAMES['table']} {counter}: {caption_text})\n"

    return result
