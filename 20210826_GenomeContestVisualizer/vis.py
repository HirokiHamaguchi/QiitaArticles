import math
import os
import sys

import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.colors import ListedColormap

A, C, G, T = 0, 1, 2, 3
NAN = 4
INF = 10**9 + 7
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
        assert False, f'inputted character"{x}" is not valid.'


def parse_for_output(ans: list) -> tuple:
    # 便宜のため数字に変換したのを元に戻す
    return "".join([ACGT[x] if x != NAN else "-" for x in ans])


def most_common(DNAs: list, idx: int, with_cnt=False) -> tuple:
    """
    DNAsのidx番目では、ACGT-の内、どれが最も多かったか、および、そのカウントを返す
    一個の[int;5]でやるならidx=0にする
    返り値はchar,(max_cnt)
    """
    cnt = [0, 0, 0, 0, 0]  # それぞれACGT-に対応
    for dna in DNAs:
        cnt[dna[idx]] += 1
    max_cnt = max(cnt)
    char = cnt.index(max_cnt)
    if not with_cnt:
        return char, max_cnt
    else:
        return cnt


# B問題のsim関数に準拠
PARM_SAME = 1  # AAなど
PARM_DIFFERENT = -3  # ACなど
PARM_NAN = -5  # A-など
PARM_NAN_NAN = -5  # --のみ


def similarity(
    a: int,
    b: int,
    same=PARM_SAME,
    different=PARM_DIFFERENT,
    nan=PARM_NAN,
    nan_nan=PARM_NAN_NAN,
) -> int:
    if a == b:
        if a != NAN:
            return same
        else:
            return nan_nan
    elif a == NAN or b == NAN:
        return nan
    else:
        return different


def dp_func(DNA1: list, DNA2: list, unstable=20) -> tuple:
    # dp[i][j] sをi文字目、tをj文字目まで見た場合の最大のペアワイズアライメント
    dp = [[-INF for _ in range(len(DNA2) + 1)] for _ in range(len(DNA1) + 1)]
    rev = [[(0, 0) for _ in range(len(DNA2) + 1)] for _ in range(len(DNA1) + 1)]
    dp[0][0] = 0

    if unstable > 0:  # 枝刈りを設けるか
        sup = max(unstable, 3 * (abs(len(DNA1) - len(DNA2))))
    else:
        sup = INF

    for i in range(1, min(len(DNA1) + 1, sup)):
        dp[i][0] = dp[i - 1][0] + PARM_NAN
        rev[i][0] = (-1, 0)
    for j in range(1, min(len(DNA2) + 1, sup)):
        dp[0][j] = dp[0][j - 1] + PARM_NAN
        rev[0][j] = (0, -1)
    for i in range(1, len(DNA1) + 1):
        for j in range(max(1, i - sup), min(len(DNA2) + 1, i + sup)):
            a = dp[i - 1][j - 1] + similarity(DNA1[i - 1], DNA2[j - 1])
            b = dp[i - 1][j] + similarity(DNA1[i - 1], NAN)
            c = dp[i][j - 1] + similarity(NAN, DNA2[j - 1])
            if a > b and a > c:
                dp[i][j] = a
                rev[i][j] = (-1, -1)
            elif b > c:
                dp[i][j] = b
                rev[i][j] = (-1, 0)
            else:
                dp[i][j] = c
                rev[i][j] = (0, -1)
    del a, b, c
    ans_value = dp[len(DNA1)][len(DNA2)]
    return ans_value, rev


def dp_re_func(DNA1: list, DNA2: list, rev: list) -> tuple:
    # dpの復元
    ans_1 = []
    ans_2 = []
    i = len(DNA1)
    j = len(DNA2)
    while i > 0 or j > 0:
        delta_i, delta_j = rev[i][j]
        i += delta_i
        j += delta_j
        ans_1.append(DNA1[i] if delta_i == -1 else NAN)
        ans_2.append(DNA2[j] if delta_j == -1 else NAN)
    ans_1.reverse()
    ans_2.reverse()
    return (ans_1, ans_2)


