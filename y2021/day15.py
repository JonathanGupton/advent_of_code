from dataclasses import dataclass, field
import heapq
from itertools import product
from typing import Generator, Optional


DangerLevel = int
Coordinate = complex
Graph = dict[Coordinate, DangerLevel]

ADJACENT = (complex(-1, 0), complex(1, 0), complex(0, -1), complex(0, 1))


def parse_input(filepath) -> list[list[DangerLevel]]:
    with open(filepath, "r") as f:
        return [[int(col) for col in row.strip()] for row in f.readlines()]


def convert_array_to_coordinate_map(
    levels_array: list[list[DangerLevel]],
) -> tuple[Graph, Coordinate]:
    cave_map: Graph = {}
    max_coordinate: Optional[complex] = None
    for y, row in enumerate(levels_array):
        for x, col in enumerate(row):
            cave_map[complex(x, y)] = col
            max_coordinate = complex(x, y)
    return cave_map, max_coordinate


def heuristic(a: Coordinate, b: Coordinate) -> int:
    x1, y1 = a.real, a.imag
    x2, y2 = b.real, b.imag
    return int(abs(x1 - x2) + abs(y1 - y2))


def neighbor_generator(
    graph: Graph, current: Coordinate, adjacent=ADJACENT
) -> Generator[Coordinate, None, None]:
    for direction in adjacent:
        if graph.get(direction + current):
            yield direction + current


@dataclass(order=True)
class PriorityCoordinate:
    priority: int
    coordinate: Coordinate = field(compare=False)


def a_star_search(graph: Graph, start: Coordinate, goal: Coordinate):
    frontier: list[Optional[PriorityCoordinate]] = []
    heapq.heappush(frontier, PriorityCoordinate(0, start))
    came_from: dict[Coordinate, Optional[Coordinate]] = {start: None}
    cost_so_far: dict[Coordinate, float] = {start: 0}

    while frontier:
        current: PriorityCoordinate = heapq.heappop(frontier)

        if current.coordinate == goal:
            break

        for neighbor in neighbor_generator(graph, current.coordinate):
            new_cost = int(cost_so_far[current.coordinate] + graph[neighbor])
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(current.coordinate, neighbor)
                heapq.heappush(frontier, PriorityCoordinate(priority, neighbor))
                came_from[neighbor] = current.coordinate
    return cost_so_far


def grow_graph(
    graph: Graph, max_coord: Coordinate, multiplier: int = 5
) -> tuple[Graph, Coordinate]:
    x_multiplier = 1 + max_coord.real
    y_multiplier = 1 + max_coord.imag
    new_graph = graph.copy()
    new_max_coordinate: Optional[Coordinate] = complex(
        x_multiplier * multiplier - 1, y_multiplier * multiplier - 1
    )
    for current in graph.keys():
        current_val = graph[current]
        for x, y in product(range(multiplier), range(multiplier)):
            new_x = x * x_multiplier
            new_y = y * y_multiplier
            new_graph[current + complex(new_x, new_y)] = (current_val + x + y) // 10 + (
                current_val + x + y
            ) % 10

    return new_graph, new_max_coordinate


def part_a():
    fp = r"data/day15.txt"
    cm_array = parse_input(fp)
    cm, max_coord = convert_array_to_coordinate_map(cm_array)
    cost_so_far = a_star_search(cm, complex(0, 0), max_coord)
    return cost_so_far[max_coord]


def part_b():
    fp = r"data/day15.txt"
    cm_array = parse_input(fp)
    cm, max_coord = convert_array_to_coordinate_map(cm_array)
    large_cm, large_max_coord = grow_graph(cm, max_coord)
    cost_so_far = a_star_search(large_cm, complex(0, 0), large_max_coord)
    return cost_so_far[large_max_coord]


if __name__ == "__main__":
    print(part_a())
    print(part_b())
