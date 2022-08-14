from collections import defaultdict
import re


Molecule = str


def file_io(source):
    with open(source, "r") as f:
        return f.read().split("\n\n")


def parse_replacements(replacements):
    graph = defaultdict(list)
    for line in replacements.strip().split("\n"):
        initial, subsequent = line.split(" => ")
        graph[initial.strip()].append(subsequent.strip())
    return graph


def replace_molecules(molecule: Molecule) -> Molecule:
    global pattern
    global graph
    for m in re.finditer(pattern, molecule):
        for substring in graph[m.group()]:
            yield molecule[: m.span()[0]] + substring + molecule[m.span()[1]:]


def reverse_graph(graph: dict[str, list[str]]) -> dict[str, str]:
    reversed_graph = dict()
    for k, v in graph.items():
        for i in v:
            reversed_graph[i] = k
    return reversed_graph


def part_a():
    src = r"data\day19.txt"
    replacements, molecule = file_io(src)
    graph = parse_replacements(replacements)
    pattern = fr"({'|'.join(graph.keys())})"
    new_molecules = set()
    matches = re.finditer(pattern, molecule)
    for m in matches:
        for substring in graph[m.group()]:
            new_molecules.add(
                molecule[: m.span()[0]] + substring + molecule[m.span()[1]:]
             )
    print(len(new_molecules))


# part_a()
src = r"data\day19_example.txt"
replacements, target = file_io(src)
target = target.strip()
graph = parse_replacements(replacements)
r_graph: dict[str, str] = reverse_graph(graph)
termination = "e"
molecule_len = len(target.strip())



"""


"""