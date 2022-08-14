from itertools import combinations
from collections import namedtuple
import numpy as np


ingredient = namedtuple(
    "Ingredient", ["name", "capacity", "durability", "flavor", "texture", "calories"]
)


def partitions(max_n: int, buckets: int):
    """Create all iterations of a positive integer divided into a given number of buckets"""
    for c in combinations(range(max_n + buckets - 1), buckets - 1):
        yield [b - a - 1 for a, b in zip((-1,) + c, c + (max_n + buckets - 1,))]


def file_io(source):
    with open(source, "r") as f:
        return f.read().strip().split("\n")


def parse_ingredient(line):
    name, values = line.split(": ")
    values = values.split(", ")
    capacity = int(values[0].split(" ")[1])
    durability = int(values[1].split(" ")[1])
    flavor = int(values[2].split(" ")[1])
    texture = int(values[3].split(" ")[1])
    calories = int(values[4].split(" ")[1])
    return ingredient(name, capacity, durability, flavor, texture, calories)


def part_a():
    f = r"data\day15.txt"
    data = file_io(f)
    ingredients = [parse_ingredient(line) for line in data]
    ingredients = np.array([ing[1:-1] for ing in ingredients])
    max_score = 0
    n_tsp = 100
    n_ingredients = len(ingredients)
    for i in partitions(n_tsp, n_ingredients):
        score = np.prod(
            np.clip(sum((ingredients.T * np.array(i)).T), a_min=0, a_max=None)
        )
        max_score = score if score > max_score else max_score
    print(max_score)


def part_b():
    f = r"data\day15.txt"
    data = file_io(f)
    ingredients = [parse_ingredient(line) for line in data]
    ingredients = np.array([i[1:] for i in ingredients])
    max_score = 0
    n_tsp = 100
    n_ingredients = len(ingredients)
    for ingredient_distribution in partitions(n_tsp, n_ingredients):
        ingredient_distribution = np.array(ingredient_distribution)
        if sum(ingredients[:, -1] * ingredient_distribution) == 500:
            score = np.prod(
                np.clip(
                    sum((ingredients[:, :-1].T * ingredient_distribution).T),
                    a_min=0,
                    a_max=None,
                )
            )
            max_score = score if score > max_score else max_score
    print(max_score)


part_a()
part_b()