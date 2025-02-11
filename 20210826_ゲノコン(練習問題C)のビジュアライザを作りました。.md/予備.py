# http://isw3.naist.jp/IS/Kawabata-lab/LECDOC_KINDAI/2009/multi_09Apr21.pdf
# http://isw3.naist.jp/IS/Kawabata-lab/LECDOC_KINDAI/2009/Alignment09Apr14_print.pdf

# C問題メモ

# --GT-T-  --GTT-
# --GT-T-  --GTT-
# -AGT-T-  -AGTT-
# GAG----  --GAG-    これはAGの繋がりを一回切った後で、
# ---T-T-  ---TT-    上図の様にしなければならない

# こういうことを考え始めると、近傍の種類は膨大になり、遷移の制御が極めて厳しくなっていく。
# その点dpはこれらを解決できる。ただ、その際のパラメータには注意が必要で、正確にスコアを最大化するように
# 設計する必要がある。これがＢ問題との相違点。 また、これらの理由につき山登りもキツイ。

# todo progressive alignmentの方の工夫。(結合順序、途中でiterの方を挟むなど。)

import sys
import time
import math
import random

input = sys.stdin.readline
random.seed(64)  # seedを固定しているので、どうしても直らない所は単に時間不足の可能性がある事に注意
A, C, G, T = 0, 1, 2, 3
NAN = 4
INF = 10**9+7
ACGT = "ACGT"


def parse_for_input(x: str) -> int:
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


def write_output(output_DNAs: list) -> None:
    sys.stderr.write("-"*50+"\n")
    print(*["".join([ACGT[x] if x != NAN else "-" for x in dna])
            for dna in output_DNAs], sep="\n")
    return None


PARM_SAME = 1  # AAなど
PARM_DIFFERENT = -2  # ACなど
PARM_NAN = -2  # A-など
PARM_NAN_NAN = -1  # --のみ


def similarity(a: int, b: int,
               same, different,
               nan, nan_nan) -> int:
    if a == b:
        if a != NAN:
            return same
        else:
            return nan_nan
    elif a == NAN or b == NAN:
        return nan
    else:
        return different


def similarity_profile(a: list, b: list,
                       same, different,
                       nan, nan_nan) -> float:
    assert isinstance(a, list) and isinstance(b, list)
    ret = 0
    for char1, p1 in enumerate(a):
        if p1 == 0:  # 枝刈り
            continue
        for char2, p2 in enumerate(b):
            if char1 < char2:  # 重複を避ける
                break
            ret += similarity(char1, char2,
                              same, different,
                              nan, nan_nan)*p1*p2
    return ret


def calc_score(N: int, M: int, DNAs: list, precise=True):
    """
    スコア計算 C_allは問題文のものと同一 S_allは結局何が一番多かったか(つまり、復元された配列)

    NはDNAの長さ
    MはDNAの個数
    output_DNAは[[int;N];M] 全てのDNAが同じ長さを有するとする
    """
    assert set(len(dna) for dna in DNAs) == set([N])
    S_all = []
    C_all = 0
    for j in range(N):
        char, cnt = most_common(DNAs, j)
        S_all.append(char)
        C_all += M-cnt
    if not precise:
        return 10000-C_all
    else:
        if 0 <= M <= 10:
            score = max(0, 200-math.floor(C_all*0.2))
        elif 35 <= M <= 40:
            score = max(0, 700-math.floor(C_all*0.1))
        else:
            score = -1
        return score, S_all


