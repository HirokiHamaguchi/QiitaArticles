# 連続ではない凸関数

**開区間**上で定義された凸関数は**連続**です。この意味で、「凸関数は連続である」と言えます。(高校数学ではこのケースしか扱わないことも多く、これのみを知りたい方はより分かりやすい文献[^easyProof]もご参照ください。)

![open_interval](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/974d791b-2602-3bee-a2b1-680437cdea8a.png)

一方で、**閉区間**上で定義された凸関数は区間の端点で**連続であるとは限りません**。一般に、凸関数はこのような縁(ふち)で不連続になり得ます。

![closed_interval](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/265dac7d-f42c-aee4-1313-4a5d4ca3b223.png)

では、このように明らかに値が断絶した、ある意味で自明な不連続関数しかないのかというと、実はそうではなく、**非自明な不連続関数も存在します**。より厳密にいえば、閉凸関数であっても、下図のように不連続な凸関数が構成できます。青点 $(0,0)$ は連続点なように見えますが、赤で示した $(0,0)$ に収束する点列を考えると、不連続点であることが分かります。

![psi3](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/f8b9da52-a639-1ccb-afe1-dc978a30ac8b.png)

本記事の内容は、Nesterovによる"Lectures on Convex Optimization"[^Nesterov]に一部準拠します。以下、教科書と表記します。

## 概要

本記事では以下のフローチャートに基づき説明します。

![flowchart](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/4d167944-3e8d-2fe7-6e8a-c6807717102f.png)

## 定義

はじめに、厳密な議論の為に定義を示します。

### 凸関数

集合 $Q$ が凸(convex)であることは、任意の $x, y \in Q$ と $\alpha \in [0, 1]$ に対して次が成立することと同値です（教科書 Definition 2.1.1）。

$$
\alpha x + (1 - \alpha) y \in Q.
$$

| 凸集合である | 凸集合でない |
| :---: | :---: |
| ![convex](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/3b35d51e-3099-9339-cdec-493933834844.png) | ![non_convex](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/4206d582-2506-f89d-e23e-ff8b9179a9f2.png) |

