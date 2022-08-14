def file_io(source):
    with open(source, "r") as f:
        return f.read().strip().split("\n")


def parse_sue_info(line):
    sue, attributes = line.split(": ", 1)
    _, sue = sue.split(" ")
    sue = int(sue)
    attr_dict = {}
    for attr_val in attributes.split(","):
        attr, val = attr_val.split(": ")
        attr = attr.strip()
        attr_dict[attr] = int(val)
    return sue, attr_dict


def create_sue_dict(data):
    sue_dict = {}
    for line in data:
        sue, attr_dict = parse_sue_info(line)
        sue_dict[sue] = attr_dict
    return sue_dict


def part_a():
    f = r"data\day16.txt"
    data = file_io(f)
    to_find = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    sue_dict = {}
    for line in data:
        sue, attr_dict = parse_sue_info(line)
        sue_dict[sue] = attr_dict
    candidates = []
    for s in sue_dict:
        if all([sue_dict[s][k] == v for k, v in to_find.items() if k in sue_dict[s]]):
            candidates.append(s)
    print(candidates[0])


def part_b():
    f = r"data\day16.txt"
    data = file_io(f)
    to_find = {
        "children": lambda x: x == 3,
        "cats": lambda x: x > 3,
        "samoyeds": lambda x: x == 2,
        "pomeranians": lambda x: x < 3,
        "akitas": lambda x: x == 0,
        "vizslas": lambda x: x == 0,
        "goldfish": lambda x: x < 5,
        "trees": lambda x: x > 3,
        "cars": lambda x: x == 2,
        "perfumes": lambda x: x == 1,
    }
    sue_dict = create_sue_dict(data)
    candidates = []
    for s in sue_dict:
        if all([v(sue_dict[s][k]) for k, v in to_find.items() if k in sue_dict[s]]):
            candidates.append(s)
    print(candidates[0])


if __name__ == '__main__':
    part_a()
    part_b()
