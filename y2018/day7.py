
from collections import defaultdict
from string import ascii_uppercase



def get_pairs(file_location) -> list[tuple[str, str]]:
    with open(file_location, "r") as f:
        return [(line[5], line[36]) for line in f]


def make_adjacency_dicts(step_pairs: list[tuple[str, str]]) -> tuple[defaultdict[str, list[str]], defaultdict[str, list[str]]]:
    node_outgoing = defaultdict(list)
    node_incoming = defaultdict(list)
    for pair in step_pairs:
        node_outgoing[pair[0]].append(pair[1])
        node_incoming[pair[1]].append(pair[0])
    for k in node_outgoing:
        node_outgoing[k] = sorted(node_outgoing[k])
    for k in node_incoming:
        node_incoming[k] = sorted(node_incoming[k])
    return node_outgoing, node_incoming


def find_start(step_pairs: list[tuple[str, str]]) -> list[str]:
    l = set()
    r = set()
    for pair in step_pairs:
        l.update(pair[0])
        r.update(pair[1])
    return sorted([*(l - r)])


def part_a(file_location):
    pairs = get_pairs(file_location)
    node_to_outgoing, node_prerequisites = make_adjacency_dicts(pairs)
    queue = [*find_start(pairs)]
    output = []
    while queue:
        current_node, queue = queue[0], queue[1:]
        output.append(current_node)
        for node in node_to_outgoing[current_node]:
            if all(node in output for node in node_prerequisites[node]):
                queue.append(node)
        queue = sorted(queue)
    return "".join(output)


def make_char_val_map(base_val: int) -> dict[str, int]:
    char_val = {}
    for i, ch in enumerate(ascii_uppercase, 1):
        char_val[ch] = base_val + i
    return char_val





def part_b(file_location, base_val=60, n_workers=5):
    char_val = make_char_val_map(base_val)
    pairs = get_pairs(file_location)
    start = find_start(pairs)
    node_outgoing, node_incoming = make_adjacency_dicts(pairs)
    workers = [[None, 0] for _ in range(n_workers)]
    time = 0




if __name__ == '__main__':
    # part_a(r"data/day7.txt") == "CABDFE"
    # file_location = r"data/day7_example_a.txt"
    file_location = r"data/day7.txt"
    print(part_a(file_location))
    # pairs = get_pairs(file_location)
    # s = find_start(pairs)