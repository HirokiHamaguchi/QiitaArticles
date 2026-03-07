"""Utility functions for LaTeX parsing and conversion."""

import re
from typing import List


def find_matching(s: str, start_pos: int, bracket_type: str = "brace") -> int:
    r"""Find the position of the closing bracket matching the opening bracket at start_pos.

    Handles nested brackets correctly by counting bracket pairs.

    Args:
        s: The string to search
        start_pos: Position of the opening bracket
        bracket_type: Type of bracket to match - "brace" for {} or "bracket" for []

    Returns:
        Position of the matching closing bracket, or -1 if not found
    """
    bracket_pairs = {
        "brace": ("{", "}"),
        "bracket": ("[", "]"),
    }

    if bracket_type not in bracket_pairs:
        return -1

    open_char, close_char = bracket_pairs[bracket_type]

    if start_pos >= len(s) or s[start_pos] != open_char:
        return -1

    count = 1
    i = start_pos + 1

    while i < len(s) and count > 0:
        if s[i] == "\\":
            # Skip escaped characters
            i += 2
            continue
        elif s[i] == open_char:
            count += 1
        elif s[i] == close_char:
            count -= 1
        i += 1

    if count == 0:
        return i - 1
    return -1


def extract_braced_content(block: str, command: str) -> List[str]:
    r"""Extract content from a LaTeX command with braced argument.

    Handles nested braces correctly.

    Args:
        block: The block content
        command: The command name (e.g., 'caption', 'begin')

    Returns:
        Content within the braces, or empty string if not found
    """
    pattern = rf"\\{command}\{{"
    matches = re.finditer(pattern, block)
    results = []

    for match in matches:
        start_brace = match.end() - 1  # Position of the opening brace
        end_brace = find_matching(block, start_brace, "brace")

        if end_brace != -1:
            results.append(block[start_brace + 1 : end_brace])

    return results


def preprocess_latex(content: str, is_japanese_mode: bool) -> str:
    r"""Preprocess LaTeX content.

    Process \ifEn...\else...\fi blocks.
    """
    if is_japanese_mode:
        # Remove \ifEn...\else...\fi blocks (delete from \ifEn to \else, then delete \fi)
        # This removes the first branch and keeps the second branch
        pattern = r"^\s*\\ifEn\s*$.*?^\s*\\else\s*$"
        content = re.sub(pattern, "", content, flags=re.MULTILINE | re.DOTALL)
        # Remove the \fi command
        pattern = r"^\s*\\fi\s*$"
        content = re.sub(pattern, "", content, flags=re.MULTILINE)
    else:
        # Remove \ifEn...\else...\fi blocks (delete from \else to \fi, then delete \ifEn)
        # This removes the second branch and keeps the first branch
        pattern = r"^\s*\\else\s*$.*?^\s*\\fi\s*$"
        content = re.sub(pattern, "", content, flags=re.MULTILINE | re.DOTALL)
        # Remove the \ifEn command
        pattern = r"^\s*\\ifEn\s*$"
        content = re.sub(pattern, "", content, flags=re.MULTILINE)

    # Remove \ifSubfilesClassLoaded{...}{} blocks
    pattern = r"\\ifSubfilesClassLoaded\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\s*\{\}"
    return re.sub(pattern, "", content, flags=re.DOTALL)
