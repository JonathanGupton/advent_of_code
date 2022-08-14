from functools import cache
from collections import Counter


def input_parser(filepath) -> tuple[str, dict[str, str]]:
    with open(filepath, "r") as f:
        template, rules = f.read().split("\n\n")
        rules_map = {}
        for rule in rules.split("\n"):
            pair, insertion = rule.split(" -> ")
            rules_map[pair] = insertion
    return template, rules_map


def grow_polymer(
    polymer: str, depth: int, rules_map: dict[str, str]
) -> Counter[str, int]:
    @cache
    def _grow_polymer(polymer: str, depth: int) -> Counter:
        nonlocal rules_map

        new_vals = Counter()
        if depth != 0:
            for i in range(1, len(polymer)):
                inserted = rules_map[polymer[i - 1 : i + 1]]
                new_vals.update(inserted)
                new_chunk = polymer[i - 1] + inserted + polymer[i]
                inner_polymer_count = _grow_polymer(new_chunk, depth - 1)
                new_vals += inner_polymer_count
        return new_vals

    start_count = Counter(polymer)
    char_count = start_count + _grow_polymer(polymer, depth=depth)
    return char_count


def score_element_count(element_count: Counter[str, int]) -> int:
    return element_count.most_common()[0][1] - element_count.most_common()[-1][1]


def part_a():
    fp = r"data/day14.txt"
    polymer, rules_map = input_parser(fp)
    depth = 10
    char_count = grow_polymer(polymer, depth=depth, rules_map=rules_map)
    score = score_element_count(char_count)
    return score


def part_b():
    fp = r"data/day14.txt"
    polymer, rules_map = input_parser(fp)
    depth = 40
    char_count = grow_polymer(polymer, depth=depth, rules_map=rules_map)
    score = score_element_count(char_count)
    return score


if __name__ == "__main__":
    print(part_a())
    print(part_b())
