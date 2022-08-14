import networkx as nx


file_location = r"data/day7_example_a.txt"

g = nx.DiGraph()
with open(file_location, "r") as f:
    for line in f:
        g.add_edge(line[5], line[36])
