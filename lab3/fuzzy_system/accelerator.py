from typing import List

from lab3.boat.sets import (ACCELERATE, FAST, DECELERATE, FAR_FROM_LAND,
                            CLOSE_TO_LAND, WRONG_DIRECTION, VERY_SLOW)
from lab3.defuzzify.defuzzify import Defuzzifier
from lab3.fuzzy_system.fuzzy_system import FuzzySystem, FuzzySystemType
from lab3.rule.rule import Rule

RULES: List[Rule] = [
    Rule([None, None, None, None, VERY_SLOW, None], ACCELERATE),

    # Speed up if enough space
    Rule([None, None, FAR_FROM_LAND, FAR_FROM_LAND, None, None], ACCELERATE),

    # Slow down a bit if too fast
    Rule([None, None, None, None, FAST, None], DECELERATE),

    # Slow down if close to land (more time to turn away)
    Rule([None, None, CLOSE_TO_LAND, CLOSE_TO_LAND, None, None], DECELERATE),
    Rule([CLOSE_TO_LAND, None, CLOSE_TO_LAND, None, None, None], DECELERATE),
    Rule([None, CLOSE_TO_LAND, None, CLOSE_TO_LAND, None, None], DECELERATE),

    # Slow down if going the wrong way
    Rule([None, None, None, None, None, WRONG_DIRECTION], DECELERATE),
]


class AcceleratorFuzzySystem(FuzzySystem):
    def __init__(self, defuzzifier: Defuzzifier):
        super().__init__(defuzzifier, FuzzySystemType.MINIMUM, RULES)
