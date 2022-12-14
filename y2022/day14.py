from __future__ import annotations
from enum import Enum
from dataclasses import dataclass


class T(Enum):
    Rock = "#"
    Sand = "+"
    Air = "."


@dataclass
class Coordinate:
    x: int
    y: int


class Sand:
    def __init__(self, coordinate: Coordinate, cave: Cave) -> None:
        self.coordinate = coordinate
        self.cave = cave
        self.stopped = False

    def drop(self) -> Coordinate:
        while not self.stopped:
            next_coordinate = Coordinate(self.coordinate.x, self.coordinate.y + 1)

            if self.cave.arr[next_coordinate.y][next_coordinate.x] == T.Air:
                self.coordinate = next_coordinate
                if next_coordinate.y == self.cave.y_max:
                    break
                continue

            next_coordinate = Coordinate(self.coordinate.x - 1, self.coordinate.y + 1)
            if self.cave.arr[next_coordinate.y][next_coordinate.x] == T.Air:
                self.coordinate = next_coordinate
                if self.coordinate.y == self.cave.y_max:
                    break
                continue

            next_coordinate = Coordinate(self.coordinate.x + 1, self.coordinate.y + 1)
            if self.cave.arr[next_coordinate.y][next_coordinate.x] == T.Air:
                self.coordinate = next_coordinate
                if self.coordinate.y == self.cave.y_max:
                    break
                continue

            self.stopped = True

        return self.coordinate


class Cave:
    def __init__(self):
        self.origin = Coordinate(500, 0)  # sand starts here
        self.arr: list[list[T]] = [[T.Air for _ in range(1000)] for _ in range(1000)]
        self.x_min = len(self.arr[0])
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.rock_paths = []
        self.sand_count = 0

    def __str__(self):
        s = ""
        for row in range(self.y_min, self.y_max + 1):
            s += (
                "".join(
                    map(lambda x: x.value, self.arr[row][self.x_min : self.x_max + 1])
                )
                + "\n"
            )
        return s

    @classmethod
    def from_file(cls, filepath) -> Cave:
        c = Cave()
        with open(filepath, "r") as f:
            for line in f.readlines():
                c.add_rock_path_from_str(line)
        c.set_bounds()
        return c

    def set_bounds(self):
        for y, row in enumerate(self.arr):
            for x, val in enumerate(row):
                if val != T.Air:
                    if y > self.y_max:
                        self.y_max = y
                    if x < self.x_min:
                        self.x_min = x
                    if x > self.x_max:
                        self.x_max = x

    def add_rock_path_from_str(self, input_line: str) -> None:
        path: list[Coordinate] = []
        for pair in input_line.split(" -> "):
            path.append(Coordinate(*map(int, pair.split(","))))

        for i, coordinate in enumerate(path[1:], 1):
            self.add_rock_path(path[i - 1], coordinate)

    def add_rock_path(self, start: Coordinate, end: Coordinate):
        self.rock_paths.append((start, end))
        if start.x == end.x:
            x = start.x
            min_y, max_y = min(start.y, end.y), max(start.y, end.y)
            self.draw_vertical_rock(min_y, max_y, x)
        else:
            y = start.y
            min_x, max_x = min(start.x, end.x), max(start.x, end.x)
            self.draw_horizontal_rock(min_x, max_x, y)

    def draw_vertical_rock(self, start, stop, x):
        for y in range(start, stop + 1):
            self.arr[y][x] = T.Rock

    def draw_horizontal_rock(self, start, stop, y):
        for x in range(start, stop + 1):
            self.arr[y][x] = T.Rock

    def draw_sand(self, coordinate) -> None:
        self.arr[coordinate.y][coordinate.x] = T.Sand

    def simulate_sand(self, print_=False) -> int:
        while True:
            sand = Sand(self.origin, self)
            coordinate = sand.drop()
            if coordinate.y >= self.y_max:
                break
            else:
                self.draw_sand(coordinate)
            self.sand_count += 1
            if print_:
                print()
                print(f"{self.sand_count}")
                print(f"{self}")

        return self.sand_count

    def simulate_infinite_floor(self, print_=False) -> int:
        pass


def part_one(filepath) -> int:
    c = Cave.from_file(filepath)
    sand_count = c.simulate_sand()
    return sand_count


def part_two(filepath) -> int:
    pass


if __name__ == "__main__":
    example = (
        r"C:\Users\Emily\PycharmProjects\advent_of_code\y2022\data\day14_example.txt"
    )
    data = r"C:\Users\Emily\PycharmProjects\advent_of_code\y2022\data\day14.txt"
    print(part_one(example))
    print(part_one(data))