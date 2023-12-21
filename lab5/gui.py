import tkinter as tk
from typing import Optional, List

import numpy as np

from lab5.neural_network import NeuralNetwork
from lab5.symbol import Symbol


class DatasetWindow:
    def __init__(
            self,
            master: tk.Tk,
            symbol: Symbol,
            count: int = 20,
            representative_point_count: int = 50,
            dataset_folder: str = "dataset",
    ):
        self.master: tk.Tk = master
        self.master.title("Paint")

        self.canvas: tk.Canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.symbol: Symbol = symbol
        self.target_count: int = count
        self.current_count: int = 0

        self.label: tk.Label = tk.Label(
            master,
            text=f"Drawings: 1/{self.target_count}\nSymbol: {self.symbol}",
            font=("Helvetica", 18), background="white", foreground="black",
        )
        self.label.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)

        self.prev_x: Optional[int] = None
        self.prev_y: Optional[int] = None

        self.current_points: np.ndarray = np.empty(shape=(0, 2))
        self.all_points: List[np.ndarray] = []

        self.representative_point_count: int = representative_point_count
        self.dataset_folder: str = dataset_folder

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.clear_canvas)

    def paint(self, event: tk.Event) -> None:
        x: int
        y: int
        x, y = event.x, event.y

        self.current_points = np.vstack([self.current_points, np.array([x, y])])

        if self.prev_x is not None and self.prev_y is not None:
            self.canvas.create_line(
                self.prev_x, self.prev_y, x, y, width=4, fill="black", capstyle=tk.ROUND, smooth=tk.TRUE,
            )

        self.prev_x = x
        self.prev_y = y

    def clear_canvas(self, _: tk.Event) -> None:
        self.all_points.append(self.current_points)
        self.current_points = np.empty(shape=(0, 2))

        self.current_count += 1
        if self.current_count == self.target_count:
            dataset: List[np.ndarray] = []

            for points in self.all_points:
                transformed_points = transform_points(points, self.representative_point_count)
                dataset.append(transformed_points.flatten())

            np.savetxt(f"./{self.dataset_folder}/{self.symbol}.txt", dataset)

            return self.master.destroy()

        self.label.config(text=f"Drawings: {self.current_count + 1}/{self.target_count}\nSymbol: {self.symbol}")
        self.canvas.delete(tk.ALL)

        self.prev_x = None
        self.prev_y = None


class PredictionWindow:
    def __init__(self, master: tk.Tk, neural_network: NeuralNetwork, representative_point_count: int = 50):
        self.master: tk.Tk = master
        self.master.title("Paint")

        self.canvas: tk.Canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.current_count: int = 0

        self.label: tk.Label = tk.Label(
            master, text="", font=("Helvetica", 36), background="white", foreground="black",
        )
        self.label.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)

        self.prev_x: Optional[int] = None
        self.prev_y: Optional[int] = None

        self.points: np.ndarray = np.empty(shape=(0, 2))

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.clear_canvas)

        self.neural_network: NeuralNetwork = neural_network
        self.representative_point_count: int = representative_point_count

    def paint(self, event: tk.Event) -> None:
        x: int
        y: int
        x, y = event.x, event.y

        self.points = np.vstack([self.points, np.array([x, y])])

        if self.prev_x is not None and self.prev_y is not None:
            self.canvas.create_line(
                self.prev_x, self.prev_y, x, y, width=4, fill="black", capstyle=tk.ROUND, smooth=tk.TRUE,
            )

        self.prev_x = x
        self.prev_y = y

    def clear_canvas(self, _: tk.Event) -> None:
        transformed_points = transform_points(self.points, self.representative_point_count)
        self.points = np.empty(shape=(0, 2))

        out = self.neural_network.predict(transformed_points.flatten())

        self.label.config(text=f"{list(Symbol)[np.argmax(out)]}")
        self.canvas.delete(tk.ALL)

        self.prev_x = None
        self.prev_y = None


def transform_points(points: np.ndarray, representative_points_count: int) -> np.ndarray:
    x, y = points[:, 0], points[:, 1]

    x = x - np.mean(x)
    y = y - np.mean(y)

    mx = np.amax(np.abs(x))
    my = np.amax(np.abs(y))

    m = max(mx, my)

    x = x / m
    y = y / m

    distances_between_points = np.sqrt((np.diff(np.column_stack((x, y)), axis=0) ** 2).sum(axis=1))
    total_distance = distances_between_points.sum()

    distance_step = total_distance / (representative_points_count - 1)

    representative_x = np.array([x[0]])
    representative_y = np.array([y[0]])

    point_index = 0
    distance = distances_between_points[0]

    for i in range(1, representative_points_count - 1):
        k = i * distance_step
        while distance <= k:
            point_index += 1
            distance += distances_between_points[point_index]

        representative_x = np.append(representative_x, x[point_index])
        representative_y = np.append(representative_y, y[point_index])

    representative_x = np.append(representative_x, x[-1])
    representative_y = np.append(representative_y, y[-1])

    return np.column_stack((representative_x, representative_y))