def dp_re_func_only_one(DNA1: list, DNA2: list, rev: list, return1: bool) -> list:
    ans = []
    i = len(DNA1)
    j = len(DNA2)
    while i > 0 or j > 0:
        delta_i, delta_j = rev[i][j]
        i += delta_i
        j += delta_j
        if return1:
            ans.append(DNA1[i] if delta_i == -1 else NAN)
        else:
            ans.append(DNA2[j] if delta_j == -1 else NAN)
    ans.reverse()
    return ans


def calc_score(N: int, M: int, DNAs: list):
    """
    スコア計算 C_allは問題文のものと同一 S_allは結局何が一番多かったか(つまり、復元された配列)

    NはDNAの長さ
    MはDNAの個数
    output_DNAは[[int;N];M] 全てのDNAが同じ長さを有するとする
    """
    assert set(len(dna) for dna in DNAs) == set([N]), (
        f"{N},{[len(dna) for dna in DNAs]}"
    )
    S_all = []
    C_all = 0
    for j in range(N):
        char, cnt = most_common(DNAs, j)
        S_all.append(char)
        C_all += M - cnt
    if 0 <= M <= 10:
        score = max(0, 200 - math.floor(C_all * 0.2))
    elif 35 <= M <= 40:
        score = max(0, 700 - math.floor(C_all * 0.1))
    else:
        raise AssertionError(
            f"M:{M} このAssertionErrorは外しても問題ありませんが、"
            + "その際スコアは-1になり、かつＭが2前後だと、表示がバグる可能性があります。"
        )
        # score = -1  # AssertionErrorを外す場合、これをコメントアウトしてください。

        # 具体的に言うと、ACGT-の全種類がグラフに登場しないと、cmapの配分がズレてしまい、
        # AがAの色以外で表示されてしまうなどのことが発生します。 すいません。。。
    return score, S_all


def make_the_difference_of_two_DNAs(M, DNAs1, DNAs2):
    score1, S_all_1 = calc_score(len(DNAs1[0]), M, DNAs1)
    score2, S_all_2 = calc_score(len(DNAs2[0]), M, DNAs2)
    _ans_value, rev = dp_func(S_all_1, S_all_2)
    for i, dna in enumerate(DNAs1):
        DNAs1[i] = dp_re_func_only_one(dna, S_all_2, rev, return1=True)
    for i, dna in enumerate(DNAs2):
        DNAs2[i] = dp_re_func_only_one(S_all_1, dna, rev, return1=False)
    difference = [[False for _ in range(len(DNAs1[0]))] for _ in range(M)]
    for dna_idx in range(M):
        for char_idx in range(len(DNAs1[0])):
            if DNAs1[dna_idx][char_idx] != DNAs2[dna_idx][char_idx]:
                difference[dna_idx][char_idx] = True
    return score1, score2, DNAs1, DNAs2, difference


def vis(M, DNAs, color_mode=None):
    N = len(DNAs[0])
    assert all([N == len(DNAs[i]) for i in range(M)]), (
        "The Ss does not have the same length"
    )

    if color_mode == "PRIMARY" or color_mode is None:
        colors = ["red", "blue", "green", "orange", "white"]
    elif color_mode == "SOFT":
        colors = ["#ff7f7f", "#7f7fff", "#7fff7f", "#ffff7f", "#ffffff"]
    else:
        colors = ["#101010", "#404040", "#808080", "#c0c0c0", "#ffffff"]
    cmap = ListedColormap(colors, name="custom")

    score, S_all = calc_score(N, M, DNAs)

    xticks = [0.5 + i for i in range(0, N, 10)]
    xticklabels = list(map(str, range(1, N + 1, 10)))
    yticks = [M - (0.5 + i) for i in range(M)]
    yticklabels = list(map(str, range(1, M + 1)))

    z = DNAs
    z.reverse()

    fig = plt.figure()
    spec = gridspec.GridSpec(
        ncols=2, nrows=2, width_ratios=[9, 1], height_ratios=[M, 1]
    )

    # メイン部分
    ax1 = fig.add_subplot(
        spec[0, 0],
        title=f"Score:{score}",
        xticks=xticks,
        xticklabels=xticklabels,
        yticks=yticks,
        yticklabels=yticklabels,
    )
    ax1.pcolormesh(z, cmap=cmap)

    # S_all部分
    ax2 = fig.add_subplot(spec[1, 0], sharex=ax1, yticks=[0.5], yticklabels=["all"])
    ax2.pcolormesh([S_all], cmap=cmap)

    # 凡例部分
    ax3 = fig.add_subplot(spec[:, 1], xticks=[], yticks=[])
    ax3.pcolormesh([[NAN], [T], [G], [C], [A]], cmap=cmap)
    ax3.text(0.5, 4.5, "A", ha="center", va="center")
    ax3.text(0.5, 3.5, "C", ha="center", va="center")
    ax3.text(0.5, 2.5, "G", ha="center", va="center")
    ax3.text(0.5, 1.5, "T", ha="center", va="center")
    ax3.text(0.5, 0.5, "NAN", ha="center", va="center")

    z.reverse()  # 一度reverseしてしまったため、また、後で再利用するため、もう一度reverse

    plt.show()


