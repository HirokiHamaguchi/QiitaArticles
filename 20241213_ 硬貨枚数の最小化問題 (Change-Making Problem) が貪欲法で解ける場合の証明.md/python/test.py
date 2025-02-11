import random
from typing import List


def greedy(a: List[int], p: int) -> int:
    x = 0
    for ai in reversed(a):
        xi = p // ai
        x += xi
        p %= ai
    return x


def bfs(a: List[int], maxP: int) -> List[int]:
    # compute the answers for the CMP
    dists = [int(1e9) for _ in range(maxP)]
    dists[0] = 0
    q = [0]
    while q:
        p = q.pop(0)
        for ai in a:
            if p + ai < maxP and dists[p + ai] > dists[p] + 1:
                dists[p + ai] = dists[p] + 1
                q.append(p + ai)
    return dists


def isGreedyOptimal(a: List[int]) -> bool:
    maxP = 1000
    slows = bfs(a, maxP)
    fasts = [greedy(a, p) for p in range(maxP)]
    return slows == fasts


def doesSatisfyRelaxedConditions(n: int, a: List[int]) -> bool:
    cond = True
    for i in range(n - 1):
        rho_i = -(-a[i + 1] // a[i])  # ceil division
        delta_i = rho_i * a[i] - a[i + 1]
        assert 0 <= delta_i < a[i]
        tf = greedy(a[:i], delta_i) < rho_i
        # print(tf, end=" ")
        cond = cond and tf
    # print()
    return cond


def trial(n: int) -> None:
    while True:
        a = random.sample(range(1, 50), n)
        a[0] = 1
        if len(set(a)) == n:
            break
    a.sort()

    if not isGreedyOptimal(a):
        return

    print(n, a)

    assert doesSatisfyRelaxedConditions(n, a)


def main():
    # for _ in range(100000):
    #     trial(5)

    a = [1, 2, 4, 5, 8]

    print(f"{isGreedyOptimal(a)=}")
    print(f"{doesSatisfyRelaxedConditions(len(a), a)=}")

    print(f"{isGreedyOptimal(a[:-1])=}")
    print(f"{doesSatisfyRelaxedConditions(len(a) - 1, a[:-1])=}")


if __name__ == "__main__":
    main()
