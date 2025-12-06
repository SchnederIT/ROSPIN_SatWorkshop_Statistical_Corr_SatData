import matplotlib.pyplot as plt
import numpy as np # Already imported, but good practice

def plot_matrix_color_scale(matrix: np.ndarray, title: str, cmap_name: str = 'viridis'):

    plt.figure(figsize=(8, 6)) 
    plt.imshow(matrix, cmap=cmap_name, interpolation='none')

    plt.colorbar(label='Intensity / Differential Value')

    plt.title(title)
    plt.xlabel("X-Coordinate (Column)")
    plt.ylabel("Y-Coordinate (Row)")
    
    plt.show()

# if __name__ == '__main__':
#     x, y = np.meshgrid(np.linspace(0, 10, 8), np.linspace(0, 10, 8))
#     dummy_data = np.sin(x) * np.cos(y) * 127 + 127
#     dummy_data = dummy_data.astype(np.uint8) # Convert to 0-255 scale
    
#     result_diff_image_array = dummy_data 

#     plot_matrix_color_scale(
#         result_diff_image_array, 
#         "Differential Dynamics Map (I_DIFF)", 
#         cmap_name='inferno'
#     )

#     plot_matrix_color_scale(
#         dummy_data, # Replace with your original IR map
#         "Original IR Map (Simulated)", 
#         cmap_name='gray'
#     )