from itertools import product
from collections import Counter

ACTIVATION = 3
STATIC = {2, 3}


def file_io(source):
    with open(source, "r") as f:
        return f.read().strip().split("\n")


def make_grid(data):
    grid = {}
    lit = set()
    for row in range(len(data)):
        for col in range(len(data)):
            grid[(row, col)] = True if data[row][col] == "#" else False
            if data[row][col] == "#":
                lit.add((row, col))
    return grid, lit


def get_adjacent(point):
    """Yield tuples adjacent to point with values+-1 for each value in input point"""
    for adj in product(*[[i + n for n in (-1, 0, 1)] for i in point]):
        if adj != point:
            yield adj


def update_grid():
    global grid
    global lit
    new_grid = grid.copy()
    new_lit = lit.copy()
    adjacent_points = []
    for light in lit:
        lit_adjacent = 0
        for l in get_adjacent(light):
            lit_adjacent += grid.get(l, 0)
        if lit_adjacent in STATIC:
            new_grid[light] = True
        else:
            new_lit.remove(light)
            new_grid[light] = False
        adjacent_points.extend(get_adjacent(light))
    adjacent_count = Counter(adjacent_points)
    for adj in adjacent_count:
        if adj in grid and adjacent_count[adj] == ACTIVATION:
            new_grid[adj] = True
            new_lit.add(adj)
    return new_grid, new_lit


def update_gridv2():
    global grid
    global lit
    new_grid = grid.copy()
    new_lit = lit.copy()
    adjacent_points = []
    for light in lit:
        if light in ((0, 0), (0, 99), (99, 0), (99, 99)):
            adjacent_points.extend(get_adjacent(light))
            continue
        else:
            lit_adjacent = 0
            for l in get_adjacent(light):
                lit_adjacent += grid.get(l, 0)
            if lit_adjacent in STATIC:
                new_grid[light] = True
            else:
                new_lit.remove(light)
                new_grid[light] = False
            adjacent_points.extend(get_adjacent(light))

    adjacent_count = Counter(adjacent_points)
    for adj in adjacent_count:
        if adj in grid and adjacent_count[adj] == ACTIVATION:
            new_grid[adj] = True
            new_lit.add(adj)
    return new_grid, new_lit


def part_a():
    global grid
    global lit
    f = r"data\day18.txt"
    data = [list(row) for row in file_io(f)]
    grid, lit = make_grid(data)

    for _ in range(100):
        grid, lit = update_grid()
    print(len(lit))


def part_b():
    global grid
    global lit
    f = r"data\day18.txt"
    data = [list(row) for row in file_io(f)]
    grid, lit = make_grid(data)
    for corner in ((0, 0), (0, 99), (99, 0), (99, 99)):
        grid[corner] = True
        lit.add(corner)
    for _ in range(100):
        grid, lit = update_gridv2()
    print(len(lit))


part_a()
part_b()
