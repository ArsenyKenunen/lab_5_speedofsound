import matplotlib.pyplot as plt
import numpy as np
from os import mkdir
from os.path import exists


if not exists("graphs"):
    mkdir("graphs")
counter = 1


def do_the_thing(before_or_after: str):
    global counter
    for exp in range(1, 11):
        plt.figure(figsize=(11, 8))
        with open(f"{before_or_after}/{exp}/data_0.txt") as _0:
            _0_values = np.array(_0.readlines(), dtype='float64')
        with open(f"{before_or_after}/{exp}/data_1.txt") as _1:
            _1_values = np.array(_1.readlines(), dtype='float64')

        t0 = np.linspace(0, 5000/500000, len(_0_values))
        t1 = np.linspace(0, 5000/500000, len(_1_values))

        # опускание графика 0
        _0_values -= np.median(_0_values)

        peak_0 = np.where(_0_values == np.max(_0_values))[0][0]
        peak_1 = np.where(_1_values == np.max(_1_values))[0][0]
        peak_0_value = _0_values[peak_0]
        peak_1_value = _1_values[peak_1]

        # смещение графика 1 для совмещения пиков
        moving_peak_1 = peak_1
        _1_values_moved = _1_values.copy()
        _1_values_moved = _1_values_moved[peak_1 - peak_0:]
        t1 = t1[:peak_0 - peak_1]

        # нормировка
        _0_values /= peak_0_value
        _1_values_moved /= peak_1_value

        plt.scatter(
            t0, _0_values,
            color='blue', s=1
        )
        plt.scatter(
            t1, _1_values_moved,
            color='red', s=1
        )
        plt.title(f"combined graphs, experiment #{exp} [{before_or_after}]")
        plt.grid(True, alpha=.3)
        plt.xlabel("time, s")
        plt.ylabel("peak height, relative units")
        plt.savefig(f"graphs/graph-{before_or_after}-{exp}.png", dpi=600, bbox_inches='tight')
        print(f"saved {counter} out of 20", end='\b\r')
        counter += 1
        plt.close()

print("rendering progress:")
do_the_thing("before")
do_the_thing("after")
print("\n")
