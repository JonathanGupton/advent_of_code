import collections
from math import ceil

def part_a() -> int:
    n_elves = 3004953
    elves = [*range(n_elves)]
    while len(elves) > 1:
        compressed_elves = [elf for elf in elves[::2]]
        if len(elves) % 2 == 1:
            elves = compressed_elves[1:]
        else:
            elves = compressed_elves
    return elves[0] + 1


def compress_across_elves(elves: list[int]) -> int:
    while (n_elves := len(elves)) > 1:
        if n_elves % 2 == 0:
            middle = ceil((n_elves - 1) / 2)
            current, left, _, right = [elves[0]], elves[1:middle], elves[middle], elves[middle + 1:]
        else:
            current, left, right = [elves[0]], elves[1:n_elves // 2], elves[(n_elves // 2) + 1:]
        elves = left + right + current
        print(elves)
    return elves[0]


elves = [i for i in range(1, 100 + 1)]
print(compress_across_elves(elves))
#
# def solve_parttwo():
#     target = 3004953
#     i = 1
#
#     while i * 3 < target:
#         i *= 3
#
#     print(target - i)
#
#
# solve_parttwo()

# print(part_a())


