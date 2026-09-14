# 最適化関連の個人的用語集

この記事は、最適化関連の用語のうち、個人的に気になったものをまとめたものです。

私が飽きるまでは更新される可能性があります。

## 目次

<!-- INDEX -->

- [最適化関連の個人的用語集](#最適化関連の個人的用語集)
  - [目次](#目次)
  - [引用について](#引用について)
  - [用語集](#用語集)
    - [(L0, L1) Smoothness](#l0-l1-smoothness)
    - [Additive Smoothing](#additive-smoothing)
    - [Alexandrov Theorem](#alexandrov-theorem)
    - [Antithetic variates](#antithetic-variates)
    - [Asplund Space](#asplund-space)
    - [Augmented Lagrangian Method](#augmented-lagrangian-method)
    - [Basic Linear Algebra Subprograms](#basic-linear-algebra-subprograms)
    - [Bayesian Network](#bayesian-network)
    - [Carathéodory's Extension Theorem](#carathéodorys-extension-theorem)
    - [Carathéodory's Theorem (Convex Hull)](#carathéodorys-theorem-convex-hull)
    - [Cheeger Constant](#cheeger-constant)
    - [Copositive Matrix](#copositive-matrix)
    - [Cosmic Closure](#cosmic-closure)
    - [Danskin's Theorem](#danskins-theorem)
    - [Dini Derivative](#dini-derivative)
    - [Eckart–Young–Mirsky Theorem](#eckartyoungmirsky-theorem)
    - [Epi-Convergence](#epi-convergence)
    - [Fixed Point](#fixed-point)
    - [Fredholm Alternative](#fredholm-alternative)
    - [Fully Composite](#fully-composite)
    - [Generalized Cauchy Point](#generalized-cauchy-point)
    - [Generalized Moment Problem](#generalized-moment-problem)
    - [Graphical Lasso](#graphical-lasso)
    - [Growth Condition](#growth-condition)
    - [Hadamard Manifold](#hadamard-manifold)
    - [Hausdroff Distance](#hausdroff-distance)
    - [Heavy-Ball Method](#heavy-ball-method)
    - [Hoffman–Pereira Matrix](#hoffmanpereira-matrix)
    - [Hopf–Rinow Theorem](#hopfrinow-theorem)
    - [Inner And Outer Semicontinuity](#inner-and-outer-semicontinuity)
    - [InverseProblem](#inverseproblem)
    - [Invex Function](#invex-function)
    - [Itoh–Abe Method](#itohabe-method)
    - [John Ellipsoid](#john-ellipsoid)
    - [KL property](#kl-property)
    - [Linear Minimization Oracle](#linear-minimization-oracle)
    - [Locus](#locus)
    - [Maximum Theorem](#maximum-theorem)
    - [Minimax Theorem](#minimax-theorem)
    - [Minkowski–Weyl Theorem](#minkowskiweyl-theorem)
    - [Motzkin's Transposition Theorem](#motzkins-transposition-theorem)
    - [Motzkin–Straus Formulation](#motzkinstraus-formulation)
    - [Moving Balls Approximation](#moving-balls-approximation)
    - [Newton–Schulz](#newtonschulz)
    - [Neyman–Pearson Classification](#neymanpearson-classification)
    - [Ordinal Regression](#ordinal-regression)
    - [Polyak inequality](#polyak-inequality)
    - [Prioritized Constraints](#prioritized-constraints)
    - [Quasiconvex](#quasiconvex)
    - [Radon's Theorem](#radons-theorem)
    - [Radon–Nikodym Derivative](#radonnikodym-derivative)
    - [ResNet](#resnet)
    - [Satisfiability Modulo Theories](#satisfiability-modulo-theories)
    - [Set-Valued Function](#set-valued-function)
    - [Sturm's Theorem](#sturms-theorem)
    - [Ursescu Theorem](#ursescu-theorem)
    - [Wasserstein DRO](#wasserstein-dro)
    - [Łojasiewicz inequality](#łojasiewicz-inequality)
  - [最後に](#最後に)

## 引用について

この記事では、自分の知らない用語をまとめるという性質上、非常に多数の引用・スクショが登場します。非営利目的ではあるものの、著作権の侵害にあたる行為をすることは私の本意ではありませんので、その運用ルールを示しておきます。

まず、Wikipediaに関しては、文章は[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)のライセンスで公開されているため、引用元を明示することで引用可能です。また、各画像についても、それぞれのライセンスを確認したうえで、適切な引用を行っています。

一方で、arXivの論文やジャーナルの論文などは、一般には転載を禁じていることが多いです。属地主義の原則に基づき、日本の著作権法において引用として認められる範囲の利用かどうかが適法性の焦点になると理解しています([出典1](https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/chosakukensha_fumei/index.html) [出典2](https://utelecon.adm.u-tokyo.ac.jp/articles/copyright/basic/) [出典3](https://www.bunka.go.jp/seisaku/chosakuken/seidokaisetsu/seminar/2024/pdf/94088901_01.pdf))。

特に、今回の場合、唯一怪しい点としては、引用と私のコメントにいわゆる主従関係があるかどうかという点です。この点に関しては、最低限の引用で済ませたり、自分の言葉による解説を多く入れたり、実験などを手元で再現して画像を載せたり、その他の情報を追加したりすることで、引用の範囲を超えないように注意しています。

## 用語集

<!-- WORDS -->

### (L0, L1) Smoothness

文献:

https://www.researchgate.net/profile/Mohammad-Alkousa-2/publication/413568957_First-Order_Methods_for_Optimization_Problems_with_Generalized_Smoothness_and_Generalized_Inexact_Oracle/links/6a8c89c7db725f1be9602a92/First-Order-Methods-for-Optimization-Problems-with-Generalized-Smoothness-and-Generalized-Inexact-Oracle.pdf

(これの[11]が以下の論文)
<br>

https://arxiv.org/abs/1905.11881

<!-- ![L0L1Smoothness_WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/L0L1Smoothness/WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING.png) -->

> Definition 1. A second order differentiable function $f$ is $(L_0,L_1)$-smooth if $\|\nabla^2 f(x)\| \le L_0 + L_1 \|\nabla f(x)\|$.

![L0L1Smoothness_WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING-Fig1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/L0L1Smoothness/WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING-Fig1.png)

解説:

$L$-Smoothnessの一般化。

上記のFig.1にあるように、いくつかの問題設定において、勾配ノルムとSmoothnessに相関があることを契機として導入されたようである。

確かに、$L$-Smoothnessの仮定は現実的な問題と不整合だとはよく感じるので、非常に妥当で面白い。

### Additive Smoothing

文献:

https://en.wikipedia.org/wiki/Additive_smoothing

![AdditiveSmoothing_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AdditiveSmoothing/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Additive_smoothing>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

Additive SmoothingはLaplace Smoothingとも呼ばれている。少しだけ値を足してから頻度を求める。
なお、[Laplacian Smoothing](https://en.wikipedia.org/wiki/Laplacian_smoothing) もあるが、そちらはグラフ理論関連の話。

### Alexandrov Theorem

文献:

https://en.wikipedia.org/wiki/Alexandrov_theorem

![AlexandrovTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AlexandrovTheorem/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Alexandrov_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

凸関数が2階微分を殆ど至る点で持つことを大まかには述べている。

なお、Rademacher's Theoremは、リプシッツ連続関数が1階微分を殆ど至る点で持つことを大まかには述べている。

詳細はRademacher's Theoremにて。

### Antithetic variates

文献:

https://en.wikipedia.org/wiki/Antithetic_variates

![AntitheticVariates_Wiki-Underlying-principle](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AntitheticVariates/Wiki-Underlying-principle.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Antithetic_variates>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![AntitheticVariates_Wiki-Example2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AntitheticVariates/Wiki-Example2.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Antithetic_variates>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

[負相関変量法・対称変量法](https://triadsou.hatenablog.com/entry/20100819/1282192611)とも呼ばれている。
モンテカルロ推定量の不偏性を保ちながら分散を小さくする。

### Asplund Space

文献:

https://arxiv.org/abs/2608.26328

https://en.wikipedia.org/wiki/Asplund_space

![Asplund_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Asplund/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Asplund_space>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

めちゃくちゃ大雑把に言えば、連続凸関数のフレシェ微分可能性について一定の保証を与えるBanach空間。

### Augmented Lagrangian Method

文献:

https://en.wikipedia.org/wiki/Augmented_Lagrangian_method

![AugmentedLagrangianMethod_Wiki-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AugmentedLagrangianMethod/Wiki-1.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Augmented_Lagrangian_method>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![AugmentedLagrangianMethod_Wiki-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AugmentedLagrangianMethod/Wiki-2.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Augmented_Lagrangian_method>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

日本語では拡張ラグランジュ関数法とも。ADMMはこの亜種。

### Basic Linear Algebra Subprograms

文献:

https://ja.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms

![BasicLinearAlgebraSubprograms_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/BasicLinearAlgebraSubprograms/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

BLASという略語の方が有名。あくまでAPIであって、実装までを定めたものではないことに注意が必要。OpenBLASが具体的な実装例。

### Bayesian Network

文献:

https://ja.wikipedia.org/wiki/%E3%83%99%E3%82%A4%E3%82%B8%E3%82%A2%E3%83%B3%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF

![BayesianNetwork_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/BayesianNetwork/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%83%99%E3%82%A4%E3%82%B8%E3%82%A2%E3%83%B3%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

[Graphical Model](https://en.wikipedia.org/wiki/Graphical_model)の特殊ケースとしてBayesian Networkが存在する。

### Carathéodory's Extension Theorem

文献:

https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%86%E3%82%AA%E3%83%89%E3%83%AA%E3%81%AE%E6%8B%A1%E5%BC%B5%E5%AE%9A%E7%90%86

![Caratheodory'sExtensionTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Caratheodory%27sExtensionTheorem/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%86%E3%82%AA%E3%83%89%E3%83%AA%E3%81%AE%E6%8B%A1%E5%BC%B5%E5%AE%9A%E7%90%86>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

最適化との馴染みはやや薄いが、Carathéodory と名のつく定理は複数存在するので、対比の為に記しておく。
混同に注意。

### Carathéodory's Theorem (Convex Hull)

文献:

https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%86%E3%82%AA%E3%83%89%E3%83%AA%E3%81%AE%E5%AE%9A%E7%90%86_(%E5%87%B8%E5%8C%85)#/languages

![Caratheodory'sTheorem(ConvexHull)_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Caratheodory%27sTheorem%28ConvexHull%29/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%86%E3%82%AA%E3%83%89%E3%83%AA%E3%81%AE%E5%AE%9A%E7%90%86_(%E5%87%B8%E5%8C%85)#/languages>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Caratheodorys theorem example.svg](<https://commons.wikimedia.org/wiki/File:Caratheodorys_theorem_example.svg>) / Tom Murphy VII（SVG、DysprosiaのPNGを基に作成） / [BSD 3-Clause License](<https://opensource.org/license/bsd-3-clause>)。

<details><summary>Caratheodorys theorem example.svg のライセンス告知全文</summary>

```text
Copyright © Dysprosia

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

</details>

解説:

証明は[高校数学の美しい物語](https://manabitimes.jp/math/1216)さんに詳しい。

[凸解析―理論と応用](https://www.maruzen-publishing.co.jp/book/b10123316.html)という本の8ページにも記載がある。

ちなみに Carathéodory's Extension Theorem の[Carathéodory](https://en.wikipedia.org/wiki/Constantin_Carath%C3%A9odory)さんと同一人物。

### Cheeger Constant

文献:

https://arxiv.org/pdf/2609.00337

(Blaschke–Santaló diagramというものの文脈で登場している)
<br>

https://en.wikipedia.org/wiki/Cheeger_constant_(graph_theory)

![CheegerConstant_Wiki-graph](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/CheegerConstant/Wiki-graph.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Cheeger_constant_(graph_theory)>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Cheeger constant.svg](<https://commons.wikimedia.org/wiki/File:Cheeger_constant.svg>) / BagLuke / [CC0 1.0](<https://creativecommons.org/publicdomain/zero/1.0/>)。

https://en.wikipedia.org/wiki/Cheeger_constant

![CheegerConstant_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/CheegerConstant/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Cheeger_constant>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

チーガー定数と読むらしい。
グラフの方が解釈が簡単だが、カットの概念に近い。
固有値評価などに応用があるらしいが、あまり理解せず。

### Copositive Matrix

文献:

https://en.wikipedia.org/wiki/Copositive_matrix

![CopositiveMatrix_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/CopositiveMatrix/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Copositive_matrix>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

半正定値の概念を $x \geq 0$ だけの場合に緩和したもの。

### Cosmic Closure

文献:

https://link.springer.com/chapter/10.1007/978-3-642-02431-3_3

(p.77近辺)

<!-- ![CosmicClosure_Variational-Analysis-Cones-and-Cosmic-Closure-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/CosmicClosure/Variational-Analysis-Cones-and-Cosmic-Closure-1.png)
![CosmicClosure_Variational-Analysis-Cones-and-Cosmic-Closure-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/CosmicClosure/Variational-Analysis-Cones-and-Cosmic-Closure-2.png)
![CosmicClosure_Variational-Analysis-Cones-and-Cosmic-Closure-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/CosmicClosure/Variational-Analysis-Cones-and-Cosmic-Closure-3.png) -->

解説:

大雑把には、$\mathbb{R}^n$ に「無限遠の方向」を点として付け加えてコンパクト化したものと言える。

直訳すると、宇宙の閉包だろうか、意図自体は3次元についての説明である、

> For $n=3$, this brings to the picture of the universe as bounded by a `celestial sphere'.

(上記の本、Variational Analysis より引用、celestial sphere は天球のこと)

より汲み取れる。命名がやたら格好良い。

### Danskin's Theorem

文献:

https://en.wikipedia.org/wiki/Danskin%27s_theorem

![Danskin'sTheorem_Wiki-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Danskin%27sTheorem/Wiki-1.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Danskin%27s_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![Danskin'sTheorem_Wiki-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Danskin%27sTheorem/Wiki-2.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Danskin%27s_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![Danskin'sTheorem_Wiki-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Danskin%27sTheorem/Wiki-3.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Danskin%27s_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![Danskin'sTheorem_Wiki-4](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Danskin%27sTheorem/Wiki-4.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Danskin%27s_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

minimax問題などにおける関数の勾配や劣勾配の計算に使われる定理。
見れば分かる通り、もし最適解が一意でかつ(ラフな意味で)病的でなければ、これはかなり自明。
本当に大切なのは、むしろ最適解が複数ある場合や、滑らかでない場合だろう。

### Dini Derivative

文献:

https://en.wikipedia.org/wiki/Dini_derivative

![DiniDerivative_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/DiniDerivative/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Dini_derivative>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

単純な片側極限と比較すると分かりやすい。

$$
\begin{align*}
f'_+(x) &= \lim_{h\downarrow 0} \frac{f(x+h)-f(x)}{h},\\
\overline D_+ f(x) &= \limsup_{h\downarrow 0} \frac{f(x+h)-f(x)}{h},\\
\underline D_+ f(x) &= \liminf_{h\downarrow 0} \frac{f(x+h)-f(x)}{h}.
\end{align*}
$$

例えば、

$$
f(x)=
\begin{cases}
x\sin(1/x), & x\neq 0,\\
0, & x=0.
\end{cases}
$$

を考えると、

$$
\begin{align*}
f'_+(0) &= \text{does not exist},\\
\overline D_+ f(0) &= +1,\\
\underline D_+ f(0) &= -1.
\end{align*}
$$

となる。

![DiniDerivative_xsin1x](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/DiniDerivative/xsin1x.png)

0に近づくにつれて通常の導関数が正負の無限大へ向かって振動することも踏まえると、中々に便利な概念で感心する。

### Eckart–Young–Mirsky Theorem

文献:

https://en.wikipedia.org/wiki/Low-rank_approximation

![EckartYoungMirskyTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/EckartYoungMirskyTheorem/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Low-rank_approximation>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

行列の低ランク近似をフロベニウスノルムによって定式化した際、その最適解は特異値分解によって得られることを示す定理。

定理自体は有名だが、このような名前がついていることは知名度が低いかも知れない。

お三方とも1900年代の数学者らしい。

### Epi-Convergence

文献:

https://en.wikipedia.org/wiki/Epi-convergence

![EpiConvergence_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/EpiConvergence/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Epi-convergence>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![EpiConvergence_Wiki-Relation-to-minimization-problems](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/EpiConvergence/Wiki-Relation-to-minimization-problems.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Epi-convergence>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

具体例があまりネットになかったので、以下に簡単な例を示す。

左は点ごとには収束しないにもかかわらずEpi-Convergenceが起きる例、右は極限で最小点集合が拡大し $\lim \operatorname{argmin} f_n \subsetneq \operatorname{argmin} f$ となる例を示す。

![EpiConvergence_epi_convergence_examples](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/EpiConvergence/epi_convergence_examples.png)

似た概念に[Gamma-Convergence](https://en.wikipedia.org/wiki/%CE%93-convergence)というのもあるらしい。

### Fixed Point

文献:

https://iiduka.net/intro/researches/fixedpoint

(飯塚先生のHP)

<!-- ![FixedPoint_iiduka](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FixedPoint/iiduka.png) -->

https://www.ohmsha.co.jp/book/9784274230066.html

(飯塚先生の著書、7章が不動点近似法で詳しい)

https://www.ism.ac.jp/~mirai/sscoke/2021/

(飯塚先生の講義資料)

解説:

上記の「連続最適化アルゴリズム」という書籍の第7章で扱われている、$T \colon C\to C$ の不動点 $x^\ast=T(x^\ast)$ を求める問題に対する、3つの代表的反復法は以下の通りである。

| 手法                             | 更新式                                 |
| :------------------------------: | :------------------------------------: |
| Banach の不動点近似法            | $x_{k+1}=T(x_k)$                       |
| Krasnosel'skiĭ–Mann 不動点近似法 | $x_{k+1}=x_k+\alpha_k (T(x_k)-x_k)$    |
| Halpern 不動点近似法             | $x_{k+1}=T(x_k)+\alpha_k (x_0-T(x_k))$ |

例として $n=2$ かつ $T$ を30度回転とした場合の、各反復法の挙動を比較する。([実装](https://github.com/HirokiHamaguchi/QiitaArticles/tree/main/20260827_OptimizationWords/FixedPoint/rotation.py))

![FixedPoint_rotation](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FixedPoint/rotation.png)

### Fredholm Alternative

文献:

https://en.wikipedia.org/wiki/Fredholm_alternative

![FredholmAlternative_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FredholmAlternative/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Fredholm_alternative>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

https://www.ism.ac.jp/~mirai/sscoke/2026/

(松井先生の講義資料, 10ページ辺り)

<!-- ![FredholmAlternative_sscoke2026-tomomi-matsui](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FredholmAlternative/sscoke2026-tomomi-matsui.png) -->

解説:

任意の行列 $(A | b)$ に対し、$P: Ax = b$ か $D: y^\top A = 0^\top, y^\top b \neq 0$ のどちらか丁度1つのみが解を持つという定理。証明は簡単で、両方の解を $x^\ast, y^\ast$ として存在を仮定すると、次のように矛盾が導かれる。

$$
0 = 0^\top x^\ast = (y^\ast)^\top A x^\ast = (y^\ast)^\top b \neq 0
$$

これはつまり、$b \in \mathrm{Im}(A)$ と $b \in \mathrm{Ker}(A^\top)^\perp$ が同値ということを言っているに過ぎない。

[Farkas' lemmaのcorollary](https://en.wikipedia.org/wiki/Farkas%27_lemma)として得られる。

### Fully Composite

文献:

https://epubs.siam.org/doi/abs/10.1137/21M1410063

Doikov, N., & Nesterov, Y. (2022). High-order optimization methods for fully composite problems. SIAM Journal on Optimization, 32(3), 2402-2427.

(この論文はOpen Access、[CC BY 4.0](http://creativecommons.org/licenses/by/4.0/))

![FullyComposite_High-Order-Optimization-Methods-for-Fully-Composite-Problems](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FullyComposite/High-Order-Optimization-Methods-for-Fully-Composite-Problems.png)

解説:

例としては、

- Optimization with functional constraints,
- Additive composite minimization,
- Functional composite minimization,
- Functional and additive composition,
- Composition with linear mapping

などとなっていく。

この統一性・抽象性が大事に思われる。

### Generalized Cauchy Point

文献:

https://doi.org/10.1007/978-0-387-40065-5

Wright, Stephen J., and Jorge Nocedal. "Numerical optimization." における説明はAlgorithm 4.4に該当。

<!-- ![GeneralizedCauchyPoint_Numerical-Optimization](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/Numerical-Optimization.png) -->

https://doi.org/10.1137/0916069

Richard H. Byrd, Peihuang Lu, Jorge Nocedal, and Ciyou Zhu. "A Limited Memory Algorithm for Bound Constrained Optimization." における説明は主にSection 2に該当。

<!-- ![GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-1.png)

![GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-2.png)

![GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-3.png) -->

解説:

正式な用語と言えるかどうかやや怪しく、注意が必要。

まず、Wright, Stephen J., and Jorge Nocedal. "Numerical optimization." の方で触れられているのは、信頼領域法の文脈においてであり、定義もやや曖昧である。

[これ](https://math.stackexchange.com/questions/2432486/generalized-cauchy-point-calculation)などが参考になるかも知れない。

Richard H. Byrd, Peihuang Lu, Jorge Nocedal, and Ciyou Zhu. "A Limited Memory Algorithm for Bound Constrained Optimization." の方では、少なくとも私の理解する限りにおいて異なる定義がされているように思われる。

こちらはSciPyのL-BFGS-B法の実装において重要な概念であり、実際に[コメント](https://github.com/scipy/scipy/blob/cacd2b498be80256532b8751f74a1bdba0c7880d/scipy/optimize/src/lbfgsb.c#L614)で参照されている。

このGCPはかなり偉い。
Box制約、つまり変数 $x$ の第 $i$ 成分が $l_i \leq x_i \leq u_i$ という制約が複数ある状況を考える。
制約なしで求まった準ニュートン方向に対し、それがBox外に出てしまうとしよう。
この時、純粋にはBoxに対する射影を考えて、それを次の反復点とするのが自然な考え方である。
しかし、この点は実は最適ではない。適切に2次元上で図を描くと簡単な反例があることはすぐ分かる。
GCPでは、Box制約に沿って折れ曲がりながら伸びていく領域において、陽に構築された目的関数の2次近似の最小値を求めるとしている。
これは私も実験したが、単純な射影よりも優れた反復点を返すので、全体の計算時間で見てもかなり速い。
また、その為のアルゴリズムとしてL-BFGSの低ランク性を活用しており、そこも偉いポイントである。
やや複雑なのが難点。

### Generalized Moment Problem

文献:

https://arxiv.org/abs/2608.24184

(この文献の[9]が下にあたる)
<br>

https://books.google.co.jp/books?id=lFi7CgAAQBAJ

![GeneralizedMomentProblem_Moments,-Positive-Polynomials-and-Their-Applications](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedMomentProblem/Moments%2C-Positive-Polynomials-and-Their-Applications.png)

解説:

未知の測度を変数とし、その[モーメント](https://ja.wikipedia.org/wiki/%E3%83%A2%E3%83%BC%E3%83%A1%E3%83%B3%E3%83%88_(%E6%95%B0%E5%AD%A6))に関する線形制約の下で測度の線形汎関数を最適化する無限次元線形計画問題である。
データが多項式の場合は[the moment Sum-of-squares (SOS) hierarchy](https://arxiv.org/abs/2608.24184)による半正定値計画緩和で近似できる。

### Graphical Lasso

文献:

https://en.wikipedia.org/wiki/Graphical_lasso

![GraphicalLasso_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GraphicalLasso/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Graphical_lasso>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![GraphicalLasso_Wiki-multivariate-normal-distribution](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GraphicalLasso/Wiki-multivariate-normal-distribution.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Graphical_lasso>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Multivariate Gaussian.png](<https://commons.wikimedia.org/wiki/File:Multivariate_Gaussian.png>) / Piotrg~commonswiki / [CC BY-SA 3.0](<https://creativecommons.org/licenses/by-sa/3.0/>)。

解説:

Graphical Lassoという名前であるが、そのグラフ要素は手法自体には出てこない。本質的にやっていることは多変量正規分布の逆共分散行列(精度行列、precision matrixとも)に関する、$L_1$ 正則化付きの推定に過ぎない。この手法の導出は、確率密度関数よりほぼ自明である。

$L_1$ 正則化をつけているから、逆行列に疎行列が出てきて、それがグラフにみなせて、解釈が楽になる、という話と理解している。

### Growth Condition

文献:

https://pubsonline.informs.org/doi/abs/10.1287/moor.2017.0889

![GrowthCondition_Error-Bounds,-Quadratic-Growth,-and-Linear-Convergence-of-Proximal-Methods](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GrowthCondition/Error-Bounds%2C-Quadratic-Growth%2C-and-Linear-Convergence-of-Proximal-Methods.png)

https://arxiv.org/pdf/2608.20642

([12]が上の文献にあたる)

![GrowthCondition_Strong-growth-and-Goldstein-subgradients-in-piecewise-smooth-optimization](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GrowthCondition/Strong-growth-and-Goldstein-subgradients-in-piecewise-smooth-optimization.png)

解説:

最適値からの目的関数値の差が解集合までの距離に応じてどれだけ増えるかを下から評価する正則性条件。
近接勾配法などの線形収束を導くために用いられる。

### Hadamard Manifold

文献:

https://en.wikipedia.org/wiki/Hadamard_manifold

![HadamardManifold_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HadamardManifold/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Hadamard_manifold>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

https://arxiv.org/pdf/2609.00540

(Hadamard Manifolds上の射影勾配法が調べられている)

解説:

書いてある通りだが、断面曲率がどこでも0以下な、完備で単連結なリーマン多様体。
双曲空間をイメージしておけば概ね良さそう。

### Hausdroff Distance

文献:

https://en.wikipedia.org/wiki/Hausdorff_distance

![HausdroffDistance_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HausdroffDistance/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Hausdorff_distance>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Hausdorff distance sample.svg](<https://commons.wikimedia.org/wiki/File:Hausdorff_distance_sample.svg>) / Rocchini / [CC BY 3.0](<https://creativecommons.org/licenses/by/3.0/>)。

解説:

Pompeiu–Hausdorff distanceとも。簡単に言えば集合同士の一番遠い点の距離を測っている。

Wikiの定義において、$X$ を地球の表面、$Y$ を陸の表面とすると、[point Nemo](https://ja.wikipedia.org/wiki/%E3%83%9D%E3%82%A4%E3%83%B3%E3%83%88%E3%83%BB%E3%83%8D%E3%83%A2)、つまり、陸から最も遠い地点の、陸からの距離は、正にHausdorff distanceで表される、ということが[Wiki](https://en.wikipedia.org/wiki/Hausdorff_distance#Applications)にも書いてある。

### Heavy-Ball Method

文献:

https://www.sciencedirect.com/science/article/pii/0041555364901375

(提案論文)
<br>

https://ieeexplore.ieee.org/document/7330562

![HeavyBallMethod_Global-convergence-of-the-Heavy-ball-method-for-convex-optimization-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HeavyBallMethod/Global-convergence-of-the-Heavy-ball-method-for-convex-optimization-1.png)

![HeavyBallMethod_Global-convergence-of-the-Heavy-ball-method-for-convex-optimization-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HeavyBallMethod/Global-convergence-of-the-Heavy-ball-method-for-convex-optimization-2.png)

解説:

Nesterovの加速勾配法との違いに注意。
計算量の比較などをしようとすると、流石に長くなりすぎるのでここでは省略するが、いつか書きたい。

### Hoffman–Pereira Matrix

文献:

https://arxiv.org/abs/2609.01010

(この論文に登場していた)
<br>

https://www.sciencedirect.com/science/article/pii/009731657390006X

(1973年の初出論文)

![HoffmanPereiraMatrix_On-copositive-matrices-with-−1,-0,-1-entries](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HoffmanPereiraMatrix/On-copositive-matrices-with-%E2%88%921%2C-0%2C-1-entries.png)

https://www.sciencedirect.com/science/article/pii/S0024379520304171

<!-- ![HoffmanPereiraMatrix_Testing-copositivity-via-mixed–integer-linear-programming](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HoffmanPereiraMatrix/Testing-copositivity-via-mixed%E2%80%93integer-linear-programming.png) -->

解説:

copositiveだが半正定値行列+非負行列という形で書けない (exceptionalである)。

```Python
import cvxpy as cp
import numpy as np

H = np.array([
    [ 1,-1, 1, 0, 0, 1,-1],
    [-1, 1,-1, 1, 0, 0, 1],
    [ 1,-1, 1,-1, 1, 0, 0],
    [ 0, 1,-1, 1,-1, 1, 0],
    [ 0, 0, 1,-1, 1,-1, 1],
    [ 1, 0, 0, 1,-1, 1,-1],
    [-1, 1, 0, 0, 1,-1, 1]
], dtype=float)

P = cp.Variable((7, 7), symmetric=True)
N = cp.Variable((7, 7), symmetric=True)

constraints = [
    H == P + N,
    P >> 0,      # P is PSD
    N >= 0       # entrywise nonnegative
]

prob = cp.Problem(cp.Minimize(0), constraints)
prob.solve()

print(prob.status)
```

これがinfeasibleになることからも数値的に示唆される。

原論文の方はextreme rayという文脈で論じており、関係性があるらしい。

### Hopf–Rinow Theorem

文献:

https://en.wikipedia.org/wiki/Hopf%E2%80%93Rinow_theorem

![HopfRinowTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/HopfRinowTheorem/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Hopf%E2%80%93Rinow_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

大分基礎的な定理。
ざっくり言えば、連結なリーマン多様体において、距離空間としての完備性や測地完備性と、閉有界集合のコンパクト性の同値性を述べ、任意の2点を結ぶ最短測地線の存在を保証する。
リーマン多様体上の最適化関連で出てくることもありそう。
Hadamard Manifoldの項で出てきたので記した。

### Inner And Outer Semicontinuity

文献:

https://en.wikipedia.org/wiki/Semi-continuity

![InnerAndOuterSemicontinuity_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/InnerAndOuterSemicontinuity/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Semi-continuity>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

[Hemicontinuity](https://en.wikipedia.org/wiki/Hemicontinuity)も参照のこと。

### InverseProblem

文献:

https://ja.wikipedia.org/wiki/%E9%80%86%E5%95%8F%E9%A1%8C

![InverseProblem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/InverseProblem/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E9%80%86%E5%95%8F%E9%A1%8C>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

https://speakerdeck.com/ssakaue/gyakusaitekika-to-kikai-gakushuu?slide=6 (坂上さんの講演資料)

<!-- ![InverseProblem_orsj-2026f-symposium-Shinsaku-Sakaue](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/InverseProblem/orsj-2026f-symposium-Shinsaku-Sakaue.png) -->

> 逆最適化は観測解 $x^\mathrm{obs}$ の最適性を説明する目的関数パラメータ $\hat{c}$ を探す問題

解説:

逆問題というと非破壊検査や医療のイメージが強いが、逆最適化という逆問題の一種で最適化と繋がっている。

### Invex Function

文献:

https://en.wikipedia.org/wiki/Invex_function

![InvexFunction_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/InvexFunction/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Invex_function>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

書いてある通り、停留点の大域最適性に関する必要十分条件としてよく使われている。

### Itoh–Abe Method

文献:

https://www.sciencedirect.com/science/article/abs/pii/0021999188901325?fr=RR-2&ref=pdf_download&rr=a38d0469ffc3d427

(提案論文)
<br>

https://link.springer.com/article/10.1007/s10208-020-09489-2

Riis, E.S., Ehrhardt, M.J., Quispel, G.R.W. et al. A Geometric Integration Approach to Nonsmooth, Nonconvex Optimisation. Found Comput Math 22, 1351–1394 (2022). https://doi.org/10.1007/s10208-020-09489-2

(この論文はOpen Access、[CC BY 4.0](http://creativecommons.org/licenses/by/4.0/))

![ItohAbeMethod_A-Geometric-Integration-Approach-to-Nonsmooth,-Nonconvex-Optimisation](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ItohAbeMethod/A-Geometric-Integration-Approach-to-Nonsmooth%2C-Nonconvex-Optimisation.png)

![ItohAbeMethod_A-Geometric-Integration-Approach-to-Nonsmooth,-Nonconvex-Optimisation-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ItohAbeMethod/A-Geometric-Integration-Approach-to-Nonsmooth%2C-Nonconvex-Optimisation-1.png)

![ItohAbeMethod_A-Geometric-Integration-Approach-to-Nonsmooth,-Nonconvex-Optimisation-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ItohAbeMethod/A-Geometric-Integration-Approach-to-Nonsmooth%2C-Nonconvex-Optimisation-2.png)

![ItohAbeMethod_A-Geometric-Integration-Approach-to-Nonsmooth,-Nonconvex-Optimisation-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ItohAbeMethod/A-Geometric-Integration-Approach-to-Nonsmooth%2C-Nonconvex-Optimisation-3.png)

解説:

勾配流などの文脈に近い。
考えている問題設定はZeroth Order Methodsに近いが、発想はかなり異なる。
もし次の反復点が見つかれば、それは絶対に関数値が減少している。
しかし、その次の反復点を見つけるのが、$n$ 個の等式を解くことを要求するので難しい。
あまり理解できていないが、Zeroth Order Methodsよりも優れている場合もありそう。

### John Ellipsoid

文献:

https://arxiv.org/pdf/2609.10888

https://en.wikipedia.org/wiki/John_ellipsoid

![JohnEllipsoid_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/JohnEllipsoid/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/John_ellipsoid>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Lowner Ellipse.webm](<https://commons.wikimedia.org/wiki/File:Lowner_Ellipse.webm>) / Gpeyre / [CC BY-SA 4.0](<https://creativecommons.org/licenses/by-sa/4.0/>)。

解説:

以下のような整理が出来る。

| 凸体を含む最小体積の楕円体 | 凸体に含まれる最大体積の楕円体 |
| :---: | :---: |
| 最小体積楕円体 | 最大体積楕円体 |
| the minimal volume ellipsoid | the maximal volume ellipsoid |
| the Löwner ellipsoid | the John ellipsoid |
| the outer Löwner–John ellipsoid | the inner Löwner–John ellipsoid |

楕円体法などに応用がある。

[シュタイナーの内接楕円](https://ja.wikipedia.org/wiki/%E3%82%B7%E3%83%A5%E3%82%BF%E3%82%A4%E3%83%8A%E3%83%BC%E3%81%AE%E5%86%85%E6%8E%A5%E6%A5%95%E5%86%86)は最大体積楕円体の特殊ケースである。

### KL property

文献:

https://doi.org/10.1007/s10107-011-0484-9

![KLProperty_Convergence-of-descent-methods-for-semi-algebraic-and-tame-problems](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/KLProperty/Convergence-of-descent-methods-for-semi-algebraic-and-tame-problems.png)

解説:

KL Propertyは、臨界点の近傍で関数値の差と劣勾配の大きさをもとに、目的関数が過度に平坦になることを排除する性質。
非凸非平滑な場合の収束解析などに用いられる。

なお、

- KL propertyのKL = Kurdyka–Łojasiewicz
- KL divergenceのKL = Kullback–Leibler

なので、人違いに注意。

### Linear Minimization Oracle

文献:

https://arxiv.org/abs/2601.20443

https://doi.org/10.1016/j.orl.2021.06.005

<!-- ![LinearMinimizationOracle_Complexity-of-linear-minimization-and-projection-on-some-sets](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/LinearMinimizationOracle/Complexity-of-linear-minimization-and-projection-on-some-sets.png) -->

解説:

$\ell_p$-ball, Nuclear norm ball, Flow polytope, Birkhoff polytope, Permutahedronなどの集合 $\mathcal{C}$ に対して、基本的にlinear minimizationの方が射影より計算量が軽いとTable 1にまとめられている。

主にFrank–Wolfe法と関連して語られる。

### Locus

文献:

https://en.wikipedia.org/wiki/Locus_(mathematics)#History_and_philosophy

![Locus_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Locus/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Locus_(mathematics)#History_and_philosophy>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

和訳は単に[軌跡](https://ja.wikipedia.org/wiki/%E8%BB%8C%E8%B7%A1_(%E6%95%B0%E5%AD%A6))。

画像にあるように、Zero locusなどで零点集合を指すので、そういった用例を時々見かける。

### Maximum Theorem

文献:

https://en.wikipedia.org/wiki/Maximum_theorem

![MaximumTheorem_Wiki-Statement](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Wiki-Statement.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Maximum_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![MaximumTheorem_Wiki-Examples](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Wiki-Examples.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Maximum_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![MaximumTheorem_Wiki-Image](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Wiki-Image.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Maximum_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

(この $f^*(\theta)$ が連続というのが主張の一つ)

https://arxiv.org/abs/2608.25789

<!-- ![MaximumTheorem_Sequential-Stability-of-the-Value-Function-and-the-Solution-Mapping-in-Berge's-Maximum-Theorem-via-Variational-Convergence](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Sequential-Stability-of-the-Value-Function-and-the-Solution-Mapping-in-Berge%27s-Maximum-Theorem-via-Variational-Convergence.png) -->

> Berge’s maximum theorem holds significant relevance in fields such as economic theory, optimal control, and optimization theory. For instance, in demand theory, it is concerned with an agent’s optimal consumption concerning prices and income, while in capital theory, with the optimal investment strategy based on the existing capital stock.

(本論文のSection 1より引用)

解説:

この定理は、パラメータに依存する最適化問題が、パラメータに関して連続的な解を持つための条件を提供している。

### Minimax Theorem

文献:

https://en.wikipedia.org/wiki/Minimax_theorem

![MinimaxTheorem_Wiki-concave-convex-functions](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinimaxTheorem/Wiki-concave-convex-functions.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Minimax_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Saddle point.svg](<https://commons.wikimedia.org/wiki/File:Saddle_point.svg>) / Nicoguaro / [CC BY 3.0](<https://creativecommons.org/licenses/by/3.0/>)。

![MinimaxTheorem_Wiki-Sion's-minimax-theorem](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinimaxTheorem/Wiki-Sion%27s-minimax-theorem.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Minimax_theorem>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

ゲーム理論が発端になっているらしい。

### Minkowski–Weyl Theorem

文献:

https://link.springer.com/book/10.1007/978-3-642-02431-3

(Variational Analysisの3. Cones and Cosmic Closureにて。証明も長いが載っている。)

(まず、以下がPolyhedralの定義。要は有限個の半空間の交わりで表せる集合。)

![MinkowskiWeylTheorem_Variational-Analysis-polyhedral](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinkowskiWeylTheorem/Variational-Analysis-polyhedral.png)

(次に、以下がconの定義。凸包。)

![MinkowskiWeylTheorem_Variational-Analysis-con](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinkowskiWeylTheorem/Variational-Analysis-con.png)

(次に、以下がposの定義。正錐包。)

![MinkowskiWeylTheorem_Variational-Analysis-pos](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinkowskiWeylTheorem/Variational-Analysis-pos.png)

(以上より、主張が理解できる。それはそうという感じがしてくる。)

![MinkowskiWeylTheorem_Variational-Analysis](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinkowskiWeylTheorem/Variational-Analysis.png)

解説:

[このサイト](https://people.inf.ethz.ch/fukudak/polyfaq/node14.html)の説明とは少し違ったように見えるが、揺れがあるのかも知れない。

[Stack Exchange](https://math.stackexchange.com/questions/1335176/what-is-the-weyl-minkowski-theorem)でも言及されている。

### Motzkin's Transposition Theorem

文献:

https://epubs.siam.org/doi/10.1137/1030065

(以下の文献と形式的な差異があるが、証明まで載っている。ただし長い。)

<!-- ![Motzkin'sTranspositionTheorem_THEORY-OF-LINEAR-AND-INTEGER-PROGRAMMING](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Motzkin%27sTranspositionTheorem/THEORY-OF-LINEAR-AND-INTEGER-PROGRAMMING.png) -->

https://www.researchgate.net/publication/2628560_Motzkin's_Transposition_Theorem_And_The_Related_Theorems_Of_Farkas_Gordan_And_Stiemke

<!-- ![Motzkin'sTranspositionTheorem_MOTZKIN’S-TRANSPOSITION-THEOREM,-AND-THE-RELATED-THEOREMS-OF-FARKAS,-GORDAN-AND-STIEMKE-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Motzkin%27sTranspositionTheorem/MOTZKIN%E2%80%99S-TRANSPOSITION-THEOREM%2C-AND-THE-RELATED-THEOREMS-OF-FARKAS%2C-GORDAN-AND-STIEMKE-1.png)

![Motzkin'sTranspositionTheorem_MOTZKIN’S-TRANSPOSITION-THEOREM,-AND-THE-RELATED-THEOREMS-OF-FARKAS,-GORDAN-AND-STIEMKE-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Motzkin%27sTranspositionTheorem/MOTZKIN%E2%80%99S-TRANSPOSITION-THEOREM%2C-AND-THE-RELATED-THEOREMS-OF-FARKAS%2C-GORDAN-AND-STIEMKE-2.png) -->

https://www.ism.ac.jp/~mirai/sscoke/2026/

(松井知己先生による講義の演習問題にほぼ同内容の出題)

解説:

出典としてやや古いものしかないが、Farkasの補題などを統一的に導けるという点で優れた一般性を持つ主張。
ただし、この定理の証明自体にFarkasの補題が用いられている。

定理そのものの主張ではないが、[この論文](https://www.researchgate.net/publication/2628560_Motzkin's_Transposition_Theorem_And_The_Related_Theorems_Of_Farkas_Gordan_And_Stiemke)におけるいくつかの線形システムが、定理で扱っている形式、つまり(c)の形式である $Ax \leq b, Bx < c$ に帰着できるという点は、重要かつ面白い。

### Motzkin–Straus Formulation

文献:

https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/maxima-for-graphs-and-a-new-proof-of-a-theorem-of-turan/AC3CC45896B053B75C856F25829CA95C

(ここでは載せないが、証明が載っている。そこそこ非自明で面白い。完全グラフの場合に帰着するのが要点っぽい。)
<br>

https://arxiv.org/pdf/1505.07077

![MotzkinStrausFormulation_Solving-the-Maximum-Clique-Problem-with-Symmetric-Rank-One-Nonnegative-Matrix-Approximation](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MotzkinStrausFormulation/Solving-the-Maximum-Clique-Problem-with-Symmetric-Rank-One-Nonnegative-Matrix-Approximation.png)

解説:

グラフの最大クリーク問題に対する連続的な定式化。
$k$ 頂点の完全グラフがあるとき、その各頂点に $1/k$ の重みを割り振ると、目的関数値は
$$
\frac{1}{k}^2 \cdot 2 \cdot \binom{k}{2} = \frac{k-1}{k} = 1 - \frac{1}{k}
$$
となるので、大まかには理解出来る。

### Moving Balls Approximation

文献:

https://epubs.siam.org/doi/abs/10.1137/090763317

(提案論文)

![MovingBallsApproximation_A-Moving-Balls-Approximation-Method-for-a-Class-of-Smooth-Constrained-Minimization-Problems-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MovingBallsApproximation/A-Moving-Balls-Approximation-Method-for-a-Class-of-Smooth-Constrained-Minimization-Problems-1.png)

![MovingBallsApproximation_A-Moving-Balls-Approximation-Method-for-a-Class-of-Smooth-Constrained-Minimization-Problems-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MovingBallsApproximation/A-Moving-Balls-Approximation-Method-for-a-Class-of-Smooth-Constrained-Minimization-Problems-2.png)

![MovingBallsApproximation_A-Moving-Balls-Approximation-Method-for-a-Class-of-Smooth-Constrained-Minimization-Problems-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MovingBallsApproximation/A-Moving-Balls-Approximation-Method-for-a-Class-of-Smooth-Constrained-Minimization-Problems-3.png)

解説:

非線形制約を各反復点の周りで二次上界による球状の凸制約に近似し、簡単な部分問題を逐次解く。
反復ごとに球の中心・半径が変化するためmoving ballsと呼ばれ、元の制約の実行可能性を保ちやすいのが特徴。

### Newton–Schulz

文献:

https://en.wikipedia.org/wiki/Newton%27s_method#Multiplicative_inverses_of_numbers_and_power_series

![NewtonSchulz_Wiki-Newton's-method](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/NewtonSchulz/Wiki-Newton%27s-method.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Newton%27s_method#Multiplicative_inverses_of_numbers_and_power_series>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

https://en.wikipedia.org/wiki/Matrix_sign_function#Newton%E2%80%93Schulz_iteration

![NewtonSchulz_Wiki-Matrix-sign-function](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/NewtonSchulz/Wiki-Matrix-sign-function.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Matrix_sign_function#Newton%E2%80%93Schulz_iteration>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

Newton–Schulz法は、大雑把には行列向けのNewton法で、適切な条件の下で二次収束するのが偉い。
具体例として、行列符号関数の計算にも用いられる。

### Neyman–Pearson Classification

文献:

https://www.science.org/doi/10.1126/sciadv.aao1659

![NeymanPearsonClassification_Neyman--Pearson-classification-algorithms-and-NP-receiver-operating-characteristics](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/NeymanPearsonClassification/Neyman--Pearson-classification-algorithms-and-NP-receiver-operating-characteristics.png)

![NeymanPearsonClassification_Neyman--Pearson-classification-algorithms-and-NP-receiver-operating-characteristics-Fig1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/NeymanPearsonClassification/Neyman--Pearson-classification-algorithms-and-NP-receiver-operating-characteristics-Fig1.png)

解説:

[第一種の過誤(偽陽性)](https://ja.wikipedia.org/wiki/%E7%AC%AC%E4%B8%80%E7%A8%AE%E9%81%8E%E8%AA%A4%E3%81%A8%E7%AC%AC%E4%BA%8C%E7%A8%AE%E9%81%8E%E8%AA%A4)を確実に抑えながら、第二種の過誤(偽陰性)を最小化する。
[deterministic nonlinearly constrained optimization](https://arxiv.org/pdf/2608.27676)の応用例として挙げられていた。

### Ordinal Regression

文献:

https://arxiv.org/abs/2608.06881

https://en.wikipedia.org/wiki/Ordinal_regression

![OrdinalRegression_Wiki-Abstract](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/OrdinalRegression/Wiki-Abstract.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Ordinal_regression>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![OrdinalRegression_Wiki-Linear-models-for-ordinal-regression](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/OrdinalRegression/Wiki-Linear-models-for-ordinal-regression.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Ordinal_regression>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

順序回帰は順序はあるものの間隔を数量化できない目的変数と、説明変数との関係をモデル化する回帰手法である。
アンケート、疾患の重症度、信用格付けなどの予測に用いられる。

### Polyak inequality

文献:

https://en.wikipedia.org/wiki/%C5%81ojasiewicz_inequality

![Polyakinequality_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Polyakinequality/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/%C5%81ojasiewicz_inequality>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

一般的にはPL不等式と呼ばれる。
Łojasiewicz inequalityの特殊ケースとして解釈出来る。

### Prioritized Constraints

文献:

https://www.sciencedirect.com/science/article/pii/S1474667017571554

(提案論文)
<br>

https://www.sciencedirect.com/science/article/pii/S0005109801001431

![PrioritizedConstraints_Linear-MPC-with-optimal-prioritized-infeasibility-handling](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/PrioritizedConstraints/Linear-MPC-with-optimal-prioritized-infeasibility-handling.png)

解説:

[優先制約](https://www.jstage.jst.go.jp/article/jacc/66/0/66_638/_pdf/-char/ja)とも呼ばれているようである。
実務寄りの要求から考えられている設定だと思われる。
そもそも制約が破られる前提でモデリングされていると思われ、通常の意味の制約とは性質が異なる。

### Quasiconvex

文献:

https://en.wikipedia.org/wiki/Quasiconvex_function

![Quasiconvex_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Quasiconvex/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Quasiconvex_function>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Quasiconvex function.png](<https://commons.wikimedia.org/wiki/File:Quasiconvex_function.png>) / Oleg Alexandrov / Public domain。 画像: [Nonquasiconvex function.png](<https://commons.wikimedia.org/wiki/File:Nonquasiconvex_function.png>) / Oleg Alexandrov / Public domain。

解説:

[準凸関数](https://ja.wikipedia.org/wiki/%E6%BA%96%E5%87%B8%E9%96%A2%E6%95%B0)とも。

### Radon's Theorem

文献:

https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%E3%81%AE%E5%AE%9A%E7%90%86

![Radon'sTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Radon%27sTheorem/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%E3%81%AE%E5%AE%9A%E7%90%86>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Radon coefficients.svg](<https://commons.wikimedia.org/wiki/File:Radon_coefficients.svg>) / David Eppstein / Public domain。

![Radon'sTheorem_Wiki-Proof](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Radon%27sTheorem/Wiki-Proof.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%E3%81%AE%E5%AE%9A%E7%90%86>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

Radon–Nikodym Derivativeで知られる[Radon](https://ja.wikipedia.org/wiki/%E3%83%A8%E3%83%8F%E3%83%B3%E3%83%BB%E3%83%A9%E3%83%89%E3%83%B3)さんの見つけた定理。
凸集合に関する基本的な性質の一つ。

[凸解析―理論と応用](https://www.maruzen-publishing.co.jp/book/b10123316.html)という本の8ページにも記載がある。

### Radon–Nikodym Derivative

文献:

https://arxiv.org/abs/2607.26562

(我々の論文)

![RadonNikodymDerivative_Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Sec2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/RadonNikodymDerivative/Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Sec2.png)

![RadonNikodymDerivative_Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Appendix](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/RadonNikodymDerivative/Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Appendix.png)

https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%EF%BC%9D%E3%83%8B%E3%82%B3%E3%83%87%E3%82%A3%E3%83%A0%E3%81%AE%E5%AE%9A%E7%90%86

![RadonNikodymDerivative_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/RadonNikodymDerivative/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%EF%BC%9D%E3%83%8B%E3%82%B3%E3%83%87%E3%82%A3%E3%83%A0%E3%81%AE%E5%AE%9A%E7%90%86>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

以下の解説が具体例を用いた説明をしており、非常に参考になる(通常のサイコロを振る際の確率測度 $P$ と、456賽を振る際の確率測度 $Q$ の関係を考えている)。

https://peng225.hatenablog.com/entry/2025/04/04/124548

ただし、少なくとも最適化の文脈でRadon–Nikodym derivativeを用いる際、確率密度関数や確率質量関数を定義することが多いと思っているので、その点はやや注意が必要。離散分布の場合、確率変数 $X$ の分布を $P_X$ とし、状態空間上の数え上げ測度（counting measure）を $\\\#$ とすると、$p_X(x)=\frac{\mathrm{d}P_X}{\mathrm{d}\\\#}(x)$ と定義できる。
連続分布かつその分布がLebesgue測度に対して絶対連続な場合には、基準測度としてLebesgue測度を用いる。
<!-- to LLM: ここの $\\\#$ を直すな。これは意図的。 -->

この間とある飲み会に行って、機械学習系の会議に出した最適化の論文(上記)で、Radon–Nikodym derivativeを持ち出したという話を友人にしたら、査読者が困っちゃうよと言われました。現に私があんまり分からなくなっているので、そうかも知れません。

### ResNet

文献:

https://arxiv.org/pdf/1811.12231

<!-- ![ResNet_IMAGENET-TRAINED-CNNS-ARE-BIASED-TOWARDS-TEXTURE](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ResNet/IMAGENET-TRAINED-CNNS-ARE-BIASED-TOWARDS-TEXTURE.png) -->

![ResNet_IMAGENET-TRAINED-CNNS-ARE-BIASED-TOWARDS-TEXTURE-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ResNet/IMAGENET-TRAINED-CNNS-ARE-BIASED-TOWARDS-TEXTURE-2.png)

https://ja.wikipedia.org/wiki/%E6%AE%8B%E5%B7%AE%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF

![ResNet_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/ResNet/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E6%AE%8B%E5%B7%AE%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

現代では古典的手法なのかも知れない。
2018年には、ImageNetで学習したCNN（ResNet-50を含む）が、大域的な形状よりも局所的な情報(texture)に引っ張られやすい傾向が指摘されている。

### Satisfiability Modulo Theories

文献:

https://ja.wikipedia.org/wiki/%E5%85%85%E8%B6%B3%E5%8F%AF%E8%83%BD%E6%80%A7%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%AD%E7%90%86%E8%AB%96

![SatisfiabilityModuloTheories_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/SatisfiabilityModuloTheories/Wiki.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E5%85%85%E8%B6%B3%E5%8F%AF%E8%83%BD%E6%80%A7%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%AD%E7%90%86%E8%AB%96>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

Moduloというのがややこしいが、剰余の意味ではなく、理論を考慮した充足可能性判定くらいの意味か。
真偽のみを扱うSATに比べて、整数や実数なども扱えるSMTは表現能力が高い。
Leanなどの定理証明支援系と比べると、表現能力は劣るが、探索能力は高い。

### Set-Valued Function

文献:

https://en.wikipedia.org/wiki/Set-valued_function

![SetValuedFunction_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/SetValuedFunction/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/Set-valued_function>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 画像: [Multivalued function.svg](<https://commons.wikimedia.org/wiki/File:Multivalued_function.svg>) / Schapel / Public domain。

https://books.google.com.pa/books?id=tiBtC4GmuKcC

![SetValuedFunction_New-Developments-in-Contact-Problems](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/SetValuedFunction/New-Developments-in-Contact-Problems.png)

解説:

Set-valued functionはcorrespondenceとも呼ばれる。

また、これらの語が一体何を意図しているのかは、読んでいる文章の文脈を非常に注意深く読む必要がある。

まず、多価関数なども含めて、いわゆる関数らしきものをまとめて指せる一番広い用語は[二項関係](https://ja.wikipedia.org/wiki/%E4%BA%8C%E9%A0%85%E9%96%A2%E4%BF%82)と言える。

あくまでWikipediaの記述に従うと、二項関係のうち、

- 左全域的なだけなら広義の「対応」
- 左全域的かつ右全域的なら狭義の「対応」
- 左全域的かつ右一意的なら「関数」(「関数関係」「写像」とも)

と呼ばれているようである(ここも文献に応じて揺れがあるので、注意が必要である、対応において空集合を割り当てることを許す場合は左全域的ですらない)。

さて、ここで $X$ と $Y$ を集合とし、その間の二項関係 $f$ を考える。
もし、$x \in X$ に対して複数の $y \in Y$ が対応する場合、一見すると右一意性が失われている。
しかし、もし $x \in X$ に対して、$Y$ の部分集合 $f(x) \subseteq Y$ が対応する、と考えると、右一意性は失われていない(つまり、終域の解釈が異なる)。
よって、広義の「対応」と呼ぶべきか、「関数」と呼ぶべきかは、かなり注意深い議論が必要になる。

ここでは誤りを避けるために、これ以上の議論には踏み込まない。

### Sturm's Theorem

文献:

https://izumi-math.jp/F_Yasuda/71_1_yasuda.pdf

https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%84%E3%83%AB%E3%83%A0%E3%81%AE%E5%AE%9A%E7%90%86

![Sturm'sTheorem_Wiki-Theorem](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Sturm%27sTheorem/Wiki-Theorem.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%84%E3%83%AB%E3%83%A0%E3%81%AE%E5%AE%9A%E7%90%86>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

![Sturm'sTheorem_Wiki-Method](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Sturm%27sTheorem/Wiki-Method.png)

出典: [Wikipedia contributors](<https://ja.wikipedia.org/wiki/%E3%82%B9%E3%83%84%E3%83%AB%E3%83%A0%E3%81%AE%E5%AE%9A%E7%90%86>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

https://www.fit.ac.jp/~h-takeda/conf/files/2015/yotsutani/02.pdf

<!-- ![Sturm'sTheorem_HiroshiTakeda-Slide](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Sturm%27sTheorem/HiroshiTakeda-Slide.png) -->

解説:

大雑把に言えば、ユークリッドの互除法を使えば、ある区間内の多項式の実根の個数を数えることが出来るというもの。
Newton法などに応用がある。

この話をしてくれた研究者は、大域最適化に関する研究をしている方だったはずですが、どのような関連があるのかは深くまで理解していません。

### Ursescu Theorem

文献:

https://en.wikipedia.org/wiki/Ursescu_theorem

解説:

難しい。set-valued mapの話。
将来的に追記予定。

### Wasserstein DRO

文献:

https://arxiv.org/pdf/2608.18123

![WassersteinDRO_Learning-the-Center-and-Radius-of-Wasserstein-Ambiguity-Sets-for-Data-Driven-Decision-Making](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Learning-the-Center-and-Radius-of-Wasserstein-Ambiguity-Sets-for-Data-Driven-Decision-Making.png)

https://doi.org/10.1007/s10107-017-1172-1

(上記の Esfahani and Kuhn (2018) にあたる)

Mohajerin Esfahani, P., Kuhn, D. Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations. Math. Program. 171, 115–166 (2018). https://doi.org/10.1007/s10107-017-1172-1

(この論文はOpen Access、[CC BY 4.0](http://creativecommons.org/licenses/by/4.0/))

![WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-1.png)

![WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-2.png)

![WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-3.png)

解説:

Wasserstein DROは、経験分布などを中心、Wasserstein距離を半径とする分布の曖昧性集合を考え、その中の最悪分布に対して意思決定を最適化する手法。
頑健性があって偉い。

### Łojasiewicz inequality

文献:

https://en.wikipedia.org/wiki/%C5%81ojasiewicz_inequality

![Łojasiewiczinequality_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/%C5%81ojasiewiczinequality/Wiki.png)

出典: [Wikipedia contributors](<https://en.wikipedia.org/wiki/%C5%81ojasiewicz_inequality>), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

解説:

一見するとかなり別々の条件を同じ名前で呼んでいるように見える。
前者は零点集合からの距離と関数値の関係であり、後者は関数値と勾配の関係となっている。
式の形をざっくりと見れば、不等号、絶対値、べき乗、定数などと要素は似ているが、仮定や指数の置き方などに複数の流儀があることには注意が必要。

なお、[Stanisław Łojasiewicz](https://en.wikipedia.org/wiki/Stanis%C5%82aw_%C5%81ojasiewicz)はポーランド人で、Łは[ポーランド語](https://ja.wikipedia.org/wiki/%C5%81)のようである。

PL不等式も参照のこと。

## 最後に

今後も追加予定です。
