from itertools import product


class Screen:
    ON = "█"
    OFF = "░"

    def __init__(self, height: int = 6, width: int = 50) -> None:
        self.height = height
        self.width = width
        self.screen = [[self.OFF] * width for _ in range(height)]

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.screen])

    def parse_instruction(self, instruction: str) -> None:
        match instruction.split():
            case ['rect', dim]:
                x, y = dim.split("x")
                x, y = int(x), int(y)
                self.set_rectangle(x, y)
            case ['rotate', 'row', target_row, 'by', n_pixels]:
                target_row = int(target_row[2:])
                n_pixels = int(n_pixels)
                self.rotate_row(target_row, n_pixels)
            case ['rotate', 'column', target_column, 'by', n_pixels]:
                target_column = int(target_column[2:])
                n_pixels = int(n_pixels)
                self.rotate_column(target_column, n_pixels)
            case _:
                raise ValueError(f"Invalid instruction: {instruction}")

    def set_rectangle(self, x, y) -> None:
        for col, row in product(range(x), range(y)):
            self.screen[row][col] = self.ON

    def rotate_row(self, row: int, n_pixels: int) -> None:
        self.screen[row] = self.screen[row][-n_pixels:] + self.screen[row][:-n_pixels]

    def rotate_column(self, column: int, n_pixels: int) -> None:
        col_vals = [row[column] for row in self.screen]
        rotated = col_vals[-n_pixels:] + col_vals[:-n_pixels]
        for row, val in enumerate(rotated):
            self.screen[row][column] = val

    @property
    def number_of_lit_pixels(self) -> int:
        lit = 0
        for row, column in product(range(self.height), range(self.width)):
            if self.screen[row][column] == self.ON:
                lit += 1
        return lit


def part_a():
    s = Screen()
    with open(r"data/day8.txt", "r") as f:
        for instruction in f.readlines():
            instruction = instruction.strip()
            s.parse_instruction(instruction)
            print()
            print(s)
    print()
    print(f"Lit pixels:  {s.number_of_lit_pixels}")


if __name__ == "__main__":
    part_a()