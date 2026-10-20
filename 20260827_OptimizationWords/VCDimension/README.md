# VC Dimension

文献:

https://en.wikipedia.org/wiki/Vapnik%E2%80%93Chervonenkis_dimension

https://qiita.com/fuyu_quant/items/f94c51a00630deff2a80

金森敬文: [統計的学習理論](https://www.kspub.co.jp/book/detail/1529052.html), 講談社 (2015) (MLP機械学習プロフェッショナルシリーズ).

解説:

2値判別のための仮説集合を $\mathcal{H}$、入力空間を $\mathcal{X}$、出力空間を $\mathcal{Y}$ とする。$\{0,1\}$ などのラベル集合を考えているので、$|\mathcal{Y}|=2$ である。

ここで $\{x_1,\ldots,x_n\}\subset\mathcal{X}$ に対し、仮説 $h \in \mathcal{H}$ という関数によって、$\{(h(x_1),\ldots,h(x_n))\in\mathcal{Y}^n\mid h\in\mathcal{H}\}$ を考えると、これは仮説(分類器)がどのようなラベルの組み合わせを出力できるかを表している。

その上で、そのような出力の要素数、つまり、分類器の表現能力を表すものとして、 $\Pi_{\mathcal{H}}(x_1,\ldots,x_n)=|\{(h(x_1),\ldots,h(x_n))\in\mathcal{Y}^n\mid h\in\mathcal{H}\}|$ を定義する。

$\Pi_{\mathcal{H}}(x_1,\ldots,x_n)=2^n$ となれば、それはいかなるラベルの組み合わせも分類器が正しく分類できることを意味する。これは shattering と呼ばれる。

そこで、VC次元を、このような完璧な分類が出来るかどうかの境界となる最大のデータ数として、次のように定義出来る:

$$
\begin{equation*}
    \mathrm{VCdim}(\mathcal{H})=\max\left\{n\in\mathbb{N}\mid\max_{x_1,\ldots,x_n\in\mathcal{X}}\Pi_{\mathcal{H}}(x_1,\ldots,x_n)=2^n\right\}
\end{equation*}
$$

任意の $n$ でshatteringが可能であれば、$\mathrm{VCdim}(\mathcal{H})=\infty$ となる。

最適化文脈では、計算量やオラクル数の下界の文脈で類似の概念が使われることがある。
