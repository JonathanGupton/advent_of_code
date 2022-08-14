from collections import deque
from typing import Literal

DIRECTION = Literal["R", "L"]
DISTANCE = int
INSTRUCTION = tuple[DIRECTION, DISTANCE]
ORIENTATION = Literal["N", "E", "S", "W"]


def file_io(input_file):
    with open(input_file, "r") as f:
        data = f.read().split(", ")
    clean_data = [(instruction[0], int(instruction[1:])) for instruction in data]
    return clean_data


class Point:
    def __init__(self, starting_orientation: ORIENTATION = "N", x: int = 0, y: int = 0):
        self.orientation = deque(["N", "E", "S", "W"], maxlen=4)
        while self.orientation[0] != starting_orientation:
            self.rotate("L")
        self.x = x
        self.y = y

    def move(self, direction: DIRECTION, distance: DISTANCE) -> None:
        self.rotate(direction)
        self.advance(distance)

    def rotate(self, direction: DIRECTION) -> None:
        match direction:
            case "L":
                self.orientation.rotate(1)
            case "R":
                self.orientation.rotate(-1)
            case _:
                raise ValueError(f"{direction} is an invalid direction.  Must be 'R' or 'L'.")

    def advance(self, distance: DISTANCE) -> None:
        match self.orientation[0]:
            case "N":
                self.y += distance
            case "E":
                self.x += distance
            case "S":
                self.y -= distance
            case "W":
                self.x -= distance

    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


def part_a() -> int:
    input_filepath = r"data/day1.txt"
    data = file_io(input_filepath)
    p = Point()
    for instruction in data:
        p.move(*instruction)
    return p.manhattan_distance()


def part_b() -> int:
    input_filepath = r"data/day1.txt"
    data = file_io(input_filepath)
    p = Point()
    visited = {(0, 0)}
    for rotation, distance in data:
        p.rotate(rotation)
        for i in range(distance):
            p.advance(1)
            if (current_location := (p.x, p.y)) in visited:
                return p.manhattan_distance()
            else:
                visited.add(current_location)


if __name__ == "__main__":
    print(part_a())
    print(part_b())
