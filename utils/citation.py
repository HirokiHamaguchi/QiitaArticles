"""Citation handling for LaTeX to Markdown conversion."""

import json
import re
from pathlib import Path
from typing import Dict, Iterable, Tuple

try:
    from config import CITE_MAPPING_FILE
except ImportError:
    # Fallback for relative imports
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from config import CITE_MAPPING_FILE


def load_cite_mapping(json_file: str = CITE_MAPPING_FILE) -> Dict[str, str]:
    """Load citation key mappings from JSON file.

    Args:
        json_file: Path to the JSON file containing citation mappings

    Returns:
        Dictionary mapping citation keys to their bibliography information
    """
    json_path = Path(__file__).parent / json_file
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Data is a flat dictionary: {citationKey: "bibliography info"}
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load {json_file}: {e}")
        return {}


def _sanitize_bbl_text(text: str) -> str:
    """Normalize LaTeX-ish bibliography text into a single readable line."""
    # Unwrap common LaTeX formatting commands.
    text = re.sub(r"\\newblock\s*", " ", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\texttt\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\url\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\doi\{([^}]*)\}", r"doi: \1", text)
    text = re.sub(r"\\penalty0\s*", " ", text)
    text = re.sub(r"\\natexlab\s*[a-zA-Z]", "", text)
    text = text.replace("~", " ")

    # Convert DOI to link format.
    text = re.sub(
        r"\bdoi:\s*([^\s,;]+)",
        r"https://doi.org/\1",
        text,
        flags=re.IGNORECASE,
    )

    # Remove remaining braces and collapse whitespace.
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _iter_bbl_entries(lines: Iterable[str]) -> Iterable[Tuple[str, str]]:
    """Yield (key, raw_text) entries from a .bbl file."""
    key = None
    buffer: list[str] = []
    bibitem_re = re.compile(r"^\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
    end_re = re.compile(r"^\\end\{thebibliography\}")

    for line in lines:
        if end_re.match(line):
            break
        match = bibitem_re.match(line)
        if match:
            if key is not None:
                yield key, "".join(buffer)
            key = match.group(1).strip()
            buffer = []
            continue

        if key is not None:
            buffer.append(line)

    if key is not None:
        yield key, "".join(buffer)


def generate_cite_mapping_from_bbl(
    bbl_file: str,
    output_json: str = CITE_MAPPING_FILE,
) -> Dict[str, str]:
    """Generate cite_mapping.json from a fixed .bbl file.

    Args:
        bbl_file: Path to the .bbl file (e.g., 0_main.bbl)
        output_json: Output JSON filename (relative to this file)

    Returns:
        The generated citation mapping dictionary.
    """
    bbl_path = Path(bbl_file)
    if not bbl_path.is_absolute():
        bbl_path = Path(__file__).parent / bbl_path

    output_path = Path(__file__).parent / output_json

    with open(bbl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    mapping: Dict[str, str] = {}
    for key, raw_text in _iter_bbl_entries(lines):
        mapping[key] = _sanitize_bbl_text(raw_text)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    return mapping


def convert_citep(content: str) -> str:
    r"""Convert \citep{key1,key2,...} to Markdown footnote references.

    Loads citation mappings from cite_mapping.json and replaces \citep commands
    with Markdown footnote references [^key]. Multiple keys can be separated by commas.

    Also appends footnote definitions to the end of content in the format:
    [^key]: bibliography information

    If a key is not found in the mapping, it defaults to "TODO".

    Args:
        content: The content string containing \citep commands

    Returns:
        Content with \citep commands converted to Markdown footnote references,
        with footnote definitions appended at the end
    """
    cite_mapping = load_cite_mapping()
    used_keys = set()

    def citep_replace(match: re.Match[str]) -> str:
        # Extract optional arguments and citation keys
        opt1 = match.group(1)  # First optional argument
        opt2 = match.group(2)  # Second optional argument
        cite_keys = match.group(3)  # Citation keys

        # Split by comma and strip whitespace
        keys = [key.strip() for key in cite_keys.split(",")]

        # Convert each key and track used keys
        footnote_refs = []
        for key in keys:
            used_keys.add(key)
            footnote_refs.append(f"[^{key}]")

        result = "".join(footnote_refs)

        # Add optional arguments if present
        optional_parts = []
        if opt1:
            optional_parts.append(opt1)
        if opt2:
            optional_parts.append(opt2)

        if optional_parts:
            result += f" [{', '.join(optional_parts)}]"

        return result

    # Replace all \citep commands (with optional arguments)
    content_converted = re.sub(
        r"~*\\citep(?:\[([^\]]*)\])?(?:\[([^\]]*)\])?\{([^}]+)\}",
        citep_replace,
        content,
    )

    # Append footnote definitions at the end
    if used_keys:
        footnote_definitions = []
        for key in sorted(used_keys):
            # Get bibliography info from mapping, default to "TODO" if not found
            bib_info = cite_mapping.get(key, "TODO")
            footnote_definitions.append(f"[^{key}]: {bib_info}")

        # Add blank line before footnotes if content doesn't end with newline
        if content_converted and not content_converted.endswith("\n"):
            content_converted += "\n"

        content_converted += "\n" + "\n".join(footnote_definitions)

    return content_converted


if __name__ == "__main__":
    # Regenerate mapping from a fixed bibliography file.
    generate_cite_mapping_from_bbl("../0_main.bbl")
