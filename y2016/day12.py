
class AssembunnyComputer:
    def __init__(self, instructions: list[str], register: dict[str, int]):
        self.register = register
        self.instructions = [instruction.split() for instruction in instructions]
        self.instruction_position = 0
        self.instructions_length = len(self.instructions)

    def process_instructions(self) -> None:
        while self.instruction_position < self.instructions_length:
            instruction = self.instructions[self.instruction_position]
            match instruction:
                case ["cpy", x, y]:
                    try:
                        x = int(x)
                        self.register[y] = x
                    except ValueError:
                        self.register[y] = self.register[x]
                    self.instruction_position += 1
                case ["inc", x]:
                    self.register[x] += 1
                    self.instruction_position += 1
                case ["dec", x]:
                    self.register[x] -= 1
                    self.instruction_position += 1
                case ["jnz", x, y]:
                    try:
                        x = int(x)
                    except ValueError:
                        x = self.register[x]
                    if x == 0:
                        self.instruction_position += 1
                    else:
                        self.instruction_position += int(y)


def part_a() -> int:
    with open(r"data/day12.txt", "r") as f:
        instructions = f.read().strip().split("\n")
    ac = AssembunnyComputer(
        instructions=instructions, register={"a": 0, "b": 0, "c": 0, "d": 0}
    )
    ac.process_instructions()
    return ac.register["a"]


def part_b() -> int:
    with open(r"data/day12.txt", "r") as f:
        instructions = f.read().strip().split("\n")
    ac = AssembunnyComputer(
        instructions=instructions, register={"a": 0, "b": 0, "c": 1, "d": 0}
    )
    ac.process_instructions()
    return ac.register["a"]


if __name__ == "__main__":
    print(part_a())
    print(part_b())
