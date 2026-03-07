"""LaTeX to Markdown converter processor class."""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Ensure imports work from doc/study directory
sys.path.insert(0, str(Path(__file__).parent))

from config import EQUATION_ENVS, MATH_ENVS, OTHER_ENVS
from converters import (
    convert_cref,
    convert_enumerate_to_md,
    convert_figure_to_md,
    convert_href_to_md,
    convert_itemize_to_md,
    convert_math_env_to_md,
    convert_proof_to_md,
    convert_section_commands,
    convert_subfile_to_md,
    convert_table_to_md,
)
from utils import preprocess_latex


class GlobalState:
    """Global state for LaTeX conversion."""

    def __init__(self) -> None:
        """Initialize global state with counters and label map."""
        self.global_counters: Dict[str, int] = {
            "figure": 0,
            "table": 0,
            "theorem": 0,
            "proposition": 0,
            "lemma": 0,
            "definition": 0,
            "corollary": 0,
            "remark": 0,
            "example": 0,
            "assumption": 0,
        }
        self.label_map: Dict[str, Tuple[str, int]] = {}

    def reset(self) -> None:
        """Reset global counters and label map."""
        for key in self.global_counters:
            self.global_counters[key] = 0
        self.label_map.clear()


# Global state instance
_global_state = GlobalState()


def get_global_state() -> GlobalState:
    """Get the global state instance."""
    return _global_state


