"""Configuration and constants for LaTeX to Markdown conversion."""

from typing import Dict

# GitHub URL configuration
USE_GITHUB_URL = True
GITHUB_RAW_URL_BASE = "https://raw.githubusercontent.com/HirokiHamaguchi/qnlab/master/"

# Environment types
MATH_ENVS = [
    "theorem",
    "proposition",
    "lemma",
    "definition",
    "corollary",
    "remark",
    "example",
    "assumption",
]
EQUATION_ENVS = ["equation", "equation*", "align", "align*"]
OTHER_ENVS = ["proof"]

# Display names for environments
ENV_DISPLAY_NAMES: Dict[str, str] = {
    "figure": "Fig.",
    "table": "Table",
    "theorem": "Theorem",
    "proposition": "Proposition",
    "lemma": "Lemma",
    "definition": "Definition",
    "corollary": "Corollary",
    "remark": "Remark",
    "example": "Example",
    "assumption": "Assumption",
}

# Default citation mapping file
CITE_MAPPING_FILE = "cite_mapping.json"
