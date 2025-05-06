import os
import json


def extract_code_blocks(ipynb_path, output_path=None):
    """
    Jupyter Notebook (.ipynb) ファイルから Python コードセルを抽出し、
    Markdown 形式のコードブロックで出力する。

    Parameters:
    - ipynb_path: 入力する .ipynb ファイルのパス
    - output_path: 結果を保存するファイルパス（省略時は標準出力）
    """
    with open(ipynb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    with open(
        "secret/monotone_0.1.2/monotone/src/monotoneC.c", "r", encoding="utf-8"
    ) as f:
        code = f.read()

    code_blocks = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            code_block = f"```python\n{source}\n```\n\n"
            code_blocks.append(code_block)

    assert len(code_blocks) == 5
    result = (
        "# PAVA\n\n"
        "monotone packageには以下のC言語のコードが包含されています([GPL-3](https://cran.r-project.org/web/licenses/GPL-3)ライセンスですのでご注意下さい)。\n\n"
        + "<details><summary>既存研究のコード</summary>\n\n"
        + f"```c{code}```\n\n"
        + "</details>\n\n"
        + "既存研究によるコードをPythonに翻訳すると以下のようになります(こちらも翻訳の元となったコードの都合上、[GPL-3](https://cran.r-project.org/web/licenses/GPL-3)ライセンスです)。\n\n"
        + "<details><summary>Pythonに翻訳したコード</summary>\n\n"
        + code_blocks[0]
        + "</details>\n\n"
        + "さて、このコードは、クラス等を使って可読性を高められます。そのようにしたのが以下のコードです。"
        + "なお、これ以降に登場するコードは全てPublic Domainとします。\n\n"
        + code_blocks[1]
        + "このコードの正当性はランダムテストにより検証済みです。\n\n"
        + "<details><summary>テスト・ビジュアライザ</summary>\n\n"
        + code_blocks[2]
        + code_blocks[3]
        + code_blocks[4]
        + "</details>\n"
    )

    if output_path:
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(result)
    else:
        print(result)


assert False, "Deprecated. Do not run."

# os.chdir(os.path.dirname(__file__))
# extract_code_blocks("PAVA.ipynb", "PAVA.md")
