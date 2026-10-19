# R-Convergence

文献:

https://en.wikipedia.org/wiki/Rate_of_convergence

解説:

Q-convergenceよりも緩くて扱いやすい収束の概念。

数列 $x_k\to L$ の誤差を $e_k=\|x_k-L\|$ とする。

Q-convergence（Quotient convergence）: $\lim_{k\to\infty} e_{k+1} / e_k^q = \mu$

例えば $q=1$、$0<\mu<1$ なら Q-linear convergence（Q線形収束）。

R-convergence（Root convergence）: $e_k\leq\varepsilon_k$ (ただし、$\varepsilon_k$ は Q-convergence する数列)

例えば、R-linear convergenceなら、$\varepsilon_k$ も Q-linear convergence する必要があり、その$k$-th rootを考えると $\limsup_{k\to\infty} e_k^{1/k} \leq \mu < 1$ となる。これがRの由来。

具体例として、$x_k=4^{-\lfloor k/2\rfloor}$、すなわち、$1$, $1$, $\frac14$, $\frac14$, $\frac1{16}$, $\frac1{16}$, $\ldots$ を考えると、Q線形収束しないが、R線形収束する。
