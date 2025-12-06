import matplotlib.pyplot as plt
import numpy as np

def plot_matrix_color_scale(matrix: np.ndarray, title: str, cmap_name: str = 'viridis'): # plot style can be "inferno", "gray", ...

    plt.figure(figsize=(8, 6)) 
    plt.imshow(matrix, cmap=cmap_name, interpolation='none')

    plt.colorbar(label='Intensity / Differential Value')

    plt.title(title)
    plt.xlabel("X-Coordinate (Column)")
    plt.ylabel("Y-Coordinate (Row)")
    
    # plt.show() # must be added after all windows definitions for multiple window show
