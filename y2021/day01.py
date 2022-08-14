from typing import Sequence

Depth = int


def file_io(filepath) -> list[Depth]:
    with open(filepath, "r") as f:
        depth_data = [int(line) for line in f]
    return depth_data


def find_depth_increase_count(depths: Sequence[Depth]) -> int:
    increases = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i - 1]:
            increases += 1
    return increases


def find_depth_window_increase_count(depths: Sequence[Depth]) -> int:
    increases = 0
    current = sum(depths[:3])
    for i in range(1, len(depths)-2):
        new_depth = sum(depths[i:i+3])
        if new_depth > current:
            increases += 1
        current = new_depth
    return increases


fp = r"data/day1.txt"
data = file_io(fp)
print(find_depth_increase_count(data))
print(find_depth_window_increase_count(data))
