# orcidlinkがuplatexでリンク不全になる問題とその対処法

本記事の要点は以下の通りです:

* orcidlinkパッケージを用いてORCIDのハイパーリンクを作成し、dvipdfmxを用いてコンパイルすると、リンク不全になることがありました。
* この問題はhyperrefパッケージに報告し、**今後解決される予定です**。もしどうしても旧版しか使えない場合は、pdflatexやxelatexを使うことで回避できます。
* 同様の問題は、**たとえ最新版であっても、TikZで作成した図にハイパーリンクをはると今後もdvipdfmxを用いたドライバでは発生する可能性があります**が、hyperrefパッケージの`\XeTeXLinkBox`コマンドを使うと、XeTeXを使う場合に限らずdvipdfmx系なら解消されます。

## 具体例

XeTeXでは、TikZで作成した図にハイパーリンクをはると、リンク不全になることがあります。以下の例は、プルリクエスト用に作成した図であるため少々ごちゃついていますが、`no text`, `\line(0,1){10}`, `\line(1,0){10}`の部分を`\href`コマンドで囲んでいますが、ハイパーリンクが生成されていません。

<img width=100% src="https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260313_orcidlink/examples_failed/examples_failed_raw__xelatex.png" alt="examples_failed_raw__xelatex">

(2026年3月20日現在における旧版のhyperrefとXeTeXを用いたコンパイル結果について、pythonでリンクを明示した画像)

そして、この問題は、**dvipdfmxを用いたドライバを使うと、たとえhyperrefの最新版を使っていても、ほぼ確実に発生します**。

<img width=100% src="https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260313_orcidlink/examples_failed/examples_failed_dvipdfmx__uplatex_dvipdfmx.png" alt="examples_failed_dvipdfmx__uplatex_dvipdfmx">

(2026年3月20日現在における旧版のhyperrefとupLaTeXを用いたコンパイル結果について、pythonでリンクを明示した画像。特に、orcidlinkパッケージを用いて作成したORCIDのハイパーリンクが機能していないことに注目。最新版のhyperrefを用いると、これがXeTeXを用いた場合と同じ挙動になる予定です。)

しかし、`\XeTeXLinkBox`コマンドを使うと、XeTeXに限らずdvipdfmxを用いたドライバであれば、リンクが機能するようになります。ただし、この問題が修正された以降のhyperrefパッケージを使っている必要があります。

```tex
% \XeTeXLinkBoxを使う例
\href{https://hirokihamaguchi.github.io/}{%
    \XeTeXLinkBox{%
        \begin{tikzpicture}[scale=0.5]%
              (中略)%
        \end{tikzpicture}%
    }%
}.
```

## 詳細

更なる詳細は以下のPRを参照してください。ここに書いていある提案の一部は、受理されておらず、別の方法で解決されているので、注意して下さい。

https://github.com/latex3/hyperref/pull/412#issuecomment-4090224717

また、hyperrefパッケージ開発者の意向で、パッケージの変更に後方互換性のない方法が採られたため、このPRの内容の再現実験をしようとすると今後は失敗する可能性があります。尤も、再現に失敗しているということはhyperrefの最新版を使っているということなので、大丈夫だとは思います。

## まとめ

ともかく、「困った」という問題を抱えてこの記事を読んでいらっしゃる方は、

* 今後リリース予定のhyperrefの最新版を使う
* どうしても旧版しか使えない場合は、pdflatexやxelatexを使う
* dvipdfmx系のドライバにて、TikZで作成した図にハイパーリンクをはる場合は、`\XeTeXLinkBox`コマンドを使う

という方法で対処してくだされば、問題は解決すると思います。

この記事がお役に立てば幸いです。

## 謝辞

この問題の解決にご尽力いただいた、hyperrefパッケージの開発者である、Ulrike Fischer(u-fischer)氏に、心より感謝申し上げます。
