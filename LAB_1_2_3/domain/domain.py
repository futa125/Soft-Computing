from __future__ import annotations

import abc
import dataclasses
import itertools
import sys

from abc import ABC
from collections.abc import Iterable
from typing import Iterator, Tuple, List, cast

from LAB_1_2_3.domain.element import DomainElement


class DomainInterface(abc.ABC, Iterable[DomainElement]):
    @abc.abstractmethod
    def get_cardinality(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_component(self, i: int) -> DomainInterface:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_components(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def index_of_element(self, domain_element: DomainElement) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def element_for_index(self, i: int) -> DomainElement:
        raise NotImplementedError


class ElementNotFoundError(Exception):
    def __init__(self, element: DomainElement):
        super().__init__(f"domain element {element} not found")


class Domain(DomainInterface, ABC):
    @staticmethod
    def int_range(start: int, end: int) -> DomainInterface:
        return SimpleDomain(start, end)

    @staticmethod
    def combine(d1: DomainInterface, d2: DomainInterface) -> DomainInterface:
        domains: List[SimpleDomain, ...] = []

        for component_number in range(d1.get_number_of_components()):
            domain: DomainInterface = d1.get_component(component_number)
            if isinstance(domain, SimpleDomain):
                domains.append(cast(SimpleDomain, d1.get_component(component_number)))

        for component_number in range(d2.get_number_of_components()):
            domain: DomainInterface = d2.get_component(component_number)
            if isinstance(domain, SimpleDomain):
                domains.append(cast(SimpleDomain, d2.get_component(component_number)))

        return CompositeDomain(domains)

    def index_of_element(self, element_to_find: DomainElement) -> int:
        i: int
        element: DomainElement

        for i, element in enumerate(self):
            if element == element_to_find:
                return i

        raise ElementNotFoundError(element_to_find)

    def element_for_index(self, index_to_find: int) -> DomainElement:
        if index_to_find < 0:
            raise IndexError("can't use negative index")

        i: int
        element: DomainElement
        for i, element in enumerate(self):
            if i == index_to_find:
                return element

        raise IndexError(f"domain element with index {index_to_find} not found")


@dataclasses.dataclass
class SimpleDomain(Domain):
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError("end index must be larger then start index")

    def get_cardinality(self) -> int:
        return self.end - self.start

    def get_component(self, _: int) -> DomainInterface:
        return self

    def get_number_of_components(self) -> int:
        return 1

    def index_of_element(self, element_to_find: DomainElement) -> int:
        return element_to_find.get_component_value(0) - self.start

    def element_for_index(self, index_to_find: int) -> DomainElement:
        return DomainElement.of(self.start + index_to_find)

    def __iter__(self) -> Iterator[DomainElement]:
        return SimpleDomainIterator(self.start, self.end, self.start)


@dataclasses.dataclass
class SimpleDomainIterator(Iterator[DomainElement]):
    _start: int
    _end: int
    _curr: int

    def __next__(self) -> DomainElement:
        if self._curr == self._end:
            raise StopIteration

        element = DomainElement((self._curr, ))
        self._curr += 1

        return element


@dataclasses.dataclass
class CompositeDomain(Domain):
    domains: List[SimpleDomain, ...]
    _product: Iterator[Tuple[int, ...]] = dataclasses.field(init=False)

    def get_cardinality(self) -> int:
        cardinality = 1

        for domain in self.domains:
            cardinality *= domain.get_cardinality()

        return cardinality

    def get_component(self, i: int) -> DomainInterface:
        if i < 0 or i >= len(self.domains):
            raise IndexError(f"index {i} out of range")

        return self.domains[i]

    def get_number_of_components(self) -> int:
        return len(self.domains)

    def __iter__(self) -> Iterator[DomainElement]:
        ranges: List[Iterable[int], ...] = []

        for domain in self.domains:
            ranges.append(range(domain.start, domain.end))

        return CompositeDomainIterator(itertools.product(*ranges))


@dataclasses.dataclass
class CompositeDomainIterator(Iterator[DomainElement]):
    _product: Iterator[Tuple[int, ...]]

    def __next__(self) -> DomainElement:
        return DomainElement(self._product.__next__())
