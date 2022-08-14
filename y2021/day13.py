from typing import Literal, Sequence

Axis = Literal['x', 'y']
Instruction = tuple[Axis, int]
Coordinate = tuple[int, int]


def input_parser(filepath) -> tuple[list[Coordinate], list[Instruction]]:
    with open(filepath, "r") as f:
        positions_str, instructions_str = f.read().split("\n\n")

    positions: list[Coordinate] = []
    for position in positions_str.split('\n'):
        position = position.split(',')
        x = int(position[0])
        y = int(position[1])
        positions.append((x, y))

    instructions: list[Instruction] = []
    for instruction in instructions_str.split('\n'):
        instruction = instruction.split()[-1].split("=")
        instruction[-1] = int(instruction[-1])
        instructions.append(instruction)
    return positions, instructions


class Transparency:
    def __init__(self, initial_positions: Sequence[Coordinate]) -> None:
        self.positions = set(initial_positions)
        self.x_max = max(self.positions, key=lambda x: x[0])[0]
        self.y_max = max(self.positions, key=lambda x: x[1])[1]

    def __len__(self) -> int:
        return len(self.positions)

    def __str__(self) -> str:
        transparency = [[' '] * self.x_max for _ in range(self.y_max)]
        for position in self.positions:
            x = position[0]
            y = position[1]
            transparency[y][x] = '█'
        output = '\n'.join([''.join(row) for row in transparency])
        return output

    def _fold_up(self, line: int) -> None:
        new_positions = set()
        for position in self.positions:
            if position[1] > line:
                new_y = line - (position[1] - line)
                new_positions.add((position[0], new_y))
            else:
                new_positions.add(position)
        self.positions = new_positions
        self.y_max = line

    def _fold_left(self, line: int) -> None:
        new_positions = set()
        for position in self.positions:
            if position[0] > line:
                new_x = line - (position[0] - line)
                new_positions.add((new_x, position[1]))
            else:
                new_positions.add(position)
        self.positions = new_positions
        self.x_max = line

    def fold(self, instruction: Instruction) -> None:
        match instruction:
            case ('x', x_line):
                self._fold_left(x_line)
            case ('y', y_line):
                self._fold_up(y_line)


def part_a() -> int:
    fp = r"data/day13.txt"
    pos, ins = input_parser(fp)
    transparency = Transparency(pos)
    transparency.fold(ins[0])
    return len(transparency)


def part_b() -> str:
    fp = r"data/day13.txt"
    initial_positions, instructions = input_parser(fp)
    transparency = Transparency(initial_positions)
    for instruction in instructions:
        transparency.fold(instruction)
    return str(transparency)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
