# ユークリッド射影の一意性と凸性の同値性に関する証明

本記事ではユークリッド射影の一意性と凸性の同値性に関する証明を行います。

https://www.math.auckland.ac.nz/~moors/chebyshevsurveyJAMS.pdf

## 概要

本記事が証明するのは、以下の定理です。

**集合 $K$ が $\mathbb{R}^m$ の非空な閉集合であるとき、$K$ が凸集合であることと、$\mathbb{R}^m$ の任意の点に対して $K$ の最近点が一意に定まることは同値である。**

この結果は、近年のサーベイ論文 [^Kuznetsov] や、Frederick A. Valentine による "Convex sets" [^Valentine] において、Motzkinの定理 (Motzkin's theorem)と呼ばれています。1935年に T. Motzkin が発表した論文がこの結果に対する最初の証明であるようです。(先述のサーベイ論文内での参考文献と、Valentineによる本とでの参考文献に齟齬があり、両方とも原本を確認できなかったため、その原論文はあえて参考文献欄に載せていません。) 本記事では、Valentineの本に記載された証明を紹介します。

[Theodore Motzkin](https://en.wikipedia.org/wiki/Theodore_Motzkin)はイスラエル系アメリカ人の数学者で、[Motzkin number](https://en.wikipedia.org/wiki/Motzkin_number)などに名を残した人物であり、[Motzkin–Taussky theorem](https://en.wikipedia.org/wiki/Motzkin%E2%80%93Taussky_theorem)という線形代数の定理でも有名のようですが、本記事で扱う定理の内容はそれとは異なることに注意して下さい。

ここで、ユークリッド空間上において、ユークリッド射影 (Euclidean projection) は一般に次のように定義されます:

$$
\operatorname{Proj}_K(x) = \underset{y \in K}{\operatorname{argmin}} \|x-y\|.
$$

これは、点 $x$ から集合 $K$ への最近点集合に対する写像に他なりません。Motzkinの定理は、$K$ が凸集合であることと、ユークリッド射影 $\operatorname{Proj}_K(x)$ の一意性に関する同値性を主張しています。特に、$K$ が閉凸集合ならば、ユークリッド射影が一意であるという事実は、最適化アルゴリズムの一つである射影勾配法 (projected gradient method) に関する解析などで重要な役割を果たします。射影勾配法に関する解説としては、例えば以下の記事が参考になり、鏡像降下法 (mirror descent) についても触れられています。

https://vene.ro/blog/mirror-descent.html

なお、余談として、Motzkinの定理の証明には、本記事で紹介する証明以外にも不動点定理を用いるものもあるようです。本記事では省略します。

https://math.stackexchange.com/questions/274810/is-a-closed-set-with-the-unique-nearest-point-property-convex

それでは、以下でMotzkinの定理の証明を行っていきます。


## 参考文献

[^Kuznetsov]: Kuznetsov, N. (2024). On analytic characterization of convex sets in $\mathbb{R}^m$ (a survey). arXiv [Math.AP]. http://arxiv.org/abs/2405.18013

[^Valentine]: Valentine, F. A. (1964). Convex sets. McGraw-Hill series in higher mathematics. McGraw-Hill Book Company.
