from collections import defaultdict
from itertools import permutations


def file_io(source):
    with open(source, "r") as f:
        return f.read().strip().split('\n')


def make_graph(data):
    graph = defaultdict(dict)
    for line in data:
        locs, dist = line.split(" = ")
        l1, l2 = locs.split(" to ")
        dist = int(dist)
        graph[l1][l2] = dist
        graph[l2][l1] = dist
    return graph


def path_length(path):
    global graph
    if len(path) < 2:
        return 0
    path_len = graph[path[0]][path[1]] + path_length(path[1:])
    return path_len


def find_min_path_length(graph):
    min_path = float("inf")
    for path in permutations(graph.keys()):
        path_len = path_length(path)
        if path_len < min_path:
            min_path = path_len
    return min_path

def find_max_path_length(graph):
    max_path = float("-inf")
    for path in permutations(graph.keys()):
        path_len = path_length(path)
        if path_len > max_path:
            max_path = path_len
    return max_path



if __name__ == '__main__':
    # f = r"data\day09_example_a.txt"
    f = r"data\day09.txt"
    d = file_io(f)
    graph = make_graph(d)
    print(find_min_path_length(graph))
    print(find_max_path_length(graph))
