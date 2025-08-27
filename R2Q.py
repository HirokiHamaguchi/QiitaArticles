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
        elif "![" in line:
            if nextIgnore:
                res.append(line)
                nextIgnore = False
                continue
            cnt = line.count("![")
            while cnt > 0:
                cnt -= 1
                alt = line[line.find("[") + 1 : line.find("]")]
                url = line[line.find("(") + 1 : line.find(")")]
                if url.startswith("http"):
                    src = url
                elif any(alt == link["alt"] for link in links):
                    link = next(link for link in links if alt == link["alt"])
                    src = link["src"]
                else:
                    raise ValueError(f"Image not found: {alt}")
                start_idx = line.find("![")
                end_idx = line.find(")") + 1
                line = (
                    line[:start_idx]
                    + f'<img width=100% src="{src}" alt="{alt}">'
                    + line[end_idx:]
                )
            res.append(line)
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


def convert_readme_to_qiita(target_dir, copy_to_clipboard=False):
    content = read_file(os.path.join(target_dir, "README.md"))

    images_json_path = os.path.join(target_dir, "images.json")
    links = load_json(images_json_path) if os.path.exists(images_json_path) else []

    lines = content.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("README.md doesn't start with '# '")

    if len(lines) < 2 or lines[1].strip() != "":
        raise ValueError("README.md format is unexpected")

    lines = lines[2:]

    res = process_lines(lines, links)
    res = replace_patterns(res)
    res = replace_vertical_bars(res)

    qiita_path = os.path.join(target_dir, "Qiita.md")

    if os.path.exists(qiita_path):
        os.chmod(qiita_path, 0o666)

    with open(qiita_path, "w", encoding="UTF-8") as f:
        f.write(res)
    os.chmod(qiita_path, 0o444)

    if copy_to_clipboard:
        pyperclip.copy(res)

    return res


def convert_directory_to_qiita(target_dir):
    if not os.path.exists(os.path.join(target_dir, "README.md")):
        print(f"Skipping {target_dir}: README.md not found")
        return False

    try:
        convert_readme_to_qiita(target_dir)
        print(f"Successfully converted {target_dir}")
        return True
    except Exception as e:
        print(f"Error converting {target_dir}: {e}")
        return False


def run_all():
    base_dir = os.path.dirname(__file__)

    directories = [
        d
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("20")
    ]

    if not directories:
        print("No directories starting with '20' found.")
        return

    directories.sort()
    print(f"Found {len(directories)} directories starting with '20'")

    success_count = 0
    for directory in directories:
        target_dir = os.path.join(base_dir, directory)
        if convert_directory_to_qiita(target_dir):
            success_count += 1

    print(
        f"\nConversion completed. {success_count}/{len(directories)} directories successfully converted."
    )


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

    if not os.path.exists(os.path.join(target_dir, "README.md")):
        raise FileNotFoundError("README.md not found")

    convert_readme_to_qiita(target_dir, copy_to_clipboard=True)
    print("Conversion completed successfully. The output is copied to the clipboard.")


if __name__ == "__main__":
    main()
    # run_all()
