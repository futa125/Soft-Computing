from lab3.domain.domain import Domain
from lab3.domain.element import DomainElement
from lab3.fuzzy_set.fuzzy_set import FuzzySetInterface
from lab3.fuzzy_set.mutable import MutableFuzzySet
from lab3.fuzzy_set.operations.binary_functions import zadeh_or, zadeh_and


def is_symmetric(fuzzy_set: FuzzySetInterface) -> bool:
    if not is_u_times_u_relation(fuzzy_set):
        return False

    for element in fuzzy_set.get_domain():
        symmetric_element = DomainElement.of(*reversed(element.values))

        if fuzzy_set.get_value_at(element) != fuzzy_set.get_value_at(symmetric_element):
            return False

    return True


def is_reflexive(fuzzy_set: FuzzySetInterface) -> bool:
    if not is_u_times_u_relation(fuzzy_set):
        return False

    for element in fuzzy_set.get_domain():
        all_components_equal = all(element.get_component_value(i) == element.get_component_value(0)
                                   for i in range(element.get_number_of_components()))

        value = fuzzy_set.get_value_at(element)

        if all_components_equal and value != 1:
            return False

    return True


def is_max_min_transitive(fuzzy_set: FuzzySetInterface) -> bool:
    for xy in fuzzy_set.get_domain():
        x, y = xy.get_component_value(0), xy.get_component_value(1)

        for element in fuzzy_set.get_domain().get_component(1):
            z = element.get_component_value(0)

            xz = DomainElement.of(x, z)
            yz = DomainElement.of(y, z)

            if fuzzy_set.get_value_at(xz) < min(fuzzy_set.get_value_at(xy), fuzzy_set.get_value_at(yz)):
                return False

    return True


def is_u_times_u_relation(fuzzy_set: FuzzySetInterface) -> bool:
    if fuzzy_set.get_domain().get_number_of_components() != 2:
        return False

    domain_1, domain_2 = fuzzy_set.get_domain().get_component(0), fuzzy_set.get_domain().get_component(1)

    if domain_1.get_cardinality() != domain_2.get_cardinality():
        return False

    x: DomainElement
    y: DomainElement
    for x, y in zip(domain_1, domain_2):
        if x.get_component_value(0) != y.get_component_value(0):
            return False

    return True


def composition_of_binary_relations(set_1: FuzzySetInterface, set_2: FuzzySetInterface) -> FuzzySetInterface:
    u = set_1.get_domain().get_component(0)
    a = set_1.get_domain().get_component(1)
    _ = set_2.get_domain().get_component(0)
    w = set_2.get_domain().get_component(1)

    uw = Domain.combine(u, w)

    result = MutableFuzzySet(uw)

    for element_u in u:
        for element_w in w:
            value: float = 0

            x = element_u.get_component_value(0)
            y = element_w.get_component_value(0)
            for element in a:
                xy = DomainElement.of(x, element.get_component_value(0))
                yz = DomainElement.of(element.get_component_value(0), y)

                value = zadeh_or()(value, zadeh_and()(set_1.get_value_at(xy), set_2.get_value_at(yz)))

            result.set(DomainElement.of(x, y), value)

    return result


def is_fuzzy_equivalence(fuzzy_set: FuzzySetInterface) -> bool:
    return is_reflexive(fuzzy_set) and is_symmetric(fuzzy_set) and is_max_min_transitive(fuzzy_set)
