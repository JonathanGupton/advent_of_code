"""Day 22 2015"""

from abc import ABC, abstractmethod


class Spell(ABC):
    """Base class for Spells"""

    @property
    @abstractmethod
    def mana_cost(self) -> int:
        """Positive value mana cost property"""
        raise NotImplementedError

    def _spend_mana(self, caster):
        caster.mana -= self.mana_cost

    @abstractmethod
    def cast(self, caster, target):
        """Base method for casting used by all spells"""
        self._spend_mana(caster)


class Effect(ABC):
    """Base class for effects that resolve over multiple turns"""

    @property
    @abstractmethod
    def default_timer(self) -> int:
        """Effect Time property to be set for all effects"""
        raise NotImplementedError

    def __init__(self, timer=default_timer):
        self.timer = timer

    def __repr__(self):
        return f"{self.__class__}(timer={self.timer})"

    def __hash__(self):
        return hash(repr(self))

    def _reduce_effect_timer(self, reduction: int = 1):
        self.timer -= reduction

    @abstractmethod
    def resolve_effect(self):
        """Action taken at the beginning of each turn to resolve the effect"""
        raise NotImplementedError


class MagicMissile(Spell):
    """
    Magic Missile spell.
    Costs 53 mana.
    It instantly does 4 damage.
    """

    mana_cost = 53
    damage = 4

    def cast(self, caster, target):
        super().cast(caster, target)
        target.hit_points -= self.damage


class Drain(Spell):
    """
    Drain spell.
    Costs 73 mana.
    It instantly does 2 damage and heals you for 2 hit points.
    """

    mana_cost = 73
    damage = 2
    heal = 2

    def cast(self, caster, target):
        super().cast(caster, target)
        target.hit_points -= self.damage
        caster.hit_points += self.heal


class Shield(Spell, Effect):
    """
    Shield spell.
    Costs 113 mana.
    It starts an effect that lasts for 6 turns.
    While it is active, your armor is increased by 7.
    """

    mana_cost = 113
    default_timer = 6

    def cast(self, caster, target):
        pass

    def resolve_effect(self):
        pass


class Poison(Spell, Effect):
    """
    Poison spell.
    Costs 173 mana.
    It starts an effect that lasts for 6 turns.
    At the start of each turn while it is active, it deals the boss 3 damage.
    """

    mana_cost = 173
    default_timer = 6
    damage = 3

    def cast(self, caster, target):
        pass

    def resolve_effect(self):
        pass


class Recharge(Spell, Effect):
    """
    Recharge spell.
    Costs 173 mana.
    It starts an effect that lasts for 5 turns.
    At the start of each turn while it is active, it gives you 101 new mana.
    """

    mana_cost = 229
    recharge_amount = 101
    default_timer = 5

    def cast(self, caster, target):
        pass

    def resolve_effect(self):
        pass


class Wizard:
    """Wizard class"""

    def __init__(self, hit_points: int = 50, mana: int = 500, mana_spent: int = 0):
        self.hit_points = hit_points
        self.mana = mana
        self.mana_spent = mana_spent

    def __repr__(self):
        return (
            f"{self.__class__}(hit_points={self.hit_points}, "
            f"mana={self.mana}, mana_spent={self.mana_spent})"
        )

    def __hash__(self):
        return hash(repr(self))


class Enemy:
    """Class representation for the enemy character"""

    def __init__(self, hit_points: int = 55, damage: int = 8):
        self.hit_points = hit_points
        self.damage = damage

    def __repr__(self):
        return f"{self.__class__}(hit_points={self.hit_points}, damage={self.damage})"

    def __hash__(self):
        return hash(repr(self))


class Turn:
    """Class to hold current turn's state"""
    def __init__(self, wizard: Wizard, enemy: Enemy):
        self.wizard: Wizard = wizard
        self.enemy: Enemy = enemy
        self.effects: dict[Effect, int] = {}

    def __repr__(self):
        return (
            f"{self.__class__}(wizard={self.wizard}, "
            f"enemy={self.enemy}, "
            f"effects={self.effects})"
        )

    def __hash__(self):
        return hash(repr(self))
