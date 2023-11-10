from __future__ import annotations

import abc
import dataclasses
import enum
from typing import List

from LAB_1_2_3.boat.inputvalues import InputValues
from LAB_1_2_3.defuzzify.defuzzify import Defuzzifier
from LAB_1_2_3.fuzzy_set.fuzzy_set import FuzzySetInterface
from LAB_1_2_3.fuzzy_set.operations.binary_functions import FloatBinaryFunction, zadeh_and, zadeh_or, hamacher_t_norm
from LAB_1_2_3.fuzzy_set.operations.operations import binary_operation
from LAB_1_2_3.rule.rule import Rule


class FuzzySystemType(enum.StrEnum):
    MINIMUM = enum.auto()
    PRODUCT = enum.auto()


@dataclasses.dataclass
class FuzzySystem(abc.ABC):
    defuzzifier: Defuzzifier
    type: FuzzySystemType
    rules: List[Rule]

    t_norm: FloatBinaryFunction = dataclasses.field(init=False)
    s_norm: FloatBinaryFunction = dataclasses.field(init=False)

    def __post_init__(self: FuzzySystem):
        if self.type == FuzzySystemType.MINIMUM:
            self.t_norm = zadeh_and()
        elif self.t_norm == FuzzySystemType.PRODUCT:
            self.t_norm = hamacher_t_norm(1)

        self.s_norm = zadeh_or()

    def decide(self: FuzzySystem, values: InputValues) -> int:
        return round(self.defuzzifier.defuzzify(self.generate_results(values)))

    def generate_results(self: FuzzySystem, values: InputValues) -> FuzzySetInterface:
        consequents: List[FuzzySetInterface] = []
        for rule in self.rules:
            out = rule.apply(values, self.t_norm)
            consequents.append(out)

        result = consequents[0]
        for consequent in consequents:
            result = binary_operation(result, consequent, self.s_norm)

        return result
