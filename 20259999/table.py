# 米国訛りと英国訛りと日本訛りが

import requests
from bs4 import BeautifulSoup


def fetch_ipa_by_region(words):
    base_url = "https://dictionary.cambridge.org/dictionary/english/"
    headers = {"User-Agent": "Mozilla/5.0"}

    ipa_dict = {}

    for word in words:
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


# 使用例
words = ["example", "test", "computer"]
ipa_results = fetch_ipa_by_region(words)

# Markdownテーブル出力
print("|  単語  |   US   |   UK   |  リンク  |")
print("|:------:|:------:|:------:|:--------:|")
for word, regions in ipa_results.items():
    us = regions.get("us", "")
    uk = regions.get("uk", "")
    link = regions.get("link", "")
    print(f"| {word} | {us} | {uk} | [link]({link}) |")
