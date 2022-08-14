from collections import Counter
from dataclasses import dataclass, field
import re


@dataclass()
class Room:
    name: str
    sector: int
    checksum: str
    deciphered: str = field(init=False)


def parse_room_string(room_string: str) -> Room:
    pattern = r"(.*)-(\d*)\[(\w*)\]"  # roomname-sector[checksum]
    match = re.match(pattern, room_string)
    return Room(match[1], int(match[2]), match[3])


def file_io(filename) -> list[Room]:
    with open(filename, "r") as f:
        rooms = [parse_room_string(line) for line in f.readlines()]
    return rooms


def is_valid_room(room: Room) -> bool:
    name = room.name.replace("-", "")
    most_common = Counter(name).most_common()
    most_common.sort(key=lambda x: x[0])  # sort the letters alphabetically
    most_common.sort(key=lambda x: x[1], reverse=True)  # sort on the count descending
    computed_checksum = "".join([x[0] for x in most_common[:5]])
    return room.checksum == computed_checksum


def convert_char(char: str, offset: int) -> str:
    if char == "-":
        return " "
    char_val = ord(char) + offset
    new_char = chr(char_val) if char_val <= 122 else chr(char_val - 26)
    return new_char


def decipher(roomname: str, sector: int):
    offset = sector % 26
    return "".join([convert_char(c, offset) for c in roomname])


def part_a():
    input_file = r"data/day4.txt"
    rooms = file_io(input_file)
    sector_sum = 0
    for room in rooms:
        if is_valid_room(room):
            sector_sum += room.sector
    return sector_sum


def part_b():
    input_file = r"data/day4.txt"
    rooms = file_io(input_file)
    for room in rooms:
        if is_valid_room(room):
            room.deciphered = decipher(room.name, room.sector)
            if room.deciphered == "northpole object storage":
                return room.sector


if __name__ == "__main__":
    print(part_a())
    print(part_b())
