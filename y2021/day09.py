from collections import defaultdict, deque
from functools import reduce


Coordinate = complex
Height = int
CoordinateMap = dict[Coordinate, Height]


def parse_input(filepath) -> CoordinateMap:
    coordinate_map = {}
    with open(filepath, "r") as f:
        for y, row in enumerate(f.read().split("\n")):
            for x, col in enumerate(row):
                coordinate_map[complex(x, y)] = int(col)
    return coordinate_map


class ThermalVentMap:
    directions = (complex(-1, 0), complex(1, 0), complex(0, -1), complex(0, 1))

    def __init__(self, coordinates: CoordinateMap) -> None:
        self.coordinates = coordinates
        self.low_points: list[Coordinate] = [
            coordinate
            for coordinate in self.coordinates
            if self.is_low_point(coordinate)
        ]
        self.basin_sizes: defaultdict[Coordinate, int] = defaultdict(int)
        self.find_basin_sizes()

    def is_low_point(self, coordinate) -> bool:
        return all(
            self.coordinates[coordinate]
            < self.coordinates.get(coordinate + direction, 9)
            for direction in self.directions
        )

    def find_basin_sizes(self) -> None:
        for low_point in self.low_points:
            self.basin_sizes[low_point] = self._breadth_first_search(low_point)

    def _breadth_first_search(self, coordinate) -> int:
        basin_coordinates = {coordinate}
        coordinate_queue = deque([coordinate])
        while coordinate_queue:
            current = coordinate_queue.popleft()
            for direction in self.directions:
                adjacent_coordinate = current + direction
                if (
                    adjacent_coordinate not in basin_coordinates
                    and self.coordinates.get(adjacent_coordinate, 9) != 9
                    and self.coordinates[adjacent_coordinate]
                    > self.coordinates[current]
                ):
                    basin_coordinates.add(adjacent_coordinate)
                    coordinate_queue.append(adjacent_coordinate)
        return len(basin_coordinates)


def part_a():
    fp = r"data/day09.txt"
    data = parse_input(fp)
    tv = ThermalVentMap(data)
    return sum(tv.coordinates[low_point] + 1 for low_point in tv.low_points)


def part_b():
    fp = r"data/day09.txt"
    data = parse_input(fp)
    tv = ThermalVentMap(data)
    return reduce(
        lambda x, y: x * y,
        sorted([size for size in tv.basin_sizes.values()], reverse=True)[:3],
    )


if __name__ == "__main__":
    print(part_a())
    print(part_b())
