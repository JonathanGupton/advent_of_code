from itertools import product

Coordinate = tuple[int, int]


class LandingZone:
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int) -> None:
        self.x_min, self.x_max, self.y_min, self.y_max = x_min, x_max, y_min, y_max

    def __repr__(self):
        return f"LandingZone(x_min={self.x_min}, x_max={self.x_max}, y_min={self.y_min}, y_min={self.y_max})"

    def position_to_lz(self, x, y) -> tuple[int, int]:
        """-1 - has not reached, 0 - within area, 1 - passed area """
        if x < self.x_min:
            x_out = -1
        elif (x >= self.x_min) and (x <= self.x_max):
            x_out = 0
        else:
            x_out = 1

        if y > self.y_max:
            y_out = -1
        elif (y <= self.y_max) and (y >= self.y_min):
            y_out = 0
        else:
            y_out = 1

        return x_out, y_out


class Probe:
    def __init__(self, x_velocity: int, y_velocity: int) -> None:
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.x_position = 0
        self.y_position = 0
        self.y_max = 0

    def __repr__(self):
        return f"{self.__class__.__name__}(position=({self.x_position}, {self.y_position}), x_velocity={self.x_velocity}, y_velocity={self.y_velocity})"

    @property
    def position(self):
        return self.x_position, self.y_position

    @property
    def velocity(self):
        return self.x_velocity, self.y_velocity

    def __iter__(self):
        return self

    def __next__(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.x_velocity = 0 if self.x_velocity == 0 else self.x_velocity - 1
        self.y_velocity = self.y_velocity - 1
        self.y_max = self.y_position if self.y_position > self.y_max else self.y_max
        return self.x_position, self.y_position


def process_probe_trajectory(probe: Probe, landing_zone: LandingZone):
    while True:
        x_to_lz, y_to_lz = landing_zone.position_to_lz(*probe.position)
        match x_to_lz, y_to_lz:
            case (-1, -1):
                next(probe)
                continue
            case (0, 0):
                return True
            case (1, _) | (_, 1):
                return False
            case _:
                next(probe)
                continue


def find_max_trajectory(landing_zone: LandingZone) -> int:
    y_max = 0
    for x, y in product(range(landing_zone.x_max + 1),
        range(landing_zone.y_min - 1, abs(landing_zone.y_min) + 1),):
        probe = Probe(x, y)
        if process_probe_trajectory(probe, landing_zone):
            y_max = probe.y_max if probe.y_max > y_max else y_max
    return y_max


def find_all_trajectories(landing_zone: LandingZone) -> int:
    trajectories = []
    for x, y in product(
        range(landing_zone.x_max + 1),
        range(landing_zone.y_min - 1, abs(landing_zone.y_min) + 1),
    ):
        probe = Probe(x, y)
        if process_probe_trajectory(probe, landing_zone):
            trajectories.append((x, y))
    return len(trajectories)


def part_a():
    x_min, x_max, y_min, y_max = 195, 238, -93, -67  # your info here
    lz = LandingZone(x_min, x_max, y_min, y_max)
    probe_y_max = find_max_trajectory(lz)
    return probe_y_max


def part_b():
    x_min, x_max, y_min, y_max = 195, 238, -93, -67  # your info here
    lz = LandingZone(x_min, x_max, y_min, y_max)
    trajectories = find_all_trajectories(lz)
    return trajectories


if __name__ == "__main__":
    print(part_a())
    print(part_b())
