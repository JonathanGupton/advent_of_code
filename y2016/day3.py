from typing import Sequence


EDGE = int
EDGES = Sequence[EDGE]


def parse_line(line: str) -> EDGES:
    return [int(num) for num in line.strip().split()]


def is_valid_triangle(edges: EDGES) -> bool:
    return max(edges) < sum(edges) - max(edges)


def part_a():
    input_file = r"data/day3.txt"
    possible_triangles = 0
    with open(input_file, "r") as f:
        for line in f.readlines():
            edges = parse_line(line)
            if is_valid_triangle(edges):
                possible_triangles += 1
    return possible_triangles


def part_b():
    input_file = r"data/day3.txt"
    possible_triangles = 0
    with open(input_file, "r") as f:
        lines = []
        for line in f:
            lines.append(parse_line(line))
            if len(lines) == 3:
                for edges in zip(*lines):
                    if is_valid_triangle(edges):
                        possible_triangles += 1
                lines = []
    return possible_triangles


if __name__ == '__main__':
    print(part_a())
    print(part_b())
