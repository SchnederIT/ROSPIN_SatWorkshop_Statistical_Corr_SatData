import cv2
import numpy as np

#====================================================================================
#   Calculates the absolute difference between the gradient of 2 input images.
#
#   Inputs: 2x 2D array
#
#   Output:
#       A 2D NumPy array representing the differential dynamics image (a numpy array).
#====================================================================================
def gradient_difference(bitmap1: np.ndarray, bitmap2: np.ndarray) -> np.ndarray:

    if not isinstance(bitmap1, np.ndarray) or not isinstance(bitmap2, np.ndarray):
        bitmap1 = np.array(bitmap1, dtype = np.float64)
        bitmap2 = np.array(bitmap2, dtype = np.float64)

    bitmap1 = np.array(bitmap1).astype(np.float64)
    bitmap2 = np.array(bitmap2).astype(np.float64)

    ddepth = cv2.CV_64F 
    
    grad_1_x = cv2.Sobel(bitmap1, ddepth, 1, 0, ksize=3) # dx=1, dy=0 (x-direction)
    grad_1_y = cv2.Sobel(bitmap1, ddepth, 0, 1, ksize=3) # dx=0, dy=1 (y-direction)
    
    grad_2_x = cv2.Sobel(bitmap2, ddepth, 1, 0, ksize=3)
    grad_2_y = cv2.Sobel(bitmap2, ddepth, 0, 1, ksize=3)
    
    amplitude_1 = cv2.magnitude(grad_1_x, grad_1_y)
    amplitude_2 = cv2.magnitude(grad_2_x, grad_2_y)

    gradient_difference = cv2.absdiff(amplitude_1, amplitude_2)
    
    gradient_difference_normalized = cv2.normalize(
        gradient_difference, 
        None, 
        0, 
        1, # normalize to values in range [0 .. 1]
        cv2.NORM_MINMAX
    )
    
    return np.float32(gradient_difference_normalized)

#====================================================================================
def calculate_spatial_correlation(bitmap_a: np.ndarray, bitmap_b: np.ndarray) -> float:

    matrix_a = np.array(bitmap_a).astype(np.float64)
    matrix_b = np.array(bitmap_b).astype(np.float64)
    
    if matrix_a.shape != matrix_b.shape:
        raise ValueError("Input bitmaps must have the exact same dimensions for correlation.")
        
    # 2. Flatten the 2D arrays into 1D vectors
    # Correlation functions work on vectors (series of measurements), so we treat
    # each pixel location as one sample point.
    vector_a = matrix_a.flatten()
    vector_b = matrix_b.flatten()
    
    # 3. Calculate the Correlation Matrix (inline method)
    # np.corrcoef(v1, v2) returns a 2x2 matrix:
    # [[ corr(v1, v1), corr(v1, v2) ],
    #  [ corr(v2, v1), corr(v2, v2) ]]
    correlation_matrix = np.corrcoef(vector_a, vector_b)
    
    # 4. Extract the Pearson Correlation Coefficient (the off-diagonal element)
    # The coefficient is located at index [0, 1] (or [1, 0]).
    correlation_coefficient = correlation_matrix[0, 1]
    
    return correlation_coefficient
#====================================================================================
def create_ratio_map(bitmap_a: np.ndarray, bitmap_b: np.ndarray) -> np.ndarray:
    A = np.array(bitmap_a).astype(np.float64)
    B = np.array(bitmap_b).astype(np.float64)

    # 1. Calculate the Ratio Index (similar to an EVI or simple ratio)
    # The output values will range from 0 to 1 (or close to it)
    # A small constant (epsilon) is added to the denominator to prevent division by zero.
    epsilon = 1e-8
    ratio_index = (A - B) / (A + B + epsilon) 

    normalized_map = cv2.normalize(
        ratio_index, 
        None, 
        0, 
        255, 
        cv2.NORM_MINMAX, 
        cv2.CV_8U # Return as 8-bit unsigned integer (bitmap)
    )
    return normalized_map

#====================================================================================
if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np

    def plot_matrix_color_scale(matrix: np.ndarray, title: str, cmap_name: str = 'viridis'): # plot style can be "inferno", "gray", ...

        plt.figure(figsize=(4, 3)) 
        plt.imshow(matrix, cmap=cmap_name, interpolation='none')

        plt.colorbar(label='Intensity / Differential Value')

        plt.title(title)
        plt.xlabel("X-Coordinate (Column)")
        plt.ylabel("Y-Coordinate (Row)")

    # a dummy test
    from dummy_bitmaps import X, Y, Z

    #  1. Calculate Gradient Difference Results 
    XYintegral = create_ratio_map(X, Y)
    YZintegral = create_ratio_map(Y, Z) # Ensure correct order if order matters
    XZintegral = create_ratio_map(X, Z)

    #  2. Set up the 2x3 Figure and Axes 
    fig, axes = plt.subplots(2, 3, figsize=(9, 6))

    #  3. Define the Data and Titles for Plotting 
    plots = [
        (X, "X (Diagonal)"),
        (Y, "Y (Radial)"),
        (Z, "Z"),
        (XYintegral, f"Diff XY (Mean: {XYintegral.mean():.2f})"),
        (YZintegral, f"Diff YZ (Mean: {YZintegral.mean():.2f})"),
        (XZintegral, f"Diff XZ (Mean: {XZintegral.mean():.2f})"),
    ]

    #  4. Loop through Data and Plot on Subplots 
    for i, (matrix, title) in enumerate(plots):
        row = i // 3  
        col = i % 3
        ax = axes[row, col] # Select the current subplot axis
        
        im = ax.imshow(matrix, cmap='viridis', origin='lower')

        plt.colorbar(im, ax=ax, label='Intensity / Differential Value', fraction=0.046, pad=0.04)
        
        # Set titles and labels
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("x (Column)")
        ax.set_ylabel("y (Row)")

    plt.tight_layout()
    plt.show()