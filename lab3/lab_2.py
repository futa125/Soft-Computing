from lab3.domain.domain import DomainInterface, Domain
from lab3.domain.element import DomainElement
from lab3.fuzzy_set.fuzzy_set import FuzzySetInterface
from lab3.fuzzy_set.mutable import MutableFuzzySet
from lab3.fuzzy_set.relations.relations import (
    is_symmetric, is_reflexive, is_max_min_transitive, is_u_times_u_relation,
    composition_of_binary_relations, is_fuzzy_equivalence
)


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
    simple_domain: DomainInterface = Domain.int_range(1, 6)
    d: DomainInterface = Domain.combine(simple_domain, simple_domain)

    r1: FuzzySetInterface = (MutableFuzzySet(d)
                             .set(DomainElement.of(1, 1), 1)
                             .set(DomainElement.of(2, 2), 1)
                             .set(DomainElement.of(3, 3), 1)
                             .set(DomainElement.of(4, 4), 1)
                             .set(DomainElement.of(5, 5), 1)
                             .set(DomainElement.of(3, 1), 0.5)
                             .set(DomainElement.of(1, 3), 0.5))

    r2: FuzzySetInterface = (MutableFuzzySet(d)
                             .set(DomainElement.of(1, 1), 1)
                             .set(DomainElement.of(2, 2), 1)
                             .set(DomainElement.of(3, 3), 1)
                             .set(DomainElement.of(4, 4), 1)
                             .set(DomainElement.of(5, 5), 1)
                             .set(DomainElement.of(3, 1), 0.5)
                             .set(DomainElement.of(1, 3), 0.1))

    r3: FuzzySetInterface = (MutableFuzzySet(d)
                             .set(DomainElement.of(1, 1), 1)
                             .set(DomainElement.of(2, 2), 1)
                             .set(DomainElement.of(3, 3), 0.3)
                             .set(DomainElement.of(4, 4), 1)
                             .set(DomainElement.of(5, 5), 1)
                             .set(DomainElement.of(1, 2), 0.6)
                             .set(DomainElement.of(2, 1), 0.6)
                             .set(DomainElement.of(2, 3), 0.7)
                             .set(DomainElement.of(3, 2), 0.7)
                             .set(DomainElement.of(3, 1), 0.5)
                             .set(DomainElement.of(1, 3), 0.5))

    r4: FuzzySetInterface = (MutableFuzzySet(d)
                             .set(DomainElement.of(1, 1), 1)
                             .set(DomainElement.of(2, 2), 1)
                             .set(DomainElement.of(3, 3), 1)
                             .set(DomainElement.of(4, 4), 1)
                             .set(DomainElement.of(5, 5), 1)
                             .set(DomainElement.of(1, 2), 0.4)
                             .set(DomainElement.of(2, 1), 0.4)
                             .set(DomainElement.of(2, 3), 0.5)
                             .set(DomainElement.of(3, 2), 0.5)
                             .set(DomainElement.of(1, 3), 0.4)
                             .set(DomainElement.of(3, 1), 0.4))

    print(f"R1 is defined by UxU? {is_u_times_u_relation(r1)}")

    print(f"R1 is symmetric? {is_symmetric(r1)}")
    print(f"R2 is symmetric? {is_symmetric(r2)}")

    print(f"R1 is reflexive? {is_reflexive(r1)}")
    print(f"R3 is reflexive? {is_reflexive(r3)}")

    print(f"R3 is max min transitive? {is_max_min_transitive(r3)}")
    print(f"R4 is max min transitive? {is_max_min_transitive(r4)}")

    u1: DomainInterface = Domain.int_range(1, 5)
    u2: DomainInterface = Domain.int_range(1, 4)
    u3: DomainInterface = Domain.int_range(1, 5)

    r1: FuzzySetInterface = (MutableFuzzySet(Domain.combine(u1, u2))
                             .set(DomainElement.of(1, 1), 0.3)
                             .set(DomainElement.of(1, 2), 1)
                             .set(DomainElement.of(3, 3), 0.5)
                             .set(DomainElement.of(4, 3), 0.5))

    r2: FuzzySetInterface = (MutableFuzzySet(Domain.combine(u2, u3))
                             .set(DomainElement.of(1, 1), 1)
                             .set(DomainElement.of(2, 1), 0.5)
                             .set(DomainElement.of(2, 2), 0.7)
                             .set(DomainElement.of(3, 3), 1)
                             .set(DomainElement.of(3, 4), 0.4))

    r1r2: FuzzySetInterface = composition_of_binary_relations(r1, r2)
    print()
    for element in (r1r2.get_domain()):
        print(f"mu({element})={r1r2.get_value_at(element):.1f}")

    u: DomainInterface = Domain.int_range(1, 5)
    r: FuzzySetInterface = (MutableFuzzySet(Domain.combine(u, u))
                            .set(DomainElement.of(1, 1), 1)
                            .set(DomainElement.of(2, 2), 1)
                            .set(DomainElement.of(3, 3), 1)
                            .set(DomainElement.of(4, 4), 1)
                            .set(DomainElement.of(1, 2), 0.3)
                            .set(DomainElement.of(2, 1), 0.3)
                            .set(DomainElement.of(2, 3), 0.5)
                            .set(DomainElement.of(3, 2), 0.5)
                            .set(DomainElement.of(3, 4), 0.2)
                            .set(DomainElement.of(4, 3), 0.2))

    r2: FuzzySetInterface = (r)

    print()
    print(f"R is a fuzzy equivalence before compositions? {is_fuzzy_equivalence(r2)}")
    for element in (r2.get_domain()):
        print(f"mu({element})={r2.get_value_at(element):.1f}")
    print()

    for i in range(1, 4):
        r2 = composition_of_binary_relations(r2, r)

        print(f"R is a fuzzy equivalence after {i} compositions? {is_fuzzy_equivalence(r2)}")
        for element in (r2.get_domain()):
            print(f"mu({element})={r2.get_value_at(element):.1f}")

        print()


if __name__ == "__main__":
    main()
