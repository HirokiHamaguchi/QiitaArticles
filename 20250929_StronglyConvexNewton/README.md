# 強凸関数だがNewton法が収束しない例

Doikov, N. (2021). [New second-order and tensor methods in convex optimization](https://dial.uclouvain.be/pr/boreal/object/boreal:260515) (Doctoral dissertation, Ph. D. thesis, Université catholique de Louvain) の Example 1.4.3.が面白かったので、走り書き程度のメモを残しておきます。

## 強凸な目的関数の例

目的関数、およびその導関数は以下の通りです。

$$
\begin{align*}
f(x) &= \log(1 + e^x) - \frac{x}{2} + \frac{\mu x^2}{2}\\
f'(x) &= \frac{e^x}{1+e^x} - \frac{1}{2} + \mu x\\
f''(x) &= \frac{e^x}{(1+e^x)^2} + \mu\\
f'''(x) &= \frac{e^x(1 - e^x)}{(1+e^x)^3}\\
f''''(x) &= \frac{e^x(1 - 4e^x + e^{2x})}{(1+e^x)^4}
\end{align*}
$$

この目的関数は、

* $\mu$-強凸
* $\max_x | f''(x) | = \frac{1}{4} + \mu$ ($e^x=1$ のとき) であるので、$\nabla f$ が $L$-smooth ($L=\frac{1}{4} + \mu$)
* $\max_x | f'''(x) | = \frac{1}{6\sqrt{3}}$ ($e^x=2-\sqrt{3}$ のとき) であるので、$\nabla^2 f$ が $M$-Lipschitz連続 ($M=\frac{1}{6\sqrt{3}}$)

という各種の良い性質を満たしますが、$\mu$ に対して初期点 $x_0$ が十分大きいとき、Newton法は収束しません。

![plot_0.1_-4](./strongly_convex_function_0.1_-4.png)
(初期点 $x_0=-4, \mu=0.1$ の場合、収束する)

![plot_0.01_-4](./strongly_convex_function_0.01_-4.png)
(初期点 $x_0=-4, \mu=0.01$ の場合、振動する)

## 強凸でない目的関数の例

ちなみに、次のような強凸でない目的関数の場合、よりシンプルな例でNewton法は発散します。

$$
\begin{align*}
f(x) &= \sqrt{1 + x^2}\\
f'(x) &= \frac{x}{\sqrt{1 + x^2}}\\
f''(x) &= \frac{1}{(1 + x^2)^{3/2}}
\end{align*}
$$

この関数は強凸ではありません($f''(x)$ は $x \to \infty$ で $0$ に近づく)。

このような関数に対してNewton法を適用すると、初期点の絶対値が1より真に大きいと発散します。

![plot_1.1](./sqrt_function_1.1.png)
(初期点 $x_0=1.1$ の場合、発散する)

## 実験コード

<!-- PROGRAM_INSERTION: main.py -->

<!-- PROGRAM_INSERTION: main2.py -->

## 終わりに

書いた後に気付いたのですが、過去に読んでいた[こちらのpdf](https://www.ism.ac.jp/~mirai/sscoke/2024/marumo-answers.pdf)と全く同じ論文からの引用をしていました。

図があると自分の理解の助けになるので、記事として残しておくことにします。
