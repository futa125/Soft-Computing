from typing import TypeAlias, Callable

FloatBinaryFunction: TypeAlias = Callable[[float, float], float]


def zadeh_and() -> FloatBinaryFunction:
    return lambda x, y: min(x, y)


def zadeh_or() -> FloatBinaryFunction:
    return lambda x, y: max(x, y)


def hamacher_t_norm(value: float) -> FloatBinaryFunction:
    return lambda x, y: (x * y) / (value + (1 - value) * (x + y - x * y))


def hamacher_s_norm(value: float) -> FloatBinaryFunction:
    return lambda x, y: (x + y - (2 - value) * x * y) / (1 - (1 - value) * x * y)
