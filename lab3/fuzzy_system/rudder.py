from typing import List

from lab3.boat.sets import (VERY_CLOSE_TO_LAND, LEFT_TURN_HARD, RIGHT_TURN_HARD, CLOSE_TO_LAND,
                            RIGHT_TURN_SOFT, LEFT_TURN_SOFT, WRONG_DIRECTION, FAR_FROM_LAND)
from lab3.defuzzify.defuzzify import Defuzzifier
from lab3.fuzzy_system.fuzzy_system import FuzzySystem, FuzzySystemType
from lab3.rule.rule import Rule

RULES: List[Rule] = [
    # Hard turn if very close
    Rule([VERY_CLOSE_TO_LAND, None, VERY_CLOSE_TO_LAND, None, None, None], RIGHT_TURN_HARD),
    Rule([None, VERY_CLOSE_TO_LAND, None, VERY_CLOSE_TO_LAND, None, None], LEFT_TURN_HARD),

    # Soft turn if kinda close
    Rule([CLOSE_TO_LAND, None, CLOSE_TO_LAND, None, None, None], RIGHT_TURN_HARD),
    Rule([None, CLOSE_TO_LAND, None, CLOSE_TO_LAND, None, None], LEFT_TURN_HARD),
    Rule([None, None, CLOSE_TO_LAND, None, None, None], RIGHT_TURN_SOFT),
    Rule([None, None, None, CLOSE_TO_LAND, None, None], LEFT_TURN_SOFT),

    # Hard turn right if going wrong way and space to turn
    Rule([None, FAR_FROM_LAND, None, FAR_FROM_LAND, None, WRONG_DIRECTION], RIGHT_TURN_HARD),
]


class RudderFuzzySystem(FuzzySystem):
    def __init__(self, defuzzifier: Defuzzifier):
        super().__init__(defuzzifier, FuzzySystemType.MINIMUM, RULES)
