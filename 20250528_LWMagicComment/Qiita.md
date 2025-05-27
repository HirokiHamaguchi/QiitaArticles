<!-- markdownlint-disable MD041 -->

VS Codeで[LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop)を使用している場合、`.tex`ファイルの先頭に以下のようなコメントを追加することで、レシピを指定できます。

```tex
%!LW recipe=recipe-name
```

このmagic commentは[LaTeX Workshop](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile#latex-recipes)のWikiに記述されています。**ただし、記事後半に記した[注意点と代替手段](#注意点と代替手段)もあるため、使用する際は注意が必要です。**

また、他にもいくつかmagic commentがありますが、それらは非推奨のようです。詳しくは[Wiki](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile#latex-recipes)の当該箇所をご覧ください。

## 詳細な説明

一例として、検索上位に来るLaTeXの[環境構築記事](https://zenn.dev/hash_yuki/articles/31855fbdb5fdf7
)で使われているレシピを使い分けます。

以下がレシピの引用ですが、これら2つのレシピを登録しているとします。

```json
// ......(中略)......
    //latexmkのビルドレシピ
    "latex-workshop.latex.recipes": [
        //bibTexを使用しない場合のレシピ
        {
            "name": "ptex2pdf (uplatex)*2",
            "tools": [
                "ptex2pdf (uplatex)",
                "ptex2pdf (uplatex)"
            ]
        },
        //bibTexを使用する場合のレシピ
        {
            "name": "ptex2pdf (uplatex) -> bibtex -> ptex2pdf (uplatex) *2",
            "tools": [
                "ptex2pdf (uplatex)",
                "pbibtex",
                "ptex2pdf (uplatex)",
                "ptex2pdf (uplatex)"
            ]
        }
    ],
// ......(中略)......
```

この内容を当該記事のように設定することで、下図のように複数のレシピが登録されます。

<img width=100% src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c5a319fd-9c04-430f-9a2c-9493aaa4c896.png" alt="recipes">

`latex-workshop.latex.recipe.default`という[設定](https://github.com/James-Yu/LaTeX-Workshop/wiki/Compile#latex-workshoplatexrecipedefault)でデフォルトの"first"を指定していると、これらレシピのうち、先頭にある`ptex2pdf (uplatex)*2`がautoBuildにおいて使われます。

一応、この設定で`lastUsed`を指定すると、`LaTeX Workshop: Build with recipe`コマンドで最後に使用されたレシピが選択されますが、自由度は低いです。

そこで、基本は前者のレシピを使いながら、ある特定のファイルでは後者のレシピを使いたい場合、以下のように`.tex`ファイルの先頭にmagic commentを追加します。

```tex
%!LW recipe=ptex2pdf (uplatex) -> bibtex -> ptex2pdf (uplatex) *2

\documentclass[a4paper,12pt]{jlreq}

\title{サンプル}
\author{Hiroki Hamaguchi}

\begin{document}
\maketitle

常にbibtexを走らせたい\cite{sample}。

\bibliographystyle{jplain}
\bibliography{sample}

\end{document}
```

すると、確かにこのレシピが使用され、ファイル毎にレシピを使い分けられます。

## 注意点と代替手段

注意として、

* localにしかレシピ名を保存しない場合に**環境に依存するtexファイルが増える**
* localの場合でもファイルを移動する際に**settings.jsonと一緒にしないと壊れる**
* 仕様を知らない人とファイル共有をすると**バグの原因になる**

などの欠点も存在します。

また、**より簡潔に正攻法で解決できる場合にはmagic commentを使う必要はありません**。

例えばTikZでは、

```tex
\documentclass{standalone}
```

を`ptex2pdf`でコンパイルすると正しく表示されないことがある一方、`pdflatex`でコンパイルすると正しく表示されることがあります。

この場合、`%!LW recipe=`で`pdflatex`を指定することも可能ですが、

```tex
\documentclass[dvipdfmx]{standalone}
```

とすれば`ptex2pdf`でも正常にコンパイル可能です。

## 有効なシナリオ

上記の欠点こそあるものの、この機能は様々なシチュエーションで便利かと思います。

例えば、やはり**図や数式などを単体で出力する**ような、Overleafにもアップしない補助的な役割を果たす`.tex`ファイルを作成する場合や、学会や出版社側からの指定で**特定のdocument classやレシピを使用する必要がある場合**などが最も有効そうなシナリオだと思います。

特に、latexmkrcを使っても`%!LW recipe=`と似たようなことは達成可能のようですが、そのような曲芸に比べれば遥かに簡潔で汎用的だと思います。このようなmagic commentの存在を把握しておくこと自体に損はないと思われます。

## 最後に

本記事が`%!LW recipe=`の周知および、快適なLaTeX生活の一助になれば幸いです。
