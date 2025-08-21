<!-- markdownlint-disable MD041 -->

Matplotlibを用いて作成された図と同じ配色を

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/7a05e6cb-6e33-3e82-3d02-9077972f7574.png" alt="AmatPlt.png">

TikZで再現する方法などについて、本稿では述べます。

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/aa72393e-126f-811f-9150-3be6e5504711.png" alt="AmatTikZ.png">

## 目次

- [LaTeXでMatplotlibやMATLABの配色を再現する方法](#latexでmatplotlibやmatlabの配色を再現する方法)
  - [目次](#目次)
  - [LaTeXでの定義方法](#latexでの定義方法)
  - [色の取得方法](#色の取得方法)
    - [tab10](#tab10)
    - [viridis](#viridis)
    - [jet](#jet)
  - [サンプル](#サンプル)
  - [色を使う時の注意点](#色を使う時の注意点)
  - [Licenseの問題について](#licenseの問題について)

## LaTeXでの定義方法

本稿の主眼がLaTeX(特にTikZ)での利用に置かれている為、最初にLaTeXでの色の定義方法を紹介します。

xcolorパッケージを用います。これは「数学の景色」さんによって詳しくまとめられています。

https://mathlandscape.com/latex-color/

具体的には、

```latex
\definecolor{myRed}{HTML}{FF0000}
```

などと定義します。

CTANにて公開されているxcolorの[公式ドキュメント](https://ctan.org/pkg/xcolor?lang=en)における`4 Colors by Name`節には、既に様々な色が定義されていることが記載されています。
もし、デフォルトの色パレットで目的が十分達成されるという場合には、それらを使うことをお勧めします。

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/ff61533f-d25e-67de-f051-911699458cd6.png" alt="xcolor.png">

しかし、本記事では更に追加して、MatplotlibやMATLABの色パレットを定義する方法を紹介します。

## 色の取得方法

関連する公式ドキュメントは以下の通りです。

https://matplotlib.org/stable/users/explain/colors/colormaps.html

Matplotlibの実装はGitHubにて公開されています。

https://github.com/matplotlib/matplotlib

### tab10

tab10とは下図右側のような配色です。([引用元](https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle))

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/06502a65-771d-6796-8a27-15ab394a1173.png" alt="dflt_style_changes-1.2x.png">

pltのデフォルトなので、見たことがある方も多いかと思います。通常の原色などと比べてより視認性が高いことが特徴です。

これらは上の画像の他にも、[実装](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_cm.py#L1281)にも直接カラーコードが記載されています。

tab10のカラーコードは以下の通りです。

```latex
\definecolor{tabA}{HTML}{1f77b4}
\definecolor{tabB}{HTML}{ff7f0e}
\definecolor{tabC}{HTML}{2ca02c}
\definecolor{tabD}{HTML}{d62728}
\definecolor{tabE}{HTML}{9467bd}
\definecolor{tabF}{HTML}{8c564b}
\definecolor{tabG}{HTML}{e377c2}
\definecolor{tabH}{HTML}{7f7f7f}
\definecolor{tabI}{HTML}{bcbd22}
\definecolor{tabJ}{HTML}{17becf}
```

しかし、個人的には、以下に示すMATLABのデフォルト配色の方が好みで、これらをよく用いています。

https://www.mathworks.com/help/matlab/creating_plots/specify-plot-colors.html

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/2940ee39-9ad2-6322-bf35-d70965597ea7.png" alt="matlab.png">

```latex
\definecolor{matlabBlue}{HTML}{0072BD}
\definecolor{matlabRed}{HTML}{D95319}
\definecolor{matlabYellow}{HTML}{EDB120}
\definecolor{matlabPurple}{HTML}{7E2F8E}
\definecolor{matlabGreen}{HTML}{77AC30}
\definecolor{matlabCyan}{HTML}{4DBEEE}
\definecolor{matlabMaroon}{HTML}{A2142F}
```

色名は自由に定義できるので、省略形でも問題ありません。私はtab10の先頭5色の順にMATLABのデフォルト配色を定義した、以下のコードを常用しています。かなり便利です。

```latex
\definecolor{cA}{HTML}{0072BD}
\definecolor{cB}{HTML}{EDB120}
\definecolor{cC}{HTML}{77AC30}
\definecolor{cD}{HTML}{D95319}
\definecolor{cE}{HTML}{7E2F8E}
```

### viridis

こちらもpltのデフォルト配色です。`plt.imshow`などで使われています。

[実装](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_cm_listed.py#L774)を覗くと256行にわたってカラーコードを直接記載するという戦略がとられていることが分かります。

その一部を使いたい時は、例えば以下のようなコードが有効かも知れません。

<details><summary>Python Code</summary>

```python
import matplotlib
import numpy as np
from typing import Tuple

def floatsToHTML(floats: Tuple[float, float, float]) -> str:
    return "".join(list(map(lambda x: f"{int(x * 255):02x}", floats)))

def floatsToRGB(floats: Tuple[float, float, float]) -> str:
    return ",".join(list(map(lambda x: str(int(x * 255)), floats)))

def floatsToLaTeX(color: Tuple[float, float, float], idx: int, method: str) -> str:
    if method == "RGB":
        return "\\definecolor{c" + str(idx) + "}{RGB}{" + floatsToRGB(color) + "}"
    elif method == "HTML":
        return "\\definecolor{c" + str(idx) + "}{HTML}{" + floatsToHTML(color) + "}"
    else:
        raise ValueError("Invalid method")

def main():
    # 好みのカラーマップ
    cmap = matplotlib.colormaps.get_cmap("viridis")
    # 色を取得したい任意の値
    values = [+1, +1 / np.sqrt(2), +1 / 2, -1 / 2, -1 / np.sqrt(2)]
    # 値の範囲
    vMax, vMin = +1, -1

    for idx, value in enumerate(values):
        color = cmap((value - vMin) / (vMax - vMin))
        assert color[-1] == 1  # alpha channel
        print(floatsToLaTeX(color[:3], idx, "RGB"))

if __name__ == "__main__":
    main()
```

</details>

実行すると、以下のような出力が得られます。

```latex
\definecolor{c0}{RGB}{253,231,36}
\definecolor{c1}{RGB}{157,217,58}
\definecolor{c2}{RGB}{94,201,97}
\definecolor{c3}{RGB}{58,82,139}
\definecolor{c4}{RGB}{69,50,127}
```

なお、冒頭の画像は以下のLaTeXコードで作成されています。私の論文で使用した図です。

https://github.com/quantum-programming/stabilizer_extent/blob/master/doc/summary/imgs/Amat.tex

### jet

`jet`も私はよく使うので、ついでに定義方法を述べておきます。

pltの`jet`は`LinearSegmentedColormap`で[実装](https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/cm.py#L40)されています。

https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html

その為、比較的短いコードで定義することができます。ビジュアライザなどをRustやJavaScripts等の他言語で実装する際にも参考になるかと思います。
以下に本質的に等価なコードを示します。

<details><summary>Python Code</summary>

```python
import numpy as np
import matplotlib
from typing import Tuple

# simply implement LinearSegmentedColormap
# https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LinearSegmentedColormap.html
def getJet(val: float) -> Tuple[float, float, float]:
    # https://github.com/matplotlib/matplotlib/blob/main/lib/matplotlib/_cm.py#L243
    _jet_data = {
        "red": (
            (0.00, 0, 0),
            (0.35, 0, 0),
            (0.66, 1, 1),
            (0.89, 1, 1),
            (1.00, 0.5, 0.5),
        ),
        "green": (
            (0.000, 0, 0),
            (0.125, 0, 0),
            (0.375, 1, 1),
            (0.640, 1, 1),
            (0.910, 0, 0),
            (1.000, 0, 0),
        ),
        "blue": (
            (0.00, 0.5, 0.5),
            (0.11, 1, 1),
            (0.34, 1, 1),
            (0.65, 0, 0),
            (1.00, 0, 0),
        ),
    }

    floats = []
    for data in _jet_data.values():
        for i in range(len(data) - 1):
            if data[i][0] <= val <= data[i + 1][0]:
                ratio = (val - data[i][0]) / (data[i + 1][0] - data[i][0])
                floats.append(data[i][2] + (data[i + 1][1] - data[i][2]) * ratio)
                break
        else:
            assert False

    return tuple(floats)

def main():
    cmap = matplotlib.colormaps.get_cmap("jet")

    # check only i/255 (i = 0, 1, 2, ..., 255)
    # otherwise, the test will fail due to the difference in the interpolation method
    for value in np.arange(0, 1, 1 / 255):
        pltColor = cmap(value)[:3]
        myColor = getJet(value)
        assert np.allclose(pltColor, myColor)

    print("test passed")

if __name__ == "__main__":
    main()
```

</details>

尤も、LaTeXでの使用が目的ならば、先述の`viridis`と同様にすれば良いと思います。

## サンプル

以下に、これらの色を用いたサンプルを示します。
これはTikZで作成されました。

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/8a9d4527-3d71-26c3-1a51-d19ef97fa695.png" alt="test.png">

<details><summary>LaTeX Code</summary>

```latex
\documentclass[tikz,dvipdfmx,dvipsnames]{standalone}

\usepackage{xcolor}

\definecolor{tabA}{HTML}{1f77b4}
\definecolor{tabB}{HTML}{ff7f0e}
\definecolor{tabC}{HTML}{2ca02c}
\definecolor{tabD}{HTML}{d62728}
\definecolor{tabE}{HTML}{9467bd}
\definecolor{tabF}{HTML}{8c564b}
\definecolor{tabG}{HTML}{e377c2}
\definecolor{tabH}{HTML}{7f7f7f}
\definecolor{tabI}{HTML}{bcbd22}
\definecolor{tabJ}{HTML}{17becf}

\definecolor{matlabBlue}{HTML}{0072BD}
\definecolor{matlabRed}{HTML}{D95319}
\definecolor{matlabYellow}{HTML}{EDB120}
\definecolor{matlabPurple}{HTML}{7E2F8E}
\definecolor{matlabGreen}{HTML}{77AC30}
\definecolor{matlabCyan}{HTML}{4DBEEE}
\definecolor{matlabMaroon}{HTML}{A2142F}

\definecolor{cA}{HTML}{0072BD}
\definecolor{cB}{HTML}{EDB120}
\definecolor{cC}{HTML}{77AC30}
\definecolor{cD}{HTML}{D95319}
\definecolor{cE}{HTML}{7E2F8E}

\definecolor{viridis0}{RGB}{253,231,36}
\definecolor{viridis1}{RGB}{157,217,58}
\definecolor{viridis2}{RGB}{94,201,97}
\definecolor{viridis3}{RGB}{58,82,139}
\definecolor{viridis4}{RGB}{69,50,127}

\definecolor{jet0}{RGB}{0,0,127}
\definecolor{jet1}{RGB}{0,0,254}
\definecolor{jet2}{RGB}{0,96,255}
\definecolor{jet3}{RGB}{0,212,255}
\definecolor{jet4}{RGB}{76,255,170}
\definecolor{jet5}{RGB}{170,255,76}
\definecolor{jet6}{RGB}{255,229,0}
\definecolor{jet7}{RGB}{255,122,0}
\definecolor{jet8}{RGB}{254,18,0}
\definecolor{jet9}{RGB}{127,0,0}

\begin{document}
\begin{tikzpicture}
    \foreach \x/\y/\color in {
            0/0/tabA,
            1/0/tabB,
            2/0/tabC,
            3/0/tabD,
            4/0/tabE,
            5/0/tabF,
            6/0/tabG,
            7/0/tabH,
            8/0/tabI,
            9/0/tabJ,
            0/1/matlabBlue,
            1/1/matlabRed,
            2/1/matlabYellow,
            3/1/matlabPurple,
            4/1/matlabGreen,
            5/1/matlabCyan,
            6/1/matlabMaroon,
            0/2/cA,
            1/2/cB,
            2/2/cC,
            3/2/cD,
            4/2/cE,
            0/3/viridis0,
            1/3/viridis1,
            2/3/viridis2,
            3/3/viridis3,
            4/3/viridis4,
            0/4/jet0,
            1/4/jet1,
            2/4/jet2,
            3/4/jet3,
            4/4/jet4,
            5/4/jet5,
            6/4/jet6,
            7/4/jet7,
            8/4/jet8,
            9/4/jet9}{
            \draw[draw=\color,fill=\color] (1.2*\x, -1.5*\y) circle (0.5);
        }

    \node[anchor=west] at (-1, 0.75-1.5*0) {\textcolor{cA}{tab10 colors}};
    \node[anchor=west] at (-1, 0.75-1.5*1) {\textcolor{cB}{matlab colors}};
    \node[anchor=west] at (-1, 0.75-1.5*2) {\textcolor{cC}{custom colors}};
    \node[anchor=west] at (-1, 0.75-1.5*3) {\textcolor{cD}{viridis colors}};
    \node[anchor=west] at (-1, 0.75-1.5*4) {\textcolor{cE}{jet colors}};
\end{tikzpicture}
\end{document}
```

</details>

## 色を使う時の注意点

釈迦に説法かも知れませんが、色を使う際にはユニバーサルデザインの観点から、いわゆる色弱者の方にも配慮する必要があります。私も完璧に守れている訳ではありませんが、なるべく配慮するようにしています。

https://tsutawarudesign.com/universal1.html

Chromeだと、`Ctrl+Shift+I`で開ける開発者ツールのRenderingタブに、`Emulate vision deficiencies`という機能があります。
これは様々な色覚異常をシミュレートする機能で、これを使って自分の作成した図がどのように見えるのかを確認することができます。
色を多用した図を作成された際には、是非活用してみてください。

https://learn.microsoft.com/en-us/microsoft-edge/devtools-guide-chromium/accessibility/emulate-vision-deficiencies

[追記]

こういうのを見かけました。参考になるかも知れません。

https://github.com/JLSteenwyk/ggpubfigs

> Color palettes are all colorblind friendly. Thus, your figures will be accessible to more people, which is inarguably better for your audience and you.

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/b039af1e-1619-4c94-af4c-64d7217b3bce.png" alt="ggpubfigs">

## Licenseの問題について

以上のことは、全て個人の非営利目的における利用を前提としていました。
これがたとえ商用利用であったとしても、下記のライセンスに従えば問題ないと思われます。

MATLABの方については単にカラーコードを使用しただけなので問題ないかと思いますが、MatplotlibのLicenseは以下のページに記載されています。

https://matplotlib.org/stable/project/license.html

> Matplotlib only uses BSD compatible code, and its license is based on the [PSF](https://docs.python.org/3/license.html) license. See the Open Source Initiative [licenses page](https://opensource.org/licenses) for details on individual licenses.
> (MatplotlibはBSD互換のコードのみを使用しており、そのライセンスはPSFライセンスに基づいています。個々のライセンスの詳細については、Open Source Initiativeのライセンスページを参照してください。)

[Wikipedia](https://ja.wikipedia.org/wiki/BSD%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9)におけるBSDライセンスの説明は以下の通りです。

> 「無保証」であることの明記と著作権およびライセンス条文自身の表示を再頒布の条件とするライセンス規定である。この条件さえ満たせば、BSDライセンスのソースコードを複製・改変して作成したオブジェクトコードを、ソースコードを公開せずに頒布できる。

もし頒布等をされる場合は、これらのライセンスに従ってください。

なお、本稿に直接登場した私が書いたコードに関しては、上記のライセンスに従って頂くという前提のもと、全ての権利を放棄します。
