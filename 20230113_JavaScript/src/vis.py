import numpy as np
import matplotlib.pyplot as plt

_innerHTML = []
_replaceChildren = []

with open("src/times.txt") as f:
    for i in range(100):
        name, time = f.readline().split()
        assert(name == ("eraseByInnerHTML:" if i %
                        2 == 0 else "eraseByReplaceChildren:"))
        time = float(time)
        if i % 2 == 0:
            _innerHTML.append(time)
        else:
            _replaceChildren.append(time)

innerHTML = np.array(_innerHTML)
replaceChildren = np.array(_replaceChildren)

plt.bar([0, 1],
        [innerHTML.mean(), replaceChildren.mean()],
        yerr=[innerHTML.std(), replaceChildren.std()],
        tick_label=['innerHTML', 'replaceChildren'],
        error_kw={"lw": 1, "capthick": 1, "capsize": 20})
plt.title("innerHTML vs. replaceChildren")
plt.xlabel("method")
plt.ylabel("average time of 50 trials [ms]")

plt.savefig("img/innerHTML_vs_replaceChildren.png")
plt.show()
