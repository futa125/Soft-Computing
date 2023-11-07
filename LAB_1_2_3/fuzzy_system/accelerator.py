from typing import List

from LAB_1_2_3.boat.sets import VERY_CLOSE_TO_LAND, SLOW, ACCELERATE, FAST, DECELERATE, FAR_FROM_LAND, CLOSE_TO_LAND
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_system.fuzzy_system import FuzzySystem, FuzzySystemType
from LAB_1_2_3.rule.rule import Rule

RULES: List[Rule] = [
    Rule([FAR_FROM_LAND, FAR_FROM_LAND, FAR_FROM_LAND, FAR_FROM_LAND, None, None], ACCELERATE),
    Rule([None, None, CLOSE_TO_LAND, CLOSE_TO_LAND, None, None], DECELERATE),
    Rule([None, None, None, None, SLOW, None], ACCELERATE),
    Rule([None, None, None, None, FAST, None], DECELERATE),
]


class AcceleratorFuzzySystem(FuzzySystem):
    def __init__(self, defuzzifier: Defuzzifier):
        super().__init__(defuzzifier, FuzzySystemType.MINIMUM, RULES)
