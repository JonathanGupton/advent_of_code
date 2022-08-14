import _md5
from collections import deque
from itertools import product
from typing import Generator, Literal, Sequence


Coordinate = complex
Dimension = int
Dimensions = Sequence[Dimension]
Direction = Literal["U", "D", "L", "R"]


def md5_hash(str_to_hash: str) -> str:
    return _md5.md5(str_to_hash.encode("ascii")).hexdigest()


def direction_from_hash(
    hashed_string: str, valid_letters: str = "bcdef"
) -> Generator[Direction, None, None]:
    directions: list[Direction] = ["U", "D", "L", "R"]
    for direction, hash_char in zip(directions, hashed_string[:4]):
        if hash_char in valid_letters:
            yield direction


def create_valid_coordinates(dimensions: Dimensions = (4, 4)) -> set[Coordinate]:
    coords = set()
    for x, y in product(*(range(i) for i in dimensions)):
        coords.add(complex(x, y))
    return coords


def move(direction: Direction) -> Coordinate:
    match direction:
        case "U":
            return complex(-1, 0)
        case "D":
            return complex(1, 0)
        case "L":
            return complex(0, -1)
        case "R":
            return complex(0, 1)


def find_shortest_path(initial_value: str, dimensions: Dimensions):
    floor_map = create_valid_coordinates(dimensions)
    goal = complex(*(dim - 1 for dim in dimensions))
    start_coordinate = complex(0, 0)
    start_path = ""
    path_deque = deque([(start_coordinate, start_path)])
    while path_deque:
        current_coordinate, current_path = path_deque.popleft()
        if current_coordinate == goal:
            break
        hashed_path = md5_hash(initial_value + current_path)
        for direction in direction_from_hash(hashed_path):
            if (new_coordinate := current_coordinate + move(direction)) in floor_map:
                new_path = current_path + direction
                path_deque.append((new_coordinate, new_path))
    return current_path


def find_longest_path(initial_value: str, dimensions: Dimensions):
    floor_map = create_valid_coordinates(dimensions)
    goal = complex(*(dim - 1 for dim in dimensions))
    current_coordinate = complex(0, 0)
    current_path = ""
    path_deque = deque([(current_coordinate, current_path)])
    max_length_path: int = 0
    while path_deque:
        current_coordinate, current_path = path_deque.popleft()
        if current_coordinate == goal:
            if len(current_path) > max_length_path:
                max_length_path = len(current_path)
            continue
        hashed_path = md5_hash(initial_value + current_path)
        for direction in direction_from_hash(hashed_path):
            if (new_coordinate := current_coordinate + move(direction)) in floor_map:
                new_path = current_path + direction
                path_deque.append((new_coordinate, new_path))
    return max_length_path


def part_a() -> str:
    return find_shortest_path("vwbaicqe", (4, 4))


def part_b() -> int:
    return find_longest_path("vwbaicqe", (4, 4))


def examples():
    print(find_shortest_path("ihgpwlah", (4, 4)) == "DDRRRD")
    print(find_shortest_path("kglvqrro", (4, 4)) == "DDUDRLRRUDRD")
    print(find_shortest_path("ulqzkmiv", (4, 4)) == "DRURDRUDDLLDLUURRDULRLDUUDDDRR")

    print(find_longest_path("ihgpwlah", (4, 4)) == 370)
    print(find_longest_path("kglvqrro", (4, 4)) == 492)
    print(find_longest_path("ulqzkmiv", (4, 4)) == 830)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
