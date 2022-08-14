from __future__ import annotations
from dataclasses import dataclass
from itertools import permutations, product
from typing import Iterable, Optional
import re


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"


class DataObject:
    def __init__(self, initial_coordinate: Coordinate, space_used: int):
        self.initial_coordinate = initial_coordinate
        self.space = space_used

    def __hash__(self):
        return hash((self.initial_coordinate, self.space))

    def __add__(self, other):
        return self.space + other

    def __radd__(self, other):
        return self.space + other


class Node:
    def __init__(
        self,
        coordinate: Coordinate,
        size: int,
        avail: int,
        initial_space_used: DataObject,
    ):
        self.coordinate = coordinate
        self.size = size
        self.avail = avail
        self._used = [initial_space_used]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(coordinate={self.coordinate}, " \
               f"size={self.size}, avail={self.avail}, used={self.used}) "

    @property
    def used(self) -> int:
        return sum(self._used)

    def is_viable_pair(self, other: Node) -> bool:
        return (self.used != 0) and (self.used < other.avail)


class FileMap:
    def __init__(self):
        self.nodes: dict[Coordinate, Node] = {}
        self.max_x = 0
        self.max_y = 0

    def __repr__(self):
        return f"{self.__class__.__name__}(nodes={self.nodes})"

    def __str__(self):
        out = []
        for y in range(self.max_y + 1):
            row = []
            for x in range(self.max_x + 1):
                current_node = self.nodes[Coordinate(x, y)]
                used = current_node.used
                size = current_node.size
                node_val = f"{used:>3} / {size:>3}"
                row.append(node_val)
            out.append("\t".join(row))
        return "\n".join(out)

    def add_node(self, node: Node) -> None:
        self.nodes[node.coordinate] = node
        self.max_x = node.coordinate.x if node.coordinate.x > self.max_x else self.max_x
        self.max_y = node.coordinate.y if node.coordinate.y > self.max_y else self.max_y

    def count_viable_pairs(self) -> int:
        viable = 0
        for node_a, node_b in permutations(self.nodes.keys(), 2):
            if self.nodes[node_a].is_viable_pair(self.nodes[node_b]):
                viable += 1
        return viable


def file_io(filepath):
    pattern = r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<use_percent>\d+)%"
    filemap = FileMap()
    with open(filepath, "r") as f:
        f.readline()
        f.readline()
        for line in f.readlines():
            x, y, size, used, avail, use_p = (
                int(val) for val in re.findall(pattern, line.strip())[0]
            )
            coordinate = Coordinate(x, y)
            data = DataObject(coordinate, used)
            filemap.add_node(Node(coordinate, size, avail, data))
        return filemap


filepath = r"data/day22.txt"
# filepath = r"data/day22_example.txt"
fm = file_io(filepath)
# print(fm)
print(fm.count_viable_pairs())