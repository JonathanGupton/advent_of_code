from itertools import permutations, chain
from collections import defaultdict


ORDER_HAPPINESS = {}


def file_io(source):
    with open(source, 'r') as f:
        return f.read().strip().split('\n')


def parse_line(line):
    line = line[:-1].split()
    person_a, person_b = line[0], line[-1]
    happiness = int(line[3]) if line[2] == "gain" else int(line[3]) * -1
    return person_a, person_b, happiness


def make_graph(data):
    graph = defaultdict(dict)
    for d in data:
        graph[d[0]][d[1]] = d[2]
    return graph


def make_arrangement(order):
    arrangement = []
    for i in range(len(order)):
        try:
            arrangement.append((order[i], order[i + 1]))
        except IndexError:
            arrangement.append((order[i], order[0]))
    return tuple(arrangement)


def find_happiness(order):
    global ORDER_HAPPINESS
    global graph
    if order in ORDER_HAPPINESS:
        return ORDER_HAPPINESS[order]
    if not order:
        return 0
    happiness = graph[order[0]] + graph[(order[0][1], order[0][0])] + find_happiness(order[1:])
    ORDER_HAPPINESS[order] = happiness
    return happiness


def part_a():
    global graph
    f = r"data\day13.txt"
    data = file_io(f)
    graph = {}
    for line in data:
        line = line[:-1].split()
        person_a, person_b = line[0], line[-1]
        happiness = int(line[3]) if line[2] == "gain" else int(line[3]) * -1
        graph[(person_a, person_b)] = happiness

    people = {*chain.from_iterable(graph.keys())}
    n = float("-inf")
    for order in permutations(people):
        order = make_arrangement(order)
        happiness = find_happiness(order)
        if happiness > n:
            n = happiness
    print(n)


def part_b():
    global graph
    f = r"data\day13.txt"
    data = file_io(f)
    graph = {}
    for line in data:
        line = line[:-1].split()
        person_a, person_b = line[0], line[-1]
        happiness = int(line[3]) if line[2] == "gain" else int(line[3]) * -1
        graph[(person_a, person_b)] = happiness

    people = {*chain.from_iterable(graph.keys())}

    # add myself
    for person in people:
        graph[(person, "me")] = 0
        graph[("me", person)] = 0
    people.add("me")


    n = float("-inf")
    for order in permutations(people):
        order = make_arrangement(order)
        happiness = find_happiness(order)
        if happiness > n:
            n = happiness
    print(n)


# part_a()
part_b()