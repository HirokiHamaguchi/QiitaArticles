import json
import os
from readme2qiita import get_target_directory, read_file


def main():
    date_str = input("Enter the date string (e.g., 20000101): ")
    base_dir = os.path.dirname(__file__)
    target_dir = get_target_directory(date_str, base_dir)
    print(f"Target directory: {target_dir}")

    assert os.path.exists(os.path.join(target_dir, "README.md"))

    content = read_file(os.path.join(target_dir, "README.md"))

    res = ""
    json_data = []
    for line in content.split("\n"):
        if "<img" in line:
            alt = line.split('alt="')[1].split('"')[0]
            src = line.split('src="')[1].split('"')[0]
            print(f"alt: {alt}, src: {src}")
            res += f"![{alt}](imgs/{alt}.png)\n"
            try:
                width = line.split('width="')[1].split('"')[0]
                json_data.append({"alt": alt, "src": src, "width": width})
            except IndexError:
                json_data.append({"alt": alt, "src": src})
        else:
            res += line + "\n"

    assert res[-1] == "\n"
    res = res[:-1]

    with open(os.path.join(target_dir, "README2.md"), "w", encoding="UTF-8") as f:
        f.write(res)

    with open(os.path.join(target_dir, "images.json"), "w", encoding="UTF-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
