import operator
from enum import StrEnum, auto
from typing import Tuple, List, Iterable, Any, Callable

import numpy as np

first: Callable[[Iterable], Any] = operator.itemgetter(0)
last: Callable[[Iterable], Any] = operator.itemgetter(-1)


class LearningAlgorithm(StrEnum):
    BACKPROPAGATION = auto()
    STOCHASTIC_BACKPROPAGATION = auto()
    MINI_BATCH_BACKPROPAGATION = auto()


class NeuralNetwork:
    def __init__(self, layers=(100, 50, 25, 5), learning_rate=0.1):
        self.layers: Tuple[int] = layers
        self.layer_count: int = len(layers)

        self.weights: List[np.ndarray] = []
        self.outputs: List[np.ndarray] = []
        self.gradients: List[np.ndarray] = []

        self.learning_rate = learning_rate

        for i in range(self.layer_count - 1):
            self.weights.append(np.random.uniform(-0.1, +0.1, (self.layers[i + 1], self.layers[i])))

    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        return x * (1 - x)

    def forward_pass(self, x):
        self.outputs = []
        network_output = x.copy()

        for weight in self.weights:
            network_output = self.sigmoid(np.dot(weight, network_output))
            self.outputs.append(network_output)

    def backward_pass(self, x, y: np.ndarray):
        self.gradients: List[np.ndarray] = []

        err: np.ndarray = (last(self.outputs) - y) * self.sigmoid_derivative(last(self.outputs))
        errors: List[np.ndarray] = [err]

        for i in reversed(range(len(self.weights) - 1)):
            err = (np.dot(self.weights[i + 1].T, first(errors))) * (self.sigmoid_derivative(self.outputs[i]))
            errors = [err] + errors

        err, *errors = errors
        self.gradients.append(np.dot(err, x.T))

        for error, output in zip(errors, self.outputs):
            self.gradients.append(np.dot(error, output.T))

    def update_weights(self):
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * self.gradients[i]

    def predict(self, x: np.ndarray) -> np.ndarray:
        self.forward_pass(x)

        return self.outputs[-1]

    def train(self, x: np.ndarray, y: np.ndarray, epochs: int, epsilon: float, alg: LearningAlgorithm, ) -> None:
        _, num_samples = x.shape
        p = np.random.permutation(num_samples)
        x = x[:, p]
        y = y[:, p]

        print_frequency: int
        for epoch in range(1, epochs + 1):
            if alg == LearningAlgorithm.BACKPROPAGATION:
                print_frequency = 1000

                self._train(x, y)
            elif alg == LearningAlgorithm.STOCHASTIC_BACKPROPAGATION:
                print_frequency = 10

                for i, (x_column, y_column) in enumerate(zip(x.T, y.T)):
                    x_train = np.zeros_like(x)
                    x_train[:, i] = x_column

                    y_train = np.zeros_like(y)
                    y_train[:, i] = y_column

                    self._train(x_train, y_train)
            elif alg == LearningAlgorithm.MINI_BATCH_BACKPROPAGATION:
                print_frequency = 200
                batch_size = 20

                x_train = np.zeros_like(x)
                y_train = np.zeros_like(y)
                for i, (x_column, y_column) in enumerate(zip(x.T, y.T)):
                    x_train[:, i] = x_column
                    y_train[:, i] = y_column

                    if (i + 1) % batch_size == 0:
                        self._train(x_train, y_train)
                        x_train = np.zeros_like(x)
                        y_train = np.zeros_like(y)
            else:
                raise Exception("unknown learning algorithm")

            loss = np.mean((self.predict(x) - y) ** 2)
            if loss < epsilon:
                print(f"Epoch {epoch}: Loss = {loss}")
                break

            if epoch == 1 or epoch % print_frequency == 0 or epoch == epochs:
                print(f"Epoch {epoch}: Loss = {loss}")

    def _train(self, x: np.ndarray, y: np.ndarray):
        self.forward_pass(x)
        self.backward_pass(x, y)
        self.update_weights()
