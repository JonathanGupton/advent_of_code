from collections import defaultdict
from typing import Optional


Cave = str
CaveMap = dict[Cave, list[Cave]]
CavePath = list[Cave]


def input_parser(filepath) -> CaveMap:
    map_data = defaultdict(list)
    with open(filepath, "r") as f:
        for line in f.readlines():
            l, r = line.strip().split("-")
            map_data[l].append(r)
            map_data[r].append(l)
    for k in map_data:
        map_data[k] = sorted(map_data[k])
    return map_data


def generate_cave_paths(cave_map: CaveMap, start: Cave) -> list[CavePath]:
    cave_paths = []

    def _generate_cave_path(
        current_position: Cave = "start",
        end_position: Cave = "end",
        current_path: Optional[CavePath] = None,
        explored: Optional[frozenset[Cave]] = None,
    ):
        nonlocal cave_paths
        nonlocal cave_map

        if not current_path:
            current_path = []

        new_path = current_path.copy()
        new_path.append(current_position)

        if not explored:
            explored = frozenset([start])

        new_explored = (
            frozenset.union(explored, [current_position])
            if current_position.islower()
            else explored.copy()
        )

        if current_position == end_position:
            cave_paths.append(new_path)
            return

        for next_position in cave_map[current_position]:
            if next_position not in explored:
                _generate_cave_path(
                    next_position, current_path=new_path, explored=new_explored
                )

    _generate_cave_path()
    return cave_paths


def generate_cave_paths_b(cave_map: CaveMap) -> list[CavePath]:
    cave_paths = []

    def _generate_cave_path(
        current_position: Cave = "start",
        end_position: Cave = "end",
        current_path: Optional[CavePath] = None,
        explored: Optional[defaultdict[Cave, int]] = None,
        allow_small_cave_return: bool = True,
    ):
        nonlocal cave_paths
        nonlocal cave_map

        if not current_path:
            current_path = []

        new_path = current_path.copy()
        new_path.append(current_position)

        if not explored:
            explored = defaultdict(int)

        new_explored = explored.copy()

        if current_position.islower():
            new_explored[current_position] += 1

        can_explore_second_small_cave = (
            not any(v > 1 for v in new_explored.values())
            if allow_small_cave_return
            else False
        )

        if current_position == end_position:
            cave_paths.append(new_path)
            return

        for next_position in cave_map[current_position]:
            if next_position == "start":
                continue
            elif next_position not in new_explored or can_explore_second_small_cave:
                _generate_cave_path(
                    next_position,
                    current_path=new_path,
                    explored=new_explored,
                    allow_small_cave_return=can_explore_second_small_cave,
                )

    _generate_cave_path()
    return cave_paths


def part_a():
    fp = r"data/day12.txt"
    cave_map = input_parser(fp)
    cp = generate_cave_paths(cave_map, "start")
    return len(cp)


def part_b():
    fp = r"data/day12.txt"
    cave_map = input_parser(fp)
    cp = generate_cave_paths_b(cave_map)
    return len(cp)


if __name__ == "__main__":
    print(part_a())
    print(part_b())
