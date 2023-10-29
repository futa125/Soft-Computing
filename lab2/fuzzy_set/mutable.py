from __future__ import annotations

import dataclasses

from typing import List

from lab2.domain.domain import DomainInterface
from lab2.domain.element import DomainElement
from lab2.fuzzy_set.fuzzy_set import FuzzySetInterface


@dataclasses.dataclass
class MutableFuzzySet(FuzzySetInterface):
    domain: DomainInterface
    memberships: List[float] = dataclasses.field(init=False)

    def __post_init__(self):
        self.memberships = [0 for _ in range(self.domain.get_cardinality())]

    def get_domain(self) -> DomainInterface:
        return self.domain

    def get_value_at(self, element: DomainElement) -> float:
        return self.memberships[self.domain.index_of_element(element)]

    def set(self, element: DomainElement, value: float) -> MutableFuzzySet:
        self.memberships[self.domain.index_of_element(element)] = value

        return self
