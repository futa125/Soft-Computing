from __future__ import annotations

import abc

from LAB_1_2_3.domain.domain import DomainInterface
from LAB_1_2_3.domain.element import DomainElement


class FuzzySetInterface(abc.ABC):
    @abc.abstractmethod
    def get_domain(self) -> DomainInterface:
        raise NotImplementedError

    @abc.abstractmethod
    def get_value_at(self, element: DomainElement) -> float:
        raise NotImplementedError