class LatexToMarkdownConverter:
    """LaTeX to Markdown converter class."""

    def __init__(self, filepath: Path, is_japanese_mode: bool) -> None:
        """Initialize converter with filepath.

        Args:
            filepath: Path to the LaTeX file to convert
            is_japanese_mode: Whether to process in Japanese mode
        """
        self.filepath = filepath
        self.is_japanese_mode = is_japanese_mode
        self.lines: List[str] = []
        self.markdown_lines: List[str] = []
        self.i = 0
        # Map from (env_name, line_number) to counter value
        self.env_counters: Dict[Tuple[str, int], int] = {}
        self.global_state = get_global_state()

    def process_environment_block(self, line: str) -> bool:
        """Process environment blocks (figure, table, itemize, enumerate, theorem-like, proof).

        Returns:
            True if the block was processed, False otherwise.
        """
        all_envs = self._get_all_envs_pattern()
        environment_match = re.match(r"\\begin\{(" + all_envs + r")\}", line)
        if not environment_match:
            self.markdown_lines.append(self.process_normal_line(line))
            self.i += 1
            return False

        env_name = environment_match.group(1)
        # Record the starting line number for this environment
        env_start_line = self.i
        block = self._collect_environment_block(env_name, line)
        cleaned_block, labels = self.extract_and_remove_labels(block)

        converted = self._convert_environment(
            env_name, cleaned_block, labels, env_start_line
        )

        if converted:
            self.markdown_lines.append(self.process_normal_line(converted))

        return True

    def _get_all_envs_pattern(self) -> str:
        """Get regex pattern for all supported environments."""
        return (
            "figure|table|itemize|enumerate|"
            + "|".join(MATH_ENVS)
            + "|"
            + "|".join(EQUATION_ENVS).replace("*", r"\*")
            + "|"
            + "|".join(OTHER_ENVS)
        )

    def _collect_environment_block(self, env_name: str, first_line: str) -> str:
        """Collect lines until \\end{env_name} is found."""
        block_lines = [first_line]
        self.i += 1

        while self.i < len(self.lines):
            block_line = self.lines[self.i].strip()
            block_lines.append(block_line)

            if f"\\end{{{env_name}}}" in block_line:
                self.i += 1
                return "\n".join(block_lines)
            self.i += 1

        raise ValueError(f"Missing \\end{{{env_name}}} in {self.filepath}")

    def _convert_environment(
        self, env_name: str, block: str, labels: List[str], env_start_line: int
    ) -> str:
        """Convert environment block to Markdown based on environment type.

        Args:
            env_name: Name of the environment
            block: Content of the environment block
            labels: List of labels in the block
            env_start_line: Starting line number of the environment

        Returns:
            Converted Markdown string
        """
        if env_name in ("figure", "table"):
            return self._convert_numbered_env(env_name, block, labels, env_start_line)
        elif env_name == "itemize":
            return convert_itemize_to_md(block)
        elif env_name == "enumerate":
            return convert_enumerate_to_md(block)
        elif env_name in MATH_ENVS:
            return self._convert_numbered_env(env_name, block, labels, env_start_line)
        elif env_name in EQUATION_ENVS:
            return block  # done in postprocessing
        elif env_name == "proof":
            return convert_proof_to_md(block, self.is_japanese_mode)
        return ""

    def _convert_numbered_env(
        self, env_name: str, block: str, labels: List[str], env_start_line: int
    ) -> str:
        """Convert numbered environment (figure, table, math) to Markdown.

        Args:
            env_name: Name of the environment
            block: Content of the environment block
            labels: List of labels in the block
            env_start_line: Starting line number of the environment

        Returns:
            Converted Markdown string
        """
        # Get the counter value that was assigned during preregister_labels
        counter = self.env_counters.get(
            (env_name, env_start_line), self.global_state.global_counters[env_name]
        )

        if env_name == "figure":
            return convert_figure_to_md(block, counter)
        elif env_name == "table":
            return convert_table_to_md(block, counter)
        else:
            return convert_math_env_to_md(block, env_name, counter)

    def preregister_labels(self) -> None:
        """Pre-scan the file to register all labels before processing.

        This ensures that \\cref{label} references can be converted correctly.
        """
        in_document = False
        i = 0
        all_envs = self._get_all_envs_pattern()

        while i < len(self.lines):
            line = self.lines[i]

            if not in_document:
                if r"\begin{document}" in line:
                    in_document = True
                i += 1
                continue

            if r"\end{document}" in line:
                break

            environment_match = re.match(
                r"\\begin\{(" + all_envs + r")\}", line.strip()
            )

            if environment_match:
                env_name = environment_match.group(1)
                i = self._preregister_env_labels(env_name, i)
            else:
                i += 1

    def _preregister_env_labels(self, env_name: str, start_idx: int) -> int:
        """Pre-register labels for a single environment block.

        Args:
            env_name: Name of the environment
            start_idx: Starting index in self.lines

        Returns:
            Updated line index
        """
        block_lines = [self.lines[start_idx].strip()]
        i = start_idx + 1

        while i < len(self.lines):
            block_line = self.lines[i].strip()
            block_lines.append(block_line)

            if f"\\end{{{env_name}}}" in block_line:
                i += 1
                break
            i += 1

        block = "\n".join(block_lines)
        _, labels = self.extract_and_remove_labels(block)

        if env_name in ("figure", "table") or env_name in MATH_ENVS:
            self.global_state.global_counters[env_name] += 1
            counter = self.global_state.global_counters[env_name]
            # Store the counter value for this specific environment instance
            self.env_counters[(env_name, start_idx)] = counter
            self.register_labels(labels, env_name, counter)

        return i

    def extract_and_remove_labels(self, block: str) -> Tuple[str, List[str]]:
        r"""Extract labels from block and return cleaned block + list of labels.

        Args:
            block: The content block to process

        Returns:
            (cleaned_block, label_list): cleaned block with labels removed, and list of label names
        """
        labels = [match.group(1) for match in re.finditer(r"\\label\{([^}]+)\}", block)]
        # Remove \label{...} along with preceding newline and whitespace if present
        cleaned_block = re.sub(r"\n\s*\\label\{[^}]+\}", "", block)
        # Also remove \label{...} without preceding newline (fallback)
        cleaned_block = re.sub(r"\\label\{[^}]+\}", "", cleaned_block)
        return cleaned_block, labels

    def register_labels(self, labels: List[str], env_name: str, counter: int) -> None:
        """Register labels in label map.

        Args:
            labels: List of label names
            env_name: Name of the environment
            counter: Counter value for this environment
        """
        for label in labels:
            self.global_state.label_map[label] = (env_name, counter)

    def process_normal_line(self, line: str) -> str:
        """Process a normal (non-environment) line.

        Args:
            line: The line to process
        """
        # Convert \subfile{...} commands first
        line = convert_subfile_to_md(line)
        # Convert \href{url}{alt}
        line = convert_href_to_md(line)
        # Convert \cref references
        line = convert_cref(line, self.global_state.label_map)
        # Convert section commands
        line = convert_section_commands(line)
        return line

    def process_file(self) -> List[str]:
        """Process the LaTeX file and return list of Markdown lines.

        Returns:
            List of Markdown lines
        """
        content = self.filepath.read_text(encoding="utf-8")
        content = preprocess_latex(content, self.is_japanese_mode)

        self.lines = content.split("\n")
        self.markdown_lines = []

        self.preregister_labels()

        in_document = False
        self.i = 0

        while self.i < len(self.lines):
            line = self.lines[self.i]

            if not in_document:
                if r"\begin{document}" in line:
                    in_document = True
                self.i += 1
                continue

            if r"\end{document}" in line:
                break

            line = line.strip()

            if line.startswith("% QIITA_GIF"):
                lines = [
                    "以下のGIFも参照して下さい。$f(x)$ の最適化において、各step毎にモデル関数が更新されていく様子を示しています。"
                    if self.is_japanese_mode
                    else "Also check the following GIF illustrating how the model function is updated at each step in optimizing $f(x)$.",
                    "",
                    "![GIF illustrating the concept](https://raw.githubusercontent.com/HirokiHamaguchi/qnlab/master/doc/imgs/quasi_newton/sixhump.gif)",
                ]
                self.markdown_lines.extend(lines)
                self.i += 1
                continue

            if line.startswith("%"):
                self.i += 1
                continue

            self.process_environment_block(line)

        return self.markdown_lines


def process_latex_file(filepath: Path, is_japanese_mode: bool) -> List[str]:
    """Process a single LaTeX file and return list of Markdown lines.

    Args:
        filepath: Path to the LaTeX file
        is_japanese_mode: Whether to process in Japanese mode

    Returns:
        List of Markdown lines
    """
    converter = LatexToMarkdownConverter(filepath, is_japanese_mode)
    return converter.process_file()
