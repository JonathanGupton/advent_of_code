from collections import deque
from typing import Sequence


Coordinate = complex


class BingoTable:
    def __init__(self, table: str) -> None:
        self.table_string = table
        self.values: dict[int, Coordinate] = {}
        self.found: dict[Coordinate, bool] = {}
        self.winning = False
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.score = 0

        for y, row in enumerate(table.split("\n")):
            for x, val in enumerate(row.split()):
                self.values[int(val)] = complex(y, x)
                self.found[complex(y, x)] = False
                self.y_max = y
                self.x_max = x

    def __contains__(self, drawn_value: int) -> bool:
        return drawn_value in self.values

    def __str__(self):
        return self.table_string

    def __repr__(self):
        return f"{self.__class__.__name__}({self.table_string})"

    def check_row(self, row_index: float) -> bool:
        return all(
            self.found[complex(row_index, col)]
            for col in range(self.y_min, self.y_max + 1)
        )

    def check_column(self, column_index: float) -> bool:
        return all(
            self.found[complex(row, column_index)]
            for row in range(self.x_min, self.x_max + 1)
        )

    def play_drawn_number(self, drawn_number: int) -> None:
        if drawn_number in self:
            location = self.values[drawn_number]
            self.found[location] = True
            if self.check_row(location.real) or self.check_column(location.imag):
                self.winning = True
                self.score = drawn_number * self.unmarked_sum

    @property
    def unmarked_sum(self) -> int:
        unmarked_sum = 0
        for k, v in self.values.items():
            unmarked_sum += k if not self.found[v] else 0
        return unmarked_sum


def parse_input(filepath) -> tuple[list[int], list[BingoTable]]:
    with open(filepath, "r") as f:
        draw_order, *table_strings = f.read().split("\n\n")
    draw_order = [int(i) for i in draw_order.split(",")]
    parsed_tables = [BingoTable(table) for table in table_strings]
    return draw_order, parsed_tables


def find_first_winning_score(
    draw_order: list[int], bingo_tables: list[BingoTable]
) -> int:
    for draw in draw_order:
        for table in bingo_tables:
            table.play_drawn_number(draw)
            if table.winning:
                return table.score


def find_last_winning_score(
    draw_order: Sequence[int], bingo_tables: Sequence[BingoTable]
) -> int:
    bingo_queue = deque(bingo_tables)
    winning_tables = deque()
    for draw in draw_order:
        temp_queue = deque()
        if not bingo_queue:
            return winning_tables[-1].score
        while bingo_queue:
            current = bingo_queue.popleft()
            current.play_drawn_number(draw)
            if current.winning:
                winning_tables.append(current)
            else:
                temp_queue.append(current)
        bingo_queue = temp_queue


def part_a() -> int:
    fp = r"data/day04.txt"
    draw_order, tables = parse_input(fp)
    return find_first_winning_score(draw_order, tables)


def part_b() -> int:
    fp = r"data/day04.txt"
    draw_order, tables = parse_input(fp)
    return find_last_winning_score(draw_order, tables)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
