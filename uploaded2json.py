import json
import re

import pyperclip  # type: ignore[import]

# 入力：Markdown形式の画像リンク文字列
input_text = """
![test_uplatex_dvipdfmx.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/6479665b-9524-48f1-a947-4eb9ad1cacfd.png)
![test_endash.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/5d29a700-800e-4cd4-8495-725943d2f451.png)
![test_uplatex_dvipdfmx_orcidlinki.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/ddca3f0d-7e71-4d33-8591-8535bc2e3bc4.png)
![test_pdflatex.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/d6bc3e5e-36fe-4119-8348-99ae6121ffb2.png)
![test_uplatex.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/0232b019-fe70-4a3e-b6a3-460845c5119f.png)
![test_lualatex.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/3fd43d70-4b06-4588-ae5d-491f67efbe05.png)
![orcidlink_package.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c2cad3b6-018a-457d-9906-bb768d13e3b0.png)
![endash_twitter.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/0fea0e12-8686-486b-b539-2533fcf978fd.png)
![bad_characters.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/08f25c7d-f59e-432e-8865-6f6a2fa5bc34.png)
![no_dvipdfmx_no_warning.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/6418a486-377a-4920-a05d-a060e7fb9920.png)
![arXiv_bbl_bib_error.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/7ff04f7a-f4be-4a04-b6e6-3785e5c608aa.png)
![x2013.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/debfc59e-82b9-4421-88c3-74ff8b1f3fec.png)
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
