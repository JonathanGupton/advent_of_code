from functools import cache
from itertools import permutations


def file_io():
    with open(r"data/day21.txt", "r") as f:
        instructions = tuple(line.strip() for line in f.readlines())
    return instructions


def swap_positions(password: list[str], position_1: int, position_2: int) -> list[str]:
    password[position_1], password[position_2] = password[position_2], password[position_1]
    return password


def rotate(password: list[str], direction: str, n_steps: int) -> list[str]:
    n_steps = n_steps % len(password)
    if direction == "right":
        return password[-n_steps:] + password[:-n_steps]
    else:
        return password[n_steps:] + password[:n_steps]


@cache
def scramble_password(password: str, instructions: tuple[str]) -> str:
    password = [*password]
    for instruction in instructions:
        instruction = instruction.split()
        match instruction:
            case ["move", "position", p1, "to", "position", p2]:
                p1, p2 = int(p1), int(p2)
                password.insert(p2, password.pop(p1))
            case ["reverse", "positions", p1, "through", p2]:
                p1, p2 = int(p1), int(p2)
                if p1 == 0:
                    password = password[0:p1] + password[p2::-1] + password[p2+1:]
                else:
                    password = password[0:p1] + password[p2:p1-1:-1] + password[p2 + 1:]
            case ["rotate", "based", "on", "position", "of", "letter", letter]:
                letter_idx = password.index(letter)
                n_steps = 1 + letter_idx
                if letter_idx >= 4:
                    n_steps += 1
                password = rotate(password, 'right', n_steps)
            case ["rotate", direction, n_steps, _]:
                n_steps = int(n_steps)
                password = rotate(password, direction, n_steps)
            case ["swap", "letter", letter_1, "with", "letter", letter_2]:
                p1, p2 = password.index(letter_1), password.index(letter_2)
                password = swap_positions(password, p1, p2)
            case ["swap", "position", p1, "with", "position", p2]:
                p1, p2 = int(p1), int(p2)
                password = swap_positions(password, p1, p2)
    return ''.join(password)


def unscramble_password(password: str, instructions: tuple[str]) -> str:
    password = [*password]
    for instruction in instructions:
        instruction = instruction.split()
        match instruction:
            case ["move", "position", p2, "to", "position", p1]:
                p1, p2 = int(p1), int(p2)
                password.insert(p2, password.pop(p1))
            case ["reverse", "positions", p1, "through", p2]:
                p1, p2 = int(p1), int(p2)
                if p1 == 0:
                    password = password[0:p1] + password[p2::-1] + password[p2 + 1:]
                else:
                    password = password[0:p1] + password[p2:p1 - 1:-1] + password[p2 + 1:]
            case ["rotate", "based", "on", "position", "of", "letter", letter]:
                letter_idx = password.index(letter)
                n_steps = 1 + letter_idx
                if letter_idx >= 4:
                    n_steps += 1
                password = rotate(password, 'left', n_steps)
            case ["rotate", direction, n_steps, _]:
                n_steps = int(n_steps)
                direction = "right" if direction == "left" else "left"
                password = rotate(password, direction, n_steps)
            case ["swap", "letter", letter_1, "with", "letter", letter_2]:
                p1, p2 = password.index(letter_1), password.index(letter_2)
                password = swap_positions(password, p1, p2)
            case ["swap", "position", p1, "with", "position", p2]:
                p1, p2 = int(p1), int(p2)
                password = swap_positions(password, p1, p2)
    return ''.join(password)


def check_scrambler():
    password = "abcde"
    instructions = ("swap position 4 with position 0",
                    "swap letter d with letter b",
                    "reverse positions 0 through 4",
                    "rotate left 1 step",
                    "move position 1 to position 4",
                    "move position 3 to position 0",
                    "rotate based on position of letter b",
                    "rotate based on position of letter d",
                    )
    password = scramble_password(password, instructions)
    print(password)


def find_unscrambled(password_chars: str, target: str, instructions: tuple[str]) -> str:
    for pw in permutations(password_chars):
        pw = ''.join(pw)
        if scramble_password(pw, instructions) == target:
            return pw


# data = file_io()
# password = "gfdhebac"
# data = tuple(reversed(data))
# print(scramble_password(password, data))

initial_chars = "abcdefgh"
target = "fbgdceah"
instructions = file_io()

pw = find_unscrambled(initial_chars, target, instructions)
print(pw)
