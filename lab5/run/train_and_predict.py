import tkinter as tk

import numpy as np

from lab5.gui import Symbol, PredictionWindow
from lab5.neural_network import NeuralNetwork, LearningAlgorithm


def train_and_predict() -> None:
    dataset_alpha = np.loadtxt("./run/dataset/α.txt").T
    dataset_beta = np.loadtxt("./run/dataset/β.txt").T
    dataset_gamma = np.loadtxt("./run/dataset/γ.txt").T
    dataset_delta = np.loadtxt("./run/dataset/δ.txt").T
    dataset_epsilon = np.loadtxt("./run/dataset/ε.txt").T

    combined_dataset = np.append(dataset_alpha, dataset_beta, axis=1)
    combined_dataset = np.append(combined_dataset, dataset_gamma, axis=1)
    combined_dataset = np.append(combined_dataset, dataset_delta, axis=1)
    combined_dataset = np.append(combined_dataset, dataset_epsilon, axis=1)

    y = np.tile(Symbol.ALPHA.one_hot_encode(), (dataset_alpha.shape[1], 1)).T
    y = np.append(y, np.tile(Symbol.BETA.one_hot_encode(), (dataset_beta.shape[1], 1)).T, axis=1)
    y = np.append(y, np.tile(Symbol.GAMMA.one_hot_encode(), (dataset_gamma.shape[1], 1)).T, axis=1)
    y = np.append(y, np.tile(Symbol.DELTA.one_hot_encode(), (dataset_delta.shape[1], 1)).T, axis=1)
    y = np.append(y, np.tile(Symbol.EPSILON.one_hot_encode(), (dataset_epsilon.shape[1], 1)).T, axis=1)

    nn = NeuralNetwork(learning_rate=0.1)
    nn.train(combined_dataset, y, epochs=100000, epsilon=10e-6, alg=LearningAlgorithm.BACKPROPAGATION)

    root = tk.Tk()
    PredictionWindow(root, nn)
    root.mainloop()


if __name__ == "__main__":
    train_and_predict()
