import http.client
import json
import os
import re
import warnings

import requests

ACCESS_TOKEN = "786a8df666e658c18f077097c4df3476071ce411"
PAGE = "1"
PAR_PAGE = "100"


def get_qiita_data():
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    api = f"/api/v2/authenticated_user/items?page={PAGE}&per_page={PAR_PAGE}"
    conn = http.client.HTTPSConnection("qiita.com", 443)
    conn.request("GET", api, headers=headers)
    res = conn.getresponse()
    if res.reason != "OK":
        print(res.status, res.reason)
        conn.close()
        raise Exception("Failed to get data from Qiita")
    data = res.read().decode("utf-8")
    conn.close()
    return json.loads(data)


def create_directory(path) -> bool:
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except OSError:
        print("Error: Creating directory. " + path)
        return False


def save_article(path, content):
    with open(os.path.join(path, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)


def download_images(path, img_urls):
    for i, img_url in enumerate(img_urls):
        # print(img_url)
        print(f"Downloading image_{i}.png ({img_url})")
        response = requests.get(img_url)
        if response.status_code != 200:
            warnings.warn(
                f"Failed to download image_{i}.png ({img_url})"
                f" (status code: {response.status_code})"
            )
            continue
        img_data = response.content
        with open(os.path.join(path, f"imgs/image_{i}.png"), "wb") as img_f:
            img_f.write(img_data)


def main():
    dirname = os.path.dirname(__file__)
    json_data = get_qiita_data()
    for item in json_data:
        created_at = item["created_at"]
        title = item["title"]
        date = created_at[:10].replace("-", "")
        path = os.path.join(dirname, date + "_" + title)
        print(path)
        success = create_directory(path)
        if not success:
            continue
        if os.path.exists(os.path.join(path, "README.md")):
            print("Already exists")
        else:
            save_article(path, item["body"])

        # img_urls = re.findall(
        #     r"https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/.*?\.(?:png|jpeg|jpg)",
        #     item["body"],
        # )
        # download_images(path, img_urls)


if __name__ == "__main__":
    main()
