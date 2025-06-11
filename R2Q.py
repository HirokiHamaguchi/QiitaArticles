# Readme 2 Qiita

import json
import os
import re

import pyperclip  # type: ignore[import]


def get_target_directory(date_str, base_dir):
    matching_dirs = [
        d
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and d.startswith(date_str)
    ]
    if len(matching_dirs) != 1:
        raise ValueError(
            "The directory matching the date string is not unique or does not exist."
        )
    return os.path.join(base_dir, matching_dirs[0])


def get_latest_modified_directory(base_dir):
    candidates = [
        d
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("20")
    ]
    if not candidates:
        raise ValueError("No directories starting with '20' found.")

    def get_dir_latest_file_mtime(dir_path):
        mtime = os.path.getmtime(dir_path)
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                mtime = max(mtime, os.path.getmtime(file_path))
        return mtime

    latest = max(
        candidates, key=lambda d: get_dir_latest_file_mtime(os.path.join(base_dir, d))
    )
    return os.path.join(base_dir, latest)


def read_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as f:
        return f.read()


def load_json(file_path):
    with open(file_path, "r", encoding="UTF-8") as f:
        return json.load(f)


def process_lines(lines, links):
    res = ["<!-- markdownlint-disable MD041 -->", ""]
    mathBlockOpen = False
    nextIgnore = False
    for line in lines:
        if line.strip() == "$$":
            res.append("\n```math" if not mathBlockOpen else "```\n")
            mathBlockOpen = not mathBlockOpen
        elif line.strip() == "> $$":
            res.append(">" if not mathBlockOpen else "> ```")
            res.append("> ```math" if not mathBlockOpen else ">")
            mathBlockOpen = not mathBlockOpen
        elif line.startswith("!["):
            if nextIgnore:
                res.append(line)
                nextIgnore = False
                continue
            alt = line[line.find("[") + 1 : line.find("]")]
            url = line[line.find("(") + 1 : line.find(")")]
            if url.startswith("http"):
                src = url
                width = "100%"
            elif any(alt == link["alt"] for link in links):
                link = next(link for link in links if alt == link["alt"])
                src = link["src"]
                width = "100%"
            else:
                raise ValueError(f"Image not found: {alt}")
            res.append(f'<img width={width} src="{src}" alt="{alt}">')
        elif line.strip() == "<!-- ignore -->":
            nextIgnore = True
        else:
            res.append(line)
    return "\n".join(res) + "\n"


def replace_patterns(res):
    res = (
        res.replace("\n\n\n", "\n\n")
        .replace("\n\n\n", "\n\n")
        .replace("\n\n\n", "\n\n")
    )
    res = res.replace("\\coloneqq", "\\mathrel{\\vcenter{:}}=").replace(
        "{dcases}", "{cases}"
    )
    for line in res.splitlines():
        if re.search(r"\\{[a-zA-Z0-9]", line):
            print(r"Warning: Add space after \{[a-zA-Z0-9] in line: " + line)
    res = res.replace("\\{", "\\lbrace").replace("\\}", "\\rbrace")
    if res.count("\\,"):
        print("Warning: \\, found. Use \\ instead.")
    return res


def replace_vertical_bars(res):
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
    return res2


def main():
    base_dir = os.path.dirname(__file__)
    target_dir = get_latest_modified_directory(base_dir)
    target_dir_core = target_dir.split(os.sep)[-1]
    is_data_correct = (
        input(f"Do you want to convert the file {target_dir_core}? (y/n): ")
        .strip()
        .lower()
    )
    if is_data_correct not in ("y", ""):
        date_str = input("Enter the date string (e.g., 20000101): ")
        target_dir = get_target_directory(date_str, base_dir)
        print(f"Target directory: {target_dir}")

    assert os.path.exists(os.path.join(target_dir, "README.md"))
    assert os.path.exists(os.path.join(target_dir, "images.json"))

    content = read_file(os.path.join(target_dir, "README.md"))
    links = load_json(os.path.join(target_dir, "images.json"))

    lines = content.splitlines()
    assert lines[0].startswith("# ")
    assert lines[1].strip() == ""
    lines = lines[2:]

    res = process_lines(lines, links)
    res = replace_patterns(res)
    res = replace_vertical_bars(res)

    with open(os.path.join(target_dir, "Qiita.md"), "w", encoding="UTF-8") as f:
        f.write(res)

    pyperclip.copy(res)
    print("Conversion completed successfully. The output is copied to the clipboard.")


if __name__ == "__main__":
    main()
