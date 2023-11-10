from LAB_1_2_3.boat.domains import DISTANCE, ANGLE, ACCELERATION, SPEED, ORIENTATION
from LAB_1_2_3.domain.element import DomainElement
from LAB_1_2_3.fuzzy_set.calculated import CalculatedFuzzySet
from LAB_1_2_3.fuzzy_set.mutable import MutableFuzzySet
from LAB_1_2_3.fuzzy_set.operations.unary_functions import l_function, gamma_function

WRONG_DIRECTION = MutableFuzzySet(ORIENTATION).set(DomainElement.of(0), 1)

CLOSE_TO_LAND = CalculatedFuzzySet(DISTANCE, l_function(40, 70))

VERY_CLOSE_TO_LAND = CalculatedFuzzySet(DISTANCE, l_function(30, 40))

FAR_FROM_LAND = CalculatedFuzzySet(DISTANCE, l_function(100, 200))

LEFT_TURN_SOFT = CalculatedFuzzySet(ANGLE, gamma_function(
    ANGLE.index_of_element(DomainElement.of(5)),
    ANGLE.index_of_element(DomainElement.of(30)),
))

RIGHT_TURN_SOFT = CalculatedFuzzySet(ANGLE, l_function(
    ANGLE.index_of_element(DomainElement.of(-30)),
    ANGLE.index_of_element(DomainElement.of(-5)),
))

LEFT_TURN_HARD = CalculatedFuzzySet(ANGLE, gamma_function(
    ANGLE.index_of_element(DomainElement.of(30)),
    ANGLE.index_of_element(DomainElement.of(90)),
))

RIGHT_TURN_HARD = CalculatedFuzzySet(ANGLE, l_function(
    ANGLE.index_of_element(DomainElement.of(-90)),
    ANGLE.index_of_element(DomainElement.of(-30)),
))

ACCELERATE = CalculatedFuzzySet(ACCELERATION, gamma_function(
    ACCELERATION.index_of_element(DomainElement.of(10)),
    ACCELERATION.index_of_element(DomainElement.of(30)),
))

DECELERATE = CalculatedFuzzySet(ACCELERATION, l_function(
    ACCELERATION.index_of_element(DomainElement.of(-30)),
    ACCELERATION.index_of_element(DomainElement.of(-10)),
))

FAST = CalculatedFuzzySet(SPEED, gamma_function(
    SPEED.index_of_element(DomainElement.of(60)),
    SPEED.index_of_element(DomainElement.of(80)),
))

VERY_SLOW = CalculatedFuzzySet(SPEED, l_function(
    SPEED.index_of_element(DomainElement.of(20)),
    SPEED.index_of_element(DomainElement.of(40)),
))
