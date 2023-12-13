from __future__ import annotations

import abc

from lab3.fuzzy_set.fuzzy_set import FuzzySetInterface


class Defuzzifier(abc.ABC):
    @abc.abstractmethod
    def defuzzify(self: Defuzzifier, fuzzy_set: FuzzySetInterface) -> float:
        raise NotImplementedError
