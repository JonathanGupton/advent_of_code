
Coordinate = complex


class CoordinateMap:
    SAFE = True
    TRAP = False

    def __init__(self, seed_row: str, n_rows: int):
        self.seed_row = seed_row
        self.n_rows = n_rows
        self.map: dict[Coordinate, bool] = {}

        for i, val in enumerate(seed_row):
            coordinate = complex(0, i)
            self.map[coordinate] = self.TRAP if val == "^" else self.SAFE

        row_width = len(seed_row)
        for row_number in range(1, n_rows):
            previous_row = row_number - 1
            for col in range(row_width):
                left = self.map.get(complex(previous_row, col - 1), self.SAFE)
                middle = self.map.get(complex(previous_row, col), self.SAFE)
                right = self.map.get(complex(previous_row, col + 1), self.SAFE)

                match [left, middle, right]:
                    case [self.TRAP, self.TRAP, self.SAFE]:
                        coordinate_value = self.TRAP
                    case [self.SAFE, self.TRAP, self.TRAP]:
                        coordinate_value = self.TRAP
                    case [self.TRAP, self.SAFE, self.SAFE]:
                        coordinate_value = self.TRAP
                    case [self.SAFE, self.SAFE, self.TRAP]:
                        coordinate_value = self.TRAP
                    case _:
                        coordinate_value = self.SAFE
                self.map[complex(row_number, col)] = coordinate_value

    @property
    def n_safe(self):
        return sum(self.map.values())


def file_io(filepath) -> str:
    with open(filepath, "r") as f:
        data = f.read().strip()
    return data


def part_a():
    fp = r"data/day18.txt"
    data = file_io(fp)
    cm = CoordinateMap(seed_row=data, n_rows=40)
    return cm.n_safe


def part_b():
    fp = r"data/day18.txt"
    data = file_io(fp)
    cm = CoordinateMap(seed_row=data, n_rows=400000)
    return cm.n_safe


if __name__ == '__main__':
    print(part_a())
    print(part_b())
