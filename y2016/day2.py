from typing import Optional, Union


KEYPAD_VALUES = Union[str, int]
ROW = list

def file_io(filename) -> list[str]:
    with open(filename, "r") as f:
        instructions = f.read().strip().split("\n")
    return instructions


class Keypad:
    def __init__(self,
                 keypad: list[ROW[Optional[KEYPAD_VALUES]]],
                 start_x: int,
                 start_y: int
                 ) -> None:
        self.keypad = keypad
        self.x = start_x
        self.y = start_y
        self.min_x, self.max_x = 0, len(self.keypad[0]) - 1
        self.min_y, self.max_y = 0, len(self.keypad) - 1
        self._code: list[KEYPAD_VALUES] = []

    @property
    def code(self) -> str:
        return "".join([str(i) for i in self._code])

    def process_instruction(self, instruction: str):
        for direction in instruction:
            match direction:
                case "U":
                    if self.y > self.min_y and self.keypad[self.y - 1][self.x]:
                        self.y -= 1
                case "L":
                    if self.x > self.min_x and self.keypad[self.y][self.x - 1]:
                        self.x -= 1
                case "D":
                    if self.y < self.max_y and self.keypad[self.y + 1][self.x]:
                        self.y += 1
                case "R":
                    if self.x < self.max_x and self.keypad[self.y][self.x + 1]:
                        self.x += 1
        self._code.append(self.keypad[self.y][self.x])


def part_a() -> str:
    input_file = r"data/day2.txt"
    instructions = file_io(input_file)
    kp = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    d = Keypad(keypad=kp, start_x=1, start_y=1)
    for instruction in instructions:
        d.process_instruction(instruction)
    return d.code


def part_b() -> str:
    input_file = r"data/day2.txt"
    instructions = file_io(input_file)
    kp = [
        [None, None, 1, None, None],
        [None, 2, 3, 4, None],
        [5, 6, 7, 8, 9],
        [None, "A", "B", "C", None],
        [None, None, "D", None, None]
    ]
    d = Keypad(keypad=kp, start_x=0, start_y=2)
    for instruction in instructions:
        d.process_instruction(instruction)
    return d.code


if __name__ == '__main__':
    print(part_a())
    print(part_b())