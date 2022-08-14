from functools import cache


@cache
def roll_regular(last_roll_val: int, max_val=100, n_rolls=3) -> tuple[int, int]:
    """
    Steps = Total number of steps to be moved
    last_roll_val = The most recent value rolled
    """
    steps = 0
    for i in range(n_rolls):
        last_roll_val += 1
        if last_roll_val > max_val:
            last_roll_val %= max_val
        steps += last_roll_val
    return steps, last_roll_val


def dirac_roll() -> int:
    for i in (1, 2, 3):
        yield i


class DiracDice:
    def __init__(
        self,
        p1_position: int,
        p2_position: int,
        p1_score: int = 0,
        p2_score: int = 0,
        board_size: int = 10,
        winning_score: int = 1000,
        times_to_roll: int = 3,
        dice_function=roll_regular,
    ):
        self.p1_position = p1_position
        self.p1_score = p1_score

        self.p2_position = p2_position
        self.p2_score = p2_score

        self.board_size = board_size

        self.winning_score = winning_score
        self.n_rolls: int = 0
        self.times_to_roll = times_to_roll

        self.dice_function = dice_function

    def __repr__(self):
        return f"{self.__class__.__name__}(p1_position={self.p1_position}, p1_score={self.p1_score}, p2_position={self.p2_position}, p2_score={self.p2_score}, n_rolls={self.n_rolls})"

    def play(self) -> int:
        last_roll_position: int = 0
        while True:
            steps_moved, last_roll_position = self.dice_function(
                last_roll_position, n_rolls=self.times_to_roll
            )
            self.n_rolls += self.times_to_roll
            self.p1_position = self.p1_position + steps_moved
            if self.p1_position > self.board_size:
                self.p1_position %= self.board_size
                if self.p1_position == 0:
                    self.p1_position = 10
            self.p1_score += self.p1_position
            if self.p1_score >= self.winning_score:
                return 1

            steps_moved, last_roll_position = self.dice_function(
                last_roll_position, n_rolls=self.times_to_roll
            )
            self.n_rolls += self.times_to_roll
            self.p2_position = self.p2_position + steps_moved
            if self.p2_position > self.board_size:
                self.p2_position %= self.board_size
                if self.p2_position == 0:
                    self.p2_position = 10
            self.p2_score += self.p2_position
            if self.p2_score >= self.winning_score:
                return 2

    def score(self):
        return self.n_rolls * min(self.p1_score, self.p2_score)


def part_a():
    p1 = 1
    p2 = 5
    dd = DiracDice(p1, p2)
    dd.play()
    print(dd.score())


if __name__ == "__main__":
    p1_pos = 4
    p2_pos = 8
    dd = DiracDice(p1_pos, p2_pos)
    dd.play()
    print(dd.score())
