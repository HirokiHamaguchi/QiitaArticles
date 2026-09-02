#!/usr/bin/env python3
"""Create one OptimizationWords entry with images copied from the clipboard."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WINDOWS_FORBIDDEN_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
URL_REFERENCE_RE = re.compile(
    r"^(?P<url>https?://\S+)(?:[ \t]+(?P<note>\(.+\)))?$"
)
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


@dataclass(frozen=True)
class ClipboardImage:
    filename: str
    image: Any


def default_directory_name(title: str) -> str:
    """Follow the compact directory naming style used by existing entries."""
    return re.sub(r"[\s\-–—]+", "", title)


def validate_windows_name(name: str, kind: str) -> str:
    if not name or name in {".", ".."}:
        raise ValueError(f"{kind}名が空です。")
    if WINDOWS_FORBIDDEN_RE.search(name) or name.endswith((" ", ".")):
        raise ValueError(f"Windowsで使用できない{kind}名です: {name}")
    if name.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES:
        raise ValueError(f"Windowsの予約名は使用できません: {name}")
    return name


def normalize_png_name(name: str) -> str:
    filename = re.sub(r"\s*([\-–—])\s*", r"\1", name.strip())
    filename = re.sub(r"\s+", "-", filename)
    if not filename.lower().endswith(".png"):
        filename += ".png"
    return validate_windows_name(filename, "画像ファイル")


def read_clipboard_image() -> Any:
    try:
        from PIL import Image, ImageGrab
    except ImportError as exc:
        raise RuntimeError(
            "クリップボード画像の取得にはPillowが必要です。"
            " `uv add pillow` などでインストールしてください。"
        ) from exc

    clipboard = ImageGrab.grabclipboard()
    if isinstance(clipboard, Image.Image):
        return clipboard.copy()

    # Explorerで画像ファイルそのものをコピーした場合にも対応する。
    if isinstance(clipboard, list) and len(clipboard) == 1:
        source = Path(clipboard[0])
        try:
            with Image.open(source) as image:
                return image.copy()
        except (OSError, ValueError) as exc:
            raise RuntimeError(f"コピーされたファイルを画像として読めません: {source}") from exc

    raise RuntimeError(
        "クリップボードに画像がありません。画像をコピーしてから再試行してください。"
    )


def prompt_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("空にはできません。")


def normalize_url_reference(value: str) -> str:
    match = URL_REFERENCE_RE.fullmatch(value.strip())
    if match is None:
        raise ValueError("URL または URL (一言解説) の形式で入力してください。")

    url = match.group("url")
    note = match.group("note")
    return url if note is None else f"{url}\n\n{note}"


def prompt_url_reference() -> str:
    while True:
        value = prompt_nonempty("URL または URL (一言解説): ")
        try:
            return normalize_url_reference(value)
        except ValueError as exc:
            print(exc)


def prompt_references() -> tuple[list[str], list[ClipboardImage]]:
    references: list[str] = []
    images: list[ClipboardImage] = []
    filenames: set[str] = set()

    print("\n文献欄を作成します。追加する種類を選んでください。")
    while True:
        command = input(
            "[t] URL/一言解説  [i] クリップボード画像  [d] 完了: "
        ).strip().lower()
        if command in {"d", "done"}:
            return references, images
        if command in {"t", "text"}:
            references.append(prompt_url_reference())
            continue
        if command not in {"i", "image"}:
            print("t、i、d のいずれかを入力してください。")
            continue

        try:
            filename = normalize_png_name(
                prompt_nonempty(
                    "論文名/Wiki + 任意の特徴（空白は-へ変換、.pngは省略可）: "
                )
            )
        except ValueError as exc:
            print(exc)
            continue
        if filename.casefold() in filenames:
            print(f"同じ画像名が既にあります: {filename}")
            continue

        input("画像をWindowsのクリップボードへコピーし、Enterを押してください: ")
        try:
            image = read_clipboard_image()
        except RuntimeError as exc:
            print(exc)
            continue
        filenames.add(filename.casefold())
        images.append(ClipboardImage(filename=filename, image=image))
        references.append(f"![{Path(filename).stem}]({filename})")
        print(f"画像を取り込みました: {filename}")


def prompt_description() -> str:
    print("\n解説を入力してください。単独の行に . を入力すると終了します。")
    lines: list[str] = []
    while True:
        line = input()
        if line == ".":
            return "\n".join(lines).strip()
        lines.append(line)


def is_url_reference(reference: str) -> bool:
    return URL_REFERENCE_RE.fullmatch(reference.splitlines()[0]) is not None


def format_references(references: list[str]) -> str:
    formatted: list[str] = []
    for index, reference in enumerate(references):
        has_note = "\n\n" in reference
        next_is_url = index + 1 < len(references) and is_url_reference(
            references[index + 1]
        )
        if has_note and next_is_url:
            reference += "\n<br>"
        formatted.append(reference)
    return "\n\n".join(formatted)


def build_readme(title: str, references: list[str], description: str) -> str:
    reference_text = format_references(references)
    return f"# {title}\n\n文献:\n\n{reference_text}\n\n解説:\n\n{description}\n"


def write_entry(
    target: Path,
    title: str,
    references: list[str],
    description: str,
    images: list[ClipboardImage],
) -> None:
    # 対話を完了してから作成するため、途中で中断しても半端な用語は残らない。
    target.mkdir(parents=False, exist_ok=False)
    try:
        for clipboard_image in images:
            clipboard_image.image.save(target / clipboard_image.filename, format="PNG")
        (target / "README.md").write_text(
            build_readme(title, references, description),
            encoding="utf-8",
            newline="\n",
        )
    except (Exception, KeyboardInterrupt):
        # 新規作成した空間だけが対象なので、安全にロールバックできる。
        for path in target.iterdir():
            path.unlink()
        target.rmdir()
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", nargs="?", help="用語の見出し（例: Maximum Theorem）")
    parser.add_argument(
        "--directory",
        help="作成するディレクトリ名（省略時は見出しから空白とハイフンを除去）",
    )
    parser.add_argument(
        "--open-explorer",
        action="store_true",
        help="作成後に用語ディレクトリをExplorerで開く",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        title = args.title.strip() if args.title else prompt_nonempty("用語の見出し: ")
    except (EOFError, KeyboardInterrupt):
        print("\n中断しました。ファイルは作成していません。")
        return 130
    directory_name = args.directory or default_directory_name(title)
    try:
        directory_name = validate_windows_name(directory_name, "ディレクトリ")
    except ValueError as exc:
        raise SystemExit(exc) from exc

    root = Path(__file__).resolve().parent
    target = root / directory_name
    if target.exists():
        raise SystemExit(f"既に存在するため上書きしません: {target}")

    print(f"作成先: {target}")
    try:
        references, images = prompt_references()
        description = prompt_description()
        write_entry(target, title, references, description, images)
    except (EOFError, KeyboardInterrupt):
        print("\n中断しました。ファイルは作成していません。")
        return 130

    print(f"作成しました: {target / 'README.md'}")
    print("全体READMEを更新します。")
    try:
        update_result = subprocess.run(
            [sys.executable, str(root / "update_readme.py")],
            check=False,
        )
        exit_code = update_result.returncode
    except KeyboardInterrupt:
        print("\n全体READMEの更新を中断しました。")
        exit_code = 130

    if exit_code == 0:
        print("全体READMEを更新しました。")
    else:
        print(f"全体READMEを更新できませんでした（終了コード: {exit_code}）。")

    if args.open_explorer:
        try:
            os.startfile(target)
        except OSError as exc:
            print(f"Explorerを開けませんでした: {exc}")
            if exit_code == 0:
                exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
