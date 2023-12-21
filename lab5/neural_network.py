from typing import Tuple, List

import numpy as np


class NeuralNetwork:
    def __init__(self, layers=(100, 64, 32, 16, 5), learning_rate=0.1):
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
        self.gradients = []

        errors: List[np.ndarray] = [np.zeros([])] * (len(self.weights) - 1)
        errors.append((self.outputs[-1] - y) * self.sigmoid_derivative(self.outputs[-1]))

        for idx in reversed(range(len(errors) - 1)):
            errors[idx] = ((np.dot(self.weights[idx + 1].T, errors[idx + 1]))
                           * (self.sigmoid_derivative(self.outputs[idx])))

        self.gradients.append(np.dot(errors[0], x.T))

        for error, output in zip(errors[1:], self.outputs):
            self.gradients.append(np.dot(error, output.T))

    def update_weights(self):
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * self.gradients[i]

    def predict(self, x: np.ndarray) -> np.ndarray:
        self.forward_pass(x)

        return self.outputs[-1]

    def train(self, num_epochs, x: np.ndarray, y: np.ndarray):
        for epoch in range(num_epochs):
            self.forward_pass(x)
            self.backward_pass(x, y)
            self.update_weights()

            if epoch % 10000 == 0 or epoch == num_epochs - 1:
                mse_loss = np.mean((self.predict(x) - y) ** 2)
                print(f"Epoch {epoch}: MSE loss = {mse_loss}")
