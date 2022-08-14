import numpy as np
from itertools import combinations, product


def input_parser(filepath):
    output = []
    with open(filepath, "r") as f:
        for i, scanner in enumerate(f.read().split("\n\n")):
            output.append(
                np.array(
                    [
                        [int(n) for n in row.split(",")]
                        for row in scanner.split("\n")[1:]
                    ]
                )
            )
    return output


def rotate_around_x(arr: np.array) -> np.array:
    x_rotation_matrix = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    return np.matmul(arr, x_rotation_matrix)


def rotate_around_y(arr: np.array) -> np.array:
    y_rotation_matrix = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    return np.matmul(arr, y_rotation_matrix)


def rotate_around_z(arr: np.array) -> np.array:
    z_rotation_matrix = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    return np.matmul(arr, z_rotation_matrix)


def apply_translation(arr: np.array, distance: np.array) -> np.array:
    return arr + distance


def check_overlap(coords1, coords2):
    coords1 = set(map(tuple, coords1))
    coords2 = set(map(tuple, coords2))
    overlap = coords1 & coords2
    return overlap


def generate_y_rotations(arr):
    for _ in range(4):
        arr = rotate_around_y(arr)
        yield arr


def generate_rotations(arr):
    side_1 = np.copy(arr)
    for rotation in generate_y_rotations(side_1):
        yield rotation

    side_2 = rotate_around_z(arr)
    for rotation in generate_y_rotations(side_2):
        yield rotation

    side_3 = rotate_around_z(side_2)
    for rotation in generate_y_rotations(side_3):
        yield rotation

    side_4 = rotate_around_z(side_3)
    for rotation in generate_y_rotations(side_4):
        yield rotation

    side_5 = rotate_around_x(arr)
    for rotation in generate_y_rotations(side_5):
        yield rotation

    side_6a = rotate_around_x(arr)
    side_6b = rotate_around_x(side_6a)
    side_6 = rotate_around_x(side_6b)
    for rotation in generate_y_rotations(side_6):
        yield rotation


def assemble_map(data):
    scanner_positions = {(0, 0, 0)}
    beacon_positions = set(map(tuple, data[0]))
    oriented_positions = [False] * len(data)
    oriented_positions[0] = True

    def find_adjacent_beacons(scanner, scanner_position):
        nonlocal scanner_positions, beacon_positions, oriented_positions, data
        for found_beacon in beacon_positions:
            for rotation in generate_rotations(scanner):
                for beacon2 in rotation:
                    offset = np.array(found_beacon) - beacon2
                    arr_w_offset = apply_translation(rotation, offset)
                    overlap = beacon_positions & set(map(tuple, arr_w_offset))
                    if len(overlap) >= 12:
                        beacon_positions.update(set(map(tuple, arr_w_offset)))
                        scanner_positions.add(tuple(offset))
                        oriented_positions[scanner_position] = True
                        return

    while not all(oriented_positions):
        for i, position_found in enumerate(oriented_positions):
            if not position_found:
                find_adjacent_beacons(data[i], i)

    return scanner_positions, beacon_positions, oriented_positions


def manhattan_distance(coord1, coord2):
    return (
        abs(coord1[0] - coord2[0])
        + abs(coord1[1] - coord2[1])
        + abs(coord1[2] - coord2[2])
    )


if __name__ == "__main__":

    fp = r"data/day19.txt"
    data = input_parser(fp)

    scanner_positions, beacon_positions, _ = assemble_map(data)
    print(f"Part A:  {len(beacon_positions)}")

    md_max = float("-inf")
    for a, b in combinations(scanner_positions, 2):
        md_max = (
            md_max if md_max > manhattan_distance(a, b) else manhattan_distance(a, b)
        )
    print(f"Part B:  {md_max}")
