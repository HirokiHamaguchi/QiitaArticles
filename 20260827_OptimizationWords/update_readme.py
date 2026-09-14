#!/usr/bin/env python3
"""Build the INDEX and WORDS sections from article-directory README files."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

INDEX_MARKER = "<!-- INDEX -->"
WORDS_MARKER = "<!-- WORDS -->"
README_NAME = "README.md"
DEFAULT_BRANCH = "main"
IMAGE_LICENSES_NAME = "image_licenses.json"
WIKIPEDIA_TEXT_LICENSE_NAME = "CC BY-SA 4.0"
WIKIPEDIA_TEXT_LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"

ATX_HEADING_RE = re.compile(r"^(#{1,6})([ \t]+)(.*?)([ \t]+#+)?$", re.MULTILINE)
MARKDOWN_IMAGE_RE = re.compile(
    r"(?P<prefix>!\[)(?P<alt>[^\]\r\n]*)(?P<middle>\]\()"
    r"(?P<target>[^\s()]+)(?P<suffix>\))"
)
HTML_IMAGE_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_IMAGE_SRC_RE = re.compile(
    r"(?P<prefix>\bsrc\s*=\s*['\"])(?P<target>[^'\"]+)(?P<suffix>['\"])",
    re.IGNORECASE,
)
HTML_ALT_RE = re.compile(
    r"(?P<prefix>\balt\s*=\s*['\"])(?P<alt>[^'\"]*)(?P<suffix>['\"])",
    re.IGNORECASE,
)
SECTION_HEADING_RE = re.compile(r"^##(?:[ \t]+|$)", re.MULTILINE)
CAPITALIZED_WORD_DOUBLE_HYPHEN_RE = re.compile(
    r"(?<![A-Za-z])(?P<left>[A-Z][A-Za-z]*)--(?=[A-Z][A-Za-z]*(?![A-Za-z]))"
)
WIKIPEDIA_SOURCE_LINE_RE = re.compile(
    r"(?m)^[ \t]*(?P<url>https?://[^\s/]+\.wikipedia\.org/wiki/\S+)[ \t]*$"
)


@dataclass(frozen=True)
class Article:
    title: str
    body: str
    source: Path


@dataclass(frozen=True)
class OutlineHeading:
    level: int
    title: str
    position: int


@dataclass(frozen=True)
class UnreplacedDoubleHyphen:
    source: Path
    line: int
    column: int
    text: str


@dataclass(frozen=True)
class LicensedMedia:
    title: str
    author: str
    source_url: str
    license_name: str
    license_url: str | None
    notice: str | None


def run_git(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def find_repo_root(start: Path) -> Path:
    try:
        return Path(run_git(start, "rev-parse", "--show-toplevel")).resolve()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Gitリポジトリを特定できません: {exc}") from exc


def github_repository(repo_root: Path) -> str:
    try:
        remote = run_git(repo_root, "remote", "get-url", "origin")
    except subprocess.CalledProcessError as exc:
        raise SystemExit("GitHub Raw URLの生成にはoriginリモートが必要です。") from exc

    if remote.startswith("git@github.com:"):
        repository = remote.removeprefix("git@github.com:")
    else:
        parsed = urlparse(remote)
        if parsed.hostname != "github.com":
            raise SystemExit(f"originがGitHubを指していません: {remote}")
        repository = parsed.path.lstrip("/")

    repository = repository.removesuffix(".git").strip("/")
    if repository.count("/") != 1:
        raise SystemExit(f"GitHubリポジトリ名をoriginから取得できません: {remote}")
    return repository


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"UTF-8として読めません: {path}") from exc


def atomic_write_utf8(path: Path, text: str) -> None:
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(text)
            temporary.flush()
            os.fsync(temporary.fileno())
            temporary_name = temporary.name
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def extract_title(path: Path, text: str) -> str:
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence:
            match = re.fullmatch(r"#[ \t]+(.+?)(?:[ \t]+#+)?", line)
            if match:
                return match.group(1).strip()
    raise SystemExit(f"先頭レベルの見出し（# タイトル）がありません: {path.name}")


def shift_headings(text: str, path: Path) -> str:
    """Shift Markdown headings by two levels while leaving fenced code untouched."""
    output: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            output.append(line)
            continue

        match = ATX_HEADING_RE.match(line.rstrip("\r\n")) if not in_fence else None
        if not match:
            output.append(line)
            continue
        level = len(match.group(1))
        if level > 4:
            raise SystemExit(
                f"見出しを2段下げるとMarkdownの上限を超えます: {path.name}: {line.strip()}"
            )
        newline = line[len(line.rstrip("\r\n")) :]
        output.append("#" * (level + 2) + line[level :].rstrip("\r\n") + newline)
    return "".join(output)


def replace_name_dashes(
    text: str, source: Path
) -> tuple[str, list[UnreplacedDoubleHyphen]]:
    """Replace ``--`` between capitalized English words with an en dash."""
    protected_spans = [
        match.span()
        for pattern in (MARKDOWN_IMAGE_RE, HTML_IMAGE_TAG_RE)
        for match in pattern.finditer(text)
    ]

    def is_in_image(offset: int) -> bool:
        return any(start <= offset < end for start, end in protected_spans)

    converted_offsets = {
        match.end() - 2
        for match in CAPITALIZED_WORD_DOUBLE_HYPHEN_RE.finditer(text)
        if not is_in_image(match.end() - 2)
    }

    def replace_match(match: re.Match[str]) -> str:
        if is_in_image(match.end() - 2):
            return match.group(0)
        return match.group("left") + "–"

    updated = CAPITALIZED_WORD_DOUBLE_HYPHEN_RE.sub(replace_match, text)
    unreplaced: list[UnreplacedDoubleHyphen] = []
    offset = 0
    for line_number, line_with_ending in enumerate(
        text.splitlines(keepends=True), start=1
    ):
        line = line_with_ending.rstrip("\r\n")
        for match in re.finditer(r"--", line):
            absolute_offset = offset + match.start()
            if absolute_offset in converted_offsets or is_in_image(absolute_offset):
                continue
            unreplaced.append(
                UnreplacedDoubleHyphen(
                    source=source,
                    line=line_number,
                    column=match.start() + 1,
                    text=line,
                )
            )
        offset += len(line_with_ending)
    return updated, unreplaced


def local_image_path(target: str, source: Path) -> Path | None:
    parsed = urlparse(target)
    if parsed.scheme or target.startswith(("//", "#", "/")):
        return None
    return (source.parent / unquote(parsed.path)).resolve()


def raw_image_url(
    target: str, source: Path, repo_root: Path, repository: str, branch: str
) -> str:
    parsed = urlparse(target)
    local_path = local_image_path(target, source)
    if local_path is None:
        return target

    try:
        relative_path = local_path.relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise SystemExit(
            f"リポジトリ外を指す画像パスは変換できません: {source.name}: {target}"
        ) from exc
    if not local_path.is_file():
        raise SystemExit(f"画像ファイルがありません: {source.name}: {target}")

    encoded_path = quote(relative_path, safe="/")
    suffix = ""
    if parsed.query:
        suffix += "?" + parsed.query
    if parsed.fragment:
        suffix += "#" + parsed.fragment
    return f"https://raw.githubusercontent.com/{repository}/{quote(branch, safe='')}/{encoded_path}{suffix}"


def image_alt(target: str, source: Path) -> str | None:
    image_path = local_image_path(target, source)
    if image_path is None:
        return None
    return f"{source.parent.name}_{image_path.stem}"


def load_image_licenses(source: Path) -> dict[str, tuple[LicensedMedia, ...]]:
    metadata_path = source.parent / IMAGE_LICENSES_NAME
    if not metadata_path.is_file():
        return {}

    try:
        document = json.loads(read_utf8(metadata_path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"画像ライセンスJSONが不正です: {metadata_path}: {exc}") from exc

    images = document.get("images") if isinstance(document, dict) else None
    if not isinstance(images, dict):
        raise SystemExit(f"imagesオブジェクトがありません: {metadata_path}")

    result: dict[str, tuple[LicensedMedia, ...]] = {}
    for filename, image_data in images.items():
        if not isinstance(filename, str) or not isinstance(image_data, dict):
            raise SystemExit(f"画像ライセンスの項目が不正です: {metadata_path}")
        image_path = source.parent / filename
        if not image_path.is_file():
            raise SystemExit(f"ライセンス対象の画像がありません: {image_path}")
        media_items = image_data.get("embedded_media")
        if not isinstance(media_items, list) or not media_items:
            raise SystemExit(f"embedded_mediaがありません: {metadata_path}: {filename}")

        parsed_items: list[LicensedMedia] = []
        for item in media_items:
            if not isinstance(item, dict):
                raise SystemExit(f"embedded_mediaの項目が不正です: {metadata_path}: {filename}")
            required = ("title", "author", "source_url", "license")
            if any(not isinstance(item.get(key), str) or not item[key] for key in required):
                raise SystemExit(f"画像ライセンスの必須値がありません: {metadata_path}: {filename}")
            license_url = item.get("license_url")
            if license_url is not None and not isinstance(license_url, str):
                raise SystemExit(f"license_urlが不正です: {metadata_path}: {filename}")
            notice = item.get("notice")
            if notice is not None and (not isinstance(notice, str) or not notice):
                raise SystemExit(f"noticeが不正です: {metadata_path}: {filename}")
            parsed_items.append(
                LicensedMedia(
                    title=item["title"],
                    author=item["author"],
                    source_url=item["source_url"],
                    license_name=item["license"],
                    license_url=license_url,
                    notice=notice,
                )
            )
        result[filename] = tuple(parsed_items)
    return result


def wikipedia_source_before(text: str, offset: int, source: Path) -> str:
    matches = list(WIKIPEDIA_SOURCE_LINE_RE.finditer(text, 0, offset))
    if not matches:
        raise SystemExit(f"Wikipedia画像より前に出典URLがありません: {source}")
    return matches[-1].group("url")


def escape_markdown_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def wikipedia_attribution(
    source_url: str, media_items: tuple[LicensedMedia, ...]
) -> str:
    parts = [
        f"出典: [Wikipedia contributors](<{source_url}>), "
        f"[{WIKIPEDIA_TEXT_LICENSE_NAME}]({WIKIPEDIA_TEXT_LICENSE_URL})。"
        "スクリーンショット・切り抜き。"
    ]
    notices: list[str] = []
    for item in media_items:
        title = escape_markdown_label(item.title)
        author = escape_markdown_label(item.author)
        license_text = escape_markdown_label(item.license_name)
        if item.license_url:
            license_display = f"[{license_text}](<{item.license_url}>)"
        else:
            license_display = license_text
        parts.append(
            f"画像: [{title}](<{item.source_url}>) / {author} / {license_display}。"
        )
        if item.notice:
            notices.append(
                "\n\n<details><summary>"
                f"{title} のライセンス告知全文"
                "</summary>\n\n```text\n"
                f"{item.notice.rstrip()}\n"
                "```\n\n</details>"
            )
    return " ".join(parts) + "".join(notices)


def rewrite_images(
    text: str, source: Path, repo_root: Path, repository: str, branch: str
) -> str:
    image_licenses = load_image_licenses(source)

    def replace_markdown(match: re.Match[str]) -> str:
        original_target = match.group("target")
        target = raw_image_url(
            original_target, source, repo_root, repository, branch
        )
        alt = image_alt(original_target, source) or match.group("alt")
        rendered = (
            match.group("prefix")
            + alt
            + match.group("middle")
            + target
            + match.group("suffix")
        )
        image_path = local_image_path(original_target, source)
        if image_path is not None and image_path.stem.startswith("Wiki"):
            wikipedia_source = wikipedia_source_before(text, match.start(), source)
            media_items = image_licenses.get(image_path.name, ())
            rendered += "\n\n" + wikipedia_attribution(wikipedia_source, media_items)
        return rendered

    def replace_html_tag(match: re.Match[str]) -> str:
        tag = match.group(0)
        src_match = HTML_IMAGE_SRC_RE.search(tag)
        if src_match is None:
            return tag

        original_target = src_match.group("target")
        target = raw_image_url(
            original_target, source, repo_root, repository, branch
        )
        alt = image_alt(original_target, source)
        tag = (
            tag[: src_match.start("target")]
            + target
            + tag[src_match.end("target") :]
        )
        if alt is None:
            return tag

        escaped_alt = html.escape(alt, quote=True)
        alt_match = HTML_ALT_RE.search(tag)
        if alt_match is not None:
            return (
                tag[: alt_match.start("alt")]
                + escaped_alt
                + tag[alt_match.end("alt") :]
            )

        closing = "/>" if tag.endswith("/>") else ">"
        return tag[: -len(closing)] + f' alt="{escaped_alt}"' + closing

    text = MARKDOWN_IMAGE_RE.sub(replace_markdown, text)
    return HTML_IMAGE_TAG_RE.sub(replace_html_tag, text)


def slugify(title: str) -> str:
    slug: list[str] = []
    for char in title.casefold().strip():
        category = unicodedata.category(char)
        if char.isspace():
            slug.append("-")
        elif category[0] not in {"P", "S", "C"} or char in {"-", "_"}:
            slug.append(char)
    return "".join(slug)


def replace_section(document: str, marker: str, generated: str) -> str:
    marker_matches = list(re.finditer(rf"(?m)^{re.escape(marker)}[ \t]*$", document))
    if len(marker_matches) != 1:
        raise SystemExit(f"{marker} はREADME.md内にちょうど1つ必要です。")

    marker_match = marker_matches[0]
    next_section = SECTION_HEADING_RE.search(document, marker_match.end())
    if next_section is None:
        raise SystemExit(f"{marker} より後に次の ## 見出しがありません。")

    before = document[: marker_match.end()].rstrip()
    after = document[next_section.start() :].lstrip("\r\n")
    return f"{before}\n\n{generated.rstrip()}\n\n{after}"


def load_articles(
    directory: Path, repo_root: Path, repository: str, branch: str
) -> tuple[list[Article], list[UnreplacedDoubleHyphen]]:
    articles: list[Article] = []
    unreplaced: list[UnreplacedDoubleHyphen] = []
    for path in directory.glob("*/README.md"):
        text = read_utf8(path)
        text, article_unreplaced = replace_name_dashes(text, path)
        unreplaced.extend(article_unreplaced)
        title = extract_title(path, text)
        body = shift_headings(text, path)
        body = rewrite_images(body, path, repo_root, repository, branch).strip()
        articles.append(Article(title=title, body=body, source=path))

    articles.sort(key=lambda article: (article.title.casefold(), article.source.name.casefold()))
    if not articles:
        raise SystemExit(f"用語Markdownファイルがありません: {directory}")
    return articles, unreplaced


def report_unreplaced_double_hyphens(
    occurrences: list[UnreplacedDoubleHyphen], directory: Path
) -> None:
    if not occurrences:
        return

    print("大文字で始まる英単語の間ではないため、置換しなかった --:")
    for occurrence in occurrences:
        source = occurrence.source.relative_to(directory).as_posix()
        print(
            f"  {source}:{occurrence.line}:{occurrence.column}: "
            f"{occurrence.text.strip()}"
        )


def read_outline_headings(document: str) -> list[OutlineHeading]:
    headings: list[OutlineHeading] = []
    in_fence = False
    position = 0
    for line in document.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence:
            match = re.fullmatch(
                r"(#{1,2})[ \t]+(.+?)(?:[ \t]+#+)?", line.rstrip("\r\n")
            )
            if match:
                headings.append(
                    OutlineHeading(
                        level=len(match.group(1)),
                        title=match.group(2).strip(),
                        position=position,
                    )
                )
        position += len(line)
    return headings


def build_index(document: str, articles: list[Article]) -> str:
    headings = read_outline_headings(document)
    top_level = [heading for heading in headings if heading.level == 1]
    sections = [heading for heading in headings if heading.level == 2]
    if len(top_level) != 1:
        raise SystemExit("README.mdには # 見出しがちょうど1つ必要です。")

    words_matches = list(
        re.finditer(rf"(?m)^{re.escape(WORDS_MARKER)}[ \t]*$", document)
    )
    if len(words_matches) != 1:
        raise SystemExit(f"{WORDS_MARKER} はREADME.md内にちょうど1つ必要です。")
    words_position = words_matches[0].start()
    words_parents = [section for section in sections if section.position < words_position]
    if not words_parents:
        raise SystemExit(f"{WORDS_MARKER} より前に親となる ## 見出しがありません。")
    words_parent = words_parents[-1]

    counts: dict[str, int] = {}
    lines: list[str] = []

    def append_link(indent: str, title: str) -> None:
        base_slug = slugify(title)
        if not base_slug:
            raise SystemExit(f"見出しからリンク先を生成できません: {title}")
        occurrence = counts.get(base_slug, 0)
        counts[base_slug] = occurrence + 1
        slug = base_slug if occurrence == 0 else f"{base_slug}-{occurrence}"
        lines.append(f"{indent}- [{title}](#{slug})")

    append_link("", top_level[0].title)
    for section in sections:
        append_link("  ", section.title)
        if section == words_parent:
            for article in articles:
                append_link("    ", article.title)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help=f"Raw URLで参照するGitブランチ（既定: {DEFAULT_BRANCH}）",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="README.mdを変更せず、更新が必要なら終了コード1を返す",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    directory = Path(__file__).resolve().parent
    readme_path = directory / README_NAME
    repo_root = find_repo_root(directory)
    repository = github_repository(repo_root)
    articles, unreplaced = load_articles(
        directory, repo_root, repository, args.branch
    )
    report_unreplaced_double_hyphens(unreplaced, directory)

    original = read_utf8(readme_path)
    updated = replace_section(original, INDEX_MARKER, build_index(original, articles))
    updated = replace_section(
        updated, WORDS_MARKER, "\n\n".join(article.body for article in articles)
    )
    if not updated.endswith("\n"):
        updated += "\n"

    if args.check:
        if updated != original:
            print(f"README is out of date: {readme_path}")
            return 1
        print(f"README is up to date: {readme_path}")
        return 0

    if updated == original:
        print(f"No changes: {readme_path}")
    else:
        atomic_write_utf8(readme_path, updated)
        print(f"Updated: {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
