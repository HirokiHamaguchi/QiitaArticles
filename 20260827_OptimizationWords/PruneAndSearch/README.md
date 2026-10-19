# Prune and Search

文献:

https://en.wikipedia.org/wiki/Prune_and_search

https://qiita.com/zhidao/items/48c07500d8cde00ba4a1

解説:

制約数に対して線形時間のLPソルバー。ただし、固定低次元に限る。MegiddoとDyerの名を冠することが多い。

IEEEの[Low-dimensional linear programming with violations](https://ieeexplore.ieee.org/document/1181981)という論文では、次のように記述されている。

> Megiddo (1984) and Dyer (1984) showed that linear programming in 2 and 3 dimensions (and subsequently, any constant number of dimensions) can be solved in linear time.

2次元ということで、パッと凸包が思い出されるが、あれは未整列な $n$ 点が与えられたときに $\mathcal{O}(n \log n)$ かかっていた。これはそういう手法とは異なり、名前の通り、理論保証付きの枝刈りをしていって、重要な制約だけを残していくことに本質がある。面白い。
