# Reply 1

Thanks for the comment. The minimum working example (MWE) is to compile the following code with pLaTeX or upLaTeX.

```latex
\documentclass[12pt,dvipdfmx]{article}

\usepackage{hyperref}
\usepackage{orcidlink}
\usepackage{tikz}

\begin{document}

orcidlink icon: \href{https://orcid.org/0009-0005-7348-1356}{\orcidlink{0009-0005-7348-1356}}\\

TikZ figure wrapped by \texttt{\string\XeTeXLinkBox}:
\href{https://example.com}{%
    \XeTeXLinkBox{%
        \begin{tikzpicture}[scale=0.8]
            \draw[fill=blue!20] (0,0) circle (1);
            \draw[fill=red!40] (-0.7,-0.7) rectangle (0.7,0.7);
        \end{tikzpicture}%
    }%
}

\end{document}
```

The two objects (the ORCID icon and the TikZ figure) are wrapped by `\XeTeXLinkBox`, but do not work as hyperlinks. ([mwe_platex.pdf](https://github.com/HirokiHamaguchi/QiitaArticles/tree/main/20260313_orcidlink/reply1_mwe/mwe_platex.pdf))
