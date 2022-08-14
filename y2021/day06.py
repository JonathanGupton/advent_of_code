from collections import deque


def parse_input(filepath) -> list[int]:
    with open(filepath, "r") as f:
        return [int(i) for i in f.read().strip().split(",")]


class LanternfishSchool:
    def __init__(self, initial_fish: list[int]):
        self.initial_state = initial_fish
        self.school: deque[int] = deque([0] * 7)
        self.day_7 = 0
        self.day_8 = 0
        for fish in initial_fish:
            self.school[fish] += 1

    def __len__(self):
        return sum(self.school) + self.day_7 + self.day_8

    def __repr__(self):
        return f"{self.__class__.__name__}(initial_fish={self.initial_state})"

    def __str__(self):
        return str(self.school)

    def __iter__(self):
        return self

    def __next__(self):
        day_zero = self.school.popleft()
        self.school.append(day_zero + self.day_7)
        self.day_7, self.day_8 = self.day_8, day_zero


def part_a():
    fp = r"data/day06.txt"
    data = parse_input(fp)
    ls = LanternfishSchool(data)
    days = 80
    for i in range(days):
        next(ls)
    return len(ls)


def part_b():
    fp = r"data/day06.txt"
    data = parse_input(fp)
    ls = LanternfishSchool(data)
    days = 256
    for i in range(days):
        next(ls)
    return len(ls)


if __name__ == '__main__':
    print(part_a())
    print(part_b())
