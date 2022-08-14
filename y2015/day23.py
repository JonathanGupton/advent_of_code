

def process(instructions: list[list[str]], registry: dict[str, int]) -> int:
    position: int = 0
    max_position: int = len(instructions)

    while position < max_position:
        instruction = instructions[position]
        match instruction:
            case ["inc", r]:
                registry[r] += 1
                position += 1
            case ["tpl", r]:
                registry[r] *= 3
                position += 1
            case ["hlf", r]:
                registry[r] /= 2
                position += 1
            case ["jmp", offset]:
                position += int(offset)
            case ["jie", r, offset]:
                if registry[r[:-1]] % 2 == 0:
                    position += int(offset)
                else:
                    position += 1
            case ["jio", r, offset]:
                if registry[r[:-1]] == 1:
                    position += int(offset)
                else:
                    position += 1
    return registry["b"]


with open(r"data/day23.txt") as f:
    s = [line.split() for line in f.readlines()]


print(process(s, {'a': 0, 'b': 0}))
print(process(s, {'a': 1, 'b': 0}))
