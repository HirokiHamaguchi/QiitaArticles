import datetime
import os
import re

import requests  # type: ignore
from bs4 import BeautifulSoup


def fetch_ipa_by_region(words):
    base_url = "https://dictionary.cambridge.org/dictionary/english/"
    headers = {"User-Agent": "Mozilla/5.0"}

    ipa_dict = {}

    for word in words:
        print(f"Fetching {word}...")
        url = base_url + word
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch {word}: Status code {response.status_code}")
            ipa_dict[word] = {"uk": "", "us": "", "link": url}
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        result = {"uk": "", "us": "", "link": url}
        for region in ["uk", "us"]:
            region_spans = soup.find_all("span", class_=f"{region} dpron-i")
            ipa_found = ""
            for region_span in region_spans:
                ipa_spans = region_span.find_all("span", class_="ipa")
                for ipa_span in ipa_spans:
                    classes = ipa_span.get("class", [])
                    if "dipa" in classes:
                        ipa_text = ipa_span.text.strip()
                        if ipa_text:
                            ipa_found = ipa_text
                            break
                if ipa_found:
                    break
            result[region] = ipa_found
        ipa_dict[word] = result

    return ipa_dict


def generate_table():
    words = [
        "example",
        "test",
        "quasi",
        "pseudo",
    ]
    ipa_results = fetch_ipa_by_region(words)

    # Markdownテーブル出力
    print("|  単語  |   US   |   UK   |  リンク  |")
    print("|:------:|:------:|:------:|:--------:|")
    for word, regions in ipa_results.items():
        us = regions.get("us", "")
        uk = regions.get("uk", "")
        link = regions.get("link", "")
        print(f"| {word} | {us} | {uk} | [link]({link}) |")


def add_pronunciation_to_readme():
    folder = os.path.dirname(os.path.abspath(__file__))
    os.chdir(folder)
    assert os.path.exists("README.md")

    # backup README.md get today's date and time
    today = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_filename = f"backup_README_{today}.md"
    with open("README.md", "r", encoding="utf-8") as original_file:
        with open(backup_filename, "w", encoding="utf-8") as backup_file:
            backup_file.write(original_file.read())

    res = []
    with open("README.md", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            res.append(line.strip())
            if re.match(r"#{2,}\s[a-zA-Z]+", line.strip()):
                word = line.strip().lstrip("#").strip()
                if i + 2 < len(lines) and (
                    lines[i + 2].startswith(word) or lines[i + 2].startswith("<!--")
                ):
                    continue
                ipa_dict = fetch_ipa_by_region([word])
                data = ipa_dict.get(word, {"us": "", "uk": "", "link": ""})
                if data["us"] == "" or data["uk"] == "":
                    res.append("")
                    res.append("<!-- No pronunciation found -->")
                else:
                    res.append("")
                    res.append(
                        f"{word} | UK {data['uk']} | US {data['us']} | [link]({data['link']})"
                    )

    print(res)
    with open("README.md", "w", encoding="utf-8") as file:
        file.write("\n".join(res) + "\n\n")


if __name__ == "__main__":
    # generate_table()
    add_pronunciation_to_readme()
