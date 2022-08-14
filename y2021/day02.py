from typing import Generator, Literal


Direction = Literal['forward', 'up', 'down']
Distance = int
Instruction = tuple[Direction, Distance]


def parse_directions(filepath) -> Generator[Instruction, None, None]:
    with open(filepath, 'r') as f:
        for line in f:
            direction, distance = line.split()
            yield direction, int(distance)


class Submarine:
    def __init__(self) -> None:
        self.depth = 0
        self.horizontal_position = 0
        self.aim = 0

    def navigate(self, instruction: Instruction) -> None:
        match instruction:
            case ("forward", forward_distance):
                self.horizontal_position += forward_distance
                self.depth += self.aim * forward_distance
            case ("down", aim_down):
                self.aim += aim_down
            case ("up", aim_up):
                self.aim -= aim_up


def part_a():
    fp = r"data/day02.txt"
    submarine = Submarine()
    for instruction in parse_directions(fp):
        submarine.navigate(instruction)
    return submarine.aim * submarine.horizontal_position


def part_b():
    fp = r"data/day02.txt"
    submarine = Submarine()
    for instruction in parse_directions(fp):
        submarine.navigate(instruction)
    return submarine.depth * submarine.horizontal_position


if __name__ == '__main__':
    print(part_a())
    print(part_b())
