"""Day 24"""
from functools import reduce
from typing import Optional


Weight = int
Weights = list[Weight, ...]
QE = int  # Quantum Entanglement


def read_in_weights(filepath) -> list[Weight, ...]:
    """IO for weight file"""
    with open(filepath) as weights_file:
        weights_data = list(int(i) for i in weights_file.readlines())
    return weights_data


class Compartment:
    def __init__(self, compartment_weights: Weights = Optional[Weights]):
        self.weights = compartment_weights if compartment_weights else []

    def __repr__(self):
        value_str = self.weights if self.weights else ""
        return f"Compartment({value_str})"

    @property
    def total_weight(self) -> Weight:
        return sum(self.weights)

    @property
    def weight_count(self) -> int:
        return len(self.weights)

    @property
    def quantum_entanglement(self) -> QE:
        return reduce(lambda x, y: x * y, self.weights, 1)

    def add_weight(self, weight: Weight) -> None:
        self.weights.append(weight)

    def remove_weight(self, weight: Weight) -> None:
        self.weights.remove(weight)

    def __add__(self, other) -> int:
        if isinstance(other, Compartment):
            return self.total_weight + other.total_weight


def subset_sum(
    weights: Weights,
    target: float,
    partial: Optional[Weights] = None,
    partial_sum: int = 0,
):
    partial = partial if partial else []
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i, n in enumerate(weights):
        remaining = weights[i + 1 :]
        yield from subset_sum(remaining, target, partial + [n], partial_sum + n)


def part_a() -> QE:
    weights = read_in_weights(r"data\day24.txt")
    n_compartments = 3
    # qe = solve(weights=weights, n_compartments=n_compartments)
    qe = 0
    return qe


if __name__ == "__main__":

    # weights = read_in_weights(r"data\day24_example.txt")
    weights = read_in_weights(r"data\day24.txt")

    weights.sort(reverse=True)
    n_compartments = 4
    goal = sum(weights) / n_compartments
    output = [subset for subset in subset_sum(weights, goal)]
    min_len = min([len(i) for i in output])
    result = min([reduce(lambda x, y: x * y, i, 1) for i in output if len(i) == min_len])