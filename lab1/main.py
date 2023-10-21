from lab1.domain.domain import DomainInterface, Domain
from lab1.domain.element import DomainElement
from lab1.fuzzy_set.calculated import CalculatedFuzzySet
from lab1.fuzzy_set.fuzzy_set import FuzzySetInterface
from lab1.fuzzy_set.mutable import MutableFuzzySet
from lab1.fuzzy_set.operations.binary_functions import zadeh_or, hamacher_t_norm
from lab1.fuzzy_set.operations.operations import unary_operation, binary_operation
from lab1.fuzzy_set.operations.unary_functions import lambda_function, zadeh_not


def debug_domain(domain: DomainInterface, heading: str) -> None:
    if heading is not None:
        print(heading)

    for element in domain:
        print(f"Domain Element: {element}")

    print(f"Domain Cardinality: {domain.get_cardinality()}")
    print()


def debug_fuzzy_set(fuzzy_set: FuzzySetInterface, heading: str) -> None:
    if heading is not None:
        print(heading)

    for element in fuzzy_set.get_domain():
        print(f"d({element})={fuzzy_set.get_value_at(element):.6f}")

    print()


def main() -> None:
    d1: DomainInterface = Domain.int_range(0, 5)
    debug_domain(d1, "Elements of Domain 1:")

    d2: DomainInterface = Domain.int_range(0, 3)
    debug_domain(d2, "Elements of Domain 2:")

    d3: DomainInterface = Domain.combine(d1, d2)
    debug_domain(d3, "Elements of Domain 3:")

    print(d3.element_for_index(0))
    print(d3.element_for_index(5))
    print(d3.element_for_index(14))
    print(d3.index_of_element(DomainElement.of(4, 1)))
    print()

    d1: DomainInterface = Domain.int_range(0, 11)
    set1: FuzzySetInterface = (MutableFuzzySet(d1)
                               .set(DomainElement.of(0), 1.0)
                               .set(DomainElement.of(1), 0.8)
                               .set(DomainElement.of(2), 0.6)
                               .set(DomainElement.of(3), 0.4)
                               .set(DomainElement.of(4), 0.2))
    debug_fuzzy_set(set1, "Set 1:")

    d2: DomainInterface = Domain.int_range(-5, 6)
    set2: FuzzySetInterface = CalculatedFuzzySet(d2, lambda_function(
        d2.index_of_element(DomainElement.of(-4)),
        d2.index_of_element(DomainElement.of(0)),
        d2.index_of_element(DomainElement.of(4)),
    ))
    debug_fuzzy_set(set2, "Set 2:")

    not_set1: FuzzySetInterface = unary_operation(set1, zadeh_not())
    debug_fuzzy_set(not_set1, "Not-Set 1:")

    union_set: FuzzySetInterface = binary_operation(set1, not_set1, zadeh_or())
    debug_fuzzy_set(union_set, "Union of Set 1 and Not-Set 1:")

    hinters: FuzzySetInterface = binary_operation(set1, not_set1, hamacher_t_norm(1))
    debug_fuzzy_set(
        hinters,
        "Intersection of Set 1 with Not-Set 1 Using Hamacher T-Norm with Parameter 1.0:"
    )


if __name__ == "__main__":
    main()
