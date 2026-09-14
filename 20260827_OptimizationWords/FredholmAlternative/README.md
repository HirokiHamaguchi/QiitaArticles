# Fredholm Alternative

文献:

https://en.wikipedia.org/wiki/Fredholm_alternative

![Wiki](Wiki.png)

https://www.ism.ac.jp/~mirai/sscoke/2026/

(松井先生の講義資料, 10ページ辺り)

<!-- ![sscoke2026-tomomi-matsui](sscoke2026-tomomi-matsui.png) -->

解説:

任意の行列 $(A | b)$ に対し、$P: Ax = b$ か $D: y^\top A = 0^\top, y^\top b \neq 0$ のどちらか丁度1つのみが解を持つという定理。証明は簡単で、両方の解を $x^\ast, y^\ast$ として存在を仮定すると、次のように矛盾が導かれる。

$$
0 = 0^\top x^\ast = (y^\ast)^\top A x^\ast = (y^\ast)^\top b \neq 0
$$

これはつまり、$b \in \mathrm{Im}(A)$ と $b \in \mathrm{Ker}(A^\top)^\perp$ が同値ということを言っているに過ぎない。

[Farkas' lemmaのcorollary](https://en.wikipedia.org/wiki/Farkas%27_lemma)として得られる。
