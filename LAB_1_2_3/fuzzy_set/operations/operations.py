from copy import deepcopy

from LAB_1_2_3.domain.element import DomainElement
from LAB_1_2_3.fuzzy_set.fuzzy_set import FuzzySetInterface
from LAB_1_2_3.fuzzy_set.mutable import MutableFuzzySet
from LAB_1_2_3.fuzzy_set.operations.binary_functions import FloatBinaryFunction
from LAB_1_2_3.fuzzy_set.operations.unary_functions import FloatUnaryFunction


def unary_operation(fuzzy_set: FuzzySetInterface, func: FloatUnaryFunction) -> FuzzySetInterface:
    new_fuzzy_set = MutableFuzzySet(deepcopy(fuzzy_set.get_domain()))

    for new_element, element in zip(new_fuzzy_set.get_domain(), fuzzy_set.get_domain()):
        old_value = fuzzy_set.get_value_at(element)
        new_value = func(old_value)

        new_fuzzy_set = new_fuzzy_set.set(new_element, new_value)

    return new_fuzzy_set


def binary_operation(
        fuzzy_set_1: FuzzySetInterface, fuzzy_set_2: FuzzySetInterface, func: FloatBinaryFunction
) -> FuzzySetInterface:
    if fuzzy_set_1.get_domain().get_cardinality() != fuzzy_set_2.get_domain().get_cardinality():
        raise ValueError("both fuzzy sets must have the same cardinality")

    new_fuzzy_set = MutableFuzzySet(deepcopy(fuzzy_set_1.get_domain()))

    new_element: DomainElement
    element_1: DomainElement
    element_2: DomainElement
    for new_element, element_1, element_2 in zip(
            new_fuzzy_set.get_domain(), fuzzy_set_1.get_domain(), fuzzy_set_2.get_domain()
    ):
        new_value = func(fuzzy_set_1.get_value_at(element_1), fuzzy_set_2.get_value_at(element_2))
        new_fuzzy_set = new_fuzzy_set.set(new_element, new_value)

    return new_fuzzy_set
