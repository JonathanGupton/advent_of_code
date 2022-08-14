from collections import deque
from functools import reduce
import json
import re


def file_io(source):
    with open(source, 'r') as f:
        return f.read().strip()


def part_a():
    f = r"data\day12.txt"
    data = file_io(f)
    pattern = r"-?\d+"
    print(reduce(lambda a, b: a + b, (int(i) for i in re.findall(pattern, data))))


def part_b():
    f = r"data\day12.txt"
    data = file_io(f)
    data = json.loads(data)
    n = 0
    q = deque([v for v in data.values()])
    while q:
        current = q.popleft()
        if type(current) is int:
            n += current
        elif type(current) is str:
            continue
        elif type(current) is list:
            for i in current:
                q.append(i)
        elif type(current) is dict:
            if 'red' not in current.keys() and 'red' not in current.values():
                q.append([v for v in current.values()])

    print(n)


part_a()
part_b()