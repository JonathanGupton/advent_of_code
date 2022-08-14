from __future__ import annotations
from itertools import permutations
from typing import Iterable, Mapping
import re

Coordinate = complex
Data = int


def file_io(filepath) -> FileMap:
    pattern = r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<use_percent>\d+)%"
    filemap = FileMap()
    with open(filepath, "r") as f:
        f.readline()
        f.readline()
        for line in f.readlines():
            x, y, size, used, avail, use_p = (
                int(val) for val in re.findall(pattern, line.strip())[0]
            )
            location = complex(x, y)
            datum = Datum(size, location)
            filemap[location] = FileNode(
                coordinate=location, data=datum, used=used, avail=avail, use_p=use_p
            )
    return filemap


class Datum:
    def __init__(self, size: int, initial_coordinate: Coordinate) -> None:
        self.size = size
        self.initial_coordinate = initial_coordinate

    def __repr__(self):
        return f"{self.__class__.__name__}(size={self.size}, initial_coordinate={self.initial_coordinate})"

    def __add__(self, other):
        return self.size + other.size

    def __radd__(self, other):
        return self.__add__(other)


class FileNode:
    def __init__(
            self, coordinate: Coordinate, size: int, used: int, avail: int, use_p: int
    ) -> None:
        self.coordinate = coordinate
        self.size = size
        self.data = [data]
        self.used = used
        self.avail = avail
        self.used_pct = use_p

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={self.size}, used={self.used}, avail={self.avail}, used_pct={self.used_pct}) "

    def __hash__(self) -> int:
        return hash((self.size, self.used, self.avail, self.used_pct, self.coordinate))

    @property
    def used(self):
        return sum(self.data)

    def is_viable_pair(self, other: FileNode) -> bool:
        return (self.used != 0) and (self.used < other.avail)

    def add_data(self, data: Data) -> None:
        if self.used == 0:
            self.used += data
            self.avail -= data

    def remove_data(self, data: Data) -> None:
        self.used = 0
        self.avail += data

    def move_data_to_other(self, data: Data, other: FileNode) -> None:
        other.add_data(data)
        self.remove_data(data)


class FileMap(dict, Mapping[Coordinate, FileNode]):
    def __init__(self, nodes: Iterable[FileNode] = None) -> None:
        super().__init__()
        if nodes:
            for node in nodes:
                self[node.coordinate] = node

    def __hash__(self) -> int:
        return hash((coordinate, node) for coordinate, node in self.items())

    def swap_nodes(self, coord_a: Coordinate, coord_b: Coordinate) -> None:
        self[coord_a], self[coord_b] = self[coord_b], self[coord_a]


def count_viable_pairs(node_map: dict[complex, FileNode]) -> int:
    viable = 0
    for node_a, node_b in permutations(node_map.keys(), 2):
        if node_map[node_a].is_viable_pair(node_map[node_b]):
            viable += 1
    return viable


def part_a():
    fp = r"data/day22.txt"
    nodes = file_io(fp)
    viable = count_viable_pairs(nodes)
    return viable


# filepath = r"data/day22.txt"
filepath = r"data/day22_example.txt"
fm = file_io(filepath)
print(part_a())
