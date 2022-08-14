from __future__ import annotations

import heapq
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import chain, takewhile
from functools import reduce
from typing import Generator, Literal, Optional

AmphipodType = Literal["A", "B", "C", "D"]


def abs_diff(a: int, b: int) -> int:
    return abs(a - b)


class Amphipod:
    __slots__ = ["amphipod_type"]

    type_map: dict[AmphipodType, int] = {"A": 0, "B": 1, "C": 2, "D": 3}
    val_map: dict[int, AmphipodType] = {0: "A", 1: "B", 2: "C", 3: "D"}

    def __init__(self, amphipod_type: AmphipodType):
        self.amphipod_type = amphipod_type

    def __repr__(self):
        return f"Amphipod({self.amphipod_type})"

    def __eq__(self, other):
        if isinstance(other, Amphipod):
            return self.amphipod_type == other.amphipod_type
        return False

    @property
    def energy(self) -> int:
        return pow(10, self.type_map[self.amphipod_type])

    def target_room_index(self) -> int:
        return self.type_map[self.amphipod_type]

    @classmethod
    def from_room_index(cls, room_index: int) -> Amphipod:
        return cls(Amphipod.val_map[room_index])


class State:
    def __init__(
        self,
        hallway: list[Optional[Amphipod]],
        rooms: list[list[Optional[Amphipod]]],
        room_size: int = 2,
    ):
        self.hallway = hallway
        self.rooms = rooms
        self.room_size = room_size

    def __repr__(self):
        return f"State(hallway={self.hallway}, rooms={self.rooms}, encoded={self.encode()})"

    def __eq__(self, other):
        if isinstance(other, State):
            return (self.hallway == other.hallway) & (self.rooms == other.rooms)
        return False

    def __str__(self):
        hallway = " ".join(
            ["_" if room is None else room.amphipod_type for room in self.hallway]
        )
        rooms = "|".join(
            [
                "".join(
                    ["_" if space is None else space.amphipod_type for space in room]
                )
                for room in self.rooms
            ]
        )
        return "|" + hallway + "|" + rooms + "|"

    @property
    def home_representation(self):
        top = "#" * 13
        hall = (
            "#"
            + "".join(
                ["." if not space else space.amphipod_type for space in self.hallway]
            )
            + "#"
        )
        room_lists = []
        for i, rooms in enumerate(zip(*self.rooms)):
            rooms = ["." if not room else room.amphipod_type for room in rooms]
            if i == 0:
                room_lists.append("###" + "#".join(rooms) + "###")
            else:
                room_lists.append("  #" + "#".join(rooms) + "#")
        room_info = "\n".join(room_lists)
        bottom = "  #########"
        return "\n".join([top, hall, room_info, bottom])

    def encode(self) -> int:
        def encoded_space(space: Optional[Amphipod]) -> int:
            match space:
                case None:
                    return 0
                case _:
                    return space.target_room_index() + 1

        rooms = [*reversed([*chain.from_iterable(self.rooms)])]
        hallway = [*reversed(self.hallway)]
        combined = [*chain(rooms, hallway)]
        mapped = [*map(encoded_space, combined)]
        output = reduce(lambda x, y: 5 * x + y, mapped, 0)
        return output

    @classmethod
    def decode(cls, encoded: int, room_size=2) -> State:
        """Convert encoded int state into collections spaces and amphipods"""

        def decode_space(encoded_space: int) -> Optional[Amphipod]:
            match encoded_space:
                case 0:
                    return None
                case 1 | 2 | 3 | 4:
                    return Amphipod.from_room_index(encoded_space - 1)

        spaces = []
        while len(spaces) < (11 + 4 * room_size):
            encoded_space = encoded % 5
            encoded = encoded // 5
            spaces.append(encoded_space)

        mapped_spaces = [decode_space(space) for space in spaces]
        room_len = int(len(mapped_spaces[11:]) / 4)

        hallway = mapped_spaces[:11]
        if len(hallway) > 11:
            raise ValueError("Hallway too long")

        rooms = [
            mapped_spaces[i : i + room_len]
            for i in range(11, len(mapped_spaces), room_len)
        ]
        if len(rooms) > 4:
            print(rooms)
            raise ValueError("Too many rooms")

        return cls(hallway=hallway, rooms=rooms)

    @classmethod
    def goal(cls, room_spaces=2) -> State:
        """Return a goal state instance"""
        hallway = [None] * 11
        rooms = [
            [Amphipod("A")] * room_spaces,
            [Amphipod("B")] * room_spaces,
            [Amphipod("C")] * room_spaces,
            [Amphipod("D")] * room_spaces,
        ]
        return cls(hallway, rooms)

    @property
    def heuristic(self) -> int:
        exit_room = 0
        for room_index, room in enumerate(self.rooms):
            current_x = self.room_x(room_index)

            for room_depth, space in enumerate(reversed(room)):
                if space and space.target_room_index() != room_index:
                    target_room_index = space.target_room_index()
                    target_x = self.room_x(target_room_index)
                    hallway_steps = max(abs_diff(current_x, target_x), 2)
                    steps = room_depth + 1 + hallway_steps
                    exit_room += space.energy * steps

        move_hallway = 0
        for hallway_index, space in enumerate(self.hallway):
            if space:
                target_room_index = space.target_room_index()
                target_x = self.room_x(target_room_index)
                steps = abs_diff(hallway_index, target_x)
                move_hallway += space.energy * steps

        enter_room = 0
        for room_index, room in enumerate(self.rooms):
            for room_depth, space in enumerate(reversed(room)):
                if space and not space.target_room_index() == room_index:
                    target_amphipod = Amphipod.from_room_index(room_index)
                    steps = room_depth + 1
                    enter_room += target_amphipod.energy * steps

        return exit_room + move_hallway + enter_room

    def is_above_room(self, hallway_index: int) -> bool:
        """Checks whether the given hallway index is above a room"""
        if hallway_index == 0:
            return False
        return ((hallway_index - 2) % 2 == 0) and (
            (hallway_index - 2) / 2 < len(self.rooms)
        )

    def is_hallway_clear(self, start_x: int, target_x: int) -> bool:
        """Check if amphipod at start_x can reach target_x"""
        if start_x == target_x:
            return True
        elif start_x < target_x:
            return all(map(lambda x: x is None, self.hallway[start_x + 1 : target_x]))
        elif start_x > target_x:
            return all(map(lambda x: x is None, self.hallway[target_x:start_x]))

    def is_room_enterable(self, room_index: int) -> bool:
        def is_enterable(space) -> bool:
            match space:
                case None:
                    return True
                case _:
                    return space.target_room_index() == room_index

        enterability = all([is_enterable(room) for room in self.rooms[room_index]])
        return enterability

    def is_room_exitable(self, room_index: int) -> bool:
        return not self.is_room_enterable(room_index)

    def room_x(self, room_index: int) -> int:
        """Maps room address to hallway index"""
        return 2 * room_index + 2

    def iter_empty_spaces(self, start_x: int):
        left = list(
            takewhile(lambda x: self.hallway[x] is None, range(start_x, -1, -1))
        )
        right = list(
            takewhile(
                lambda x: self.hallway[x] is None, range(start_x + 1, len(self.hallway))
            )
        )
        empty_spaces = list(chain.from_iterable([left, right]))
        return empty_spaces

    def room_to_hallway_transitions(self):
        for room_index, room in enumerate(self.rooms):
            yielded = False
            if self.is_room_exitable(room_index):
                for room_depth, amphipod in enumerate(room):
                    if amphipod and not yielded:
                        yielded = True
                        current_x = self.room_x(room_index)
                        for target_x in self.iter_empty_spaces(current_x):
                            if not self.is_above_room(target_x):
                                steps = room_depth + 1 + abs_diff(current_x, target_x)
                                energy = steps * amphipod.energy
                                state = deepcopy(self)
                                (
                                    state.hallway[target_x],
                                    state.rooms[room_index][room_depth],
                                ) = (
                                    state.rooms[room_index][room_depth],
                                    state.hallway[target_x],
                                )
                                yield state, energy

    def hallway_to_room_transitions(self):
        for current_x, amphipod in enumerate(self.hallway):
            if amphipod:
                target_room_index = amphipod.target_room_index()

                if not self.is_room_enterable(target_room_index):
                    continue

                target_x = self.room_x(target_room_index)
                if not self.is_hallway_clear(current_x, target_x):
                    continue

                target_room_depth = (
                    len(
                        list(
                            takewhile(
                                lambda x: x is None, self.rooms[target_room_index]
                            )
                        )
                    )
                    - 1
                )

                steps = target_room_depth + 1 + abs_diff(current_x, target_x)
                energy = steps * amphipod.energy

                state = deepcopy(self)
                (
                    state.rooms[target_room_index][target_room_depth],
                    state.hallway[current_x],
                ) = (
                    state.hallway[current_x],
                    state.rooms[target_room_index][target_room_depth],
                )
                yield state, energy

    def transitions(self) -> Generator[tuple[State, int], None, None]:
        for state, energy in chain(
            self.hallway_to_room_transitions(), self.room_to_hallway_transitions()
        ):
            yield state, energy


