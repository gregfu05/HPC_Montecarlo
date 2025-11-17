import json
import os

import matplotlib.pyplot as plt


def save_plot(x, y, xlabel, ylabel, title, fname):
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    directory = os.path.dirname(fname)
    if directory:
        os.makedirs(directory, exist_ok=True)
    plt.savefig(fname)
    plt.close()


def load_json(fname):
    with open(fname, "r", encoding="utf-8") as fh:
        return json.load(fh)
