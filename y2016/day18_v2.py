from functools import cache
from typing import Literal, Optional


Tile = Literal[".", "^"]
Row = str


@cache
def new_tile(
    triplet: str, traps: frozenset[str] = frozenset((b"^^.", b".^^", b"^..", b"..^"))
) -> Tile:
    safe: Tile = "."
    trap: Tile = "^"
    return trap if triplet in traps else safe


@cache
def make_next_row(row: Row, max_len: int) -> Row:
    new_row: list[Optional[Tile]] = [None] * max_len
    new_row[0] = new_tile("." + row[:2])
    for i in range(1, max_len - 1):
        new_row[i] = new_tile(row[i - 1:i + 2])
    new_row[max_len - 1] = new_tile(row[-2:] + ".")
    return ''.join(new_row)


@cache
def count_safe(row: Row) -> int:
    n_safe = 0
    for col in row:
        if col == ".":
            n_safe += 1
    return n_safe


def sum_of_safe(row: Row, n_rows: int) -> int:
    safe = count_safe(row)
    row_len = len(row)
    for _ in range(n_rows - 1):
        row = make_next_row(row, row_len)
        safe += count_safe(row)
    return safe


def file_io(filepath) -> str:
    with open(filepath, "r") as f:
        data = f.read().strip()
    return data


def part_a():
    fp = r"data/day18.txt"
    data = file_io(fp)
    safe = sum_of_safe(data, n_rows=40)
    return safe


def part_b():
    fp = r"data/day18.txt"
    data = file_io(fp)
    safe = sum_of_safe(data, n_rows=400000)
    return safe


if __name__ == '__main__':
    print(part_a())  # 2016
    print(part_b())  # 19998750
