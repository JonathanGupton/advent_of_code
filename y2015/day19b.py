from collections import defaultdict, UserString
from functools import cache
from typing import Optional

Graph = dict[str, list[str]]


def file_io(datafile):
    """Read in data"""
    with open(datafile, "r") as f:
        data, molecule = f.read().split("\n\n")
    graph = defaultdict(list)
    for adjacency_pair in data.split("\n"):
        mol, replacement = adjacency_pair.split(" => ")
        graph[mol].append(replacement)
    return graph, molecule


def reverse_graph(graph: Graph) -> Graph:
    reversed_graph = defaultdict(list)
    for k, v in graph.items():
        for i in v:
            reversed_graph[i].append(k)
    return reversed_graph


class Molecule(UserString):
    """Class to iterate over molecule strings to yield possible matches"""

    def __init__(self, molecule: str):
        super().__init__(molecule)
        self.graph: Optional[Graph] = None

    def __iter__(self) -> tuple[int, int]:
        """Yields slice locations for the molecule's valid sub-molecules"""
        start = 0
        molecule_length = len(self)
        max_target_length = max([len(k) for k in self.graph.keys()]) + 1
        while start < molecule_length:
            for i in range(max_target_length):
                if self[start : start + i] in self.graph:
                    yield start, start + i
            start += 1

    def __call__(self, graph: Graph):
        self.graph = graph
        return self

    def is_valid(self, termination_molecule: str = "e") -> bool:
        if self == termination_molecule:
            return True
        return termination_molecule not in self


def assemble_molecule(
    molecule: Molecule, start: int, stop: int, replacement: str
) -> Molecule:
    """Replace a molecule's sub-molecule with a new value"""
    return Molecule(molecule[:start] + replacement + molecule[stop:])


def calibrate(molecule: Molecule, graph: Graph) -> int:
    """Determine the number of distinct molecules that can be generated in
    one step from a given starting molecules"""
    distinct_molecules = set()
    for start, stop in molecule(graph):
        inner_molecule = molecule[start:stop]
        for replacement in graph[inner_molecule]:
            new_molecule = assemble_molecule(molecule, start, stop, replacement)
            distinct_molecules.add(new_molecule)
    return len(distinct_molecules)



def create_edges(graph: Graph) -> tuple[tuple[str, str]]:
    edges = []
    for key, vals in graph.items():
        for item in vals:
            edges.append((key, item))
    edges.sort(key=lambda x: len(x[0]), reverse=True)
    return tuple(edges)


def shortest_fabrication_length(
    molecule: Molecule, graph: Graph, termination_molecule: str
) -> float:
    edges = create_edges(graph)

    @cache
    def disassemble(
        m: Molecule, edges=edges, termination_molecule=termination_molecule
    ) -> Optional[int]:
        if m == termination_molecule: return 0
        shortest_path = float("inf")
        for edge in edges:
            if edge[0] in m:
                start = 0
                submolecule_len = len(edge[0])
                while m.find(edge[0], start) != -1:
                    start = m.find(edge[0], start)
                    stop = start + submolecule_len
                    new_molecule = assemble_molecule(m, start, stop, edge[1])
                    if new_molecule.is_valid():
                        path_len = 1 + disassemble(new_molecule)
                        if path_len != float("inf"):
                            return path_len
                    start = stop
        return shortest_path
    shortest_len_path = disassemble(molecule, edges, termination_molecule)
    return shortest_len_path


if __name__ == "__main__":
    # source = "data//day19_example.txt"
    source = "data//day19.txt"
    g, m_str = file_io(source)
    rg = reverse_graph(g)
    m = Molecule(m_str)
    # m = Molecule("CRnCaSiRnBFArFYBFArSiRnBFArF")
    # print(calibrate(m, g))
    shortest_len = shortest_fabrication_length(m, rg, "e")
    print(shortest_len)