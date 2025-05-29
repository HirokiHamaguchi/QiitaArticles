# 英語での読み方が難しい数学の用語・記法

英語での読み方が難しい数学の用語・記法をまとめます。

本記事は以下の節から構成されます。

1. [発音](#発音) 数学にまつわる英単語の発音など
2. [数式の読み方](#数式の読み方) 数式・記法の非自明な読み方
3. [その他](#その他) 筆者が知らなかった単語など

この記事は筆者が例を見つけたときに更新する可能性があります。

---

本記事の一部は、服部 久美子さん著の『数学のための英語教本 ―読むことから始めよう―』の内容に触発されて書きました。とても良い本だと思いますので、お勧めです。以下、本書のことを「教本」と言及します。

https://www.kyoritsu-pub.co.jp/book/b10003278.html

<img width="25%" alt=""><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOHuOtNKEgfQ0INW3V8rm3MfH8nu_GU_n6SQ&s" alt="教本" width="50%"/><img width="25%" alt="">

---

## 発音

発音記号はCambridge Dictionaryを参考にしています。

https://dictionary.cambridge.org/ja/

### 一般用語

#### scalar

スカラーとよく言われますが、発音はスケイラに近いです。

参考: 教本 p.17

#### vector

ベクタに近い発音です。

参考: 教本 p.17

#### matrix

メイトリクスに近い発音です。

参考: 教本 p.24

#### eigenvalue

アイゲンバリューに近い発音です。

参考: 教本 p.24

#### eigenvector

アイゲンベクターに近い発音です。

参考: 教本 p.24

#### algebra

最初のアにアクセントがある。

参考: [河東先生のHP](https://www.ms.u-tokyo.ac.jp/~yasuyuki/english2.htm)

#### finite

参考: [河東先生のHP](https://www.ms.u-tokyo.ac.jp/~yasuyuki/english2.htm)

#### infinite

参考: [河東先生のHP](https://www.ms.u-tokyo.ac.jp/~yasuyuki/english2.htm)

#### tensor

#### dimension

だいめんしょん

#### affine

affine
アファインに近い発音です。

#### quasi

それぞれクワジ、クワザイに近い発音です。

クワジ派 [YouTube-SciPy](https://youtu.be/VIoWzHlz7k8?t=724)

クワザイ派 [YouTube](https://www.youtube.com/watch?v=CjCBzOwHa3s&t=608s) (恐らくこの方はインドっぽい?)

#### pseudo

シュードに近い発音です。

pseudo-inverse 一般化逆行列 (Moore–Penrose inverse とも)

$$
A=U\Sigma V^\top \implies A^+ = V \Sigma^+ U^\top
$$
where
$$
\Sigma^+ = \mathrm{diag}(\sigma_1^{-1}, \sigma_2^{-1}, \ldots, \sigma_r^{-1}, 0, \ldots, 0)
$$

参考: [高校数学の美しい物語](https://manabitimes.jp/math/2746)

#### chaos

ケイオスに近い発音です。

カオス理論 数的誤差のため予測が困難とされている、二重振り子などの複雑な現象を扱う理論

#### wolfe

orthogonal 分布フーリエ（Fourier）解析

#### height

ハイト(高さ)

#### anti

エンタイ,エンティ(反~)

#### relative

レラティブ(相対)

ラプラス（Laplace）変換 パラメトリック（parametric）イメージ（image：像）

カーネル（kernel：核）

イデアル（ideal：イデアル）

### 固有名詞

#### Hermitian

ハーミシャンに近い発音です。

参考: 教本 p.76

#### Jacobian

ジャコビアンに近い発音です。

参考: 教本 p.76

#### Erdos

#### Poisson

Poisson distribution ポアソン分布 ($P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$)

USの方の発音だと、soʊnにアクセントがあります。
日本訛りだとpwəにアクセントがあると思います。

#### Banach

#### Hausdorff

#### Wasserstein

$$
W_p(\mu, \nu) = \inf_{\gamma \in \Gamma(\mu, \nu)} \left(\mathbf{E}_{(x, y) \sim \gamma} d(x, y)^p \right)^\frac{1}{p}
$$

($\Gamma(\mu, \nu)$ がカップリング、つまり、よくある堆積した土の例でいうところの移動方法の集合なので、堆積を移動する最小コストを表す)

参考: [Wikipedia](https://en.wikipedia.org/wiki/Wasserstein_metric)

#### Gaussian

ゴーシアン???

#### Barzilai

バジライに近い発音です。

参考: [YouTube](https://www.youtube.com/watch?v=thtr1yH4Z38&t=27s), [forvo](https://forvo.com/search/Barzilai), [How To Pronounce](https://www.howtopronounce.com/barzilai)

#### Borwein

Borwein ボォー(ル)ウェイン

Barzilai--Borwein法のBorweinさんです。
個人的事情から本記事の[おまけ](#おまけ-barzilai--borwein法)で数理的な解説をしています。

[Borwein積分](https://en.wikipedia.org/wiki/Borwein_integral)のBorweinさん親子と子供側と同一人物でもあります。

$$
\begin{align*}
  & \int_0^\infty \frac{\sin(x)}{x}\frac{\sin(x/3)}{x/3}\cdots\frac{\sin(x/15)}{x/15} \, \mathrm{d}x \\
={}& \frac{467807924713440738696537864469}{935615849440640907310521750000}~\pi \\
\approx{}& \frac \pi 2 - 2.31\times 10^{-11}.
\end{align*}
$$

参考: [YouTube (By 3Blue1Brown)](https://youtu.be/851U557j6HE?t=220), [How To Pronounce](https://www.howtopronounce.com/borwein)

#### Zorn

Zorn's lemma: 半順序集合Pは、その全ての鎖(つまり、全順序部分集合)がPに上界を持つとする。このとき、Pは少なくともひとつの極大元を持つ。([Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%84%E3%82%A9%E3%83%AB%E3%83%B3%E3%81%AE%E8%A3%9C%E9%A1%8C))

日本語だとツォルンの補題とよく言われますが、英語ではゾーンに近い発音のこともあるようです。

[Zornさん](https://en.wikipedia.org/wiki/Max_August_Zorn)がドイツ人であり、German: [tsɔʁn]とあることから、日本語の方が本来に近い発音かもしれません。

参考: [YouTube](https://www.youtube.com/watch?v=f8Rv2PHxAwQ&t=222s)

####

https://x.com/banban7866/status/1083747445597585408

#### Springer

出版社

https://ell.stackexchange.com/a/192428

https://x.com/mirucaaura/status/1427144163082924032

## 数式の読み方

### 一般

#### equal

https://ejje.weblio.jp/content/equal

#### power

$x^2$
$x^3$
$x^n$
$10^5$
$10^-5$

#### root

$\sqrt{2}$
$\sqrt[3]{2}$
$\sqrt[n]{2}$

#### other

https://librivox.org/uploads/xx-nonproject/Handbook%20for%20Spoken%20Mathematics.pdf

#### bar

集合記号

## その他

いろいろ調べる過程で、自分が知らなかった英単語をいくつか見かけたので、記しておきます。

### 基礎

#### contrapositive

対偶

#### tautology

#### reciprocal

https://www.etymonline.com/word/reciprocal

### 線形代数

#### non-singular

non-singular

#### homomorphism

homo homeo

#### endomorph

自己準同型

industryと同根らしいです。

#### idempotent

#### nilpotent

### 最適化

#### strictly convex

狭義凸 ($f(tx + (1-t)y) < tf(x) + (1-t)f(y)$ と等号のない不等式で凸不等式を満たす関数)

「真に凸」と言いますが「真凸」と訳すと誤訳です。

参考: 私のやらかし

#### proper convex

真凸 (少なくとも一つの $x$ に対して $f(x) < \infty$ が成立し、全ての $x$ に対して $f(x) \geq -\infty$ が成立する凸関数)

参考: [Wiki](https://ja.wikipedia.org/wiki/%E7%9C%9F%E5%87%B8%E5%87%BD%E6%95%B0)

### Twitter

#### radii

radiusの複数形

参考: [Twitter](https://x.com/tenseiYN99/status/1925438036420304931)

#### equilibria

参考: 上記ツイートのリプライ

#### entire function

整関数

https://ja.wikipedia.org/wiki/%E6%95%B4%E9%96%A2%E6%95%B0

複素数平面の全域で定義される正則函数を指す。
関数全体ではない。

参考: 私の友人の鍵垢ツイート

#### annihilator

(アナイアレイター)

参考: https://x.com/Keyneqq/status/1037263459514114048

#### denote

Let A (数式) denote B (内容).

それ以外の使い方は多くの場合に非推奨とされる。

参考: 教本 p.90

https://x.com/sesiru8/status/1325372621169463296

#### 他サイト

参考用に、数学における英語の用語がまとまったサイトをいくつか列挙しておきます。

Hyper Collocation

https://hypcol.marutank.net/ja/

---

https://www.ryugakusite.com/article/high_school_math/

https://sorabalab.com/glossary/glossary.html

## 最後に

以上です。

**他にも面白い例をご存じの方は、是非教えてください!!!**

---

最後に少しだけ補足です。

特に[発音](#発音)のような一覧を見ると全部覚えるの怠いなぁと私は思うのですが、英語を話すときにこれらを全て厳守する必要はないと思っています。よく言われていることですが、訛りや文法の間違いは文意が正確に伝わる限り許容されがちです。

ただ、私は特にリスニングで発音の違いに苦労しています。お恥ずかしながら私は未だに英語の発音が聞き取れない/聞き慣れない正しい発音に気を取られて文意を掴み損ねる、ということがあります。ただ、予めその傾向を把握しておけば、楽に聞き取れることも増えると思います。

例えば、インドの方の発音は、[quasi](#quasi)の節でも暗示されているように、イギリス英語の影響を受けていることが多いです。18世紀頃から1947年8月15日のインド独立まで、イギリスの植民地だった影響と思われます。また、[Wiki](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%83%B3%E3%83%89%E8%8B%B1%E8%AA%9E)によると、"R"を強く発音する傾向があるらしいです(water（水）- ウォータル)。

また、フランスの方の発音は、イギリス英語的な傾向に加え、フランス語の影響も当然受けているので、"R"や"H"の音が特徴的です。例えば、"hospital"（病院）は、オスピタルのように発音される方が多いらしいです([参考](https://qa.speakbuddy.jp/qa/247))。実際私もHessianの"H"が抜かれている発音を聞いたことがあります。

私は全く詳しくないものの、「インド・ヨーロッパ語族」に英語、インドのサンスクリット語・ヒンディー語、フランス語は分類されていますが、語派としては異なるらしく、特にフランス語はロマンス語派に分類されるようです。英語はゲルマン語派に分類されます。

![Sekai-no-gengo](https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Sekai-no-gengo.png/1200px-Sekai-no-gengo.png?20081022180809)

Auf at Japanese Wikipedia, [CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/), via Wikimedia Commons

こういった傾向も踏まえた上で、辞書的な発音を知っておくことは、数学的主張の理解に有効だと思います。

本記事が皆様の数学に関する英語の理解に役立てば幸いです。

## おまけ Barzilai--Borwein法

https://en.wikipedia.org/wiki/Barzilai-Borwein_method

本記事の途中で言及したBarzilai--Borwein法は、かなり面白いアルゴリズムなので、少しだけ記します。

Barzilai--Borwein法[^BB]は、凸関数に対する単純な勾配法において、step sizeを次のいずれかに設定する方法です。

$$
\alpha_k^{\mathrm{LONG}} = \frac{\langle s_k, s_k \rangle}{\langle s_k, y_k \rangle} \quad \text{or} \quad \alpha_k^{\mathrm{SHORT}} = \frac{\langle s_k, y_k \rangle}{\langle y_k, y_k \rangle}
$$

準Newton法において、セカント条件 $B_{k+1} s_k = y_k$ が重要であることを前提とします ([参考スライド p.28](https://www.kurims.kyoto-u.ac.jp/coss/coss2023/slides/narushima-lecture.pdf))。

すると、ヘッシアン行列の近似 $B_{k+1}$ として単位行列の定数倍 $1/\alpha I$ を使おうとすると、

$$
\begin{align*}
  & \argmin_{\alpha} \| s_k / \alpha - y_k \|^2\\

={}& \argmin_{\alpha} (\alpha^{-2} \|s_k\|^2 - 2 \alpha^{-1} \langle s_k, y_k \rangle + \|y_k\|^2)\\
={}& \frac{\|s_k\|^2}{\langle s_k, y_k \rangle}
\end{align*}
$$

あるいは、

$$
\begin{align*}
    & \argmin_{\alpha} \| s_k - \alpha y_k \|^2\\
={}& \argmin_{\alpha} (\|s_k\|^2 - 2 \alpha \langle s_k, y_k \rangle + \alpha^2 \|y_k\|^2)\\
={}& \frac{\langle s_k, y_k \rangle}{\|y_k\|^2}
\end{align*}
$$

かを使うのが自然です。これらは正に上記のBarzilai--Borwein法のstep sizeに対応します。

ここで、$\alpha_k^{\mathrm{LONG}}$ と $\alpha_k^{\mathrm{SHORT}}$ の大小関係を考えると、

$$
\begin{align*}
    &\|s_k\| \|y_k\| \geq \langle s_k, y_k \rangle \quad \text{(Cauchy--Schwarz)}\\
\implies{} & \frac{\|s_k\|^2}{\langle s_k, y_k \rangle} \geq \frac{\langle s_k, y_k \rangle}{\|y_k\|^2} \\
\implies{} & \alpha_k^{\mathrm{LONG}} \geq \alpha_k^{\mathrm{SHORT}}
\end{align*}
$$

であるため、この命名が自然であることも分かります。

なお、このstep sizeはBB step sizeとも呼ばれます[^BBStepSize]。

Rayleigh商との関係でも捉えられます[^rayleigh]。

[^BB]: [Barzilai, J., & Borwein, J. M. (1988). Two-point step size gradient methods. IMA journal of numerical analysis, 8(1), 141-148.](https://academic.oup.com/imajna/article-abstract/8/1/141/802460)

[^BBStepSize]: [Tan, C., Ma, S., Dai, Y. H., & Qian, Y. (2016). Barzilai--Borwein step size for stochastic gradient descent. Advances in neural information processing systems, 29.](https://proceedings.neurips.cc/paper/2016/hash/c86a7ee3d8ef0b551ed58e354a836f2b-Abstract.html)

[^rayleigh]: [Raydan, M. (1993). On the Barzilai and Borwein choice of steplength for the gradient method. IMA Journal of Numerical Analysis, 13(3), 321-326.](https://academic.oup.com/imajna/article-abstract/13/3/321/703847?redirectedFrom=fulltext)
