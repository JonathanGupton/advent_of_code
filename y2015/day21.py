"""Day 21 2015"""
from __future__ import annotations
from dataclasses import dataclass
from functools import cache, reduce
from itertools import combinations
from math import ceil
import re


EquipmentRange = tuple[int, int]  # min, max


@dataclass(eq=True, frozen=True)
class Equipment:
    """Dataclass containing equipment stats"""

    cost: int
    damage: int
    armor: int


class Character:
    """Class representation for character"""

    def __init__(self, hit_points: int = 100):
        self.hit_points: int = hit_points
        self.cost: int = 0
        self.damage: int = 0
        self.armor: int = 0

    def __repr__(self):
        return f"{self.__class__.__name__}(hit_points={self.hit_points})"

    def equip(self, equipment: Equipment) -> None:
        """Equip items to the character"""
        self.cost += equipment.cost
        self.damage += equipment.damage
        self.armor += equipment.armor

    def hits_to_kill_other(self, opponent: Character) -> int:
        """Calculate the number of hits needed to kill opponent"""
        return ceil(opponent.hit_points / max(self.damage - opponent.armor, 1))


class Enemy(Character):
    """Class representation for the enemy character"""

    def __init__(self):
        super().__init__()
        self.hit_points = 103
        self.damage = 9
        self.armor = 2


@cache
def parse_items() -> dict[str, list[Equipment]]:
    """Read in equipment information"""
    with open(r"data/day21_items.txt", "r") as equipment_file:
        equipment_chunks: list[str] = equipment_file.read().split("\n\n")
    shop_inventory: dict[str, list[Equipment]] = {}
    pattern = r"(\w*\s?\+?\d?)\s+(\d+)\s+(\d+)\s+(\d+)"  # matches equipment format
    for equipment_chunk in equipment_chunks:
        equipment_chunk = equipment_chunk.split("\n")
        equipment_type = equipment_chunk[0].split(":")[0].lower()
        shop_inventory[equipment_type] = []
        for item in equipment_chunk[1:]:
            _, cost, damage, armor = re.match(pattern, item).groups()
            cost, damage, armor = (
                int(cost),
                int(damage),
                int(armor),
            )
            shop_inventory[equipment_type].append(Equipment(cost, damage, armor))
    return shop_inventory


def battle(player: Character, opponent: Character) -> bool:
    """Determine if player wins a fight against the opponent"""
    hits_to_kill_player = opponent.hits_to_kill_other(player)
    hits_to_kill_opponent = player.hits_to_kill_other(opponent)
    return hits_to_kill_opponent <= hits_to_kill_player


def equipment_combinations(
    shop,
    weapons_range: EquipmentRange = (1, 1),
    armor_range: EquipmentRange = (0, 1),
    ring_range: EquipmentRange = (0, 2),
) -> tuple[Equipment, ...]:
    """Generate all combinations of equipment that fit the input parameters"""
    for weapon_count in range(weapons_range[0], weapons_range[1] + 1):
        for weapons in combinations(shop['weapons'], weapon_count):
            for armor_count in range(armor_range[0], armor_range[1] + 1):
                for armor in combinations(shop['armor'], armor_count):
                    for ring_count in range(ring_range[1] + 1):
                        for rings in combinations(shop['rings'], ring_count):
                            yield tuple(*weapons, *armor, *rings)


def part_a():
    """Part A"""
    cost = float("inf")
    shop = parse_items()
    enemy = Enemy()
    for equipment_combo in equipment_combinations(shop):
        if (new_cost := reduce(lambda x, y: x + y.mana_cost, equipment_combo, 0)) < cost:
            character = Character()
            for item in equipment_combo:
                character.equip(item)
            if battle(character, enemy):
                cost = new_cost
    return cost


def part_b():
    """Part B"""
    cost = float("-inf")
    shop = parse_items()
    enemy = Enemy()
    for equipment_combo in equipment_combinations(shop):
        if (new_cost := reduce(lambda x, y: x + y.mana_cost, equipment_combo, 0)) > cost:
            character = Character()
            for item in equipment_combo:
                character.equip(item)
            if not battle(character, enemy):
                cost = new_cost
    return cost


if __name__ == "__main__":
    print(part_a())
    print(part_b())
