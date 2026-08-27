# Generalized Cauchy Point

文献:

https://doi.org/10.1007/978-0-387-40065-5

https://doi.org/10.1137/0916069

スクショ:

Wright, Stephen J., and Jorge Nocedal. "Numerical optimization." における説明

![_GeneralizedCauchyPoint_Numerical-Optimization.png](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GeneralizedCauchyPoint_Numerical-Optimization.png)

Richard H. Byrd, Peihuang Lu, Jorge Nocedal, and Ciyou Zhu. "A Limited Memory Algorithm for Bound Constrained Optimization." における説明

![_GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-1](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-1.png)

![_GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-2](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-2.png)

![_GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-3](https://raw.githubusercontent.com/HirokiHamaguchi/QiitaArticles/main/20260827_OptimizationWords/_GeneralizedCauchyPoint_A-Limited-Memory-Algorithm-for-Bound-Constrained-Optimization-3.png)

解説:

この用語は正式な用語と言えるかどうかやや怪しく、注意が必要。

まず、Wright, Stephen J., and Jorge Nocedal. "Numerical optimization." の方で触れられているのは、信頼領域法の文脈においてであり、定義もやや曖昧である。

[これ](https://math.stackexchange.com/questions/2432486/generalized-cauchy-point-calculation)などが参考になるかも知れない。

Richard H. Byrd, Peihuang Lu, Jorge Nocedal, and Ciyou Zhu. "A Limited Memory Algorithm for Bound Constrained Optimization." の方では、少なくとも私の理解する限りにおいて異なる定義がされているように思われる。

後者の方は、SciPyのL-BFGS-B法の実装において重要な概念であり、実際に[コメント](https://github.com/scipy/scipy/blob/cacd2b498be80256532b8751f74a1bdba0c7880d/scipy/optimize/src/lbfgsb.c#L614)で参照されている。

こちらの文脈に基づいて記すと、このGCPはかなり偉い。
Box制約、つまり変数 $x$ の第 $i$ 成分が $l_i \leq x_i \leq u_i$ という制約が複数ある状況を考える。
制約なしで求まった準ニュートン方向に対し、それがBox外に出てしまうとしよう。
この時、純粋にはBoxに対する射影を考えて、それを次の反復点とするのが自然な考え方である。
しかし、この点は実は最適ではない。適切に2次元上で図を描くと簡単な反例があることはすぐ分かる。
GCPでは、Box制約に沿って折れ曲がりながら伸びていく領域において、陽に構築された目的関数の2次近似の最小値を求めるとしている。
これは私も実験したが、単純な射影よりも優れた反復点を返すので、全体の計算時間で見てもかなり速い。
また、その為のアルゴリズムとしてL-BFGSの低ランク性を活用しており、そこも偉いポイントである。

ただ、偉すぎるが故にやや複雑なのが難点である。
