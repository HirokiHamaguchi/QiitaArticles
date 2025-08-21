from pathlib import Path
import re
import requests

# todo: twitterのリンクは除外?
# todo: doiのリンクは除外?
# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get("https://twitter.com/username/status/1234567890")



def check_validity(url, readme):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    response = None
    try:
        response = requests.head(url, headers=headers, allow_redirects=True)
        if response.status_code < 400:
            return True
        if "qiita-image" in url and response.status_code == 403:
            print(f"Warning: Access forbidden for {url}. Skipping.")
            return True
        if response.status_code == 429:
            print(f"Warning: Rate limit exceeded for {url}. Skipping.")
            return True
    except requests.RequestException:
        pass

    assert response is not None
    print(f"Invalid link: {url} in {readme} (Status Code: {response.status_code}, Reason: {response.reason})")
    return False

def extract_urls(text):
    urls = []
    i = 0
    while i < len(text):
        if text[i:i+7] == 'http://' or text[i:i+8] == 'https://':
            start = i
            i += 7 if text[i:i+7] == 'http://' else 8
            balance = 0
            while i < len(text):
                char = text[i]
                # URLの終了条件
                if char in " \t\n\"'<>[]{}":
                    if balance == 0:
                        break
                elif char == '(':
                    balance += 1
                elif char == ')':
                    balance -= 1
                    if balance < 0:
                        break
                i += 1
            url = text[start:i]
            # 末尾の記号はURLの一部でなければ除去
            while url and url[-1] in '.,;!?"\'<>[]{}':
                url = url[:-1]
            urls.append(url)
        else:
            i += 1
    return urls

def main():
    root_dir = Path(__file__).resolve().parent.parent
    for subdir in root_dir.iterdir():
        if subdir.is_file() or not (subdir / 'readme.md').is_file():
            continue
        print("-" * 20+ f" {subdir.name} " + "-" * 20)
        if subdir.name=="20220330_UmetaniHeuristic":
            print("skip")
            continue
        readme = subdir / 'readme.md'
        content = readme.read_text(encoding='utf-8')
        links = extract_urls(content)
        for link in links:
            check_validity(link, readme)

if __name__ == '__main__':
    # main()
    check_validity("https://doi.org/10.1103/PhysRevLett.118.090501","")

