import json
import re

import pyperclip  # type: ignore[import]

# 入力：Markdown形式の画像リンク文字列
input_text = """
![IMG_5009.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/9bd73f93-d2d8-471e-a1e0-9be60fbb9087.jpeg)
![IMG_5008.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/b45eca5f-8b80-40b9-86eb-af198fb2f1dd.jpeg)
![crosscut.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/5f0c3f9e-8241-4d88-bdb6-1263e97cb24f.png)
![thm42_proof.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/4ef19299-28b6-48b7-b2aa-6021a3204849.png)
![thm42.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/fdb68e7d-51ca-4fa5-a1c7-a1700668c558.png)
"""

# 正規表現でaltとURLを抽出
pattern = r"!\[(.*?)\]\((.*?)\)"
matches = re.findall(pattern, input_text)


# altから拡張子を除いた名前に変換
def clean_alt(alt_text):
    return re.sub(r"\.\w+$", "", alt_text)


# JSON形式のデータを作成
image_data = [{"src": url, "alt": clean_alt(alt)} for alt, url in matches]

# JSON出力
json_output = json.dumps(image_data, indent=4)


pyperclip.copy(json_output)
print("Conversion completed successfully. The output is copied to the clipboard.")
