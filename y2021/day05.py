from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Generator


@dataclass(frozen=True, order=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> Coordinate:
        new_x = self.x + other[0]
        new_y = self.y + other[1]
        return Coordinate(new_x, new_y)


SegmentPair = tuple[Coordinate, Coordinate]


class OceanMap:
    def __init__(self, parse_diagonal: bool = True):
        self._map: defaultdict[Coordinate, int] = defaultdict(int)
        self.parse_diagonal = parse_diagonal

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(parse_diagonal={self.parse_diagonal})"

    def __len__(self) -> int:
        return len(self._map)

    def add_segment(self, segment_pair: SegmentPair) -> None:
        start, stop = segment_pair
        if start.y == stop.y:
            self.add_horizontal_segment(segment_pair)
        elif start.x == stop.x:
            self.add_vertical_segment(segment_pair)
        elif self.parse_diagonal:
            self.add_diagonal_segment(segment_pair)

    def add_horizontal_segment(self, segment_pair: SegmentPair) -> None:
        start, stop = segment_pair
        y = start.y
        min_x, max_x = min(start.x, stop.x), max(start.x, stop.x)
        for x in range(min_x, max_x + 1):
            self._map[Coordinate(x, y)] += 1

    def add_vertical_segment(self, segment_pair: SegmentPair) -> None:
        start, stop = segment_pair
        x = start.x
        min_y, max_y = min(start.y, stop.y), max(start.y, stop.y)
        for y in range(min_y, max_y + 1):
            self._map[Coordinate(x, y)] += 1

    def add_diagonal_segment(self, segment_pair: SegmentPair) -> None:
        start, stop = segment_pair
        x_delta = 1 if start.x < stop.x else -1
        y_delta = 1 if start.y < stop.y else -1
        current_position = start
        while current_position != stop:
            self._map[current_position] += 1
            current_position = current_position + (x_delta, y_delta)
        self._map[stop] += 1

    @property
    def n_overlapping_segments(self) -> int:
        return len([(k, v) for k, v in self._map.items() if v > 1])


def parse_input(filepath) -> Generator[SegmentPair, None, None]:
    with open(filepath, "r") as f:
        for line in f.readlines():
            l, *_, r = line.strip().split()
            l_x, l_y = l.split(",")
            l_x, l_y = int(l_x), int(l_y)
            r_x, r_y = r.split(",")
            r_x, r_y = int(r_x), int(r_y)
            yield Coordinate(l_x, l_y), Coordinate(r_x, r_y)


def part_a() -> int:
    fp = r"data/day05.txt"
    ocean_map = OceanMap(parse_diagonal=False)
    for coordinate_pair in parse_input(fp):
        ocean_map.add_segment(coordinate_pair)
    return ocean_map.n_overlapping_segments


def part_b() -> int:
    fp = r"data/day05.txt"
    ocean_map = OceanMap(parse_diagonal=True)
    for coordinate_pair in parse_input(fp):
        ocean_map.add_segment(coordinate_pair)
    return ocean_map.n_overlapping_segments


if __name__ == '__main__':
    print(part_a())
    # print(part_b())
