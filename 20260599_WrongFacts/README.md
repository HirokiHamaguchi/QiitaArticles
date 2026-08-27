# 大学数学において間違えやすい事実

私はかなり感覚的に数学をやってしまうきらいがあるのですが、それ故に数えきれない間違いの数々を犯してきた自覚があります。
ここにそのうちのいくつかを挙げてみます。

自分の専門が連続最適化なので、幾分か凸解析に内容が偏っていますが、ご容赦ください。

## 集合位相

## 解析

### 1次元上の閉区間とは線分のようなものではない

1点集合が反例です。ある$a \in \bbR$に対して、$[a,a]$は閉区間ですが、これは線分ではなく、点です。

### 閉集合に端があるとは限らない

\bbRが反例です。

### 開集合の連続写像の像は開集合ではない

反例

### 閉集合の凸包は閉集合ではない

例として、(\mathbb{R}^2) で

[
A={(x,y)\in\mathbb{R}^2: x>0,\ y\ge 1/x}\cup{(0,0)}
]

を考えます。

これは **閉集合** です。実際、(x_n>0,\ y_n\ge 1/x_n) で有限な点に収束する列を考えると、もし (x_n\to 0) なら (1/x_n\to\infty) なので (y_n) は有限値に収束できません。したがって有限な極限点はすべて元の集合に入ります。さらに ((0,0)) も加えてあるので閉です。

一方、この集合の凸包は閉ではありません。実際、

[
(0,0)\in A,\qquad (x,1/x)\in A \quad (x>0)
]

なので、任意の (0<t<1) について

[
t(x,1/x)+(1-t)(0,0)=(tx,t/x)
]

は (\operatorname{conv}(A)) に入ります。

ここで (X=tx,\ Y=t/x) とおくと

[
XY=t^2.
]

したがって、任意の (X>0,\ Y>0) に対し、十分小さい (t>0) を選べば (XY=t^2) となるようにできるので、

[
{(X,Y):X>0,\ Y>0}\subset \operatorname{conv}(A).
]

逆に、(A) は第一象限の内部と原点に含まれているので、

[
\operatorname{conv}(A)\subset {(0,0)}\cup{(x,y):x>0,\ y>0}.
]

よって

[
\operatorname{conv}(A)={(0,0)}\cup{(x,y):x>0,\ y>0}.
]

これは閉集合ではありません。例えば

[
(1,1/n)\in \operatorname{conv}(A)
]

ですが、

[
(1,1/n)\to (1,0),
]

かつ ((1,0)\notin \operatorname{conv}(A)) です。

したがって、閉集合 (A) の凸包 (\operatorname{conv}(A)) が閉でない例になっています。


有限次元、たとえば (\mathbb{R}^n) では **はい、閉集合です**。

理由は単純です。

[
A\subset \mathbb{R}^n
]

が有界閉集合なら、Heine–Borel の定理により (A) はコンパクトです。有限次元ではコンパクト集合の凸包もコンパクトなので、

[
\operatorname{conv}(A)
]

はコンパクト、したがって閉集合です。

したがって

[
\boxed{\mathbb{R}^n \text{ では、有界閉集合の凸包は閉集合である。}}
]

もう少し具体的には、Carathéodory の定理により

[
\operatorname{conv}(A)
======================

\left{
\sum_{i=0}^n \lambda_i a_i:
a_i\in A,\ \lambda_i\ge 0,\ \sum_{i=0}^n\lambda_i=1
\right}.
]

右辺はコンパクト集合

[
\Delta_n\times A^{n+1}
]

の連続像なのでコンパクトです。よって閉です。

ただし、**無限次元空間では一般には偽**です。

例として Hilbert 空間 (\ell^2) を考え、標準基底を (e_n) として

[
A={0}\cup{e_n:n\in\mathbb{N}}
]

とおきます。これは (\ell^2) の有界閉集合です。

この凸包は

[
\operatorname{conv}(A)
======================

\left{
x\in \ell^2:
x_n\ge 0,\ x \text{ は有限台},\ \sum_{n=1}^\infty x_n\le 1
\right}.
]

しかし

[
x=\left(\frac12,\frac14,\frac18,\dots\right)
]

は (\ell^2) に属し、

[
x_n\ge 0,\qquad \sum_{n=1}^\infty x_n=1
]

ですが、有限台ではないので

[
x\notin \operatorname{conv}(A).
]

一方、部分和

[
x^{(N)}=\left(\frac12,\frac14,\dots,\frac1{2^N},0,0,\dots\right)
]

は (\operatorname{conv}(A)) に入り、

[
x^{(N)}\to x \quad \text{in } \ell^2.
]

したがって (\operatorname{conv}(A)) は閉ではありません。

結論：

[
\boxed{
\begin{array}{ll}
\mathbb{R}^n \text{ など有限次元では} & \text{有界閉集合の凸包は閉。}\
\text{無限次元ノルム空間では} & \text{一般には閉とは限らない。}
\end{array}
}
]


###　無限次元において、コンパクト集合の凸包はコンパクトとは限らない

有限集合では、コンパクト集合の凸包はコンパクトです。

https://books.google.de/books?id=4hIq6ExH7NoC&pg=PA185&redir_esc=y#v=onepage&q&f=false

Caratheodory.

https://mathoverflow.net/questions/22562/convex-hull-of-finite-set-is-compact

https://math.stackexchange.com/questions/3577490/convex-hull-of-compact-set-is-compact-in-finite-dimensional-complex-vector-space

### 閉凸関数の定義域は閉集合ではない

### 有限個のもので覆えていることがコンパクトではない

### 連続関数の定義はε-δ論法のが定義とは限らない

これも勘違いの内容の補足が先に必要なので、補足します。

### コンパクト集合上の連続関数はリプシッツ連続であるとは限らない

微分可能性が必要です。

## 確率

### 確率変数とは変数ではない

言われてみれば当たり前すぎるというか、定義なのですが、いかんせん慣れていないとどうも理解が難しいです。

### 確率分布は乱数生成器ではない

np.random.normal()は正規分布に従う乱数生成器

z \sim \calN(0,1)は正規分布

## おまけ

ノージャンル

### -1 × -1 = 1は定義ではない

これはまず勘違いの内容を正確に記す必要があります。中学数学を教える文脈で-1 × -1 = 1を定義として教えている人がいたとしても、それを批判する意味では**ありません**。これは大学数学の文脈です。

### B(0,1)は多様体ではない

###

https://x.com/TKT_Yamamoto/status/2051156798120636712