def parse_input(filepath) -> tuple[Amphipod]:
    with open(filepath, "r") as f:
        return tuple(map(Amphipod, filter(lambda x: x in "ABCD", f.read())))


@dataclass(order=True)
class Entry:
    priority: int
    encoded_state: int = field(compare=False)


def solve(initial_state: State, room_size=2):
    pq: list[Optional[Entry]] = []
    heapq.heappush(pq, Entry(0, initial_state.encode()))

    came_from = {initial_state.encode(): None}
    score = {initial_state.encode(): 0}

    encoded_goal = State.goal(room_spaces=room_size).encode()

    while pq:
        encoded_current_state = heapq.heappop(pq).encoded_state
        if encoded_current_state == encoded_goal:
            break
        current_state = State.decode(encoded_current_state, room_size=room_size)
        current_score = score[encoded_current_state]

        for next_state, transition_score in current_state.transitions():
            encoded_next_state = next_state.encode()
            tentative_score = current_score + transition_score
            if (
                encoded_next_state not in score
                or tentative_score < score[encoded_next_state]
            ):
                score[encoded_next_state] = tentative_score
                heapq.heappush(
                    pq,
                    Entry(tentative_score + next_state.heuristic, encoded_next_state),
                )
                came_from[encoded_next_state] = current_state.encode()
    return came_from, score


