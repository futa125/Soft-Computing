import dataclasses

from lab3.domain.domain import DomainInterface
from lab3.domain.element import DomainElement
from lab3.fuzzy_set.fuzzy_set import FuzzySetInterface
from lab3.fuzzy_set.operations.unary_functions import IntUnaryFunction


@dataclasses.dataclass
class CalculatedFuzzySet(FuzzySetInterface):
    domain: DomainInterface
    unary_function: IntUnaryFunction

    def get_domain(self) -> DomainInterface:
        return self.domain

    def get_value_at(self, element: DomainElement) -> float:
        return self.unary_function(self.domain.index_of_element(element))
