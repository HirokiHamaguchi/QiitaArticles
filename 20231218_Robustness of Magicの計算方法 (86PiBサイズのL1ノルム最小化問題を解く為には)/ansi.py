import time


def log(i, d):
    # ANSIエスケープシーケンスを使ったカーソル移動
    print(f"\033[1F\033[0K i = {i}, d = {d}")


def main():
    t0 = time.perf_counter()

    for i in range(1000):
        # 適当な処理
        d = 0
        for j in range(10000):
            d += j**0.5

        # ログ出力
        log(i, d)

    t1 = time.perf_counter()

    print(f"duration = {t1 - t0}[ms]")


if __name__ == "__main__":
    main()
