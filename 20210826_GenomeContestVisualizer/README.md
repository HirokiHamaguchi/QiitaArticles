# ゲノコン

## 概要

注意 本記事は **「ゲノコン2021 ー DNA配列解析チャレンジ」** に参加されている方を想定読者としています。

https://atcoder.jp/contests/genocon2021/tasks/genocon2021_c

この練習問題Cのビジュアライザを作りました。
また、壊れているかも知れません。使用は自己責任でお願いします。
windows環境で、かつpythonの実行環境をお持ちの方を主に想定しています。多分macでも動くと思いますが。

## 使用方法

下のコードをcopy and pasteした上で、vis.pyとして保存し、
コマンドラインなどでpython vis.py out.txt PRIMARYなどとして実行してください。
(windows powershellなどを使用している場合はpy vis.py out.txt PRIMARYなど)
最後の引数(PRIMARY)は他にSOFTとBWがあります。(記事末尾参照)

out.txtは一行目に行数、二行目以降に出力を書いてください。

例

```out.txt
10
GGAGGTTA-TTGCT--GTGGAG-GTAC-TGGAGA-AGGA-GGA-TGCTAGCG-TT-GGGT-AAACCAC-G-AGC-ATTTTGACTT-G-T-ACT--TC-GCCTC----
--GGGTTA-TTGCT--GTTGTGAGTAC-TGGAGACAGGAGGGAGTGTTAGAG-TTGGGGT-AAACCACAGTAGCTCATGTCACTTGGATAACTCGTCAGCCTC----
---GGTCACTCGCT--GTGGAGAGTACTTTGAGACAGGAGGGAGTGCTAGAGTTTGGGGTAAAACCACAGCAGCTCATG-CACTTGGATATCT-GTGAG-C-C----
-GAGGTTA-GTGCT--GTGGAGAGTAC-TGGAGACAGGAGGGAGTGCTAGAG-TTGGGGT-AAAGCACAGCA-CCATTCACTGATAAATGTCAGGCCTAGGGG----
--GAGGTA-TTGCT--GTGGAGGGTAC-TGGAGACAGGA-GGAGTGCTAGAGGTTGGGGTAAAACCACAGCAGCTCAT-TTACTT-GAT-ACT-GTCAGGCTC-AGG
-GAGGTTATTTGCT--GTGGAGAGTTACT-GAGACA--TGGG-GTGCCA-AG-TT-GGGT--AGCTACAGCAGCTCATTTCACTT-GAT-ACT-G-CAGGCTCTCAG
--GAGTTAATTTC---GTGGAGAGTACTAGAGCACAGGAGGGAG-GCCAGA--TTGGGGT-ATACCACAGCAGCTCGT-TCACTT---TAACT-GTCAGGC-CCTCA
ACAGTTTAATTGATGGGCGGAGAGTAC-TGGAGACAGGAGGGAGTGCTAGAG--TGGGGT-AAACCACAGCAGCATCTTTCA-TT--ATAACT-GTCAG--------
CAAGGTT-TTTTCGCTGTGGAGAGTAC-TGGAGAC-CG-GGGAGTG-TAGACTTTGGGGT---ATCAC-GTAG--CAGCTTATTTCG--ACTTTGT-A--CT-GTAA
--GAGTTA-TTTCT--GTGGAGAGAAC-TGGAGAC-GGAGGGAGTGCTAGAG-TTGGGGT-AAACACCAGGCAGCCATTTCACTT-GATAACT-GTCAGGC-C--TT
```

## コード

