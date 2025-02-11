1, 5, 10, 50, 100, 500円硬貨を使用してちょうど $p$円支払う最小の硬貨枚数が貪欲法で求められることを厳密に証明します。

またその拡張として、貪欲法が最適解を与える再帰的な必要十分条件に関する既存研究の証明を、日本語でまとめます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/e2c411ec-b204-addb-a3d8-292c3c930665.jpeg" width="100%" alt="combined.jpg">

出典: [財務省通常貨幣一覧](https://www.mof.go.jp/policy/currency/coin/general_coin/list.htm)

## 初めに

$n$枚の硬貨があり、それぞれの価値が $a_1, \\: a_2, \ldots, a_n$ $(a_1 < \dots < a_n)$ 円であるとします。この時、ちょうど$p$円支払う最小の硬貨枚数を求める問題は**Change-Making Problem** (**CMP**) [^Martello]、またはお釣り生成問題[^iida]と呼ばれます。

俗称として、お釣りの枚数の最小化問題[^ebi]・硬貨の組み合わせ問題[^Tech]・コインの問題[^s417]などとも呼ばれ、本記事では分かりやすさの観点から「硬貨枚数の最小化問題」と呼びます。

常にちょうど支払えるよう、本記事では $a_1=1$ とし、各$a_i$円硬貨の支払枚数を$x_i$とします。この時、CMPは以下の最適化問題として定式化されます。

```math
\begin{align*}
\text{(CMP)       minimize} \quad & \sum_{i=1}^n x_i \\
\text{subject to} \quad & \sum_{i=1}^n a_i x_i = p, \\
& x_i \in \mathbb{N} \quad \text{for $1 \leq i \leq n$}.
\end{align*}
```

ここで、「全ての $i \in \lbrace 1, 2, \ldots, n-1 \rbrace$ で $a_{i+1}$ が $a_i$ の倍数」という条件を課します。以下、これを**倍数条件**と呼びます。例えば、現在の日本の硬貨は、5円は1円の倍数、10円は5円の倍数、50円は10円の倍数、……と、確かに倍数条件を満たしています。

倍数条件付きCMPの最適解は、「価値の降順に支払える最大枚数を支払い続ける」という貪欲法で求められることが広く知られ[^s417] [^algoMethod] [^algoLogic]、競プロでも出題があります[^AtCoder]。例えば、123円は100円硬貨1枚、10円硬貨2枚、1円硬貨3枚で支払うのが最適です。しかし、その証明は簡潔なものの厳密に与えるのは容易ではありません。

本記事の前半では、倍数条件付きCMPに対する貪欲法が最適解を与えることについて、証明を複数与えます。証明にあたり多くの着眼点が存在しますが、そのどれであっても証明自体は可能だと示すことが本記事の意義および目的です。ネット上にいくつか類似の記事はありますが、本記事では厳密かつ完全な証明に焦点を当てます。

本記事の後半では、この条件を緩和した場合にも、貪欲法が最適解を与えることが知られており、それについて記します。こちらは文献[^iida]を引用する形で他の複数記事が言及していますが、元論文が孫引きになってしまっている為、情報を日本語でまとめて提供する観点から記します。

## 前半:倍数条件付きCMP

「全ての $i \in \lbrace 1, 2, \ldots, n-1 \rbrace$ で $a_{i+1}$ が $a_i$ の倍数」という倍数条件付きCMPに対して、貪欲法が最適解を与えることを示します。

### 貪欲法の擬似コード

Pythonでの貪欲法の実装は以下の通りです。この貪欲法は「価値の降順に支払える最大枚数を支払い続ける」アルゴリズムになっています。このアルゴリズムの出力結果が問題(CMP)の実行可能解であることは、$a_1=1$ であることから明らかです。

```python
from typing import List

def greedy1(a: List[int], p: int) -> int:
    x = 0
    for ai in reversed(a):
        xi = 0
        while p >= ai:
            xi += 1
            p -= ai
        x += xi
    return x
```

また、より効率的には以下のように実装できます。

```python
from typing import List

def greedy2(a: List[int], p: int) -> int:
    x = 0
    for ai in reversed(a):
        xi = p // ai   # 操作Q
        x += xi
        p %= ai        # 操作R
    return x
```

これら $x = (x_1, \dots, x_n)$ を貪欲解と呼びます。

### 注意するべき点

証明にあたり、倍数条件をきちんと意識する必要があります。倍数条件を無くした場合には貪欲法が必ずしも最適解を与えない為です。

1, 3, 4円硬貨がある時、6円を支払うとします。$n=3,$ $a_1=1,$ $a_2=3,$ $a_3=4,$ $p=6$ となります。

貪欲法だと、4円×1枚+1円×2枚で**3枚**ですが、最適解は3円×2枚で**2枚**です。

この反例に十分に注意しながら、証明を進めます。

### 貪欲解の定式化

便宜上 $a_{n+1}$ を $p$ より真に大きい $a_n$ の倍数とします。当然 $a_{n+1}$円硬貨は使われないので、このような硬貨が存在するとしても問題ありません。いくつかの証明に共通した前提として、以下を示します:

> 貪欲解は
>
> ```math
> x_i = \left\lfloor \frac{p \bmod{a_{i+1}}}{a_i} \right\rfloor
> ```
>
> である。

$i=n$ の場合は明らかです。$i\leq n-1$ において、$x_i$ を求める擬似コード中の `操作Q` の時点で、変数 $p$ の値は `操作R` により $(\dots((p \bmod{a_{n}}) \bmod{a_{n-1}})\dots) \bmod{a_{i+1}}$ ですが、倍数条件よりこれは $p \bmod{a_{i+1}}$ と等しいです。したがって、`操作Q` で $\lfloor \cdot / a_i \rfloor$ という操作がされるので、$x_i$ は上記の値と一致します。

### 証明

CMPの最適解 $x^\*$ が、`greedy1`の出力結果と一致すること、あるいは、`greedy2`の出力結果である $x_i=\left\lfloor (p \bmod{a_{i+1}}) / a_i \right\rfloor$ と一致することを、3通りの方法で示します。

#### 証明1 直接証明

大まかな気持ちとして、100円未満の硬貨で支払う金額は100円未満までであって欲しいです。この条件を満たすには、100円硬貨は使える最大枚数を使わなければならず、これは貪欲解そのものです。これを厳密に示します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/83227fe9-f1a5-3541-2f44-e7d8384f7bea.png" width="100%" alt="fig1.png">

$n=1$ の時、$a_1=1$ なので $x_1=x_1^\*=p$ より最適です。以下、$n \geq 2$ とします。

任意の $i \leq n-1$ に対し、倍数条件より $a_{i+1}/ a_i$ は整数です。もし $x_i^\* \geq a_{i+1}/a_i$ だと、$a_i$円硬貨 $a_{i+1}/a_i$ 枚を $a_{i+1}$円硬貨 $1$枚で両替すれば使用枚数が減るので矛盾します。よって $x_i^\* \in \mathbb{N}$ より、

```math
x_i^* \leq \frac{a_{i+1}}{a_i} -1
```

が成立します。この不等式から、

```math
\sum_{j=1}^{i} a_j x_j^* \leq \sum_{j=1}^{i} (a_{j+1} - a_j) = a_{i+1} - a_1 < a_{i+1}
```

が成立し、$a_{i+1}$円未満の硬貨による最適な支払額は $a_{i+1}$円未満です。

##### 証明 1.1

ここで、$p$ が $a_n$円以上だとします。$a_{n-1}$円以下の硬貨では、高々 $a_n$円未満までしか最適解は支払わない為、$p \geq a_n$ である限り、最適解は $a_n$円硬貨を使い続けます。よって、$n$枚目の最適解 $x_n^\*$ は貪欲解 $x_n$ と一致します。

同様に、全ての $i$ について $x_i^\*=x_i$ が成立し、貪欲解が最適解であることが示されました。

##### 証明 1.2

$\sum_{j=1}^{i} a_j x_j^\* < a_{i+1}$ は $i=n$ でも成立します。ここから $x_i^\* = \lfloor (p \bmod{a_{i+1}}) / a_i \rfloor$ を導きます。支払い金額がちょうど $p$円なので、

```math
\sum_{j=1}^{n} a_j x_j^* = p
```

でした。したがって、倍数条件より、

```math
\begin{align*}
(p \bmod {a_{i+1}}) ={}&
\left( \sum_{j=1}^{n} a_j x_j^* \bmod {a_{i+1}} \right)\\
={}& \left(\sum_{j=1}^{i} a_j x_j^* \bmod {a_{i+1}} \right)\\
={}& \sum_{j=1}^{i} a_j x_j^*\quad (\because a_{i+1}\text{未満})\\
\end{align*}
```

となります。両辺に $\lfloor \cdot / a_i \rfloor$ を適用することで、

```math
\begin{align*}
\left\lfloor \frac{p \bmod{a_{i+1}}}{a_i} \right\rfloor ={}& \left\lfloor \frac{\sum_{j=1}^{i} a_j x_j^*}{a_i} \right\rfloor \\
={}& x_i^* + \left\lfloor \frac{\sum_{j=1}^{i-1} a_j x_j^*}{a_i} \right\rfloor\\
={}& x_i^* \quad \left(\because \sum_{j=1}^{i-1} a_j x_j^* < a_i \right)
\end{align*}
```

である為、

```math
x_i^* = \left\lfloor \frac{p \bmod{a_{i+1}}}{a_i} \right\rfloor
```

が導けました。

#### 証明2 帰納法

大まかな気持ちとして、123円を支払う時、最小価値の硬貨である1円硬貨に着目すると、当然 $(123 \bmod 5) = 3$枚使うべきですし、それは簡単に示せそうです。これを基に価値の昇順に帰納法を回せば良さそうです。これを厳密に示します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/d53942c9-bd59-d76b-8a61-cf51ae18c628.png" width="100%" alt="fig2.png">

$n$ についての帰納法で、最適解が貪欲解に一致することを証明します。

$n=1$ では先述同様明らかです。

$n=k+1$ とします。倍数条件と $a_1=1$ より、$p \equiv \sum_{i=1}^{k+1} a_i x_i^\* \equiv x_1^\* \pmod{a_{2}}$ です。もし $x_1^\* \geq a_2$ だと、$a_1=1$円硬貨 $a_2$ 枚を $a_2$円硬貨1枚で両替すれば使用枚数が減り矛盾します。よって、

```math
x_1^* = (p \bmod{a_{2}}) = \left\lfloor \frac{p \bmod{a_{2}}}{a_1} \right\rfloor
```

となります。

以上より、$p^\prime=p-(p \bmod a_2)$円 を $a^\prime_1=a_2, \\: a^\prime_2=a_3, \\: \dots, \\: a^\prime_k=a_{k+1}$円硬貨の $k$種類で支払う問題に帰着されます（便宜上 $a_{k+1}^\prime$ も適当に定めます）。この問題の最適解は各変数を $a_2$ で割った問題の最適解と等しいことは簡単に確かめられます。帰納法の仮定より $2 \leq i \leq k+1$ について、

```math
\begin{align*}
x_i^* &= \left\lfloor \frac{p^\prime/a_2 \bmod a^\prime_{i}/a_2}{a^\prime_{i-1}/a_2} \right\rfloor \quad (\because \text{帰納法の仮定}) \\
    &= \left\lfloor \frac{p^\prime \bmod a^\prime_{i}}{a^\prime_{i-1}} \right\rfloor \quad (\because \text{剰余演算の性質}) \\
    &= \left\lfloor \frac{(p-(p \bmod a_2)) \bmod a_{i+1}}{a_i} \right\rfloor \quad (\because \text{定義}) \\
    &= \left\lfloor \frac{p \bmod a_{i+1}}{a_i} \right\rfloor \quad (\because \text{倍数条件など})
\end{align*}
```

が導けるので、$n=k+1$ でも成立し、帰納法が回ります。つまり、貪欲法の出力が最適解であることが示されました。

アルゴリズム自体は価値の降順に求めますが、`greedy2`に基づいた帰納法においては、価値の昇順の方が枚数を確定させやすいというのは、意外な点でしょうか。

#### 証明3 貪欲以外の非最適性

大まかな気持ちとして、105円支払う時、100円硬貨は1枚使うべきで、それを50円硬貨2枚で支払うべきではありません。厄介な点は、100円硬貨の不使用は、必ずしも50円硬貨2枚の使用を意味しないことです。しかしその時には、5円硬貨3枚などの無駄が存在することや、100円分ちょうどの硬貨の組合せが存在することは言えて、使用枚数を減らす両替が可能です。これを厳密に示します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/9b56d528-df3b-a1ff-2629-e53e159a95a9.png" width="100%" alt="fig3.png">

問題(CMP)の貪欲解以外の任意の実行可能解 $y = (y_1, \dots, y_n)$ では、ある硬貨が存在して、その価値が $a_t\\:(t>1)$ 円であり、$a_t$円未満の硬貨による支払額が $a_t$円以上です。`greedy1`の`while`文において、$p \geq a_t$を満たしている内に、次の硬貨を使用開始しているような $t>1$ が存在しないと、貪欲解に一致するからです。

解 $y$ が上記性質を持つならば、非最適であることを示します（証明1で示した事実の対偶になっており、本質的に等価です）。

#### 証明 3.1

「$y_i \geq a_{i+1}/a_i$ なる $i$ が存在する」ことを示します。このような $i$ が存在するとき、証明1と同様に $a_i$円硬貨 $a_{i+1}/a_i$枚を $a_{i+1}$円硬貨 $1$枚で両替すれば、使用枚数が減ります。つまり、貪欲解以外は非最適です。

$t$ 未満の全ての $i$ について、$y_i \leq a_{i+1}/a_i -1$ と仮定します。この時、

```math
\begin{align*}
\sum_{i=1}^{t-1} a_i y_i &\leq \sum_{i=1}^{t-1} a_i \left( \frac{a_{i+1}}{a_i} - 1 \right) \\
&= \sum_{i=1}^{t-1} (a_{i+1} - a_i) \\
&= a_t - a_1 \\
&< a_t
\end{align*}
```

であり、

```math
\sum_{i=1}^{t-1} a_i y_i \geq a_t
```

という上記性質に矛盾します。したがって、「$y_i \geq a_{i+1}/a_i$ なる $i$ が存在する」ことが示され、貪欲解以外は非最適だと示されました。

#### 証明 3.2

「$a_t$円未満の硬貨による支払額が $a_t$円以上ならば、そこからちょうど $a_t$円を支払うような硬貨の組合せが存在する」ことを示します。これが言えれば、その分を $a_t$円硬貨で両替することで使用枚数が減り、非最適だと示されます。

$1 \leq i \leq t-1$ について、$a_i$円硬貨を $y_i$枚使い、$a_t$円以上を支払っているとします。つまり、

```math
\sum_{i=1}^{t-1} a_i y_i \geq a_t
```

です。ここで、$a_t > 0$ なので、

```math
\begin{align*}
\sum_{i=s+1}^{t-1} a_i y_i <{}& a_t \\
\sum_{i=s}^{t-1} a_i y_i \geq{}& a_t
\end{align*}
```

を満たす $s$ が存在します。変形して、

```math
\begin{gather*}
a_t - \sum_{i=s+1}^{t-1} a_i y_i > 0\\
y_s \geq \frac{a_t - \sum_{i=s+1}^{t-1} a_i y_i}{a_s}
\end{gather*}
```

より、$a_s$円硬貨 $y_s$枚の内、

```math
\frac{a_t - \sum_{i=s+1}^{t-1} a_i y_i}{a_s}
```

枚が取り出せます。これは倍数条件より自然数です。以上より、

```math
\begin{align*}
a_t \text{円} = {}& a_s \text{円} \times \frac{a_t - \sum_{i=s+1}^{t-1} a_i y_i}{a_s} \text{枚}\\
& + \sum_{i=s+1}^{t-1} (a_i \text{円} \times y_i \text{枚})
\end{align*}
```

となる為、「$a_t$円未満の硬貨による支払額が $a_t$円以上ならば、そこからちょうど $a_t$円を支払うような硬貨の組合せが存在する」ことが示され、 $a_t$円硬貨と両替すれば使用枚数が減ります。

以上より、貪欲解以外は非最適、つまり、貪欲解が最適だと示されました。

### 前半まとめ

倍数条件付きCMPに対して、貪欲法が最適解を与えることを、3通りの証明で示しました。

証明1.1のみ文献[^stackexchange]を参考にしましたが、他の証明は独自に書いたので、誤りや簡略化の余地があるかもしれません。もしそうであれば、ご指摘いただけると幸いです。

なお、証明方法は多岐にわたりますが、その本質は恐らくかなりシンプルで、「両替操作で損をしない」というのが鍵になっていると私は考えています。下図も参照して下さい。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/acfbc1b7-b19e-a06b-4425-18e686393823.png" width="100%" alt="fig5.png">

いわゆる貪欲法証明の典型[^penguin]と通じるものがあり、非常に面白いです。

## 後半:再帰的な必要十分条件付きCMP

話の後半に移ります。

ネット上の先行記事を参照したところ、整数ナップサック問題の特殊な場合としてCMPを扱い、貪欲法の最適性が示せるとしてる記事が複数見受けられました。飯田氏の論文[^iida]を引用したもので、その論文ではHu, Lenardによる1976年の結果[^Hu]を引用しています。なお、これはMagazine et al. による1975年の結果[^Magazine]の簡略化です。

問題(CMP)より広いクラスの問題として、以下の整数ナップサック問題があります。

```math
\begin{align*}
\text{(KP)       minimize} \quad & \sum_{i=1}^n c_i x_i \\
\text{subject to} \quad & \sum_{i=1}^n a_i x_i = p, \\
& x_i \in \mathbb{N} \quad \text{for $1 \leq i \leq n$}.
\end{align*}
```

つまり、$a_i$円の硬貨が1枚あたり $c_i$ のコストを持つ最適化問題です。$c_i=1$ の時、問題(KP)は問題(CMP)に一致します。文献[^Hu]では、$c_i$ も含めて貪欲法が最適解を与える条件を示していますが、本記事の主眼がCMPにある為、その結果を $c_i=1$ の場合に限定して記します。

$1 = a_1 < a_2 < \dots < a_n$ という条件を先程同様に課しておきます。

この時、倍数条件の代わりに、ある緩和された条件を課したとしても、貪欲法が最適解を与えます。本記事の後半では、そのような場合を考えていきます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/26832d83-ebe4-1db2-b3e2-f9bb9f5d6e31.png" width="100%" alt="fig4.png">

出典: [Euro coins](https://en.wikipedia.org/wiki/Euro_coins) （緩和条件を満たす 1, 2, 5ユーロセント）

### 主張

$p\in \mathbb{N}, \\: i \in \lbrace 1, 2, \ldots, n \rbrace$ とします。

$\mathrm{OPT}\_i(p)$ は $p$円を $a_1, \\: a_2, \\: \dots, \\: a_i$円硬貨で支払う際の最小枚数と定義します。

$\mathrm{GRE}\_i(p)$ は $p$円を $a_1, \\: a_2, \\: \dots, \\: a_i$円硬貨で支払う際の貪欲法の出力枚数と定義します。

全ての $i \in \lbrace 1, 2, \ldots, n-1 \rbrace$ に対して、

```math
a_{i+1} = \rho_i a_i - \delta_i \quad (0 \leq \delta_i < a_i)
```

を満たすものとして、$\rho_i, \\: \delta_i$ を定義します。

この時、以下が成立します。

> 全ての $i \in \lbrace 1, 2, \ldots, n-1 \rbrace$ で $\mathrm{GRE}\_i(\delta_i) < \rho_i$ が成り立つとする。この時、任意の $p \in \mathbb{N}$ に対し、
>
> ```math
> \mathrm{GRE}_n(p) = \mathrm{OPT}_n(p)
> ```
>
> が成り立つ。つまり、貪欲法が最適解を与える。

以下、「全ての $i \in \lbrace 1, 2, \ldots, n-1 \rbrace$ で $\mathrm{GRE}\_i(\delta_i) < \rho_i$ が成り立つ」という条件を**緩和条件**と呼びます。

### 主張の証明

$n$ に関する帰納法で示します。

$n=1$ の時、$\mathrm{GRE}\_1(p)=\mathrm{OPT}\_1(p)=p$ より明らかです。

$n=k$ の時、$\mathrm{GRE}\_k(p)=\mathrm{OPT}\_k(p)$ が任意の $p \in \mathbb{N}$ に対して成立すると仮定します。

硬貨の種類数を増やすと貪欲法が悪化する状況を考えます。つまり、ある $\overline{p}$ に対し、$\mathrm{GRE}\_{k+1}(\overline{p}) > \mathrm{GRE}\_k(\overline{p})$ を仮定します。ただし、$\overline{p}$ はこの仮定を満たす最小の金額とします。

$\overline{p}<a_{k+1}$ ならば $\mathrm{GRE}\_{k+1}(\overline{p}) = \mathrm{GRE}\_k(\overline{p})$ が成立し矛盾、
$\overline{p} = a_{k+1}$ ならば $\mathrm{GRE}\_{k+1}(\overline{p}) = 1 < \mathrm{GRE}\_k(\overline{p})$ より矛盾です。

したがって、$\overline{p} > a_{k+1}$ であり、

```math
\begin{align*}
            &\mathrm{GRE}_{k+1}(\overline{p}) > \mathrm{GRE}_k(\overline{p}) \\
\Rightarrow {} & \mathrm{GRE}_{k+1}(\overline{p} - a_{k+1}) \geq \mathrm{GRE}_k(\overline{p})\\
\Rightarrow {} & \mathrm{GRE}_{k}(\overline{p} - a_{k+1}) \geq \mathrm{GRE}_k(\overline{p}) \\
              & (\because \text{$\overline{p}$未満では種類数減少で非改善})\\
\Rightarrow {} & \mathrm{GRE}_k(\delta_k) + \mathrm{GRE}_k(\overline{p} - a_{k+1}) \geq \mathrm{GRE}_k(\delta_k) + \mathrm{GRE}_k(\overline{p})\\
\Rightarrow {} & \mathrm{GRE}_k(\delta_k) + \mathrm{GRE}_k(\overline{p} - a_{k+1}) \geq \mathrm{GRE}_k(\delta_k + \overline{p})\\
            & (\because \text{帰納法の仮定である $\mathrm{GRE}_k$ の最適性})\\
\end{align*}
```

と評価できます。また、$a_{k+1}= \rho_k a_k - \delta_k$ より、$\delta_k + \overline{p} = \rho_k a_k + (\overline{p} - a_{k+1})$ なので、右辺は、

```math
\mathrm{GRE}_k(\delta_k + \overline{p}) = \rho_k + \mathrm{GRE}_k(\overline{p} - a_{k+1})
```

と等しく、

```math
\mathrm{GRE}_k(\delta_k) \geq \rho_k
```

が成立します。これは緩和条件である $\mathrm{GRE}\_k(\delta_k) < \rho_k$ に矛盾するので、結局、硬貨の種類数を増やすと貪欲法が悪化するような状況は存在しません。

次に、帰納法を回すべく $\mathrm{GRE}\_{k+1}(p) = \mathrm{OPT}\_{k+1}(p)$ を示します。

$x_{k+1}^\*$ を $\mathrm{OPT}\_{k+1}(p)$ における $a_{k+1}$円硬貨の枚数とします。
先程の議論より硬貨の種類数を増やしても貪欲法は悪化しないので、

```math
\begin{align*}
   &\mathrm{GRE}_{k}(p-x_{k+1}^*a_{k+1}) \\
\geq{}& \mathrm{GRE}_{k+1}(p-x_{k+1}^*a_{k+1}) \quad (\because \text{先程の議論})\\
\geq{}& \mathrm{OPT}_{k+1}(p-x_{k+1}^*a_{k+1}) \quad (\because \text{$\mathrm{OPT}$ の最適性})\\
={}& \mathrm{OPT}_{k}(p-x_{k+1}^*a_{k+1}) \quad (\because \text{$x_{k+1}^*$ の定義})\\
={}&\mathrm{GRE}_{k}(p-x_{k+1}^*a_{k+1}) \quad (\because \text{帰納法})
\end{align*}
```

です。よって、不等号では等号が成立し、

```math
\mathrm{GRE}_{k+1}(p-x_{k+1}^*a_{k+1}) = \mathrm{OPT}_{k+1}(p-x_{k+1}^*a_{k+1})
```

となります。これより、

```math
\begin{align*}
    & \mathrm{GRE}_{k+1}(p) \\
  = {} & \mathrm{GRE}_{k+1}(p-x_{k+1}^*a_{k+1}) + x_{k+1}^* \quad (\because \text{貪欲法の定義}) \\
  = {} & \mathrm{OPT}_{k+1}(p-x_{k+1}^*a_{k+1}) + x_{k+1}^* \quad (\because \text{上記の関係式}) \\
  = {} & \mathrm{OPT}_{k+1}(p) \quad (\because \text{$x_{k+1}^*$ の定義})
\end{align*}
```

となり、帰納法が回りました。

よって、全ての $p \in \mathbb{N}$ に対して $\mathrm{GRE}\_n(p) = \mathrm{OPT}\_n(p)$ が成り立ち、貪欲法が最適解を与えることが示されました。

原論文をかなり大幅に整理しましたが、本質は変えていないかと思います。理解するのに時間が掛かりましたが、非常に賢い証明ですね。

### 緩和条件を満たす具体例

緩和条件 $\mathrm{GRE}\_i(\delta_i) < \rho_i$ は、倍数条件を包含します。

```math
a_{i+1}= \rho_i a_i - \delta_i \quad (0 \leq \delta_i < a_i)
```

でした。倍数条件が成立するならば、

```math
\mathrm{GRE}_i(\delta_i = 0) = 0 < \rho_i = a_{i+1}/a_i
```

なので、緩和条件が成立しています。

そして、緩和条件は、先に示した1, 2, 5ユーロセントの場合にも成立します。実際、

```math
5 = 3 \times 2 - 1 = \rho_2 \times 2 - \delta_2
```

であり、

```math
\mathrm{GRE}_2(\delta_2=1) = 1 < \rho_2 = 3
```

なので、緩和条件は成立しています。つまり、この場合でも貪欲法は最適解を与えます。

### 緩和条件を満たさない具体例

一方、記事前半でお見せした1, 3, 4円硬貨の場合（6円は2枚で支払うのが最適）では、

```math
4 = 2 \times 3 - 2 = \rho_2 \times 3 - \delta_2
```

であり、

```math
\mathrm{GRE}_2(2) = 2 \geq \rho_2 = 2
```

なので、倍数条件のみならず、緩和条件も満たしません。

実際、ある固定された硬貨の種類数 $k$ で $\mathrm{GRE}\_k(p) = \mathrm{OPT}\_k(p)$ が全ての $p \in \mathbb{N}$ で成立するという前提の下、$\mathrm{GRE}\_{k+1}(p) = \mathrm{OPT}\_{k+1}(p)$ が全ての $p \in \mathbb{N}$ で成立するならば、緩和条件 $\mathrm{GRE}\_k(\delta_k) < \rho_k$ がその $k$ で成立します。つまり、緩和条件は「再帰的な必要十分条件("recursive necessary and sufficient conditions" [^Hu])」 と言えます。

証明の帰納法において、$\mathrm{GRE}\_{k+1}(p) = \mathrm{OPT}\_{k+1}(p)$ が全ての $p\in \mathbb{N}$ で成立するならば、

```math
\begin{align*}
     & \mathrm{GRE}_{k}(\delta_k)\\
= {} & \mathrm{GRE}_{k+1}(\delta_k) \quad (\because \delta_k < a_k < a_{k+1})\\
= {} & \mathrm{GRE}_{k+1}(\rho_k a_k - a_{k+1})\\
= {} & \mathrm{GRE}_{k+1}(\rho_k a_k) -1 \\
= {} & \mathrm{OPT}_{k+1}(\rho_k a_k) -1 \quad (\because \text{仮定}) \\
\leq {} & \mathrm{OPT}_{k}(\rho_k a_k) -1 \quad (\because \mathrm{OPT}_{k+1} \text{の最適性}) \\
= {} & \mathrm{GRE}_{k}(\rho_k a_k) -1 \quad (\because \text{帰納法の仮定})\\
= {} &\rho_k -1 \\
< {} & \rho_k
\end{align*}
```

が成り立ち、

```math
\mathrm{GRE}_{k}(\delta_k) < \rho_k
```

と緩和条件が導かれ、確かに再帰的な必要十分条件だと言えます。

### 注意

ややこしいですが、本記事で述べた主張は「再帰的な必要十分条件」であって、「必要十分条件」ではありません。

$n=5,$ $a_1=1,$ $a_2=2,$ $a_3=4,$ $a_4=5,$ $a_5=8$ の時、貪欲法は最適解を与えますが、緩和条件を満たしません。

実際、$a_{3+1}=5$ と $a_3=4$ に対して、

```math
5 = 2 \times 4 - 3 = \rho_3 \times 4 - \delta_3
```

であり、

```math
\mathrm{GRE}_3(\delta_3=3) =2 \geq \rho_3 = 2
```

と、緩和条件を満たしていません。

$n=4,$ $a_1=1,$ $a_2=2,$ $a_3=4,$ $a_4=5$ の時点で貪欲法は最適解を与えないので、帰納法の前提がそもそも成り立っていない、ということです。

### 直感的理解

緩和条件は、一見すると何を言っているのか分かりにくいですが、前半で述べた「両替操作で損をしない」という直感に繋がります。下図も参照して下さい。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/a64d351e-db07-d57f-ef90-7b24f3a54718.png" width="100%" alt="fig6.png">

倍数条件では、$a_{i+1}$円硬貨の両替として、$a_{i}$円硬貨のみを考えました。

一方、緩和条件では、$a_{i+1}$円硬貨の両替として、$a_{i}$円硬貨と、それ以下の価値の硬貨による $\mathrm{GRE}\_i(\delta_i)$枚を合わせたものを考えている、と直感的には理解出来ます。$\mathrm{GRE}_i(\delta_i) < \rho_i$ は、両替操作によって確かに枚数が減少するということを保証しているのです。

ここまで俯瞰すると、一歩本質的理解に近づけた気がして私は非常に楽しいです。

## 謝辞

本記事は私が受け持っているTA業務を契機として書きました。

守秘義務として、TA業務で知り得た個人情報等は一切記載していません。

しかし、その契機を与えてくれた後輩達に深く感謝の意を表します。

## 通貨の画像について

https://www.mof.go.jp/faq/currency/07af.htm

> デジタルカメラ等で撮影したこれらの画像データをホームページやブログに掲載した場合については、その行為自体は「通貨及証券模造取締法」の取締りの対象とはなりませんが、掲載した写真が印刷された場合には、同法に抵触する可能性がありますので、十分ご注意下さい。

[^Martello]: Martello, S. (1990). Knapsack problems: Algorithms and computer implementations. Section 5.1.

[^iida]: 飯田浩志. (2005). 整数ナップサック問題が多項式時間で解ける特殊な場合を定める条件について. Discussion paper series, 101, 1-7.

[^ebi]: えびちゃんの日記. (2022). [初心者が陥りがちな嘘貪欲やコーナーケースやその他諸々に関して](https://rsk0315.hatenablog.com/entry/2022/08/27/164644).

[^Tech]: Technical Memorandum. (2011). [硬貨の組み合わせ問題（貪欲法の簡単な例題）](https://dminor11th.blogspot.com/2011/04/blog-post_28.html).

[^s417]: s417-lama. (2018). [硬貨の問題が貪欲法で解けるための条件](https://qiita.com/s417-lama/items/0cdd95fddb2067876896).

[^algoMethod]: アルゴ式. [貪欲法とは](https://algo-method.com/descriptions/95).

[^algoLogic]: アルゴリズムロジック. (2020). [貪欲なアルゴリズム（greedy）入門](https://algo-logic.info/greedy/).

[^AtCoder]: AtCoder. (2021). [Factorial Yen Coin](https://atcoder.jp/contests/abc208/tasks/abc208_b).

[^stackexchange]: Misha Lavrov. (2017). [Proving that greedy coin change algorithm gives optimal solution under certain conditions](https://math.stackexchange.com/questions/2433735/proving-that-greedy-coin-change-algorithm-gives-optimal-solution-under-certain-c).

[^penguin]: ぺんぎんメモ. (2020). [貪欲法の証明の典型](https://penguinshunya.hatenablog.com/entry/2020/01/21/093846).

[^Hu]: Hu, T. C., & Lenard, M. L. (1976). Optimality of a heuristic solution for a class of knapsack problems. Operations Research, 24(1), 193-196.

[^Magazine]: Magazine, M. J., Nemhauser, G. L., & Trotter Jr, L. E. (1975). When the greedy solution solves a class of knapsack problems. Operations Research, 23(2), 207-217.
