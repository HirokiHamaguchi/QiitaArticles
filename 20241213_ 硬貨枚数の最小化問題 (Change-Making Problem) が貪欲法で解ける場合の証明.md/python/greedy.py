from typing import List


def greedy(a: List[int], p: int) -> int:
    x = 0
    for ai in reversed(a):
        x += p // ai
        p %= ai
    return x


def main():
    a = [1, 5, 10, 50, 100, 500]
    p = 620
    print(greedy(a, p))


if __name__ == "__main__":
    main()