```vis.py
import os
import sys
import math
from collections import Counter
from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

A, C, G, T = 0, 1, 2, 3
NAN = 4
INF = 10**9+7
ACGT = "ACGT"


def parse_for_input(x):
    # 便宜の為数字に変換
    if x == "A":
        return A
    elif x == "C":
        return C
    elif x == "G":
        return G
    elif x == "T":
        return T
    elif x == "-":
        return NAN
    else:
        assert False, f"inputted character\"{x}\" is not valid."


def parse_for_output(ans: list) -> tuple:
    # 便宜のため数字に変換したのを元に戻す
    return "".join([ACGT[x] if x != NAN else "-" for x in ans])


def calc_score(N, M, output_Ss):
    # スコア計算 C_allは問題文のものと同一 S_allは結局何が一番多かったか(つまり、復元された配列)
    S_all = []
    C_all = 0
    for j in range(N):
        char, cnt = Counter([output_Ss[i][j]
                             for i in range(M)]).most_common()[0]
        S_all.append(char)
        C_all += M-cnt
    if 0 <= M <= 10:
        score = max(0, 200-math.floor(C_all*0.2))
    elif 35 <= M <= 40:
        score = max(0, 700-math.floor(C_all*0.1))
    else:
        raise AssertionError(f"M:{M}")
    return score, S_all


def main(path, color_mode=None):
    with open(path) as f:
        M = int(f.readline())
        output_Ss = [list(map(parse_for_input, f.readline()[:-1]))
                     for _ in range(M)]

    N = len(output_Ss[0])
    assert all([N == len(output_Ss[i]) for i in range(M)]),\
        "The Ss does not have the same length"

    if color_mode == "PRIMARY" or color_mode is None:
        colors = ['red', 'blue', 'green', 'orange', 'white']
    elif color_mode == "SOFT":
        colors = ['#ff7f7f', '#7f7fff', '#7fff7f', '#ffff7f', '#ffffff']
    else:
        colors = ['#101010', '#404040', '#808080', '#c0c0c0', '#ffffff']
    cmap = ListedColormap(colors, name="custom")

    score, S_all = calc_score(N, M, output_Ss)

    xticks = [0.5+i for i in range(0, N, 10)]
    xticklabels = list(map(str, range(1, N+1, 10)))
    yticks = [M-(0.5+i) for i in range(M)]
    yticklabels = list(map(str, range(1, M+1)))

    z = output_Ss
    z.reverse()

    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=2,
                             width_ratios=[9, 1],
                             height_ratios=[M, 1])

    # メイン部分
    ax1 = fig.add_subplot(spec[0, 0],
                          title=f"Score:{score}",
                          xticks=xticks,
                          xticklabels=xticklabels,
                          yticks=yticks,
                          yticklabels=yticklabels)
    ax1.pcolormesh(z, cmap=cmap)

    # S_all部分
    ax2 = fig.add_subplot(spec[1, 0],
                          sharex=ax1,
                          yticks=[0.5],
                          yticklabels=["all"])
    ax2.pcolormesh([S_all], cmap=cmap)

    # 凡例部分
    ax3 = fig.add_subplot(spec[:, 1],
                          xticks=[],
                          yticks=[])
    ax3.pcolormesh([[NAN], [T], [G], [C], [A]], cmap=cmap)
    ax3.text(0.5, 4.5, "A", ha='center', va='center')
    ax3.text(0.5, 3.5, "C", ha='center', va='center')
    ax3.text(0.5, 2.5, "G", ha='center', va='center')
    ax3.text(0.5, 1.5, "T", ha='center', va='center')
    ax3.text(0.5, 0.5, "NAN", ha='center', va='center')

    plt.show()


if __name__ == '__main__':
    args = sys.argv
    if not os.path.exists(args[1]):
        raise AssertionError("指定されたパスが存在しないようです。 "
                             + "python vis.py \"out.txt\"などとしてみて下さい。")

    if len(args) == 2:
        main(args[1])
    elif len(args) == 3:
        if args[2] not in ["PRIMARY", "SOFT", "BW"]:
            raise AssertionError(f"{args[1]};色の指定方法が正しくありません。 "
                                 + "\"PRIMARY\",\"SOFT\",\"BW\"からお選びください。")
        main(args[1], args[2])
    else:
        sys.stderr.write(args, "\n")
        sys.stderr.write(
            "実行方法が異なります python vis.py out.txt PRIMARY などとしてみて下さい。")
```

## 使用例

いずれも問題文にある出力例です。

### PRIMARY

![PRIMARY.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/48e05408-ef39-c8cd-2f2d-22cf3b2faaf6.png)

### SOFT

![SOFT.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/f76dd92d-d60c-f065-7565-13556bbf9c8f.png)

### BW

![BW.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/0691d383-2a16-5781-fdf4-16d2a8e4b6c3.png)

## 余談

意外と「こうすれば線が揃うのに!」みたいなのが分かりやすい気がしませんか? 私はします。お役に立てば幸いです。
