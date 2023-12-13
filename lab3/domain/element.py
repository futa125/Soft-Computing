from __future__ import annotations

import dataclasses
from typing import Tuple


@dataclasses.dataclass
class DomainElement:
    values: Tuple[int, ...]

    def get_number_of_components(self) -> int:
        return len(self.values)

    def get_component_value(self, i: int) -> int:
        if i < 0:
            raise IndexError("component index must be a positive value")

        if i >= len(self.values):
            raise IndexError("component index ouf of range")

        return self.values[i]

    @staticmethod
    def of(*values: int) -> DomainElement:
        return DomainElement(values)

    def __eq__(self: DomainElement, other: DomainElement) -> bool:
        return self.values == other.values

    def __repr__(self) -> str:
        if len(self.values) == 0:
            return "Empty"

        joined_values: str = ', '.join(str(x) for x in self.values)

        if len(self.values) == 1:
            return joined_values

        return f"({joined_values})"
