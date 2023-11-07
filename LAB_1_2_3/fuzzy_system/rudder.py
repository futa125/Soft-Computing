from typing import List

from LAB_1_2_3.boat.sets import VERY_CLOSE_TO_LAND, LEFT_TURN_HARD, RIGHT_TURN_HARD, CLOSE_TO_LAND, RIGHT_TURN_SOFT, \
    LEFT_TURN_SOFT
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_system.fuzzy_system import FuzzySystem, FuzzySystemType
from LAB_1_2_3.rule.rule import Rule

RULES: List[Rule] = [
    Rule([None, VERY_CLOSE_TO_LAND, None, None, None, None], LEFT_TURN_HARD),
    Rule([VERY_CLOSE_TO_LAND, None, None, None, None, None], RIGHT_TURN_HARD),
    Rule([None, None, None, VERY_CLOSE_TO_LAND, None, None], LEFT_TURN_HARD),
    Rule([None, None, VERY_CLOSE_TO_LAND, None, None, None], RIGHT_TURN_HARD),
    Rule([None, CLOSE_TO_LAND, None, CLOSE_TO_LAND, None, None], LEFT_TURN_SOFT),
    Rule([CLOSE_TO_LAND, None, CLOSE_TO_LAND, None, None, None], RIGHT_TURN_SOFT),
]


class RudderFuzzySystem(FuzzySystem):
    def __init__(self, defuzzifier: Defuzzifier):
        super().__init__(defuzzifier, FuzzySystemType.MINIMUM, RULES)
