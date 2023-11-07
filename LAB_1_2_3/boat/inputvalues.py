from __future__ import annotations

import dataclasses
from typing import List, Iterator


@dataclasses.dataclass
class InputValues:
    L: int
    D: int
    LK: int
    DK: int
    V: int
    S: int

    _current: int = dataclasses.field(init=False, default=0)
    _values: List[int] = dataclasses.field(init=False, default_factory=list)

    def __post_init__(self: InputValues) -> None:
        self._values = [self.L, self.D, self.LK, self.DK, self.V, self.S]

    def __iter__(self: InputValues) -> Iterator[int]:
        return iter(self._values)
