from typing import Sequence
"""
The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant.
"""



"""
example
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.

11 steps
"""

COMPONENT = str
FLOOR = Sequence[COMPONENT]
FACTORY = Sequence[FLOOR]


def generate_factory_positions(factory: FACTORY) -> FACTORY:
    yield factory


floors = {
    1: ("E", "HM", "LM"),
    2: ("HG",),
    3: ("LG",),
    4: ()
}
