from enum import StrEnum

import numpy as np


class Symbol(StrEnum):
    ALPHA = "α"
    BETA = "β"
    GAMMA = "γ"
    DELTA = "δ"
    EPSILON = "ε"

    def one_hot_encode(self) -> np.ndarray:
        if self == Symbol.ALPHA:
            return np.array([1.0, 0.0, 0.0, 0.0, 0.0])

        if self == Symbol.BETA:
            return np.array([0.0, 1.0, 0.0, 0.0, 0.0])

        if self == Symbol.GAMMA:
            return np.array([0.0, 0.0, 1.0, 0.0, 0.0])

        if self == Symbol.DELTA:
            return np.array([0.0, 0.0, 0.0, 1.0, 0.0])

        if self == Symbol.EPSILON:
            return np.array([0.0, 0.0, 0.0, 0.0, 1.0])

        raise Exception("unknown symbol")
