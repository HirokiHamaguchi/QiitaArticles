import sys
from pathlib import Path

import pytest

OPTIMIZATION_WORDS_DIR = Path(__file__).parents[1] / "20260827_OptimizationWords"
sys.path.insert(0, str(OPTIMIZATION_WORDS_DIR))

from new_word import build_readme, normalize_url_reference  # noqa: E402


def test_normalize_url_reference_accepts_url_only():
    assert normalize_url_reference("https://example.com/article") == (
        "https://example.com/article"
    )


def test_normalize_url_reference_moves_note_to_its_own_paragraph():
    assert normalize_url_reference("https://example.com/article (一言解説)") == (
        "https://example.com/article\n\n(一言解説)"
    )


@pytest.mark.parametrize(
    "value",
    ["任意のテキスト", "https://example.com/article 一言解説"],
)
def test_normalize_url_reference_rejects_other_formats(value):
    with pytest.raises(ValueError):
        normalize_url_reference(value)


def test_build_readme_adds_break_when_url_follows_note():
    references = [
        normalize_url_reference("https://example.com/first (次の文献を参照)"),
        normalize_url_reference("https://example.com/second"),
    ]

    result = build_readme("Example", references, "Description")

    assert (
        "https://example.com/first\n\n"
        "(次の文献を参照)\n<br>\n\n"
        "https://example.com/second"
    ) in result


def test_build_readme_does_not_add_break_when_image_follows_note():
    references = [
        normalize_url_reference("https://example.com/article (我々の論文)"),
        "![Article](Article.png)",
    ]

    result = build_readme("Example", references, "Description")

    assert "(我々の論文)\n\n![Article](Article.png)" in result
    assert "<br>" not in result
