import sys
from pathlib import Path

import pytest

OPTIMIZATION_WORDS_DIR = Path(__file__).parents[1] / "20260827_OptimizationWords"
sys.path.insert(0, str(OPTIMIZATION_WORDS_DIR))

from update_readme import replace_name_dashes, rewrite_images  # noqa: E402


@pytest.mark.parametrize(
    "text",
    [
        "<!-- comment -->\n",
        "<!--\nalpha--beta and Bellman--Ford\n-->\n",
        "<!-- unclosed Bellman--Ford\n",
        "| --- | --- |\n",
        "|:--|--:|:--:|\n",
        ":--- | ---:\n",
        "  | --- |\r\n",
        "---\n",
        "  ----  \n",
        "- --\n",
        "![Bellman--Ford](Bellman--Ford.png)\n",
        '<img src="Bellman--Ford.png" alt="Bellman--Ford">\n',
    ],
)
def test_replace_name_dashes_ignores_obvious_non_prose(text):
    updated, unreplaced = replace_name_dashes(text, Path("README.md"))

    assert updated == text
    assert unreplaced == []


def test_replace_name_dashes_keeps_prose_checks_around_excluded_markup():
    source = Path("Example/README.md")
    text = (
        "<!-- hidden --> Bellman--Ford\n"
        "| --- | :---: |\n"
        "<!-- multiline\ncomment --> alpha--beta\n"
        "| alpha--beta | value |\n"
        "--\n"
    )

    updated, unreplaced = replace_name_dashes(text, source)

    assert updated == text.replace("Bellman--Ford", "Bellman–Ford")
    assert [(item.source, item.line, item.column, item.text) for item in unreplaced] == [
        (source, 4, 18, "comment --> alpha--beta"),
        (source, 5, 8, "| alpha--beta | value |"),
        (source, 6, 1, "--"),
    ]


def test_rewrite_images_adds_wikipedia_and_embedded_media_licenses(tmp_path):
    article_dir = tmp_path / "Example"
    article_dir.mkdir()
    source = article_dir / "README.md"
    (article_dir / "Wiki.png").touch()
    (article_dir / "image_licenses.json").write_text(
        """{
          "images": {
            "Wiki.png": {
              "embedded_media": [{
                "title": "Example.svg",
                "author": "Example author",
                "source_url": "https://commons.wikimedia.org/wiki/File:Example.svg",
                "license": "CC BY 3.0",
                "license_url": "https://creativecommons.org/licenses/by/3.0/",
                "notice": "Example license notice"
              }]
            }
          }
        }""",
        encoding="utf-8",
    )
    text = "https://en.wikipedia.org/wiki/Example\n\n![Wiki](Wiki.png)\n"

    result = rewrite_images(text, source, tmp_path, "owner/repo", "main")

    assert "[Wikipedia contributors](<https://en.wikipedia.org/wiki/Example>)" in result
    assert "[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)" in result
    assert "[Example.svg](<https://commons.wikimedia.org/wiki/File:Example.svg>)" in result
    assert "Example author" in result
    assert "[CC BY 3.0](<https://creativecommons.org/licenses/by/3.0/>)" in result
    assert "Example.svg のライセンス告知全文" in result
    assert "Example license notice" in result


def test_rewrite_images_adds_wikipedia_license_without_image_metadata(tmp_path):
    article_dir = tmp_path / "Example"
    article_dir.mkdir()
    source = article_dir / "README.md"
    (article_dir / "Wiki-Definition.png").touch()
    text = "https://ja.wikipedia.org/wiki/Example\n\n![Wiki](Wiki-Definition.png)\n"

    result = rewrite_images(text, source, tmp_path, "owner/repo", "main")

    assert "Wikipedia contributors" in result
    assert "CC BY-SA 4.0" in result
    assert "画像:" not in result