def _test_encode_decode():
    hallway = [None, None, None, None, None, None, None, None, None, None, None]
    rooms = [
        [Amphipod("B"), Amphipod("A")],
        [Amphipod("C"), Amphipod("D")],
        [Amphipod("B"), Amphipod("C")],
        [Amphipod("D"), Amphipod("A")],
    ]

    state = State(hallway, rooms)
    encoded_state = state.encode()
    decoded_state = State.decode(encoded_state)
    print(state == decoded_state)

    hallway = [
        Amphipod("B"),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    rooms = [
        [None, Amphipod("A")],
        [Amphipod("C"), Amphipod("D")],
        [Amphipod("B"), Amphipod("C")],
        [Amphipod("D"), Amphipod("A")],
    ]

    state = State(hallway, rooms)
    encoded_state = state.encode()
    decoded_state = State.decode(encoded_state)
    print(state == decoded_state)

    hallway = [
        Amphipod("B"),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        Amphipod("A"),
    ]
    rooms = [
        [None, None],
        [Amphipod("C"), Amphipod("D")],
        [Amphipod("B"), Amphipod("C")],
        [Amphipod("D"), Amphipod("A")],
    ]

    state = State(hallway, rooms)
    encoded_state = state.encode()
    decoded_state = State.decode(encoded_state)
    print(state == decoded_state)

    hallway = [
        Amphipod("B"),
        Amphipod("C"),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        Amphipod("A"),
    ]
    rooms = [
        [None, None],
        [None, Amphipod("D")],
        [Amphipod("B"), Amphipod("C")],
        [Amphipod("D"), Amphipod("A")],
    ]

    state = State(hallway, rooms)
    encoded_state = state.encode()
    decoded_state = State.decode(encoded_state)
    print(state == decoded_state)

    hallway = [
        None,
        Amphipod("A"),
        None,
        None,
        None,
        Amphipod("D"),
        None,
        Amphipod("B"),
        None,
        Amphipod("D"),
        None,
    ]
    rooms = [
        [None, Amphipod("A")],
        [None, Amphipod("B")],
        [Amphipod("C"), Amphipod("C")],
        [None, None],
    ]

    state = State(hallway, rooms)
    encoded_state = state.encode()
    decoded_state = State.decode(encoded_state)
    print(state == decoded_state)

    hallway = [
        Amphipod("A"),
        Amphipod("A"),
        None,
        Amphipod("B"),
        None,
        Amphipod("B"),
        None,
        Amphipod("D"),
        None,
        Amphipod("B"),
        Amphipod("C"),
    ]
    rooms = [
        [None, None],
        [None, Amphipod("D")],
        [None, Amphipod("C")],
        [None, None],
    ]

    state = State(hallway, rooms)
    encoded_state = state.encode()
    decoded_state = State.decode(encoded_state)
    print(state == decoded_state)


def part_a():
    fp = r"data/day23.txt"
    arrangement = parse_input(fp)
    hallway = [None] * 11
    rooms = [
        [arrangement[0], arrangement[4]],
        [arrangement[1], arrangement[5]],
        [arrangement[2], arrangement[6]],
        [arrangement[3], arrangement[7]],
    ]
    state = State(hallway, rooms)
    came_from, score = solve(state)
    goal = State.goal().encode()
    return score[goal]


def part_b():
    fp = r"data/day23.txt"
    arrangement = parse_input(fp)
    hallway = [None] * 11
    rooms = [
        [arrangement[0], Amphipod("D"), Amphipod("D"), arrangement[4]],
        [arrangement[1], Amphipod("C"), Amphipod("B"), arrangement[5]],
        [arrangement[2], Amphipod("B"), Amphipod("A"), arrangement[6]],
        [arrangement[3], Amphipod("A"), Amphipod("C"), arrangement[7]],
    ]
    room_size = 4
    state = State(hallway, rooms)
    came_from, score = solve(state, room_size=room_size)
    goal = State.goal(room_size).encode()
    return score[goal]


if __name__ == "__main__":
    print(part_a())
    print(part_b())
