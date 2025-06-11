import json
import re

import pyperclip  # type: ignore[import]

# 入力：Markdown形式の画像リンク文字列
input_text = """
![p3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c45d97ca-66e2-4129-8fdd-76d2a88eb925.png)
![scipy_IR.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/06349ee7-d06a-44fe-891f-6607fafb8632.png)
![p1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/6ac04acd-65a6-41a1-b91f-b06efae9429f.png)
![p2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/0a8d8f3f-a85f-4d72-9b22-0b04ddb86b48.png)
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
