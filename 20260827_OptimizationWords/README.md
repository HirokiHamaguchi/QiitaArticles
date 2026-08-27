# 最適化関連の個人的用語集

この記事は、最適化関連の用語のうち、個人的に気になったものをまとめたものです。

私が飽きるまでは更新される可能性があります。

## 目次

<!-- INDEX -->

- [最適化関連の個人的用語集](#最適化関連の個人的用語集)
  - [目次](#目次)
  - [用語集](#用語集)
    - [Antithetic variates](#antithetic-variates)
    - [Generalized Moment Problem](#generalized-moment-problem)
    - [Growth Condition](#growth-condition)
    - [KL property](#kl-property)
    - [Newton–Schulz](#newtonschulz)
    - [Ordinal Regression](#ordinal-regression)
    - [Wasserstein DRO](#wasserstein-dro)
  - [最後に](#最後に)

## 用語集

<!-- WORDS -->

### Antithetic variates

文献:

https://en.wikipedia.org/wiki/Antithetic_variates

スクショ:

![_AntitheticVariates_Wiki-Underlying-principle](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_AntitheticVariates_Wiki-Underlying-principle.png)

![_AntitheticVariates_Wiki-Example2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_AntitheticVariates_Wiki-Example2.png)

解説:

[負相関変量法・対称変量法](https://triadsou.hatenablog.com/entry/20100819/1282192611)とも呼ばれている。
モンテカルロ推定量の不偏性を保ちながら分散を小さくする。

### Generalized Moment Problem

文献:

https://arxiv.org/abs/2608.24184

https://books.google.co.jp/books?id=lFi7CgAAQBAJ

スクショ:

![_GeneralizedMomentProblem_Moments,-Positive-Polynomials-and-Their-Applications.png](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GeneralizedMomentProblem_Moments%2C-Positive-Polynomials-and-Their-Applications.png)

解説:

未知の測度を変数とし、その[モーメント](https://ja.wikipedia.org/wiki/%E3%83%A2%E3%83%BC%E3%83%A1%E3%83%B3%E3%83%88_(%E6%95%B0%E5%AD%A6))に関する線形制約の下で測度の線形汎関数を最適化する無限次元線形計画問題である。
データが多項式の場合は[the moment Sum-of-squares (SOS) hierarchy](https://arxiv.org/abs/2608.24184)による半正定値計画緩和で近似できる。

### Growth Condition

文献:

https://arxiv.org/pdf/2608.20642

https://pubsonline.informs.org/doi/abs/10.1287/moor.2017.0889

スクショ:

![_GrowthCondition_Error-Bounds,-Quadratic-Growth,-and-Linear-Convergence-of-Proximal-Methods](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GrowthCondition_Error-Bounds%2C-Quadratic-Growth%2C-and-Linear-Convergence-of-Proximal-Methods.png)

![_GrowthCondition_Strong-growth-and-Goldstein-subgradients-in-piecewise-smooth-optimization](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GrowthCondition_Strong-growth-and-Goldstein-subgradients-in-piecewise-smooth-optimization.png)

解説:

最適値からの目的関数値の差が解集合までの距離に応じてどれだけ増えるかを下から評価する正則性条件。
近接勾配法などの線形収束を導くために用いられる。

### KL property

文献:

https://doi.org/10.1007/s10107-011-0484-9

スクショ:

![_KLProperty_Convergence-of-descent-methods-for-semi-algebraic-and-tame-problems](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_KLProperty_Convergence-of-descent-methods-for-semi-algebraic-and-tame-problems.png)

解説:

KL Propertyは、臨界点の近傍で関数値の差と劣勾配の大きさをもとに、目的関数が過度に平坦になることを排除する性質。
非凸非平滑な場合の収束解析などに用いられる。

なお、

- KL propertyのKL = Kurdyka–Łojasiewicz
- KL divergenceのKL = Kullback–Leibler

なので、人違いに注意。

### Newton–Schulz

文献:

https://en.wikipedia.org/wiki/Matrix_sign_function#Newton%E2%80%93Schulz_iteration

https://en.wikipedia.org/wiki/Newton%27s_method#Multiplicative_inverses_of_numbers_and_power_series

スクショ:

![_NewtonSchulz_Wiki-Newton's-method](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_NewtonSchulz_Wiki-Newton%27s-method.png)

![_NewtonSchulz_Wiki-Matrix-sign-function](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_NewtonSchulz_Wiki-Matrix-sign-function.png)

解説:

Newton–Schulz法は、大雑把には行列向けのNewton法で、二次収束するのが偉い。
具体例として、行列符号関数の計算にも用いられる。

### Ordinal Regression

文献:

https://en.wikipedia.org/wiki/Ordinal_regression

https://arxiv.org/abs/2608.06881

スクショ:

![_OrdinalRegression_Wiki-Abst](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_OrdinalRegression_Wiki-Abst.png)

![_OrdinalRegression_Wiki-Linera-models-for-ordinal-regression](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_OrdinalRegression_Wiki-Linera-models-for-ordinal-regression.png)

解説:

順序回帰は順序はあるものの間隔を数量化できない目的変数と、説明変数との関係をモデル化する回帰手法である。
アンケート、疾患の重症度、信用格付けなどの予測に用いられる。

### Wasserstein DRO

文献:

https://arxiv.org/pdf/2608.18123

https://doi.org/10.1007/s10107-017-1172-1

スクショ:

![_WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-1.png)

![_WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-2.png)

![_WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_WassersteinDRO_Data-driven-distributionally-robust-optimization-using-the-Wasserstein-metric-3.png)

![_WassersteinDRO_Learning-the-Center-and-Radius-of-Wasserstein-Ambiguity-Sets-for-Data-Driven-Decision-Making](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_WassersteinDRO_Learning-the-Center-and-Radius-of-Wasserstein-Ambiguity-Sets-for-Data-Driven-Decision-Making.png)

解説:

Wasserstein DROは、経験分布などを中心、Wasserstein距離を半径とする分布の曖昧性集合を考え、その中の最悪分布に対して意思決定を最適化する手法。
頑健性があって偉い。

## 最後に

引用の仕方が不正確で申し訳ないですが、個人的なメモなためご容赦ください。