(Wikipedia「[凸集合](https://ja.wikipedia.org/wiki/%E5%87%B8%E9%9B%86%E5%90%88)」より引用 / [CheCheDaWaff](https://commons.wikimedia.org/wiki/File:Convex_polygon_illustration1.svg), CC BY-SA 4.0, via Wikimedia Commons)

また、拡大実数に値を取る関数 $f\colon \mathbb{R}^n \to \mathbb{R} \cup \lbrace \pm\infty \rbrace$ のdomainは次のように定義されます。

$$
\mathrm{dom} ~ f = \lbrace x \in \mathbb{R}^n \mathrel{\mid} \lvert f(x) \rvert < \infty \rbrace.
$$

つまり、実数の範囲内に値を取る点の集合です ([effective domain](https://en.wikipedia.org/wiki/Effective_domain)として $-\infty$ の場合を含めることもあります)。本記事および教科書では $\mathrm{dom} ~ f \neq \emptyset$ を仮定します。

なお、真凸関数 (proper convex function)[^proper]は $\mathrm{dom} ~ f \neq \emptyset$ と $f(x) \neq -\infty$ が条件の為、代わりに真凸関数であることを仮定しても殆ど同じ議論になります。

そして、$f$ が凸関数であることは、$\mathrm{dom} ~ f$ が凸であり、かつ、任意の $x, y \in \mathrm{dom} ~ f$ と $\alpha \in [0, 1]$ に対して次が成立することと同値です（教科書 Definition 3.1.1）。

$$
f(\alpha x + (1 - \alpha) y) \leq \alpha f(x) + (1 - \alpha) f(y).
$$

### 連続

関数 $f$ が $\mathrm{dom} ~ f$ で連続であることは、任意の $\overline{x} \in \mathrm{dom} ~ f$ において $f$ が連続であることと同値です。

ある $\overline{x} \in \mathrm{dom} ~ f$ において $f$ が連続であることは、$\overline{x}$ に収束する任意の点列 $\lbrace x_k \rbrace \subseteq \mathrm{dom} ~ f$ に対し、$\lbrace f(x_k) \rbrace$ が $f(\overline{x})$ に収束すること、すなわち、

$$
\lim_{k \to \infty} x_k = \overline{x} \implies \lim_{k \to \infty} f(x_k) = f(\overline{x})
$$

が成立することと同値です[^continuous]。

## 凸関数が全域で定義されている場合

凸関数について、一般に次の主張が成り立つことが知られています[^Hiriart-Urruty]。

**凸関数は、$\mathrm{dom} ~ f$ の相対的内部で連続である。**

本記事の主題ではないので、詳細は[Appendix](#appendix-凸関数は相対定期内部で連続である)に譲りますが、簡単に言うと、縁(ふち)でない部分では凸関数は連続であるし、また縁の部分では不連続になり得るということです。

特に、$\mathrm{dom} ~ f$ が $\mathbb{R}^n$ 全体ならば、その相対的内部も $\mathbb{R}^n$ 全体なので、次の系が導かれます。

$\mathrm{dom} ~ f$ **が空間全域となる** （$\pm \infty$ に値を取らない） **凸関数は連続である。**

そして、この主張を言い換えると、次と等価です[^stackexchange]。

**凸関数** $f\colon \mathbb{R}^n \to \mathbb{R}$ **は連続である。**

値域が $\mathbb{R}$ であり、$\mathbb{R} \cup \lbrace \pm\infty \rbrace$ ではないことに注意して下さい。1次元だと $ax+b, x^2, \lvert x \rvert, e^x$ などの関数が該当します。ただし、$1/x$ や $-\log x$ すら、この「$\mathrm{dom} ~ f$ が空間全域となる」という条件を満たさないことに注意して下さい。

## 閉凸関数でない場合

前節では、全域で定義されている場合、つまり $\mathrm{dom} ~ f = \mathbb{R}^n$ である場合について考えました。以下では、$\mathrm{dom} ~ f \neq \mathbb{R}^n$ である場合について考えます。つまり、$\pm \infty$ に値を取ることがある場合です。ここで、凸関数の性質を議論する上で重要な性質である、閉凸(closed convex)について定義します。

### 閉凸の定義

まず、エピグラフを定義します。関数 $f\colon \mathbb{R}^n \to \mathbb{R}$ のエピグラフ(epigraph)は次のように定義されます。

$$
\mathrm{epi}\ f = \lbrace (x, t) \in \mathbb{R}^{n+1} \mathrel{\mid} x \in \mathrm{dom} ~ f, ~ f(x) \leq t \rbrace.
$$

![epi](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c551751d-3df4-46f9-1d15-4b67e2101075.png)

連続性を議論する上で重要な性質が閉凸です。関数 $f$ が閉凸であることは、エピグラフが閉集合であることと同値です（教科書 Definition 3.1.2）。

以下は閉凸な例です。右の例では、$\mathrm{dom} ~ f$ は $\lbrace x \in \mathbb{R} \mathrel{\mid} x > 0 \rbrace$ と開区間ですが、閉凸関数です。

| 閉凸 | 閉凸 |
| :---: | :---: |
| ![closed_interval_closed_convex](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/122d0d6e-fbaa-ba51-3ba0-e9379121f381.png) | ![closed_interval_inf.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/f8ec86df-b250-be82-319b-fd8a01bbf4dc.png)<br> |

また、以下は閉凸でない例です。

| 閉凸でない | 閉凸でない |
| :---: | :---: |
| ![open_interval](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/974d791b-2602-3bee-a2b1-680437cdea8a.png) | ![closed_interval](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/265dac7d-f42c-aee4-1313-4a5d4ca3b223.png) |

定義と見比べて下さい。

### 連続でない例

凸関数に閉凸という条件を課さない場合、不連続な例が容易に構築出来ます。以下がその一例です。

![closed_interval](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/265dac7d-f42c-aee4-1313-4a5d4ca3b223.png)

この関数が凸関数であることは、凸関数の定義

$$
f(\alpha x + (1 - \alpha) y) \leq \alpha f(x) + (1 - \alpha) f(y)
$$

において、$x$ または $y$ が区間の左端である時のみ非自明ですが、確かに定義を満たしています。よって、閉凸でないなら不連続な凸関数は確かに存在します。

余談として、以下の例は不連続ですが、そもそも非凸です。不連続点が $\mathrm{dom} ~ f$ の境界になければならないのは、凸性の担保の為と言えます。

![closed_interval_non_convex](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/dd1f9e47-2179-3637-6790-a2f0158b6667.png)

以上で、閉凸関数ではないという、ある種自明な例外を議論しました。

ここで、閉凸関数であるという条件を課した時、不連続な例が存在するのか否かは、かなり非自明な問いです。それが実は存在する、ということを次節で示します。

## 閉凸関数である場合

閉凸関数である場合について考えます。この場合、Appendixで示すように、[閉凸関数は下半連続である](#appendix-閉凸関数は下半連続である)ことは示されますが、連続であるとは限りません。具体的には、以下のことが成り立ちます。

* 2変数以上の場合、閉凸関数 $f$ は連続であるとは限らない。
* 1変数の場合、閉凸関数 $f$ は必ず連続である。

これらをそれぞれ証明します。

### 2変数以上の場合

2変数以上の場合、閉凸関数であっても連続であるとは限らないことを、反例で示します。簡単のため、2変数の場合のみ示しますが、多変数でも同様です。

$g\in \mathbb{R}$ と $\gamma \in \mathbb{R}$ に対して、

$$
\begin{align*}
\phi(y,g,\gamma) &\coloneqq gy - \frac{\gamma}{2}y^2, \\
\psi(g,\gamma) &\coloneqq \sup_{y \in \mathbb{R}} \phi(y,g,\gamma)
\end{align*}
$$

と定義します。$\psi(g,\gamma)$ の具体的な値は、$\frac{\partial}{\partial y}\phi = g-\gamma y$ であることから、以下のように求まります。

$$
\psi(g,\gamma) = \begin{cases}
0 & \mathrm{if}~g=\gamma=0,\\
\frac{g^2}{2\gamma} & \mathrm{if}~\gamma > 0,\\
\infty & \text{otherwise}.
\end{cases}
$$

$\psi$ が閉凸関数であることを証明します。凸性の証明は容易なので省略します。一般に、ある関数 $f$ が閉である、つまりエピグラフ $\lbrace (x,t) \mathrel{\mid} x \in \mathrm{dom} ~ f,~ f(x) \leq t \rbrace$ が閉集合であることは、任意の $c \in \mathbb{R}$ に対して、劣位集合(sublevel set) $\lbrace x \mathrel{\mid} x \in \mathrm{dom} ~ f,~f(x) \leq c \rbrace$ が閉集合であることと[同値](https://ja.wikipedia.org/wiki/%E9%96%89%E5%87%B8%E5%87%BD%E6%95%B0)です。十分性は自明で、必要性も点列を用いた議論などで示せます。ここで、$\psi(g,\gamma) \leq c$ を満たす $(g,\gamma)$ は $c$ の値で場合分けすると、それぞれ閉集合であることが分かります。よって、任意の劣位集合が閉集合であり、$\psi$ は閉、特に閉凸関数であることが示されます。

ここで、$\psi$ を図示すると、冒頭でも示した以下のグラフになります。

![psi](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/76f15f8d-0f1f-d743-16a6-6ff384cb13fc.png)

図では $\gamma$ の下限を少しずつ変えて示しています。このグラフは青点 $(g,\gamma)=(0,0)$ において $\psi(g,\gamma)=0$ ですが、$g \neq 0$ では $\gamma \to 0$ において $\psi(g,\gamma) \to \infty$ です。

ここで、赤の点列は、ある $\beta>0$ に対し、次を満たす点列です。

$$
\begin{cases}
\displaystyle \lim_{k \to \infty} (g_k,\gamma_k)= (0,0), \\
\displaystyle \lim_{k \to \infty} \psi(g_k,\gamma_k)= \beta.
\end{cases}
$$

$\gamma > 0$ において $\psi(\sqrt{\gamma}g,\gamma) = \frac{1}{2} \lVert g \rVert_2^2$ であることを用いると作れます。これは、

$$
\lim_{k \to \infty} \psi(g_k,\gamma_k) = \beta \neq 0 = \psi(0,0) = \psi(\lim_{k \to \infty} (g_k,\gamma_k))
$$

と、$\psi$ が不連続であることを示しています。よって、$\psi$ は閉凸関数であっても不連続だと分かります。

この小節のまとめとして、以下のことを強調しておきます。

**2変数以上の閉凸関数** $f$ **は** $\mathrm{dom} ~ f$ **で連続であるとは限らない。**

### 1変数の場合

1変数の場合、閉凸関数 $f$ は $\mathrm{dom} ~ f$ で連続であることを示します。上記の2変数の場合と、違いに注目して下さい。

具体的には、以下などが連続です。

![closed_interval_closed_convex](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/122d0d6e-fbaa-ba51-3ba0-e9379121f381.png)

系として開区間で定義された凸関数の連続性が従います。なお、この事実はかなり簡単に示せますが、そのような証明は別の記事[^easyProof]などを参照して下さい。

![open_interval](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/974d791b-2602-3bee-a2b1-680437cdea8a.png)

では、1変数の閉凸関数 $f$ が $\mathrm{dom} ~ f$ で連続であることを示します。

#### 「1変数の閉凸関数はdom fで連続である」の証明

任意の $\overline{x} \in \mathrm{dom} ~ f \subseteq \mathbb{R}$ に対して、$f$ が $\overline{x}$ で連続だと示します。

点列 $\lbrace x_k \rbrace \subseteq \mathrm{dom} ~ f$ が $\overline{x}$ に収束するとします。[Appendix](#appendix-閉凸関数は下半連続である)に示すように、$f$ は閉凸ならば下半連続です。つまり、以下は一般に成立します。

$$
\liminf_{k \to \infty} f(x_k) \geq f(\overline{x})
$$

この時、
$$
\limsup_{k \to \infty} f(x_k) \leq f(\overline{x})
$$
であることを示せば、上極限と下極限が一致する為、その極限は $f(\overline{x})$ に一致し、$f$ が $\overline{x}$ で連続であることが示されます[^supInf]。

重要な事として、1変数、つまり、数直線上の凸関数のdomainは、それが凸集合であるという性質上、一つの区間の形以外にありえません。また、$\mathrm{dom} ~ f \neq \emptyset$ であることを仮定しています。

つまり、$x_k \to \overline{x}$ より、$k$ が十分大きい任意の $x_k$ は、高々2つの固定された $\overline{y}_1, \overline{y}_2\in \mathrm{dom} ~ f$ を用いて、

$$
x_k \in \lbrace (1-\alpha_k) \overline{x} + \alpha_k \overline{y}_1, (1-\alpha_k) \overline{x} + \alpha_k \overline{y}_2 \rbrace \quad (\alpha_k \in [0, 1])
$$

と表せます。例えば以下の図では、赤点が $\lbrace x_k \rbrace$ を示しますが、十分 $\overline{x}$ に近い点は、そのように表せることが分かります。

![why_interval_1](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/9f6b27df-fcaf-4518-03ad-ad47c4ed8b39.png)

また、凸関数の定義より、

$$
\begin{cases}
f(x_k) \leq (1-\alpha_k) f(\overline{x}) + \alpha_k f(\overline{y}_1) \\
f(x_k) \leq (1-\alpha_k) f(\overline{x}) + \alpha_k f(\overline{y}_2)
\end{cases}
$$

のいずれかが成立します。ここで、$x_k \to \overline{x}$ より、$\alpha_k \to 0$ が導かれます。そして、上記不等式で $\alpha_k \to 0$ とすると、

$$
\limsup_{k \to \infty} f(x_k) \leq f(\overline{x})
$$

が導かれます。これは、$f$ が $\overline{x}$ で上半連続であることを示しています。よって、$f$ は $\overline{x}$ で連続であり、特に、$f$ は $\mathrm{dom} ~ f$ で連続です。

#### 2変数関数の場合、何故証明が回らないのか

先の証明が何故2変数以上の場合に回らないのか、という点について考察します。

関数 $\psi$ は、閉凸関数だが連続ではない2変数関数でした。

![psi3](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/f8b9da52-a639-1ccb-afe1-dc978a30ac8b.png)

そのdomainである $\mathrm{dom} ~ \psi =$ $(\mathbb{R} \times \lbrace \gamma > 0 \rbrace) \cup \lbrace (0,0) \rbrace$ および赤の点列を2次元平面上にプロットしたのが下図です。

![why_interval_2](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/9e681295-3cad-6e42-cbd9-21e8beafc543.png)

この点列では、先の証明で仮定した $\overline{y}_1,~\overline{y}_2$ に相当するものが無限個必要になってしまいます。これでは $x_k \to \overline{x}$ としても、$\alpha_k \to 0$ とは限らないため、先の証明が回りません。

ここに1変数の場合と2変数以上の場合の決定的な違いがあると考えています。

## まとめ

本記事では、凸関数の連続性について、以下のことを示しました。

![flowchart](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/4d167944-3e8d-2fe7-6e8a-c6807717102f.png)

理解の一助になれば幸いです。

以下、いくつかのAppendixを示します。

## Appendix 凸関数は相対定期内部で連続である

[凸関数が全域で定義されている場合](#凸関数が全域で定義されている場合)の節で、凸関数は相対的内部で連続であると述べました。ここでは、その証明を示します。

### 相対的内部の定義

まず、[アファイン包 (affine hull)](https://en.wikipedia.org/wiki/Affine_hull) を定義します。集合 $S$ のアファイン包は、$S$ の要素のすべてのアファイン結合の集合、つまり、

$$
\mathrm{aff} (S)=\left\{\sum_{i=1}^k \alpha_i x_i \mathrel{\mid} k>0, ~ x_i\in S, ~ \alpha_i \in \mathbb{R}, ~ \sum_{i=1}^k \alpha_i=1 \right\}.
$$

です。例えば、3次元空間において、同一直線状にない3点の集合 $S$ のアファイン包は、その3点を通る平面全体になります。

$S$ の凸包も似た定義ですが、$\alpha_i$ が非負であることが追加の条件として課され、$S$ の凸包はその3点を頂点とする三角形になります。

次に、[相対的内部 (relative interior)](https://en.wikipedia.org/wiki/Relative_interior) を定義します (Chapter A, Definition 2.1.1 [^Hiriart-Urruty])。相対的内部とは、内部の概念をアファイン包に対して定義したもの、つまり、

$$
\mathrm{ri} (S) = \left\{ x \in S \mathrel{\mid} \exists r > 0 ~ \text{s.t.} ~ B(x, r) \cap \mathrm{aff} (S) \subseteq S \right\}
$$

として定義されます。ただし、$B(x,r)$ で、$x$ を中心とする半径 $r$ の閉球を表すとします。

特に、空間を $\mathrm{aff} (S)$ に限定して考えると、$\mathrm{ri} (S)$ は単に $S$ の内部となります。

### 「凸関数は相対的内部で連続である」の証明

では、凸関数が相対的内部で連続であることを示します。大まかには文献[^Hiriart-Urruty]の内容に従います。

まず、補題(Chapter B, Theorem 3.1.2 [^Hiriart-Urruty])として、$x_0$ を $\mathrm{ri} (\mathrm{dom} ~ f)$ の任意の点とし、十分小さい $\delta$ に対し、

$$
m \leq f(x) \leq M \quad \forall x \in B(x_0, 2\delta) \cap \mathrm{aff} (\mathrm{dom} ~ f)
$$

を満たす定数 $m,M$ が存在することを示します。元証明はやや雑に議論しているので少し別の証明を与えます。$\mathrm{aff} (\mathrm{dom} ~ f)$ の次元を $k$ $(\leq n)$ としておきます。

まず、上界 $M$ の存在性を示します。簡潔さのため、$\mathrm{aff} (\mathrm{dom} ~ f)$ に議論を限定します (厳密には、各集合に ${} \cap \mathrm{aff} (\mathrm{dom} ~ f)$ を付ければよいです)。$x_0$ が相対的内点であることから、ある $\delta > 0$ が存在して、

$$
B(x_0, 2 \sqrt{k} \delta) \subseteq \mathrm{dom} ~ f
$$

と書けるので、$\mathrm{aff} (\mathrm{dom} ~ f)$ の適当な基底を用いて、$B(x_0, 2 \sqrt{k} \delta)$ の内部に超立方体 $C$ を入れることができます。特に、$C$ の内部にある $B(x_0, 2\delta)$ の任意の点は、$C$ の頂点の凸結合で表せます。また、$C$ の頂点集合を $\lbrace x_i \rbrace_{i=1}^{2^k}$ とします。

![ri_dom_f_continuous.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/1bea1c76-6b86-4903-a88b-2bb73d18ca23.png)

凸結合の係数 $\lbrace \alpha_i \rbrace_{i=1}^{2^k}$ $\left(\sum_{i=1}^{2^k} \alpha_i = 1, \ \alpha_i \geq 0\right)$ を用いて、任意の $x \in B(x_0, 2\delta)$ は、

$$
f(x) = f\left( \sum_{i=1}^{2^k} \alpha_i x_i \right) \leq \sum_{i=1}^{2^k} \alpha_i f(x_i) \leq \max_{i} f(x_i)
$$

と評価できます。よって、$M \coloneqq \max_{i} f(x_i)$ とすれば、$f(x) \leq M$ が成立します。

次に、下界 $m$ の存在性を示します (元証明を追ってもらえるとself-containedな議論になりますが、長くなりすぎるので[支持超平面定理](https://en.wikipedia.org/wiki/Supporting_hyperplane) (関連:[分離超平面定理](https://ja.wikipedia.org/wiki/%E5%88%86%E9%9B%A2%E8%B6%85%E5%B9%B3%E9%9D%A2%E5%AE%9A%E7%90%86))は既知とします)。

$f$ のエピグラフは定義より凸集合で、$(x_0,f(x_0))$ を通る超平面が存在します。また、$x_0$ が相対的内点であることから、その超平面は、$\mathrm{aff}(S)$ に対して垂直ではありません(簡潔に言えば、劣微分の傾きが無限ではないということです)。よって、ある $s \in \mathbb{R}^n$ が存在して、

$$
f(x) \geq f(x_0) + \langle s, x - x_0 \rangle, \quad (\forall x \in \mathrm{dom} ~ f)
$$

特に、コーシーシュワルツの不等式より、

$$
f(x) \geq f(x_0) - \lVert s \rVert \lVert x - x_0 \rVert \geq f(x_0) - 2\delta \lVert s \rVert \quad (\forall x \in B(x_0, 2\delta))
$$

となるので $m \coloneqq f(x_0) - 2\delta \lVert s \rVert$ とすれば、$f(x) \geq m$ が成立します。

よって、確かにリプシッツ連続性を保証する $\delta$ が存在することが分かりました。

---

続いて、一般の凸関数に対する次の主張を示します (Chapter B, Lemma 3.1.1 [^Hiriart-Urruty])。ある $x_0 \in \mathbb{R}^n$, $\delta>0$ および $m, M \in \mathbb{R}$ が存在して、

$$
m \leq f(x) \leq M \quad \forall x \in B(x_0, 2\delta)
$$

を満たすとします。このとき、$f$ は $B(x_0, \delta)$ で[リプシッツ連続](https://en.wikipedia.org/wiki/Lipschitz_continuity)である、つまり、ある $L > 0$ が存在して、

$$
\lvert f(y) - f(y') \rvert \leq L \lVert y - y' \rVert \quad (\forall y, y' \in B(x_0, \delta))
$$

となります。

証明をします。二つの相異なる $y, y'$ を $B(x_0, \delta)$ から取り、

$$
y'' \coloneqq y' + \delta \frac{y' - y}{\lVert y' - y \rVert} \in B(x_0, 2\delta)
$$

とおきます。すると、$y''$ は、$y'$ を中心として $y$ と反対側に $\delta$ だけ離れた点であることが、定義より分かります。よって、$y'$ は $y$ と $y''$ を結ぶ線分上、つまり、

$$
y' = \frac{\lVert y' - y \rVert}{\delta + \lVert y' - y \rVert} y'' + \frac{\delta}{\delta + \lVert y' - y \rVert} y
$$

となります。これに、凸関数の定義を適用すると、

$$
f(y') \leq \frac{\lVert y' - y \rVert}{\delta + \lVert y' - y \rVert} f(y'') + \frac{\delta}{\delta + \lVert y' - y \rVert} f(y)
$$

であるので、$m \leq f(x) \leq M$ を用いて、

$$
\begin{align*}
f(y') - f(y) &\leq \frac{\lVert y' - y \rVert}{\delta + \lVert y' - y \rVert} (f(y'') - f(y))\\
&\leq \frac{M - m}{\delta} \lVert y' - y \rVert
\end{align*}
$$

が成立します。$y$ と $y'$ を入れ替えても議論は同様に成立するので、先ほどの不等式の左辺に絶対値がつき、$f$ が $B(x_0, \delta)$ でリプシッツ連続であることが示されました。

---

最後に、$\mathrm{aff}(\mathrm{dom} ~ f)$ に議論を限定して、先ほどの補題を用いると、ある $L > 0$ が存在して、

$$
\lvert f(y) - f(y') \rvert \leq L \lVert y - y' \rVert
$$

となることが分かります。$y \to y'$ とすると、$\lvert f(y) - f(y') \rvert \to 0$ となり、直ちに連続性を導きます。よって、凸関数は、$\mathrm{dom} ~ f$ の相対的内部で連続であるという主張が示されました。

## Appendix 閉凸関数は下半連続である

続いて、閉凸関数は下半連続であるという主張を示します(教科書 Theorem 3.1.4.1)。閉凸関数は連続であるとは限らないですが、それを弱めた性質が下半連続性であり、それは成立するということです。

本節では、下半連続の定義を示し、その後に閉凸関数は下半連続であることを示します。

### 下半連続の定義

ある $\overline{x} \in \mathrm{dom} ~ f$ において $f$ が下半連続であることは、$\overline{x}$ に収束する任意の点列 $\lbrace x_k \rbrace \subseteq \mathrm{dom} ~ f$ に対し、

$$
\liminf_{k \to \infty} f(x_k) \geq f(\overline{x})
$$

が成立することと同値です。下図も参照して下さい。

<!-- ignore -->
![lower_semi_continuous](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/b11fe54c-a7ae-7843-df80-402b9d6cf6f5.png)

(Wikipedia「[半連続](https://ja.wikipedia.org/wiki/%E4%B8%8B%E5%8D%8A%E9%80%A3%E7%B6%9A)」より引用 / [Mktyscn](https://commons.wikimedia.org/wiki/File:Lower_semi.svg), Public domain, via Wikimedia Commons)

実際、$\psi$ の例でも $(\overline{g},\overline{\gamma})=(0,0)$ に収束する赤点で示した点列も、関数値 $\psi$ は $\beta>0$ に収束し、

$$
\liminf_{k \to \infty} \psi(g_k,\gamma_k) = \beta \geq \psi(0,0) = 0
$$

を満たしています。

![psi3](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/f8b9da52-a639-1ccb-afe1-dc978a30ac8b.png)

（なお、本記事では省略しますが真凸関数かつ閉凸関数であることの必要十分条件は、それが下半連続である[^closedConvex]ことです）

### 「閉凸関数は下半連続である」の証明

$f$ が閉凸関数は下半連続であることを示します。

$\overline{x}$ に収束する任意の点列 $\lbrace x_k \rbrace \subseteq \mathrm{dom} ~ f$ に対し、点列 $\lbrace (x_k, f(x_k)) \rbrace \subseteq \mathrm{epi}\ f$ を考えます。

$$
\overline{f} \coloneqq \liminf_{k \to \infty} f(x_k) \geq f(\overline{x})
$$

が言えれば良いです。

$\overline{f}$ の値に基づく場合分けを行います。なお、$\overline{f}$ は常に拡大実数 $\mathbb{R} \cup \lbrace \pm\infty \rbrace$ 内に存在します。$\liminf$ になじみがない方は、文献[^supInf]も参考にして下さい。

* $\overline{f} \in \mathbb{R}$ の場合

$\liminf$ の性質[^supInf]より、ある部分列 $\lbrace f(x_{k_j}) \rbrace$ が $\overline{f} \in \mathbb{R}$ に収束します。$\lbrace x_k \rbrace$ は $\overline{x}$ に収束する点列でした。なので、収束部分列の性質[^subArray]として、$x_{k_j}$ も $\overline{x}$ に収束します。以上より、$\lbrace (x_{k_j}, f(x_{k_j})) \rbrace$ は $(\overline{x}, \overline{f})$ に収束します。

ここで、閉凸関数の定義より $\mathrm{epi}\ f$ は閉集合である為、その内で定義される任意の点列は、極限を持つならばそれは $\mathrm{epi}\ f$ 内に存在します。

よって、点列 $\lbrace (x_{k_j}, f(x_{k_j})) \rbrace$ は $(\overline{x}, \overline{f})$ という極限を持つため、それは $\mathrm{epi}\ f$ 内に存在します。つまり、
$$
(\overline{x}, \overline{f}) \in \mathrm{epi}\ f
\iff
\overline{f} \geq f(\overline{x})
$$
が成り立ち、主張は成立します。

* $\overline{f} = -\infty$ の場合

条件より $\liminf_{k \to \infty} f(x_k) = -\infty$ です。$\overline{x} \in \mathrm{dom} ~ f$ なので $f(\overline{x})-1$ は固定された実数値です。よって、ある部分点列 $\lbrace x_{k_j} \rbrace$ が存在し、$f(x_{k_j}) \leq f(\overline{x})-1$ が成り立ちます。$\mathrm{epi}\ f$ の定義より $\lbrace (x_{k_j}, f(\overline{x})-1) \rbrace \subseteq \mathrm{epi}\ f$ で、収束先は $(\overline{x}, f(\overline{x})-1)$ です。

先程と同様に閉性よりこれは $(\overline{x}, f(\overline{x})-1) \in \mathrm{epi}\ f$ を導きます。

しかし、これは $f(\overline{x}) \leq f(\overline{x})-1 \iff 0 \leq -1$ を意味し矛盾です。なので、そもそもの仮定が誤りだと分かります。

* $\overline{f} = \infty$ の場合

この場合、$\overline{f} = \infty \geq f(\overline{x})$ は自明です。

以上より、場合分けは尽くされ、
$$
\overline{f} = \liminf_{k \to \infty} f(x_k) \geq f(\overline{x})
$$
が成り立ち、$f$ は $\overline{x}$ で下半連続です。

## 謝辞

本記事は所属研究室の輪読準備の一環として書かれました。
研究室の皆様に感謝致します。

[^Nesterov]: Nesterov, Yurii. [Lectures on convex optimization](https://link.springer.com/book/10.1007/978-3-319-91578-4). Vol. 137. Springer, 2018.

[^Hiriart-Urruty]: Hiriart-Urruty, J.-B., & Lemaréchal, C. (2001). Fundamentals of convex analysis. Springer. https://doi.org/10.1007/978-3-642-56468-0

[^continuous]: MATHPEDIA. [位相空間論5:連続写像](https://old.math.jp/wiki/%E4%BD%8D%E7%9B%B8%E7%A9%BA%E9%96%93%E8%AB%965%EF%BC%9A%E9%80%A3%E7%B6%9A%E5%86%99%E5%83%8F#.E5.91.BD.E9.A1.8C_5.18_.28.E7.82.B9.E5.88.97.E3.82.92.E7.94.A8.E3.81.84.E3.81.9F.E7.82.B9.E3.81.AB.E3.81.8A.E3.81.91.E3.82.8B.E9.80.A3.E7.B6.9A.E6.80.A7.E3.81.AE.E7.89.B9.E5.BE.B4.E3.81.A5.E3.81.91.29) (命題 5.18). 2021.

[^stackexchange]: Misha Lavrov. [Is a convex function always continuous?](https://math.stackexchange.com/questions/2961783/is-a-convex-function-always-continuous). Stack Exchange, 2018.

[^easyProof]: 数学の景色. [凸関数と凸不等式(イェンセンの不等式)についてかなり詳しく](https://mathlandscape.com/convex-func/#toc7). 2023.

[^supInf]: 数学の景色. [上極限,下極限(limsup,liminf)の定義と例と性質2つ](https://mathlandscape.com/limsup-liminf/#toc6). 2022.

[^proper]: Wikipedia. [真凸関数](https://ja.wikipedia.org/wiki/%E7%9C%9F%E5%87%B8%E5%87%BD%E6%95%B0). 2022.

[^closedConvex]: Wikipedia. [閉凸函数](https://ja.wikipedia.org/wiki/%E9%96%89%E5%87%B8%E5%87%BD%E6%95%B0). 2016.

[^subArray]: 野村数学研究所. [点列の収束と任意の部分列の収束](https://www.nomuramath.com/lroj6ogu/).
