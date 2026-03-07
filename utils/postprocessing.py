"""Post-processing functions for LaTeX to Markdown conversion."""

import re
import sys
from pathlib import Path

# Ensure imports work from doc/study directory
sys.path.insert(0, str(Path(__file__).parent))

from citation import convert_citep
from converters import (
    convert_equation_environments,
    convert_href_to_md,
    convert_nested_itemize_enumerate,
)


def post_process_content(content: str) -> str:
    """Apply post-processing conversions to content.

    This is applied after main environment processing to handle conversions
    that should apply recursively inside other environments (like proof).

    Order matters: equation conversion first, then nested list environments,
    then cref conversion.

    Args:
        content: The content to post-process

    Returns:
        Post-processed content
    """
    # First apply equation environment conversion
    content = convert_equation_environments(content)
    # Convert \href{url}{alt} to Markdown links
    content = convert_href_to_md(content)
    # Then convert nested itemize/enumerate
    content = convert_nested_itemize_enumerate(content)
    # Remove labels and \myQED
    content = re.sub(r"\\label\{[^}]+\}", "", content)
    content = re.sub(r"--(?=[A-Z])", "–", content)
    content = content.replace("\\myQED", "")
    content = content.replace("^*", "^\\ast")
    assert "\\norm{" not in content
    assert "\\qty" not in content
    # Note: citep conversion is applied in for_qiita_post_process
    return content


def for_qiita_post_process(content: str) -> str:
    """Apply Qiita-specific post-processing to content.

    Converts math blocks, processes various LaTeX commands, and applies
    citation conversion with footnote definitions at the end.

    Args:
        content: The content to post-process

    Returns:
        Post-processed content ready for Qiita
    """
    lines = content.splitlines()
    resList = []
    mathBlockOpen = False
    for line in lines:
        if line.strip() == "$$":
            resList.append("\n```math" if not mathBlockOpen else "```\n")
            mathBlockOpen = not mathBlockOpen
        elif line.strip() == "> $$":
            resList.append(">" if not mathBlockOpen else "> ```")
            resList.append("> ```math" if not mathBlockOpen else ">")
            mathBlockOpen = not mathBlockOpen
        else:
            resList.append(line)
    res = "\n".join(resList) + "\n"
    res = re.sub(r"\n{3,}", "\n\n", res)
    res = res.replace("\\coloneqq", "\\mathrel{\\vcenter{:}}=").replace(
        "{dcases}", "{cases}"
    )
    for line in res.splitlines():
        if re.search(r"\\{[a-zA-Z0-9]", line):
            print(r"Warning: Add space after \{[a-zA-Z0-9] in line: " + line)
    res = res.replace("\\{", "\\lbrace").replace("\\}", "\\rbrace")
    if res.count("\\,"):
        print("Warning: \\, found. Use \\ instead.")

    cnt = res.count("\\|")
    if cnt % 2 == 1:
        raise ValueError(f"Odd number of \\| found: {cnt}")
    lastIdx = 0
    res2 = ""
    for vertNum, resIdx in enumerate(re.finditer(r"\\\|", res)):
        res2 += res[lastIdx : resIdx.start()]
        res2 += "\\lVert" if vertNum % 2 == 0 else "\\rVert"
        lastIdx = resIdx.end()
    res2 += res[lastIdx:]

    # Apply citep conversion with footnote definitions
    res2 = convert_citep(res2)

    return res2
