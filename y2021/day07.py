from functools import cache
import numpy as np


def parse_input(filepath):
    return np.loadtxt(filepath, dtype=np.int32, delimiter=",")


@cache
def calculate_consumption(n_steps):
    return sum([i for i in range(n_steps + 1)])


def part_a():
    fp = r"data/day07.txt"
    data = parse_input(fp)
    min_gas = float("inf")
    for i in range(max(data)):
        min_gas = min_gas if min_gas < sum(abs(data - i)) else sum(abs(data - i))
    return min_gas


def part_b():
    fp = r"data/day07.txt"
    data = parse_input(fp)
    min_gas = float("inf")
    for i in range(max(data)):
        temp_arr = np.array([calculate_consumption(x) for x in abs(data - i)])
        min_gas = min_gas if min_gas < sum(temp_arr) else sum(temp_arr)
    return min_gas


if __name__ == "__main__":
    print(part_a())
    print(part_b())
