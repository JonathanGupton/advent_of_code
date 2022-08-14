from collections import deque
from typing import Optional


X = int
Y = int
Coordinate = tuple[X, Y]


class FloorMap:
    def __init__(self, office_designer_favorite_number: int):
        self.office_designer_favorite_number = office_designer_favorite_number

    def is_open_space(self, x, y):
        result = bin(
            x * x + 3 * x + 2 * x * y + y + y * y + self.office_designer_favorite_number
        )[2:]
        n_ones = 0
        for i in result:
            if i == "1":
                n_ones += 1
        is_open_space = n_ones % 2 == 0
        return is_open_space


def find_adjacent_coordinates(x: X, y: Y) -> Coordinate:
    adjacent_coordinates = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]
    for new_x, new_y in adjacent_coordinates:
        if new_x + x >= 0 and new_y + y >= 0:
            yield (new_x + x, new_y + y)
        else:
            continue


def part_a() -> int:
    office_designer_favorite_number = 1358
    fm = FloorMap(office_designer_favorite_number)
    x_target = 31
    y_target = 39

    root = (1, 1)
    q = deque()
    explored = {root}
    q.append([root])
    route_length = 0
    while q:
        current_group = q.popleft()
        new_group = []
        for current in current_group:
            if current[0] == x_target and current[1] == y_target:
                return route_length
            for adjacent in find_adjacent_coordinates(*current):
                if adjacent not in explored and fm.is_open_space(*adjacent):
                    explored.add(adjacent)
                    new_group.append(adjacent)
        q.append(new_group)
        route_length += 1


def part_b() -> int:
    office_designer_favorite_number = 1358
    fm = FloorMap(office_designer_favorite_number)
    target_route_length = 50

    root = (1, 1)
    q = deque()
    explored = {root}
    q.append([root])
    route_length = 0
    locations_found = 1
    while q and route_length != target_route_length:
        current_group = q.popleft()
        new_group = []
        for current in current_group:
            for adjacent in find_adjacent_coordinates(*current):
                if adjacent not in explored and fm.is_open_space(*adjacent):
                    explored.add(adjacent)
                    new_group.append(adjacent)
        locations_found += len(new_group)
        q.append(new_group)
        route_length += 1
    return locations_found


if __name__ == '__main__':
    print(part_a())
    print(part_b())
