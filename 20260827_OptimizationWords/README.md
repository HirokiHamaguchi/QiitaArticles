# 最適化関連の個人的用語集

この記事は、最適化関連の用語のうち、個人的に気になったものをまとめたものです。

私が飽きるまでは更新される可能性があります。

## 目次

<!-- INDEX -->

- [最適化関連の個人的用語集](#最適化関連の個人的用語集)
  - [目次](#目次)
  - [用語集](#用語集)
    - [(L0, L1) Smoothness](#l0-l1-smoothness)
    - [Additive Smoothing](#additive-smoothing)
    - [Antithetic variates](#antithetic-variates)
    - [Asplund Space](#asplund-space)
    - [Augmented Lagrangian Method](#augmented-lagrangian-method)
    - [Bayesian Network](#bayesian-network)
    - [Carathéodory's Extension Theorem](#carathéodorys-extension-theorem)
    - [Carathéodory's Theorem (Convex Hull)](#carathéodorys-theorem-convex-hull)
    - [Eckart–Young–Mirsky Theorem](#eckartyoungmirsky-theorem)
    - [Fredholm Alternative](#fredholm-alternative)
    - [Generalized Cauchy Point](#generalized-cauchy-point)
    - [Generalized Moment Problem](#generalized-moment-problem)
    - [Graphical Lasso](#graphical-lasso)
    - [Growth Condition](#growth-condition)
    - [KL property](#kl-property)
    - [Maximum Theorem](#maximum-theorem)
    - [Minimax Theorem](#minimax-theorem)
    - [Motzkin's Transposition Theorem](#motzkins-transposition-theorem)
    - [Newton–Schulz](#newtonschulz)
    - [Neyman–Pearson Classification](#neymanpearson-classification)
    - [Ordinal Regression](#ordinal-regression)
    - [Quasiconvex](#quasiconvex)
    - [Radon's Theorem](#radons-theorem)
    - [Radon–Nikodym Derivative](#radonnikodym-derivative)
    - [Set-Valued Function](#set-valued-function)
    - [Sturm's Theorem](#sturms-theorem)
    - [Wasserstein DRO](#wasserstein-dro)
  - [最後に](#最後に)

## 用語集

<!-- WORDS -->

### (L0, L1) Smoothness

文献:

https://www.researchgate.net/profile/Mohammad-Alkousa-2/publication/413568957_First-Order_Methods_for_Optimization_Problems_with_Generalized_Smoothness_and_Generalized_Inexact_Oracle/links/6a8c89c7db725f1be9602a92/First-Order-Methods-for-Optimization-Problems-with-Generalized-Smoothness-and-Generalized-Inexact-Oracle.pdf

(これの[11]が以下の論文)
<br>

https://arxiv.org/abs/1905.11881

![L0L1Smoothness_WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/L0L1Smoothness/WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING.png)

![L0L1Smoothness_WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING-Fig1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/L0L1Smoothness/WHY-GRADIENT-CLIPPING-ACCELERATES-TRAINING-Fig1.png)

解説:

$L$-Smoothnessの一般化。
上記のFig.1にあるように、勾配ノルムとSmoothnessに相関があることを契機として導入されたようである。
確かに、$L$-Smoothnessの仮定は現実的な問題と不整合だとはよく感じるので、非常に妥当で面白い。

### Additive Smoothing

文献:

https://en.wikipedia.org/wiki/Additive_smoothing

![AdditiveSmoothing_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AdditiveSmoothing/Wiki.png)

解説:

Additive SmoothingはLaplace Smoothingとも呼ばれている。
なお、[Laplacian Smoothing](https://en.wikipedia.org/wiki/Laplacian_smoothing) もあるが、そちらはグラフ理論関連の話。

### Antithetic variates

文献:

https://en.wikipedia.org/wiki/Antithetic_variates

![AntitheticVariates_Wiki-Underlying-principle](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AntitheticVariates/Wiki-Underlying-principle.png)

![AntitheticVariates_Wiki-Example2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AntitheticVariates/Wiki-Example2.png)

解説:

[負相関変量法・対称変量法](https://triadsou.hatenablog.com/entry/20100819/1282192611)とも呼ばれている。
モンテカルロ推定量の不偏性を保ちながら分散を小さくする。

### Asplund Space

文献:

https://arxiv.org/abs/2608.26328

https://en.wikipedia.org/wiki/Asplund_space

![Asplund_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Asplund/Wiki.png)

解説:

めちゃくちゃ大雑把に言えばフレシェ微分が自由にできる空間。

### Augmented Lagrangian Method

文献:

https://en.wikipedia.org/wiki/Augmented_Lagrangian_method

![AugmentedLagrangianMethod_Wiki-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AugmentedLagrangianMethod/Wiki-1.png)

![AugmentedLagrangianMethod_Wiki-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/AugmentedLagrangianMethod/Wiki-2.png)

解説:

日本語では拡張ラグランジュ関数法とも。ADMMはこの亜種。

### Bayesian Network

文献:

https://ja.wikipedia.org/wiki/%E3%83%99%E3%82%A4%E3%82%B8%E3%82%A2%E3%83%B3%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF

![BayesianNetwork_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/BayesianNetwork/Wiki.png)

解説:

[Graphical Model](https://en.wikipedia.org/wiki/Graphical_model)の特殊ケースとしてBayesian Networkが存在する。

### Carathéodory's Extension Theorem

文献:

https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%86%E3%82%AA%E3%83%89%E3%83%AA%E3%81%AE%E6%8B%A1%E5%BC%B5%E5%AE%9A%E7%90%86

![Caratheodory'sExtensionTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Caratheodory%27sExtensionTheorem/Wiki.png)

解説:

最適化との馴染みはやや薄いが、Carathéodory と名のつく定理は複数存在するので、対比の為に記しておく。
混同に注意。

### Carathéodory's Theorem (Convex Hull)

文献:

https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%86%E3%82%AA%E3%83%89%E3%83%AA%E3%81%AE%E5%AE%9A%E7%90%86_(%E5%87%B8%E5%8C%85)#/languages

![Caratheodory'sTheorem(ConvexHull)_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Caratheodory%27sTheorem%28ConvexHull%29/Wiki.png)

解説:

証明は[高校数学の美しい物語](https://manabitimes.jp/math/1216)さんに詳しい。

todo: 書籍での例を記す

ちなみに Carathéodory's Extension Theorem の[Carathéodory](https://en.wikipedia.org/wiki/Constantin_Carath%C3%A9odory)さんと同一人物。

### Eckart–Young–Mirsky Theorem

文献:

![EckartYoungMirskyTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/EckartYoungMirskyTheorem/Wiki.png)

解説:

行列の低ランク近似をフロベニウスノルムによって定式化した際、その最適解は特異値分解によって得られることを示す定理。
定理自体は有名だが、このような名前がついていることは知名度が低いかも知れない。
お三方とも1900年代の数学者らしい。

### Fredholm Alternative

文献:

https://en.wikipedia.org/wiki/Fredholm_alternative

![FredholmAlternative_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FredholmAlternative/Wiki.png)

https://www.ism.ac.jp/~mirai/sscoke/2026/

(松井知己先生による講義資料)

![FredholmAlternative_sscoke2026-tomomi-matsui](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/FredholmAlternative/sscoke2026-tomomi-matsui.png)

解説:

書いてある通りだが、$b \in \mathrm{Im}(A)$ と $b \in \mathrm{Ker}(A^\top)^\perp$ が同値ということを言っているに過ぎない。
[Farkas' lemmaのcorollary](https://en.wikipedia.org/wiki/Farkas%27_lemma)として得られる。

### Generalized Cauchy Point

文献:

https://doi.org/10.1007/978-0-387-40065-5

Wright, Stephen J., and Jorge Nocedal. "Numerical optimization." における説明

![GeneralizedCauchyPoint_Numerical-Optimization](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/Numerical-Optimization.png)

https://doi.org/10.1137/0916069

Richard H. Byrd, Peihuang Lu, Jorge Nocedal, and Ciyou Zhu. "A Limited Memory Algorithm for Bound Constrained Optimization." における説明

![GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-1.png)

![GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-2.png)

![GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GeneralizedCauchyPoint/A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-3.png)

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

![GraphicalLasso_Wiki-multivariate-normal-distribution](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/GraphicalLasso/Wiki-multivariate-normal-distribution.png)

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

### Maximum Theorem

文献:

https://en.wikipedia.org/wiki/Maximum_theorem

![MaximumTheorem_Wiki-Statement](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Wiki-Statement.png)

![MaximumTheorem_Wiki-Examples](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Wiki-Examples.png)

![MaximumTheorem_Wiki-Image](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Wiki-Image.png)

(この $f^*(\theta)$ が連続というのが主張の一つ)

https://arxiv.org/abs/2608.25789

![MaximumTheorem_Sequential-Stability-of-the-Value-Function-and-the-Solution-Mapping-in-Berge's-Maximum-Theorem-via-Variational-Convergence](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MaximumTheorem/Sequential-Stability-of-the-Value-Function-and-the-Solution-Mapping-in-Berge%27s-Maximum-Theorem-via-Variational-Convergence.png)

解説:

この定理は、パラメータに依存する最適化問題が、パラメータに関して連続的な解を持つための条件を提供している。

### Minimax Theorem

文献:

https://en.wikipedia.org/wiki/Minimax_theorem

![MinimaxTheorem_Wiki-concave-convex-functions](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinimaxTheorem/Wiki-concave-convex-functions.png)

![MinimaxTheorem_Wiki-Sion's-minimax-theorem](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/MinimaxTheorem/Wiki-Sion%27s-minimax-theorem.png)

解説:

ゲーム理論が発端になっているらしい。

### Motzkin's Transposition Theorem

文献:

https://epubs.siam.org/doi/10.1137/1030065

(以下の文献と形式的な差異があるが、証明まで載っている。ただし長い。)

![Motzkin'sTranspositionTheorem_THEORY-OF-LINEAR-AND-INTEGER-PROGRAMMING](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Motzkin%27sTranspositionTheorem/THEORY-OF-LINEAR-AND-INTEGER-PROGRAMMING.png)

https://www.researchgate.net/publication/2628560_Motzkin's_Transposition_Theorem_And_The_Related_Theorems_Of_Farkas_Gordan_And_Stiemke

![Motzkin'sTranspositionTheorem_MOTZKIN’S-TRANSPOSITION-THEOREM,-AND-THE-RELATED-THEOREMS-OF-FARKAS,-GORDAN-AND-STIEMKE-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Motzkin%27sTranspositionTheorem/MOTZKIN%E2%80%99S-TRANSPOSITION-THEOREM%2C-AND-THE-RELATED-THEOREMS-OF-FARKAS%2C-GORDAN-AND-STIEMKE-1.png)

![Motzkin'sTranspositionTheorem_MOTZKIN’S-TRANSPOSITION-THEOREM,-AND-THE-RELATED-THEOREMS-OF-FARKAS,-GORDAN-AND-STIEMKE-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Motzkin%27sTranspositionTheorem/MOTZKIN%E2%80%99S-TRANSPOSITION-THEOREM%2C-AND-THE-RELATED-THEOREMS-OF-FARKAS%2C-GORDAN-AND-STIEMKE-2.png)

https://www.ism.ac.jp/~mirai/sscoke/2026/

(松井知己先生による講義の演習問題にほぼ同内容の出題)

解説:

出典としてやや古いものしかないが、Farkasの補題などを統一的に導けるという点で優れた一般性を持つ主張。ただし、この定理の証明自体にFarkasの補題が用いられている。

定理そのものの主張ではないが、いくつかの線形システムが定理で扱っている形式、つまり(c)の形式である $Ax \leq b, Bx < c$ に帰着できるという点は、重要かつ面白い。

### Newton–Schulz

文献:

https://en.wikipedia.org/wiki/Newton%27s_method#Multiplicative_inverses_of_numbers_and_power_series

![NewtonSchulz_Wiki-Newton's-method](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/NewtonSchulz/Wiki-Newton%27s-method.png)

https://en.wikipedia.org/wiki/Matrix_sign_function#Newton%E2%80%93Schulz_iteration

![NewtonSchulz_Wiki-Matrix-sign-function](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/NewtonSchulz/Wiki-Matrix-sign-function.png)

解説:

Newton–Schulz法は、大雑把には行列向けのNewton法で、二次収束するのが偉い。
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

![OrdinalRegression_Wiki-Linear-models-for-ordinal-regression](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/OrdinalRegression/Wiki-Linear-models-for-ordinal-regression.png)

解説:

順序回帰は順序はあるものの間隔を数量化できない目的変数と、説明変数との関係をモデル化する回帰手法である。
アンケート、疾患の重症度、信用格付けなどの予測に用いられる。

### Quasiconvex

文献:

https://en.wikipedia.org/wiki/Quasiconvex_function

![Quasiconvex_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Quasiconvex/Wiki.png)

解説:

[準凸関数](https://ja.wikipedia.org/wiki/%E6%BA%96%E5%87%B8%E9%96%A2%E6%95%B0)とも。

### Radon's Theorem

文献:

https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%E3%81%AE%E5%AE%9A%E7%90%86

![Radon'sTheorem_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Radon%27sTheorem/Wiki.png)

![Radon'sTheorem_Wiki-Proof](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Radon%27sTheorem/Wiki-Proof.png)

解説:

Radon–Nikodym Derivativeで知られる[Radon](https://ja.wikipedia.org/wiki/%E3%83%A8%E3%83%8F%E3%83%B3%E3%83%BB%E3%83%A9%E3%83%89%E3%83%B3)さんの見つけた定理。
凸集合に関する基本的な性質の一つ。

### Radon–Nikodym Derivative

文献:

https://arxiv.org/abs/2607.26562

(我々の論文)

![RadonNikodymDerivative_Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Sec2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/RadonNikodymDerivative/Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Sec2.png)

![RadonNikodymDerivative_Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Appendix](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/RadonNikodymDerivative/Adaptive-Gradient-Based-Methods-for-a-Broader-Class-of-Optimization-Problems-under-Performative-Prediction-Appendix.png)

https://ja.wikipedia.org/wiki/%E3%83%A9%E3%83%89%E3%83%B3%EF%BC%9D%E3%83%8B%E3%82%B3%E3%83%87%E3%82%A3%E3%83%A0%E3%81%AE%E5%AE%9A%E7%90%86

![RadonNikodymDerivative_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/RadonNikodymDerivative/Wiki.png)

解説:

以下の解説が具体例を用いた説明をしており、非常に参考になる(通常のサイコロを振る際の確率測度 $P$ と、456賽を振る際の確率測度 $Q$ の関係を考えている)。

https://peng225.hatenablog.com/entry/2025/04/04/124548

ただし、少なくとも最適化の文脈でRadon–Nikodym derivativeを用いる際、確率密度関数や確率質量関数を定義することが多いと思っているので、その点はやや注意が必要。離散分布の場合、確率変数 $X$ の分布を $P_X$ とし、状態空間上の数え上げ測度（counting measure）を $\\\#$ とすると、$p_X(x)=\frac{\mathrm{d}P_X}{\mathrm{d}\\\#}(x)$ と定義できる。連続分布の場合は、数え上げ測度がLebesgue測度に置き換わる。

この間とある飲み会に行って、機械学習系の会議に出した最適化の論文(上記)で、Radon–Nikodym derivativeを持ち出したという話を友人にしたら、査読者が困っちゃうよと言われました。現に私があんまり分からなくなっているので、そうかも知れません。

### Set-Valued Function

文献:

https://en.wikipedia.org/wiki/Set-valued_function

![SetValuedFunction_Wiki](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/SetValuedFunction/Wiki.png)

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

![Sturm'sTheorem_Wiki-Method](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Sturm%27sTheorem/Wiki-Method.png)

https://www.fit.ac.jp/~h-takeda/conf/files/2015/yotsutani/02.pdf

![Sturm'sTheorem_HiroshiTakeda-Slide](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/Sturm%27sTheorem/HiroshiTakeda-Slide.png)

解説:

大雑把に言えば、ユークリッドの互除法を使えば、ある区間内の多項式の実根の個数を数えることが出来るというもの。
Newton法などに応用がある。

この話をしてくれた研究者は、大域最適化に関する研究をしている方だったはずですが、どのような関連があるのかは深くまで理解していません。

### Wasserstein DRO

文献:

https://arxiv.org/pdf/2608.18123

![WassersteinDRO_Learning-the-Center-and-Radius-of-Wasserstein-Ambiguity-Sets-for-Data-Driven-Decision-Making](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Learning-the-Center-and-Radius-of-Wasserstein-Ambiguity-Sets-for-Data-Driven-Decision-Making.png)

https://doi.org/10.1007/s10107-017-1172-1

(上記の Esfahani and Kuhn (2018) にあたる)

![WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-1.png)

![WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-2.png)

![WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/WassersteinDRO/Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-3.png)

解説:

Wasserstein DROは、経験分布などを中心、Wasserstein距離を半径とする分布の曖昧性集合を考え、その中の最悪分布に対して意思決定を最適化する手法。
頑健性があって偉い。

## 最後に

引用の仕方が不正確で申し訳ないですが、個人的なメモなためご容赦ください。
