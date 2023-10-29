from typing import TypeAlias, Callable

IntUnaryFunction: TypeAlias = Callable[[int], float]
FloatUnaryFunction: TypeAlias = Callable[[float], float]


def l_function(alpha: int, beta: int) -> IntUnaryFunction:
    def _l_function(value: int) -> float:
        if value < alpha:
            return 1

        if value >= beta:
            return 0

        return (beta - value) / (beta - alpha)

    return _l_function


def gamma_function(alpha: int, beta: int) -> IntUnaryFunction:
    def _gamma_function(value: int) -> float:
        if value < alpha:
            return 0

        if value >= beta:
            return 1

        return (value - alpha) / (beta - alpha)

    return _gamma_function


def lambda_function(alpha: int, beta: int, gamma: int) -> IntUnaryFunction:
    def _lambda_function(value: int) -> float:
        if value < alpha:
            return 0

        if value >= gamma:
            return 0

        if alpha <= value < beta:
            return (value - alpha) / (beta - alpha)

        return (gamma - value) / (gamma - beta)

    return _lambda_function


def zadeh_not() -> FloatUnaryFunction:
    return lambda x: 1 - x