def vis_difference(
    M: int,
    score1: int,
    score2: int,
    DNAs1: list,
    DNAs2: list,
    difference: list,
    color_mode=None,
):
    N = len(DNAs1[0])
    assert set([len(dna) for dna in DNAs1] + [len(dna) for dna in DNAs2]) == set([N]), (
        "The DNAs does not have the same length"
    )

    if color_mode == "PRIMARY" or color_mode is None:
        colors = ["red", "blue", "green", "orange", "white"]
    elif color_mode == "SOFT":
        colors = ["#ff7f7f", "#7f7fff", "#7fff7f", "#ffff7f", "#ffffff"]
    else:
        colors = ["#101010", "#404040", "#808080", "#c0c0c0", "#ffffff"]
    cmap = ListedColormap(colors, name="custom")

    xticks = [0.5 + i for i in range(0, N, 10)]
    xticklabels = list(map(str, range(1, N + 1, 10)))
    yticks = [M - (0.5 + i) for i in range(M)]
    yticklabels = list(map(str, range(1, M + 1)))

    DNAs1.reverse()
    DNAs2.reverse()
    difference.reverse()

    fig = plt.figure()

    # メイン部分
    ax = fig.add_subplot(
        title=f"score1:{score1},score2:{score2}",
        xticks=xticks,
        xticklabels=xticklabels,
        yticks=yticks,
        yticklabels=yticklabels,
    )
    ax.pcolormesh(DNAs1, cmap=cmap, alpha=0.5)
    ax.pcolormesh(DNAs2, cmap=cmap, alpha=0.5)
    for y in range(len(difference)):
        for x in range(len(difference[0])):
            if difference[y][x]:
                ax.text(x + 0.5, y + 0.5, "!", ha="center", va="center")

    plt.show()


def main(args):
    if not os.path.exists(args[1]):
        raise AssertionError(
            "指定されたパスが存在しないようです。 "
            + 'python vis.py "out.txt"などとしてみて下さい。'
        )

    if len(args) == 3 or len(args) == 4:
        if len(args) == 4:
            if args[3] not in ["PRIMARY", "SOFT", "BW"]:
                raise AssertionError(
                    f"{args[1]};色の指定方法が正しくありません。 "
                    + '"PRIMARY","SOFT","BW"からお選びください。'
                )
            else:
                color_mode = args[3]
        else:
            color_mode = None
        path1 = args[1]
        path2 = args[2]
        with open(path1) as f:
            M_ = int(f.readline())
            DNAs1 = [
                list(map(parse_for_input, f.readline().rstrip("\n"))) for _ in range(M_)
            ]
        with open(path2) as f:
            M = int(f.readline())
            assert M_ == M, "二つのファイルのＭが異なります"
            DNAs2 = [
                list(map(parse_for_input, f.readline().rstrip("\n"))) for _ in range(M)
            ]
        score1, score2, DNAs1, DNAs2, difference = make_the_difference_of_two_DNAs(
            M, DNAs1, DNAs2
        )
        vis(M, DNAs1, color_mode)
        vis(M, DNAs2, color_mode)
        vis_difference(M, score1, score2, DNAs1, DNAs2, difference, color_mode)
    else:
        sys.stderr.write(args, "\n")
        sys.stderr.write(
            "実行方法が異なります python vis.py out.txt PRIMARY などとしてみて下さい。"
        )


if __name__ == "__main__":
    args = sys.argv
    main(args)

# > py vis.py out1.txt out2.txt SOFT
