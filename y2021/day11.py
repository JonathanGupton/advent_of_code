
Coordinate = complex
Energy = int
OctopusMap = dict[Coordinate, Energy]


def input_parser(filepath):
    cave_data = {}
    with open(filepath, "r") as f:
        for y, row in enumerate(f.readlines()):
            for x, col in enumerate(row.strip()):
                cave_data[complex(x, y)] = int(col)
    return cave_data


class Octopodes:

    adjacent = [
        complex(-1, -1),
        complex(0, -1),
        complex(1, -1),

        complex(-1, 0),
        complex(1, 0),

        complex(-1, 1),
        complex(0, 1),
        complex(1, 1)
        ]

    def __init__(self, octopus_map: OctopusMap) -> None:
        self.octopus_map = octopus_map
        self.n_flashes = 0
        self.max_energy = 9

        self.max_x = 0
        self.max_y = 0
        for coordinate in octopus_map:
            self.max_x = coordinate.real if coordinate.real > self.max_x else self.max_x
            self.max_y = coordinate.imag if coordinate.imag > self.max_y else self.max_y
        self.max_x = int(self.max_x)
        self.max_y = int(self.max_y)

    def __str__(self):
        table = [[0 for _ in range(self.max_x + 1)] for __ in range(self.max_y + 1)]
        for k, v in self.octopus_map.items():
            table[int(k.imag)][int(k.real)] = v
        return "\n".join("".join([str(i) for i in line]) for line in table)

    def _increment_all_octopodes(self):
        for octopus in self.octopus_map:
            self.octopus_map[octopus] += 1

    def __iter___(self):
        return self

    def __next__(self):
        flashed = set()
        to_flash = set()
        for octopus in self.octopus_map:
            self.octopus_map[octopus] += 1
            if self.octopus_map[octopus] > self.max_energy:
                to_flash.add(octopus)

        while to_flash:
            next_to_flash = set()
            for current in to_flash:
                flashed.add(current)
                self.octopus_map[current] = 0
                for adj in self.adjacent:
                    adj_octopus = adj + current
                    if adj_octopus in self.octopus_map and adj_octopus not in flashed and adj_octopus not in to_flash:
                        self.octopus_map[adj_octopus] += 1
                        if self.octopus_map[adj_octopus] > self.max_energy:
                            next_to_flash.add(adj_octopus)
            to_flash = next_to_flash
        self.n_flashes += len(flashed)

    @property
    def synchronized(self) -> bool:
        return all(self.octopus_map[complex(0, 0)] == val for val in self.octopus_map.values())


def part_a():
    fp = r"data/day11.txt"
    data = input_parser(fp)
    octopodes = Octopodes(data)
    for _ in range(100):
        next(octopodes)
    return octopodes.n_flashes


def part_b():
    fp = r"data/day11.txt"
    data = input_parser(fp)
    octopodes = Octopodes(data)
    elapsed_time = 0
    while not octopodes.synchronized:
        next(octopodes)
        elapsed_time += 1
    return elapsed_time


if __name__ == '__main__':
    print(part_a())
    print(part_b())
