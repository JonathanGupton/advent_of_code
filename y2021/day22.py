from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
import re
from typing import Generator


@dataclass(frozen=True)
class Vertex:
    x: int
    y: int
    z: int

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


class Cuboid:
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max):
        self.x_range = (x_min, x_max)
        self.y_range = (y_min, y_max)
        self.z_range = (z_min, z_max)

        self.vertices = defaultdict(list)
        for x, y, z in product(self.x_range, self.y_range, self.z_range):
            vertex = Vertex(x, y, z)

            self.vertices[vertex] = []

            # add adjacent vertices
            other_x = self.x_range[0] if self.x_range[1] == x else self.x_range[1]
            self.vertices[vertex].append(Vertex(other_x, y, z))
            other_y = self.y_range[0] if self.y_range[1] == y else self.y_range[1]
            self.vertices[vertex].append(Vertex(x, other_y, z))
            other_z = self.z_range[0] if self.z_range[1] == z else self.z_range[1]
            self.vertices[vertex].append(Vertex(x, y, other_z))

    def __repr__(self):
        return f"Cuboid(x_range={self.x_range}, y_range={self.y_range}, z_range={self.z_range})"

    @property
    def volume(self):
        return (
            (self.x_range[1] - self.x_range[0])
            * (self.y_range[1] - self.y_range[0])
            * (self.z_range[1] - self.z_range[0])
        )

    def intersect(self, other: Cuboid) -> bool:
        return (
            (
                (self.x_range[0] <= other.x_range[1])
                & (self.x_range[1] >= other.x_range[0])
            )
            & (
                (self.y_range[0] <= other.y_range[1])
                & (self.y_range[1] >= other.y_range[0])
            )
            & (
                (self.z_range[0] <= other.z_range[1])
                & (self.z_range[1] >= other.z_range[0])
            )
        )


class Reactor:
    def __init__(self):
        self.vertices: dict[Vertex, list[Vertex]] = {}
        self.volume = 0

    def add_cuboid(self, cuboid: Cuboid) -> None:
        if not self.vertices:
            self.vertices = cuboid.vertices
            self.volume = cuboid.volume
        else:
            pass




def generate_reboot_steps(filepath) -> Generator[str, None, None]:
    with open(filepath, "r") as f:
        for line in f.readlines():
            yield line.strip()


if __name__ == "__main__":
    fp = r"data/day22_example_a_1.txt"
    # fp = r"data/day22_example_a_2.txt"
    # fp = r"data/day22.txt"
    c = []
    pattern = r"\b(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    with open(fp, "r") as f:
        for line in f.readlines():
            instruction, *ranges = re.match(pattern, line).groups()
            c.append(Cuboid(*tuple(map(int, ranges))))

    r = Reactor()
    r.add_cuboid(c[0])
    