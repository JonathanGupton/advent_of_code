import numpy as np


Coordinate = tuple[int, int]
CoordinatePair = tuple[Coordinate, Coordinate]


def parse_input(filepath) -> tuple[list[CoordinatePair], int]:
    max_dim = 0
    coordinates = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            l, *_, r = line.strip().split()
            l_x, l_y = l.split(",")
            l_x, l_y = int(l_x), int(l_y)
            r_x, r_y = r.split(",")
            r_x, r_y = int(r_x), int(r_y)

            left = (l_x, l_y)
            right = (r_x, r_y)
            coordinates.append((left, right))

            max_dim = (
                max(l_x, l_y, r_x, r_y)
                if max(l_x, l_y, r_x, r_y) > max_dim
                else max_dim
            )
    return coordinates, max_dim


fp = r"data/day05_example.txt"
line_segments, dimensions = parse_input(fp)
_map = np.zeros((dimensions + 1, dimensions + 1), dtype=np.uint16)
for left, right in line_segments:
    if left[0] == right[0]:
        _map[min(left[1], right[1]) : max(left[1], right[1]) + 1, left[0]] += 1
    elif left[1] == right[1]:
        _map[left[1], min(left[0], right[0]) : max(left[0], right[0]) + 1] += 1
    else:
        np.fill_diagonal(
            _map[
                min(left[1], right[1]) : max(left[1], right[1]) + 1,
                min(left[0], right[0]) : max(left[0], right[0]) + 1,
            ],
            _map[
                min(left[1], right[1]) : max(left[1], right[1]) + 1,
                min(left[0], right[0]) : max(left[0], right[0]) + 1,
            ].diagonal()
            + 1,
        )


print((_map > 1).sum())
