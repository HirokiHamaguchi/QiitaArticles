# arXivなどへ論文投稿をする際の、LaTeXに関する諸問題とその対処法

論文原稿を投稿する際に、私が詰まった問題などについて本記事ではまとめます。

私はLaTeXに特段詳しい訳ではないので、記事の一部はその背景等も含めて完全に把握をしている訳ではなく、不完全な情報である可能性もあります。そのような記事を書くのは私としても非常に心苦しいのですが、しかし執筆現在において私の見つけ出せる範囲内にあまり情報がなく、またGoogleのAI要約やChatGPTの回答に誤りが含まれていたため、やむを得ずこのような記事を書きました。

もし何かしら情報をお持ちの方がいらっしゃいましたら、是非ご教授頂けますと幸いです。また、この記事は問題が発生する度に更新する可能性があります。

本記事では、以下の諸問題を扱います:

<!-- no toc -->
* [orcidlinkのリンク不全](#orcidlinkコマンドがuplatexで反応しない問題)
* [arXivでのBibTeXエラー](#arxivに投稿する際のbibtexエラー)
* [arXivでのsubfile認識](#arxivでsubfileが認識されない問題)
* [arXivでのendash使用](#arxivでendashを使う際の注意点)

なお、特にarXivに投稿する際に問題点が生じて本記事をご参照なさっている場合、arXivの公式ページを参照することが一番確実な方法だと思いますので、以下にリンクを載せておきます。本記事はあくまでその補足程度の体験談としてご参照頂ければ幸いです。

https://info.arxiv.org/help/submit_tex.html

## orcidlinkコマンドがupLaTeXで反応しない問題

orcidlinkコマンドを使って、ORCIDのアイコンおよびハイパーリンクを作成した時、upLaTeX+dvipdfmxの環境だと、一見正常にコンパイルされているように見えますが、実は機能しない現象があります。本節ではその問題について述べます。執筆時点では本問題に言及している記事を私は見つけられず、この記事執筆の動機となった現象です。

### 背景

ORCIDは、研究者の識別子の一つで、論文などにORCIDを記載することが推奨されることがあります。arXivもORCIDとの連携は推奨しています。

> ORCID® iDs are unique researcher identifiers designed to provide a transparent method for linking researchers and contributors to their activities and outputs. (…… 中略 ……) It will help with the ongoing challenge of distinguishing your research activities from those of others with similar names.
> We encourage all arXiv authors to link their ORCID iD with arXiv.
>
> (ORCID® iDは、研究者や貢献者をその活動や成果に透明な方法で結びつけるために設計された一意の識別子です。(…… 中略 ……)名前が似ている他の人の研究活動と区別するという継続的な課題に役立ちます。我々はすべてのarXiv著者がORCID iDをarXivにリンクすることを奨励します。)

([arXiv公式ページ](https://info.arxiv.org/help/orcid.html)より。最終閲覧日: 2026年3月12日。翻訳、抜粋は筆者による。)

特に、orcidlink packageは、ORCIDのアイコンとハイパーリンクを簡単に作成できる便利なパッケージで、近年は利用されている論文も増えているように思っています。

https://ctan.org/pkg/orcidlink

![orcidlink_package](orcidlink_package.png)

### 動作例

このorcidlink packageは、環境によって不完全な動作をします。以下に動作例を載せます。TeX Live 2025を使用しています。

#### pdfLaTeX

pdfLaTeXは、PDFを直接出力するLaTeXのエンジンの一つで、特に非日本語圏では主流になっているとの言説もみかけます。デフォルトでは日本語を扱うことは出来ませんが、`\orcidlink`コマンドは正常に機能します。

https://ctan.org/pkg/pdftex?lang=en

![test_pdflatex](test_pdflatex.png)

(`pdflatex` でコンパイルした場合。ORCIDアイコンは正しく描画され、全てのリンクが機能する。)

<details><summary>pdfLaTeXのコード</summary>

<!-- PROGRAM_INSERTION: test_pdflatex.tex -->

</details>

#### luaLaTeX

luaLaTeXは、Luaというプログラミング言語を組み込んだLaTeXのエンジンの一つで、近年は特に日本語を扱う際に使われることが増えてきています。こちらも`\orcidlink`コマンドは正常に機能します。

https://www.luatex.org/

![test_lualatex](test_lualatex.png)

(`lualatex` でコンパイルした場合。ORCIDアイコンは正しく描画され、全てのリンクが機能する。)

<details><summary>luaLaTeXのコード</summary>

<!-- PROGRAM_INSERTION: test_lualatex.tex -->

</details>

#### upLaTeX

upLaTeXは、一昔前の日本語LaTeXにおける主流エンジンの一つで、現在も日本語を扱う際に使われることがあります。本来、dvipdfmxと組み合わせて使うことが推奨されているようですが、誤ってdvipdfmxオプションを付けずにコンパイルしてしまうと、以下のような現象が起きます。

https://ctan.org/pkg/uplatex

![test_uplatex](test_uplatex.png)

(`uplatex` でコンパイルし、かつ `documentclass` に `dvipdfmx` オプションを付けていない場合。ORCIDアイコン自体が描画されず、さらに節参照リンクや `\url` も含めて、`hyperref` 由来のリンクが全体的に壊れる。)

<details><summary>upLaTeXのコード</summary>

<!-- PROGRAM_INSERTION: test_uplatex.tex -->

</details>

この場合でも、リンクに枠線などを出していないと、一見正常にコンパイルされているように見えるため、やや気が付きにくいです。特に、VS Code上では警告が出ないことがあります。

![no_dvipdfmx_no_warning](no_dvipdfmx_no_warning.png)

ただし、以下のような警告文がOUTPUTのLaTeX Compilerのログに出ていることが分かります。これが何故VS CodeのPROBLEMSタブに出ないかは不明です。

```txt
dvipdfmx:warning: Unknown token "SDict" dvipdfmx:warning: Interpreting PS code failed!!! Output might be broken!!! dvipdfmx:warning: Interpreting special command ps: (ps:) failed.
```

簡単にこの原因を説明すると、driverの不一致が原因でこのような警告が出ています。尤も、pdfなどの画像を含めていると、明示的にエラーが出るという点では、やや気が付きやすいです。

#### upLaTeX + dvipdfmx

正しくdvipdfmxオプションを付けてコンパイルした場合、以下のような現象が起きます。

https://ctan.org/pkg/dvipdfmx

![test_uplatex_dvipdfmx](test_uplatex_dvipdfmx.png)

(`uplatex` でコンパイルし、かつ `documentclass` に `dvipdfmx` オプションを付けた場合。ORCIDアイコンは描画され、通常の `hyperref` のリンクも機能するが、**ORCIDのリンクだけは反応しない**。)

<details><summary>upLaTeX + dvipdfmxのコード</summary>

<!-- PROGRAM_INSERTION: test_uplatex_dvipdfmx.tex -->

</details>

画像の通り、upLaTeX+dvipdfmxの環境では、ORCIDアイコンは描画され、通常の `hyperref` のリンクも機能しますが、ORCIDのリンクだけは反応しないという現象が起きます。このように、特にupLaTeX+dvipdfmxの場合に、**かなり気付きにくい形でorcidlinkは壊れることがあります**。また、先ほどと同様、VS Code上では警告が出ないことがあります。

### 原因の考察

upLaTeX+dvipdfmxの環境で、何故orcidlinkのリンクだけが反応しないのか、以下に考察を述べます。

[orcidlink package](https://ctan.org/pkg/orcidlink)の[GitHubにある実装](https://github.com/duetosymmetry/orcidlink-LaTeX-command/blob/master/orcidlink.sty)を見ると、内部でhyperrefコマンドを使っています。以下がその実装の引用です。

<details><summary>orcidlink.styの実装</summary>

```tex
\NeedsTeXFormat{LaTeX2e}[1994/06/01]
\ProvidesPackage{orcidlink}
    [2024/06/26 v1.1.0 Support ORCID's three different ID formats.]

\RequirePackage{hyperref}
\RequirePackage{tikz}

\ProcessOptions\relax

\usetikzlibrary{svg.path}

\definecolor{orcidlogocol}{HTML}{A6CE39}
\tikzset{
  orcidlogo/.pic={
    \fill[orcidlogocol] svg{M256,128c0,70.7-57.3,128-128,128C57.3,256,0,198.7,0,128C0,57.3,57.3,0,128,0C198.7,0,256,57.3,256,128z};
    \fill[white] svg{M86.3,186.2H70.9V79.1h15.4v48.4V186.2z}
                 svg{M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z}
                 svg{M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1C84.2,46.7,88.7,51.3,88.7,56.8z};
  }
}

%% Reciprocal of the height of the svg whose source is above.  The
%% original generates a 256pt high graphic; this macro holds 1/256.
\newcommand{\@OrigHeightRecip}{0.00390625}

%% We will compute the current X height to make the logo the right height
\newlength{\@curXheight}

%% Prevent externalization of the ORCiD logo.
\newcommand{\@preventExternalization}{%
\ifcsname tikz@library@external@loaded\endcsname%
\tikzset{external/export next=false}\else\fi%
}

\newcommand{\orcidlogo}{%
\texorpdfstring{%
\setlength{\@curXheight}{\fontcharht\font`X}%
\XeTeXLinkBox{%
\@preventExternalization%
\begin{tikzpicture}[yscale=-\@OrigHeightRecip*\@curXheight,
xscale=\@OrigHeightRecip*\@curXheight,transform shape]
\pic{orcidlogo};
\end{tikzpicture}%
}}{}}

\DeclareRobustCommand\orcidlinkX[3]{\href{https://orcid.org/#2}{%
\ifstrempty{#1}{}{#1\,}\orcidlogo\ifstrempty{#3}{}{\,#3}}}
\newcommand{\orcidlinkf}[1]{\orcidlinkX{}{#1}{https://orcid.org/#1}}
\newcommand{\orcidlinkc}[1]{\orcidlinkX{}{#1}{#1}}
\newcommand{\orcidlinki}[2]{\orcidlinkX{#1}{#2}{}}
\newcommand{\orcidlink}[1]{\orcidlinkX{}{#1}{}}

\endinput
```

</details>

具体的には、`TikZ`で描画したものに対して、`hyperref`の`\href`コマンドでリンクを付けている形になっています。XeLaTeXを使う場合に関しては、このような場合に対する不具合は古くから知られているようで、実際、上の実装では`\XeTeXLinkBox`を使うことで、リンクが機能するように工夫されているようです。v1.0.4のアップデートでこれが解消されたとの記載が公式ドキュメントにありました。upLaTeXについては、特に情報を見つけられませんでした。

https://tex.stackexchange.com/questions/563279/using-hyperref-with-includegraphics-doesnt-work-with-xelatex

リンクが反応しない原因は、このように画像に対してハイパーリンクを付けようとすると、特にドライバなどの処理系に依存したの問題発生するためだと思われます。

### 解決策

以下に、この問題に対する暫定的な解決策を述べます。

#### 解決策0: そもそもorcidlinkを使わない

研究室の助教さんと雑談していたら、そもそもorcidlinkを使わなくていいのでは、と言われました。

その通りな気もします。

実際、直近のarXivの論文を見ていると、Physicsの論文では大体15%程度、Mathの論文では大体5%程度の論文がorcidlinkを使っているように見えます。
出版社側から指定されている訳でもなければ、そもそも使わないという選択肢も十分にあり得ると思います。

ただ、個人的にはgmailよりも追跡性が高い識別子であるORCIDは良い取り組みだなと思っていたので、出来れば使いたいと思っており、このような記事を書いている次第です。

#### 解決策1: pdfLaTeX・luaLaTeX・XeLaTeXの使用

簡易的な解決策の一つは、pdfLaTeX・luaLaTeX・XeLaTeXを使うことです。昨今はpdfLaTeXが国際的に主流であり、またluaLaTeXやXeLaTeXも広く使われているようですので、その流れに乗っていれば大抵の問題は起きないと思います。pdfLaTeXでも例えばCJKパッケージを使うことで日本語入力は可能なので、代替案にはなり得ると思います。

外部リンクなどをはることは省略しますが、特にluaLaTeXは使用を促す記事も多く、やや速度が遅いという欠点はあるものの、こういった現象を未然に防ぐという観点からは有望な選択肢のように思われます。

#### 解決策2: orcidlinkiコマンドの使用

また、upLaTeXを使う場合でも、先ほどのorcidlinkの実装にもあった`\orcidlinki`などを使うと、文字側にハイパーリンクを付けられるので、それで対処することも可能かもしれません。

![test_uplatex_dvipdfmx_orcidlinki](test_uplatex_dvipdfmx_orcidlinki.png)

<details><summary>orcidlinkiコマンドを使った例</summary>

<!-- PROGRAM_INSERTION: test_uplatex_dvipdfmx_orcidlinki.tex -->

</details>

画像自体にはリンクが機能しないままですが、ほぼ同様の機能を実現できます。

以上がorcidlinkのリンクがupLaTeX+dvipdfmxの環境で反応しない問題についての考察と暫定的な解決策になります。

## arXivに投稿する際のBibTeXエラー

続いて、arXivに投稿する際のBibTeXエラーについて述べます。

Overleafのsubmit機能を使うと良いことが知られています。
一般的には、この機能で出力されるbblファイルを含めて、arXivにアップロードすれば、問題なく処理されるはずです。

しかし、完全にbblファイルやbibファイルがない状態でOverleaf上でコンパイルが通るとしても、次のようなエラーが出てくることがあります。

![arXiv_bbl_bib_error](arXiv_bbl_bib_error.png)

```txt
The scan did not detect a bibliography. Please include one.
Both bbl and bib files are missing
```

私の場合、これはsubfilesの内側で、次のようにif文付きのbibliographyコマンドを使っていたことが原因でした。

```tex
\ifSubfilesClassLoaded{
    \bibliography{myReferences.bib}
}{}
```

本来if文によって、これは完全に無視されるので、一切コンパイルには関与しないのですが、arXiv側のシステムがあまり賢くないようで、このようなエラーが出てしまうようです。これを手動で削除したら解決しました。

つまり、より抽象的に言えば、arXiv側のシステムの解析で、使用の可能性が疑われるbibファイルが少しでもあると、実際に使用されていないとしても、エラーが出る可能性があり、それを削除するのが重要、というのが本節の結論となります。

## arXivでsubfileが認識されない問題

同様の話として、subfileが認識されない問題もあります。

先述のarXivの公式ページには、以下のような記述があります。

> You can submit a collection of TeX input/include files, e.g. separate chapters, foreword, appendix, etc, and custom macros (see below) packaged in a (possibly compressed) .tar or .zip file. Main files (or "Toplevel files") can be in the root or in a subdirectory, **but note that compilation is always done from the root of your submission directory, even if the main file is in a subdirectory**. This is important when you use \include or \input or any other command that includes data from external files.
>
> (TeXの入力ファイルやincludeファイル、例えば別々の章、前書き、付録などを、（必要に応じて圧縮された）.tarや.zipファイルにまとめて提出できます。メインファイル（または「トップレベルファイル」）はルートまたはいずれかのサブディレクトリに置くことができますが、**コンパイルは常に提出ディレクトリのルートから行われることに注意してください**。これは、\includeや\inputなどのコマンドを使用して外部ファイルからデータを含める場合に重要です。)

([arXiv公式ページ](https://info.arxiv.org/help/submit_tex.html)より。最終閲覧日: 2026年3月12日。翻訳、強調は筆者による。)

特に、手元の環境とコンパイルが行われるディレクトリが異なる場合に、相対パスが壊れ、特にトラブルが起きやすいと思います。一番簡単なのは、mainとなるtexファイルをフォルダーの中ではなく、ルート直下に配置することだと思います。そうすれば、殆どの環境で両者が一致し、トラブルが起きにくくなると思います。

## arXivでendashを使う際の注意点

最後に、arXivでendash(–)をtitleに使うときの注意点について述べます。

前提として、endash(–)は、主に2人以上の人名をつなげるときによく使われます。例えば高校数学でも扱われるコーシーシュワルツの不等式は、Wikipediaでは[Cauchy–Schwarz inequality](https://en.wikipedia.org/wiki/Cauchy%E2%80%93Schwarz_inequality)とendash(–)を用いて表記されています。LaTeXでは、通常`--`と書くとendash(–)になります。

しかし、arXivに投稿する際に、タイトルなどのmetadataで--と書くと、これendash(–)として処理されず、単なるダブルハイフン(--)のまま表示されてしまい、やや見栄えが悪くなります。また、arXivはmetadataとして、ASCII以外の文字は受け付けないので、endash(–)を直接書くことも出来ません。よって、**あくまで私の知る限りにおいて、このダブルハイフンを用いる手法が最善だと思います**。

![bad_characters](bad_characters.png)
(Our metadata fields only accept ASCII input. Unicode characters should be converted to its TeX equivalent)

一方で、endashをarXivのmetadataで`\unicode{x2013}`のように、Unicodeエスケープで指定する手法もあるようです。HTMLでは正しく処理されるので、一見良いように思えます。しかし、**この手法は全くおすすめ出来ません**。あえてリンクは載せませんが、2026年現在、arXivのmetadataでendashを使う際に、これを勧める記事がトップヒットしますが、**これはかなり危険な方法だと思います**。

![endash_twitter](endash_twitter.png)
(Unicodeによるendashの使用例に関するツイート)

具体的には、以下のかなり重大な欠点を抱えています:

* 参考文献としてbibtexで読み込んで使おうとすると、`\unicode{x2013}`が正しく処理されず、**エラーになり得ることがある**。
* ロードのタイミング(?)では正しく描画されず、代わりに`\unicode{x2013}`の文字列が**そのまま表示されることがある**。

![test_endash](test_endash.png)
(LaTeXでは、`$\unicode{x2013}$`は正しく処理されず、コンパイルエラーになる。)

![x2013](x2013.png)
(過去に投稿した私の論文。タイトルに`\unicode{x2013}`を使ってしまっている。その後、修正しました。)

よって、endashを使うときは、厳密な表記ではないという点から少し不満点は残りますが、普通に`--`と書くのが一番安全で確実な方法だと思います。

## 最後に

以上、いくつかの問題についてまとめました。

本記事は今後も更新する可能性があります。何か新しい情報が分かり次第、随時更新していきたいと思います。
