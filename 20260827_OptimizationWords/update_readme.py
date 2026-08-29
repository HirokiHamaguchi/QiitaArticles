#!/usr/bin/env python3
"""Build the INDEX and WORDS sections of README.md from sibling Markdown files."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlparse

INDEX_MARKER = "<!-- INDEX -->"
WORDS_MARKER = "<!-- WORDS -->"
README_NAME = "README.md"
DEFAULT_BRANCH = "main"

ATX_HEADING_RE = re.compile(r"^(#{1,6})([ \t]+)(.*?)([ \t]+#+)?$", re.MULTILINE)
MARKDOWN_IMAGE_RE = re.compile(r"(!\[[^\]\r\n]*\]\()([^\s()]+)(\))")
HTML_IMAGE_RE = re.compile(
    r"(<img\b[^>]*?\bsrc\s*=\s*['\"])([^'\"]+)(['\"])", re.IGNORECASE
)
SECTION_HEADING_RE = re.compile(r"^##(?:[ \t]+|$)", re.MULTILINE)


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


def raw_image_url(
    target: str, source: Path, repo_root: Path, repository: str, branch: str
) -> str:
    parsed = urlparse(target)
    if parsed.scheme or target.startswith(("//", "#", "/")):
        return target

    local_path = (source.parent / parsed.path).resolve()
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


def rewrite_images(
    text: str, source: Path, repo_root: Path, repository: str, branch: str
) -> str:
    def replace(match: re.Match[str]) -> str:
        target = raw_image_url(
            match.group(2), source, repo_root, repository, branch
        )
        return match.group(1) + target + match.group(3)

    text = MARKDOWN_IMAGE_RE.sub(replace, text)
    return HTML_IMAGE_RE.sub(replace, text)


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
) -> list[Article]:
    articles: list[Article] = []
    for path in directory.glob("*.md"):
        if path.name.casefold() == README_NAME.casefold():
            continue
        if path.name.casefold() == "Qiita.md".casefold():
            continue
        text = read_utf8(path)
        title = extract_title(path, text)
        body = shift_headings(text, path)
        body = rewrite_images(body, path, repo_root, repository, branch).strip()
        articles.append(Article(title=title, body=body, source=path))

    articles.sort(key=lambda article: (article.title.casefold(), article.source.name.casefold()))
    if not articles:
        raise SystemExit(f"用語Markdownファイルがありません: {directory}")
    return articles


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
    articles = load_articles(directory, repo_root, repository, args.branch)

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
