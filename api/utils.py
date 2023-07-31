import gc
import io

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from . import MinimizeDeviation


def find_params_for_best_deviation(pairs_list: MinimizeDeviation):
    pairs_list = pairs_list.root
    n = len(pairs_list)
    pairs_np = np.array(pairs_list)
    pairs_np = pairs_np[pairs_np[:, 0].argsort()]
    x_set = np.unique(pairs_np[:, 0], return_index=False)
    if x_set.shape[0] == 1:
        best_a = best_b = np.average(pairs_np[:, 1])
        best_c = x_set[0]
        best_deviation = sum((x[1] - best_b) ** 2 for x in pairs_list)
    else:
        a_list = np.cumsum(pairs_np[:-1, 1]) / np.arange(1, n)
        b_list = np.cumsum(pairs_np[1:, 1][::-1])[::-1] / np.arange(n - 1, 0, -1)
        best_a, best_b, best_c, best_deviation = None, None, None, None
        for i in range(n - 1):
            if pairs_np[i, 0] == pairs_np[i + 1, 0]:
                continue
            a, b = a_list[i], b_list[i]
            deviation = np.sum(np.square(pairs_np[: i + 1, 1] - a)) + np.sum(
                np.square(pairs_np[i + 1 :, 1] - b)
            )
            if best_deviation is None or deviation < best_deviation:
                best_deviation = deviation
                best_c = (pairs_np[i, 0] + pairs_np[i + 1, 0]) / 2
                best_a = a
                best_b = b

    best_deviation = (best_deviation / n) ** 0.5
    fig: plt.Figure
    ax: Axes
    fig, ax = plt.subplots(num=1, clear=True)
    ax.set_title(
        f"F(x) = {best_a} if x < {best_c} else {best_b} \n minimum deviation = {best_deviation}"
    )
    ax.scatter(pairs_np[:, 0], pairs_np[:, 1], color="red")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    x = np.linspace(x_set.min() - 1, best_c, 3)
    y = np.zeros(3) + best_a
    ax.plot(x, y)
    x = np.linspace(best_c, x_set.max() + 1, 3)
    y = np.zeros(3) + best_b
    ax.plot(x, y)
    image = io.BytesIO()
    plt.savefig(image, format="png")
    image.seek(0)

    fig.clear()
    plt.close(fig)
    gc.collect()

    return best_a, best_b, best_c, image
