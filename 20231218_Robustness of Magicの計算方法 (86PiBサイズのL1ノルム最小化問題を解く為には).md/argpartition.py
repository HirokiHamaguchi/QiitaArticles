import numpy as np


def topK_argsort(data, k):
    # O(N log N)
    args = np.argsort(data)[-k:]
    return data[args]


def topK_argpartition(data, k):
    # O(N)
    args = np.argpartition(data, -k)[-k:]
    return data[args]


def topK_threshold(data, k):
    # 適切な閾値を事前情報から推定
    threshold = 0.99
    data_large = data[data > threshold]
    if len(data_large) < k:
        # 削りすぎてしまった場合(失敗)
        return topK_argpartition(data, k)
    else:
        # 閾値を超えるデータがk個以上ある場合(成功)
        return topK_argpartition(data_large, k)


def main():
    import time
    import matplotlib.pyplot as plt

    NUM_SEED = 300
    k = 100
    mean_times_argpartition = []
    mean_times_threshold = []
    ub_times_argpartition = []
    ub_times_threshold = []
    lb_times_argpartition = []
    lb_times_threshold = []
    Ns = np.linspace(1e4, 1e6, 21)
    for _n in Ns:
        print(f"n={_n}")
        n = int(_n)

        times_argpartition = []
        times_threshold = []

        for seed in range(NUM_SEED):
            # 0以上1未満の一様乱数をn個生成
            np.random.seed(seed)
            data = np.random.random(n)

            t0 = time.perf_counter()
            ans_argpartition = topK_argpartition(data, k)
            t1 = time.perf_counter()
            times_argpartition.append(t1 - t0)

            t0 = time.perf_counter()
            ans_threshold = topK_threshold(data, k)
            t1 = time.perf_counter()
            times_threshold.append(t1 - t0)

            assert np.allclose(np.sort(ans_argpartition), np.sort(ans_threshold))

        mean_argpartition = np.mean(times_argpartition)
        mean_threshold = np.mean(times_threshold)
        std_argpartition = np.std(times_argpartition)
        std_threshold = np.std(times_threshold)
        ub_argpartition = mean_argpartition + std_argpartition
        ub_threshold = mean_threshold + std_threshold
        lb_argpartition = mean_argpartition - std_argpartition
        lb_threshold = mean_threshold - std_threshold

        mean_times_argpartition.append(mean_argpartition)
        mean_times_threshold.append(mean_threshold)
        ub_times_argpartition.append(ub_argpartition)
        ub_times_threshold.append(ub_threshold)
        lb_times_argpartition.append(lb_argpartition)
        lb_times_threshold.append(lb_threshold)

    plt.figure(figsize=(8, 4))
    plt.plot(Ns, mean_times_argpartition, label="argpartition")
    plt.plot(Ns, mean_times_threshold, label="threshold")
    plt.fill_between(Ns, lb_times_argpartition, ub_times_argpartition, alpha=0.1)
    plt.fill_between(Ns, lb_times_threshold, ub_times_threshold, alpha=0.1)
    plt.xlabel("data size ($N$)")
    plt.ylabel("time (sec)")
    plt.legend(loc="upper left")
    plt.title("topK argpartition vs. topK threshold")
    plt.savefig("argpartition.png")


if __name__ == "__main__":
    main()
