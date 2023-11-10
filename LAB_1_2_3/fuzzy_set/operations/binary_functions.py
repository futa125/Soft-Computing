from typing import TypeAlias, Callable

import numba

FloatBinaryFunction: TypeAlias = Callable[[float, float], float]


@numba.njit
def zadeh_and() -> FloatBinaryFunction:
    return lambda x, y: min(x, y)


@numba.njit
def zadeh_or() -> FloatBinaryFunction:
    return lambda x, y: max(x, y)


@numba.njit
def hamacher_t_norm(value: float) -> FloatBinaryFunction:
    return lambda x, y: (x * y) / (value + (1 - value) * (x + y - x * y))


@numba.njit
def hamacher_s_norm(value: float) -> FloatBinaryFunction:
    return lambda x, y: (x + y - (2 - value) * x * y) / (1 - (1 - value) * x * y)
