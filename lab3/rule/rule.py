from __future__ import annotations

import dataclasses
from typing import List

from lab3.boat.inputvalues import InputValues
from lab3.domain.element import DomainElement
from lab3.fuzzy_set.fuzzy_set import FuzzySetInterface
from lab3.fuzzy_set.operations.binary_functions import FloatBinaryFunction
from lab3.fuzzy_set.operations.operations import unary_operation


@dataclasses.dataclass
class Rule:
    antecedent: List[FuzzySetInterface]
    consequent: FuzzySetInterface

    def apply(self: Rule, value: InputValues, t_norm: FloatBinaryFunction) -> FuzzySetInterface:
        alpha: float = 1

        fuzzy_set: FuzzySetInterface
        input_value: int

        for fuzzy_set, input_value in zip(self.antecedent, value):
            if fuzzy_set is None:
                continue

            alpha = t_norm(alpha, fuzzy_set.get_value_at(DomainElement.of(input_value)))

        return unary_operation(self.consequent, lambda x: t_norm(x, alpha))