def vis(output_DNAs, seed: int = -1, color_mode: str = "SOFT", precise: bool = True) -> int:
    """qiitaにあげたやつ"""
    M = len(output_DNAs)
    N = max([len(output_DNAs[i]) for i in range(M)])
    output_DNAs = [dna+[NAN]*(N-len(dna)) for dna in output_DNAs]
    if precise:
        score, S_all = calc_score(N, M, output_DNAs, precise=True)
    else:
        _, S_all = calc_score(N, M, output_DNAs, precise=True)
        score = calc_score(N, M, output_DNAs, precise=False)

    from matplotlib.colors import ListedColormap
    from matplotlib import gridspec
    import matplotlib.pyplot as plt
    if color_mode == "PRIMARY" or color_mode is None:
        colors = ['red', 'blue', 'green', 'orange', 'white']
    elif color_mode == "SOFT":
        colors = ['#ff7f7f', '#7f7fff', '#7fff7f', '#ffff7f', '#ffffff']
    else:
        colors = ['#101010', '#404040', '#808080', '#c0c0c0', '#ffffff']
    cmap = ListedColormap(colors, name="custom")

    xticks = [0.5+i for i in range(0, N, 10)]
    xticklabels = list(map(str, range(0, N, 10)))  # 1-indexの場合は1,N+1
    yticks = [M-(0.5+i) for i in range(M)]
    yticklabels = list(map(str, range(0, M)))  # 1-indexedの場合は1,M+1

    z = output_DNAs
    z.reverse()

    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=2,
                             width_ratios=[9, 1],
                             height_ratios=[M, 1])

    # メイン部分
    ax1 = fig.add_subplot(spec[0, 0],
                          title=f"Seed:{seed} Score:{score}",
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


def dp_func(DNA1: list, DNA2: list, unstable=30) -> tuple:
    # dp[i][j] sをi文字目、tをj文字目まで見た場合の最大のペアワイズアライメント
    dp = [[-INF for _ in range(len(DNA2)+1)] for _ in range(len(DNA1)+1)]
    rev = [[(0, 0) for _ in range(len(DNA2)+1)] for _ in range(len(DNA1)+1)]
    dp[0][0] = 0

    if unstable > 0:  # 枝刈りを設けるか
        sup = max(unstable, 3*(abs(len(DNA1)-len(DNA2))))
    else:
        sup = INF

    for i in range(1, min(len(DNA1)+1, sup)):
        dp[i][0] = dp[i-1][0]+PARM_NAN
        rev[i][0] = (-1, 0)
    for j in range(1, min(len(DNA2)+1, sup)):
        dp[0][j] = dp[0][j-1]+PARM_NAN
        rev[0][j] = (0, -1)
    for i in range(1, len(DNA1)+1):
        for j in range(max(1, i-sup), min(len(DNA2)+1, i+sup)):
            a = dp[i-1][j-1]+similarity(DNA1[i-1], DNA2[j-1], same=PARM_SAME,
                                        different=PARM_DIFFERENT, nan=PARM_NAN, nan_nan=PARM_NAN_NAN)
            b = dp[i-1][j]+similarity(DNA1[i-1], NAN, same=PARM_SAME,
                                      different=PARM_DIFFERENT, nan=PARM_NAN, nan_nan=PARM_NAN_NAN)
            c = dp[i][j-1]+similarity(NAN, DNA2[j-1], same=PARM_SAME,
                                      different=PARM_DIFFERENT, nan=PARM_NAN, nan_nan=PARM_NAN_NAN)
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


# def dp_re_func(DNA1: list, DNA2: list, rev: list) -> tuple:
#     # dpの復元
#     ans_1 = []
#     ans_2 = []
#     i = len(DNA1)
#     j = len(DNA2)
#     while i > 0 or j > 0:
#         delta_i, delta_j = rev[i][j]
#         i += delta_i
#         j += delta_j
#         ans_1.append(DNA1[i] if delta_i == -1 else NAN)
#         ans_2.append(DNA2[j] if delta_j == -1 else NAN)
#     ans_1.reverse()
#     ans_2.reverse()
#     return (ans_1, ans_2)


def most_common(DNAs: list, idx: int, with_cnt=False) -> tuple:
    """
    DNAsのidx番目では、ACGT-の内、どれが最も多かったか、および、そのカウントを返す
    with_probをwith_cntに変更した 一個の[int;5]でやるならidx=0にする
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


# def neighbor_joining(Ss):
#     # https://en.wikipedia.org/wiki/Neighbor_joining
#     # O(N^3)
#     num_of_leaf = len(Ss)
#     first_N = num_of_leaf
#     dist = dict()
#     for i in range(num_of_leaf):
#         for j in range(i+1, num_of_leaf):
#             # 距離関数として、実は他にも方法があるが、今回はこれでごまかす
#             d = dp_func(Ss[i], Ss[j])[0]  # ans_value
#             dist[(i, j)] = d
#             dist[(j, i)] = d
#     guide_tree = []

#     # wikiの例 残しておく
#     # d = [[0, 5, 9, 9, 8],
#     #      [5, 0, 10, 10, 9],
#     #      [9, 10, 0, 8, 7],
#     #      [9, 10, 8, 0, 3],
#     #      [8, 9, 7, 3, 0], ]
#     # for i in range(num_of_leaf):
#     #     for j in range(i+1, num_of_leaf):
#     #         dist[(i, j)] = d[i][j]
#     #         dist[(j, i)] = d[i][j]

#     while num_of_leaf > 2:
#         Q = calc_Q_matrix(dist, num_of_leaf, first_N)
#         f, g = min(Q, key=Q.get)
#         guide_tree.append((f, g))
#         fu, gu = dist_from_pair_to_new_node(f, g, dist, num_of_leaf, first_N)
#         new_dist = dict()
#         for (i, j), value in dist.items():
#             if i == g or j == g:
#                 continue
#             if i == f:  # fをuとしている事に注意
#                 new_dist[(i, j)] = dist_from_new_node_to_others(j, f, g, dist)
#             elif j == f:
#                 new_dist[(i, j)] = dist_from_new_node_to_others(i, f, g, dist)
#             else:
#                 new_dist[(i, j)] = value
#             new_dist[(j, i)] = new_dist[(i, j)]
#         num_of_leaf -= 1
#         dist = new_dist

#     i, j = list(dist.keys())[0]
#     assert i < j and list(dist.keys())[1] == (j, i) and len(dist.keys()) == 2
#     guide_tree.append((i, j))

#     return guide_tree


# def calc_Q_matrix(dist, num_of_leaf, first_N) -> dict:
#     Q = dict()
#     for i, j in dist.keys():
#         Q[(i, j)] = (num_of_leaf-2)*dist[(i, j)]\
#             - sum(dist.get((i, k), 0) for k in range(first_N))\
#             - sum(dist.get((j, k), 0) for k in range(first_N))
#     return Q


# def dist_from_pair_to_new_node(f, g, dist, num_of_leaf, first_N):
#     fu = (dist[(f, g)]/2)+(1/(2*(num_of_leaf-2)))*(sum(dist.get((f, k), 0) for k in range(first_N))
#                                                    - sum(dist.get((g, k), 0) for k in range(first_N)))
#     gu = dist[(f, g)]-fu
#     return fu, gu


# def dist_from_new_node_to_others(k, f, g, dist):
#     return (dist[(f, k)]+dist[(g, k)]-dist[(f, g)])/2


class Profile:
    def __init__(self, DNAs, integrated=None, integrated_with_cnt=None) -> None:
        self.DNAs = DNAs  # どのDNAを保持しているか なお、これは元のSsの順番に基づく
        self.length = len(DNAs[0])  # 個々のDNAの長さ
        assert set([len(dna) for dna in DNAs]) == set([self.length])
        if integrated is not None:
            self.integrated = integrated  # 代表者で作成した仮想的なDNA
        elif len(self.DNAs) == 1:
            self.integrated = DNAs[0].copy()
        else:
            self.integrated = self.integrate_from_DNAs()
        self.integrated_with_cnt = integrated_with_cnt

    def integrate_from_DNAs(self) -> list:
        return [most_common(self.DNAs, idx)[0] for idx in range(self.length)]

    def integrate_with_cnt(self) -> list:  # 主としてdp_func_profile用
        if self.integrated_with_cnt is None:
            if len(self.DNAs) > 1:
                self.integrated_with_cnt = [most_common(self.DNAs, idx, with_cnt=True)
                                            for idx in range(self.length)]
            else:
                self.integrated_with_cnt = [[1 if c == char else 0 for c in range(5)]
                                            for char in self.DNAs[0]]
        return self.integrated_with_cnt

# progressive alignmentに関する資料
# https://web.stanford.edu/class/cs262/presentations/lecture16.pdf


def dp_func_profile(profile1: Profile, profile2: Profile,
                    same,
                    different,
                    nan,
                    nan_nan,
                    unstable=15) -> tuple:
    """
       A   C   G   T   NAN
    px=0.8 0.2 0.0 0.0 0.0
    py=0.6 0.0 0.0 0.0 0.4
    とあった時、(25-5)/2+5=15通りのsimilarityを計算して、それを基に考えていく
    """
    # sys.stderr.write(f"dp_func_profile is using {same:+} as same\n")
    # sys.stderr.write(f"dp_func_profile is using {different:+} as different\n")
    # sys.stderr.write(f"dp_func_profile is using {nan:+} as nan\n")
    # sys.stderr.write(f"dp_func_profile is using {nan_nan:+} as nan_nan\n")

    p1 = profile1.integrate_with_cnt()  # これは[[int;5];len(proflie.length)]
    p2 = profile2.integrate_with_cnt()
    NAN_p1 = [0, 0, 0, 0, len(profile1.DNAs)]
    NAN_p2 = [0, 0, 0, 0, len(profile2.DNAs)]
    dp = [[-INF for _ in range(len(p2)+1)]
          for _ in range(len(p1)+1)]
    rev = [[(0, 0) for _ in range(len(p2)+1)]
           for _ in range(len(p1)+1)]
    dp[0][0] = 0

    if unstable > 0:  # 枝刈りを設けるか
        sup = max(unstable, 3*(abs(len(p1)-len(p2))))
    else:
        sup = INF

    for i in range(1, min(len(p1)+1, sup)):
        dp[i][0] = dp[i-1][0] + \
            similarity_profile(
                p1[i-1], NAN_p2, same=same, different=different, nan=nan, nan_nan=nan_nan)
        rev[i][0] = (-1, 0)
    for j in range(1, min(len(p2)+1, sup)):
        dp[0][j] = dp[0][j-1] + \
            similarity_profile(
                NAN_p1, p2[j-1], same=same, different=different, nan=nan, nan_nan=nan_nan)
        rev[0][j] = (0, -1)
    for i in range(1, len(p1)+1):
        for j in range(max(1, i-sup), min(len(p2)+1, i+sup)):
            a = dp[i-1][j-1] + \
                similarity_profile(
                    p1[i-1], p2[j-1], same=same, different=different, nan=nan, nan_nan=nan_nan)
            b = dp[i-1][j] + \
                similarity_profile(
                    p1[i-1], NAN_p2, same=same, different=different, nan=nan, nan_nan=nan_nan)
            c = dp[i][j-1] + \
                similarity_profile(
                    NAN_p1, p2[j-1], same=same, different=different, nan=nan, nan_nan=nan_nan)
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
    # print(*dp, sep="\n")
    ans_value = dp[len(p1)][len(p2)]
    return ans_value, rev


def second_largest(numbers: list) -> tuple:
    assert len(numbers) == 5

    first, second = numbers[0], numbers[1]
    if first < second:
        first, second = second, first

    for n in numbers[2:]:
        if n > first:
            second = first
            first = n
        elif n > second:
            second = n

    return first, second


def _dp_fpPC_calc_score(M, cnt1, cnt2):
    # if len(profile1.DNAs) == 1:
    #     assert sum(cnt1) == 1
    #     if max(cnt2)==cnt2[cnt1.index(1)]:
    #         return (1+cnt2[cnt1.index(1)]-M)
    #     else:
    #         return ()
    # else:
    #     assert sum(cnt2) == 1
    #     return 1+cnt1[cnt2.index(1)]-M
    a_plus_b = [a+b for a, b in zip(cnt1, cnt2)]
    m1, m2 = second_largest(a_plus_b)
    ret = (m1-M)*M+(m2)
    # ret = max(a+b for a, b in zip(cnt1, cnt2)) - M
    return ret


def dp_func_profile_ProblemC(profile1: Profile, profile2: Profile, unstable=20) -> tuple:
    """C問題に特化したdpとして、profile1に一個のみ(len(profile1.DNAs)==1)、
    profile2に他を統合するような形で渡して、問題のスコア関数をそのまま計算する"""
    assert len(profile1.DNAs) == 1 or len(profile2.DNAs) == 1, "これが制約"
    M = len(profile1.DNAs)+len(profile2.DNAs)
    p1 = profile1.integrate_with_cnt()  # これは[[int;5];len(proflie.length)]
    p2 = profile2.integrate_with_cnt()
    NAN_p1 = [0, 0, 0, 0, len(profile1.DNAs)]
    NAN_p2 = [0, 0, 0, 0, len(profile2.DNAs)]
    dp = [[0 for _ in range(len(p2)+1)]
          for _ in range(len(p1)+1)]
    rev = [[(0, 0) for _ in range(len(p2)+1)]
           for _ in range(len(p1)+1)]
    dp[0][0] = INF  # 変えた 元は全て-INF,ここが0であった。

    if unstable > 0:  # 枝刈りを設けるか
        sup = max(unstable, 3*(abs(len(p1)-len(p2))))
    else:
        sup = INF

    for i in range(1, min(len(p1)+1, sup)):
        dp[i][0] = dp[i-1][0] + _dp_fpPC_calc_score(M, p1[i-1], NAN_p2)
        rev[i][0] = (-1, 0)
    for j in range(1, min(len(p2)+1, sup)):
        dp[0][j] = dp[0][j-1] + _dp_fpPC_calc_score(M, NAN_p1, p2[j-1])
        rev[0][j] = (0, -1)

    if len(profile2.DNAs) == 1:  # bとcどちらを優先すべきか
        # profile1にNANを入れたくないというお気持ち
        for i in range(1, len(p1)+1):
            for j in range(max(1, i-sup), min(len(p2)+1, i+sup)):
                a = dp[i-1][j-1] + _dp_fpPC_calc_score(M, p1[i-1], p2[j-1])
                b = dp[i-1][j] + _dp_fpPC_calc_score(M, p1[i-1], NAN_p2)
                c = dp[i][j-1] + _dp_fpPC_calc_score(M, NAN_p1, p2[j-1])
                if a >= b and a >= c:
                    dp[i][j] = a
                    rev[i][j] = (-1, -1)
                elif b >= c:
                    dp[i][j] = b
                    rev[i][j] = (-1, 0)
                else:
                    dp[i][j] = c
                    rev[i][j] = (0, -1)
    elif len(profile1.DNAs) == 1:
        # profile2にNANを入れたくないというお気持ち
        for i in range(1, len(p1)+1):
            for j in range(max(1, i-sup), min(len(p2)+1, i+sup)):
                a = dp[i-1][j-1] + _dp_fpPC_calc_score(M, p1[i-1], p2[j-1])
                c = dp[i][j-1] + _dp_fpPC_calc_score(M, NAN_p1, p2[j-1])
                b = dp[i-1][j] + _dp_fpPC_calc_score(M, p1[i-1], NAN_p2)
                if a >= c and a >= b:
                    dp[i][j] = a
                    rev[i][j] = (-1, -1)
                elif c >= b:
                    dp[i][j] = c
                    rev[i][j] = (0, -1)
                else:
                    dp[i][j] = b
                    rev[i][j] = (-1, 0)
    else:
        raise AssertionError
    del a, b, c
    ans_value = dp[len(p1)][len(p2)]
    return ans_value, rev


def dp_re_func_profile(profile1: Profile, profile2: Profile, rev: list) -> tuple:
    i = len(profile1.integrated)
    j = len(profile2.integrated)
    p1_new_DNAs = [[] for _ in range(len(profile1.DNAs))]
    p2_new_DNAs = [[] for _ in range(len(profile2.DNAs))]
    p1_new_inte = []
    p2_new_inte = []
    while i > 0 or j > 0:
        delta_i, delta_j = rev[i][j]
        i += delta_i
        j += delta_j
        if delta_i == 0:
            for idx in range(len(profile1.DNAs)):
                p1_new_DNAs[idx].append(NAN)
            p1_new_inte.append(NAN)
        else:
            for idx in range(len(profile1.DNAs)):
                p1_new_DNAs[idx].append(profile1.DNAs[idx][i])
            p1_new_inte.append(profile1.integrated[i])
        if delta_j == 0:
            for idx in range(len(profile2.DNAs)):
                p2_new_DNAs[idx].append(NAN)
            p2_new_inte.append(NAN)
        else:
            for idx in range(len(profile2.DNAs)):
                p2_new_DNAs[idx].append(profile2.DNAs[idx][j])
            p2_new_inte.append(profile2.integrated[j])
    for dna in p1_new_DNAs:
        dna.reverse()
    for dna in p2_new_DNAs:
        dna.reverse()
    p1_new_inte.reverse()
    p2_new_inte.reverse()
    profile1 = Profile(p1_new_DNAs, integrated=p1_new_inte)
    profile2 = Profile(p2_new_DNAs, integrated=p2_new_inte)
    return profile1, profile2


def integrate_two_profiles(profile1: Profile, profile2: Profile) -> Profile:
    # ans_value, rev = dp_func(profile1.integrated,
    #                          profile2.integrated)
    ans_value, rev = dp_func_profile_ProblemC(profile1, profile2)
    profile1, profile2 = dp_re_func_profile(profile1, profile2, rev)
    return Profile(DNAs=profile1.DNAs+profile2.DNAs)


def progressive_alignment(Ss):
    profiles = [Profile([dna]) for dna in Ss]

    evolutionary_tree = [(i-1, i) for i in range(1, len(Ss))]
    # evolutionary_tree = neighbor_joining(Ss) これを使用の際は注意。 特に順序が保たれていない。

    for idx1, idx2 in evolutionary_tree:
        # sys.stderr.write(f"{idx1},{idx2}\n")
        profile1 = profiles[idx1]  # こっちが多い方
        profile2 = profiles[idx2]  # こっちが一個の方
        new_profile = integrate_two_profiles(profile1, profile2)
        profiles[idx2] = new_profile
    raise AssertionError("Ok!!!!")
    return profiles[-1].DNAs


def iterative_refinement(M, DNAs, raw_DNAs,
                         same, different, nan, nan_nan,
                         use_p3_score_func: bool):
    """
    先程挙げたpdfからの引用：
    One problem of progressive alignment:
    • Initial alignments are “frozen” even when new evidence comes
    """
    DNA_length = len(DNAs[0])
    all_integrated = [most_common(DNAs, idx, with_cnt=True)
                      for idx in range(DNA_length)]  # [[int;5];DNA_length]
    for j in range(M):
        all_integrated_without_j = [[(cnt-(1 if char == DNAs[j][idx] else 0))
                                     for char, cnt in enumerate(cnts)]
                                    for idx, cnts in enumerate(all_integrated)]  # [[int;5];DNA_length]
        profile1 = Profile(DNAs=[raw_DNAs[j]],
                           integrated_with_cnt=None)  # 注目DNA
        profile2 = Profile(DNAs=DNAs[:j]+DNAs[j+1:],
                           integrated_with_cnt=all_integrated_without_j)  # 他の子たち

        if not use_p3_score_func:
            _ans_value, rev = dp_func_profile(profile1, profile2,
                                              same=same,
                                              different=different,
                                              nan=nan,
                                              nan_nan=nan_nan)
        else:
            _ans_value, rev = dp_func_profile_ProblemC(profile1, profile2)

        profile1, profile2 = dp_re_func_profile(profile1, profile2, rev)

        DNAs = [profile1.DNAs[0] if idx == j else profile2.DNAs[idx - (1 if idx > j else 0)]
                for idx in range(M)]

        # !!!!!!
        # ここでremove_unnecessary_NANをするとバグる 理由は未だ不明
        # !!!!!!

        if len(DNAs[0]) != DNA_length:  # 長さに変更が生じた場合、all_integratedも変更する必要がある。
            DNA_length = len(DNAs[0])
            all_integrated = [most_common(DNAs, idx, with_cnt=True)
                              for idx in range(len(DNAs[0]))]

        # vis(DNAs, seed=j, precise=False)

    return DNAs

# # # # # # # # 以下山登りパート # # # # # # # #


class ListDict(object):
    # https://stackoverflow.com/questions/15993447/python-data-structure-for-efficient-add-remove-and-random-choice
    # This is a data structure that can add a new element, remove an existing element,
    # and choose a random element, all in better than O(n) time.
    def __init__(self):
        self.item_to_position = dict()
        self.items = list()

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    # def remove_item(self, item):
    #     position = self.item_to_position.pop(item)
    #     last_item = self.items.pop()
    #     if position != len(self.items):
    #         self.items[position] = last_item
    #         self.item_to_position[last_item] = position

    def replace_item(self, item, new_item):  # 自分で追加
        position = self.item_to_position.pop(item)
        self.items[position] = new_item
        self.item_to_position[new_item] = position

    def choose_random_item(self):
        return random.choice(self.items)

    def __contains__(self, item):
        return item in self.item_to_position

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)


def annealing_init(M, DNAs) -> ListDict:
    not_decided = ListDict()
    assert set([len(DNAs[i]) for i in range(M)]) == set([len(DNAs[0])])
    for char_idx in range(len(DNAs[0])):
        char, cnt = most_common(DNAs, char_idx)
        if cnt == M:
            for dna_idx in range(M):
                if char_idx > 0 and DNAs[dna_idx][char_idx-1] == NAN:
                    not_decided.add_item((dna_idx, char_idx))
                # 重複して追加するのを避けるため、elif
                elif char_idx < len(DNAs[0])-1 and DNAs[dna_idx][char_idx+1] == NAN:
                    not_decided.add_item((dna_idx, char_idx))
        else:
            for dna_idx in range(M):
                if DNAs[dna_idx][char_idx] != NAN:
                    not_decided.add_item((dna_idx, char_idx))
    return not_decided


def right_to_left(M, DNAs, dna_idx, char_idx):
    # 二点swapのための関数
    first_score = 0
    first_score += most_common(DNAs, char_idx-1)[1]
    first_score += most_common(DNAs, char_idx)[1]
    original_char = DNAs[dna_idx][char_idx]
    DNAs[dna_idx][char_idx-1] = original_char
    DNAs[dna_idx][char_idx] = NAN
    second_score = 0

    del_col = False  # 空白行が出来た場合、効率化の為に削除
    char, max_cnt = most_common(DNAs, char_idx)
    if char == NAN and max_cnt == M:
        del_col = True

    second_score += most_common(DNAs, char_idx-1)[1]
    second_score += max_cnt

    return True, second_score-first_score, -1, original_char, del_col


def left_to_right(M, DNAs, dna_idx, char_idx):
    # 二点swapのための関数
    first_score = 0
    first_score += most_common(DNAs, char_idx)[1]
    first_score += most_common(DNAs, char_idx+1)[1]
    original_char = DNAs[dna_idx][char_idx]
    DNAs[dna_idx][char_idx+1] = original_char
    DNAs[dna_idx][char_idx] = NAN
    second_score = 0

    del_col = False  # 空白行が出来た場合、効率化の為に削除
    char, max_cnt = most_common(DNAs, char_idx)
    if char == NAN and max_cnt == M:
        del_col = True

    second_score += max_cnt
    second_score += most_common(DNAs, char_idx+1)[1]
    return True, second_score-first_score, +1, original_char, del_col


def annealing_modify(M, DNAs, dna_idx, char_idx):
    # 二点swap
    if random.random() < 0.5:
        if char_idx > 0 and DNAs[dna_idx][char_idx-1] == NAN:
            return right_to_left(M, DNAs, dna_idx, char_idx)
        elif char_idx < len(DNAs[0])-1 and DNAs[dna_idx][char_idx+1] == NAN:
            return left_to_right(M, DNAs, dna_idx, char_idx)
    else:
        if char_idx < len(DNAs[0])-1 and DNAs[dna_idx][char_idx+1] == NAN:
            return left_to_right(M, DNAs, dna_idx, char_idx)
        elif char_idx > 0 and DNAs[dna_idx][char_idx-1] == NAN:
            return right_to_left(M, DNAs, dna_idx, char_idx)
    return False, None, None, None, False  # 最後のはdel_col


def annealing(M, DNAs, ANNEALING_TL: float, START_TEMP: float, END_TEMP: float):
    # と言う名の山登り
    # score = calc_score(len(DNAs[0]),M,DNAs,precise=False)
    not_decided = annealing_init(M, DNAs)  # ListDict
    now = time.perf_counter()-start_time
    annealing_cnt = 0

    while now < ANNEALING_TL:  # and len(not_decided) != 0:
        annealing_cnt += 1
        # dna_idxは列番号、char_idxは行番号
        dna_idx, char_idx = not_decided.choose_random_item()

        is_modify_succeeded, delta_score, delta_char_idx, original_char, del_col =\
            annealing_modify(M, DNAs, dna_idx, char_idx)
        if not is_modify_succeeded:
            now = time.perf_counter()-start_time
            continue

        # temp = START_TEMP + (END_TEMP-START_TEMP) * now / ANNEALING_TL

        # # 遷移確率の計算
        # if delta_score >= 0.0:
        #     prob = 1.0
        # elif delta_score/temp <= -10.0:
        #     prob = -1.0
        # else:
        #     prob = math.exp(delta_score/temp)
        # print(temp, delta_score, prob)

        # # 遷移
        # if prob > random.random():

        if delta_score >= 0:  # これは山登り
            # sys.stderr.write(f"score changed!; {delta_score:+}\n")
            # not_decided.remove((dna_idx, char_idx)) # これがいけなかった 二回以上移動することもある
            not_decided.replace_item(
                (dna_idx, char_idx), (dna_idx, char_idx+delta_char_idx))
            if del_col:  # 基本的に列は増やしすぎなので、消すメインで大丈夫と思われる
                DNAs = remove_unnecessary_NAN(M, DNAs, char_idx=char_idx)
                for item in not_decided:
                    i, j = item
                    if j >= char_idx:
                        if j == char_idx:
                            raise AssertionError
                        j -= 1
                    not_decided.replace_item(item, (i, j))
        # 復元
        else:
            DNAs[dna_idx][char_idx] = original_char
            DNAs[dna_idx][char_idx+delta_char_idx] = NAN
        now = time.perf_counter()-start_time

    # debug用 一応とっておく
    # print(sorted([(i, j) for i, j in not_decided if j >= 110]))
    # assert all(DNAs[i][j] != NAN for i, j in not_decided)

    sys.stderr.write(f"annealing_cnt:{annealing_cnt}\n")
    return DNAs


# テスト
# DNAs = [[G, A, A, G, T, T, A],
#         [G, A, C, NAN, T, T, A],
#         [G, A, A, C, T, G, A],
#         [G, T, A, C, T, G, A]]
# DNAs = iterative_refinement(4, DNAs)
# vis(DNAs)
# exit()

# # # # # # # # 以上山登りパート # # # # # # # #


def remove_unnecessary_NAN(M, DNAs, char_idx=None) -> list:
    # char_idxがNoneでない時、その行のみを削除する
    if char_idx is None:
        i = 0
        while i < len(DNAs[0]):
            flag = True
            for idx in range(M):
                if DNAs[idx][i] != NAN:
                    flag = False
                    break
            if flag:
                for idx in range(M):
                    del DNAs[idx][i]
            else:
                i += 1
    else:
        for idx in range(M):
            del DNAs[idx][char_idx]
    return DNAs


def integrate_two_profiles_old_version(profile1: Profile, profile2: Profile) -> Profile:
    ans_value, rev = dp_func(profile1.integrated,
                             profile2.integrated)  # dp_funcでいいことに注意
    profile1, profile2 = dp_re_func_profile(profile1, profile2, rev)
    return Profile(DNAs=profile1.DNAs+profile2.DNAs)


def progressive_alignment_old_version(Ss):
    profiles = [Profile([dna]) for dna in Ss]
    evolutionary_tree = [(0, i) for i in range(1, len(Ss))]
    for idx1, idx2 in evolutionary_tree:
        profile1 = profiles[idx1]
        profile2 = profiles[idx2]
        new_profile = integrate_two_profiles_old_version(profile1, profile2)
        profiles[idx1] = new_profile
    return profiles[0].DNAs


def solve(M, Ss) -> list:
    """ここでのDNAsとは、[[int;(最終的な個々のDNAの長さ)];M]という形式を取る"""

    # スタート点その１
    DNAs = progressive_alignment(Ss)
    DNAs = remove_unnecessary_NAN(M, DNAs)
    score_after_progressive_alignment =\
        calc_score(len(DNAs[0]), M, DNAs, precise=False)

    # スタート点その2 (誤解を避けるため、出来るだけ冗長な変数名)
    DNAs_generated_by_old_version = progressive_alignment_old_version(Ss)
    DNAs_generated_by_old_version = remove_unnecessary_NAN(M,
                                                           DNAs_generated_by_old_version)
    score_after_progressive_alignment_generated_by_old_version =\
        calc_score(len(DNAs_generated_by_old_version[0]), M,
                   DNAs_generated_by_old_version, precise=False)

    if score_after_progressive_alignment_generated_by_old_version >\
            score_after_progressive_alignment:
        DNAs = DNAs_generated_by_old_version
        score_after_progressive_alignment =\
            score_after_progressive_alignment_generated_by_old_version

    sys.stderr.write("score(after progressive_alignment):"
                     + f"{score_after_progressive_alignment}\n")

    last_score = score_after_progressive_alignment
    delta_score = 1
    while delta_score > 0 and time.perf_counter()-start_time < 8.0:
        DNAs = iterative_refinement(M, DNAs, raw_DNAs=Ss,
                                    same=None,
                                    different=None,
                                    nan=None,
                                    nan_nan=None,
                                    use_p3_score_func=True)
        DNAs = remove_unnecessary_NAN(M, DNAs)
        score = calc_score(len(DNAs[0]), M, DNAs, precise=False)
        delta_score = score-last_score
        sys.stderr.write("(score(delta score)(now using p3 score func):"
                         + f"{delta_score:+})\n")
        last_score = score

    sys.stderr.write("score(after iterative_refinement3):"
                     + f"{last_score}\n")

    sys.stderr.write("$$$NOW(before annealing):"
                     + f"{time.perf_counter()-start_time:.03}s$$$\n")

    DNAs = annealing(M, DNAs, ANNEALING_TL=9.0,
                     START_TEMP=None, END_TEMP=None)
    score_after_annealing = calc_score(len(DNAs[0]), M, DNAs, precise=False)
    sys.stderr.write("score(after annealing):"
                     + f"{score_after_annealing}\n")
    DNAs = remove_unnecessary_NAN(M, DNAs)

    return DNAs


def main(seed=1, l_or_s="s", is_local=True) -> int:
    global start_time

    # 入力受け取り
    if not is_local:
        M = int(input())
        Ss = [list(map(parse_for_input, input().rstrip("\n")))
              for _ in range(M)]
    else:
        with open(f"test_{l_or_s}sim_{seed:02}.txt") as f:
            M = int(f.readline().rstrip())
            Ss = [list(map(parse_for_input, f.readline().rstrip()))
                  for _ in range(M)]
    start_time = time.perf_counter()

    # 解答
    output_DNAs = solve(M, Ss)

    # スコア計算
    if is_local:
        score = calc_score(len(output_DNAs[0]), M,
                           output_DNAs, precise=False)
        # vis(output_DNAs, seed=seed)
        # write_output(output_DNAs)
        return score

    # 出力書き出し
    else:
        write_output(output_DNAs)
        return 0


if __name__ == "__main__":
    main(is_local=False)  # 提出用
    exit()

    # main(seed=8, l_or_s="s", is_local=True)
    # exit()
    # main(l_or_s="l")

    import pandas as pd
    import datetime
    df = pd.read_csv("score.csv")
    # df = pd.DataFrame()

    print("seed,score")
    seeds = []
    scores = []

    for seed in range(0, 100):
        print("\n\nNew trial")
        score = main(seed, l_or_s="s")
        print(f"FinalResult: seed={seed},score={score}")

        seeds.append(seed)
        scores.append(score)
    df['seed'] = seeds
    df[f'score({datetime.datetime.now()})'] = scores
    df.to_csv("score.csv", index=False)
