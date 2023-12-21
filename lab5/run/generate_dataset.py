import tkinter as tk

from lab5.gui import DatasetWindow, Symbol


def generate_dataset(sym: Symbol, count: int = 20) -> None:
    root = tk.Tk()
    DatasetWindow(root, sym, count)
    root.mainloop()


if __name__ == "__main__":
    symbol: Symbol
    for symbol in Symbol:
        generate_dataset(symbol)
