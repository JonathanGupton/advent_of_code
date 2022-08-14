from collections import deque
from typing import Optional


DiscLevel = int


class Disc:
    def __init__(self, n_positions: int, start_position: int):
        self.n_positions = n_positions
        self.start_position = start_position
        self.position = deque([i for i in range(n_positions)])
        while self.position[0] != self.start_position:
            self.position.rotate()

    @property
    def current(self):
        return self.position[0]

    def rotate(self):
        self.position.rotate(-1)

    def __repr__(self):
        return repr(self.position)

    def __str__(self):
        return self.__repr__()


class DiscCollection(dict[DiscLevel, Disc]):
    pass


class Ball:
    def __init__(self, drop_time: int):
        self.drop_time = drop_time
        self.y_position = 0
        self.collision = False

    def __repr__(self):
        return f"{self.__class__.__name__}(drop_time={self.drop_time}, y_position={self.y_position})"

    def __next__(self):
        self.y_position += 1

    def __iter__(self):
        return self


class BallCollection(list[Ball]):
    pass


class DiscMachine:
    def __init__(self, discs: list[Disc]):
        self.disc_collection = DiscCollection()
        for level, disc in enumerate(discs, 1):
            self.disc_collection[level] = disc
        self.max_disc_level: int = len(self.disc_collection)
        self.time: int = 0
        self.bc = BallCollection()
        self.drop_new_ball()
        self.pass_through_ball: Optional[Ball] = None

    def __iter__(self):
        return self

    def __next__(self):
        self.advance_clock(n_seconds=1)
        self.rotate_discs()
        self.process_balls()
        self.drop_new_ball()

    def advance_clock(self, n_seconds: int = 1):
        self.time += n_seconds

    def rotate_discs(self):
        for disc in self.disc_collection:
            self.disc_collection[disc].rotate()

    def process_balls(self):
        for position, ball in enumerate(self.bc):
            next(self.bc[position])
            ball_y_position = self.bc[position].y_position
            if ball_y_position > self.max_disc_level:
                self.pass_through_ball = self.bc[position]
                return
            if self.disc_collection[ball_y_position].current != 0:
                self.bc[position].collision = True
        self.bc = [ball for ball in self.bc if ball.collision is False]

    def drop_new_ball(self):
        self.bc.append(Ball(drop_time=self.time))


def file_io(input_file):
    output = []
    with open(input_file, "r") as f:
        for line in f.read().strip().split("\n"):
            _, _, _, n_positions, _, _, _, _, _, _, _, pos = line.split()
            n_positions = int(n_positions)
            pos = int(pos[:-1])
            output.append(Disc(n_positions, pos))
    return output


# filename = r"data/day15_example.txt"
# filename = r"data/day15.txt"
filename = r"data/day15_b.txt"
data = file_io(filename)

# d1 = Disc(5, 4)
# d2 = Disc(2, 1)

dm = DiscMachine(data)
while dm.pass_through_ball is None:
    next(dm)
print(dm.pass_through_ball)
