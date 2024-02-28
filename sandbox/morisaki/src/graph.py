import csv
import numpy as np
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        pass

    def generate_heatmap(self, data, x_labels='', y_labels='', title=''):
        data_array = np.array(data)
        plt.figure(figsize=(8, 6))
        plt.imshow(data_array, cmap='Blues_r', interpolation='nearest')
        plt.colorbar(label='Value')
        plt.title(title)
        plt.xlabel(x_labels)
        plt.ylabel(y_labels)

        plt.xticks(np.arange(len(x_labels)), labels=x_labels, rotation=45, ha="right")
        plt.yticks(np.arange(len(y_labels)), labels=y_labels)

        for i in range(len(y_labels)):
            for j in range(len(x_labels)):
                plt.text(j, i, data[i, j], ha="center", va="center", color="w")

        plt.tight_layout()
        plt.show()