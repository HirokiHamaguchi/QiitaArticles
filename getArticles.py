import re
import os
import http.client
import json
import time
import requests  # Add this import


def main(dirname: str):
    USER_ID = "hari64"
    ACCESS_TOKEN = "786a8df666e658c18f077097c4df3476071ce411"

    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
    }

    # Assume that the number of items is less than 100
    PAGE = "1"
    PAR_PAGE = "100"

    conn = http.client.HTTPSConnection("qiita.com", 443)
    conn.request(
        "GET",
        "/api/v2/authenticated_user/items?page=" + PAGE + "&per_page=" + PAR_PAGE,
        headers=headers,
    )
    res = conn.getresponse()
    if res.reason != "OK":
        print(res.status, res.reason)
        conn.close()
        raise Exception("Failed to get data from Qiita")

    data = res.read().decode("utf-8")
    jsonStr = json.loads(data)
    for num in range(len(jsonStr)):
        created_at = jsonStr[num]["created_at"]
        title = jsonStr[num]["title"]
        date = created_at[:10].replace("-", "")

        path = os.path.join(dirname, date + "_" + title + ".md")
        print(path)

        try:
            # create folder if not exists
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Creating directory. " + path)
            continue

        with open(os.path.join(path, "Qiita.md"), "w", encoding="utf-8") as f:
            f.write(jsonStr[num]["body"])

        img_urls = re.findall(
            r"https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/.*?\.png",
            jsonStr[num]["body"],
        )

        for i, img_url in enumerate(img_urls):
            print(img_url)
            response = requests.get(img_url)  # Use requests to get the image
            if response.status_code != 200:
                print(response.status_code, response.reason)
                continue

            img_data = response.content
            with open(os.path.join(path, f"image_{i}.png"), "wb") as img_f:
                img_f.write(img_data)

        break

    conn.close()


if __name__ == "__main__":
    main(os.path.dirname(__file__))
