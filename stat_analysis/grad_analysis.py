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
        2**8 - 1, # normalize to values in range [0 .. 2^bitNum - 1]
        cv2.NORM_MINMAX
    )
    
    return np.uint8(gradient_difference_normalized)

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

    # --- 1. Calculate Gradient Difference Results ---
    XYintegral = gradient_difference(X, Y)
    YZintegral = gradient_difference(Y, Z) # Ensure correct order if order matters
    XZintegral = gradient_difference(X, Z)

    # --- 2. Set up the 2x3 Figure and Axes ---
    fig, axes = plt.subplots(2, 3, figsize=(9, 6))
    # 'axes' is now a 2D NumPy array of subplots: [[ax00, ax01, ax02], [ax10, ax11, ax12]]

    # Flatten the axes array for easier iteration, or address them by index
    # axes[row, column]
    
    # --- 3. Define the Data and Titles for Plotting ---
    plots = [
        (X, "X (Diagonal)"),
        (Y, "Y (Radial)"),
        (Z, "Z"),
        (XYintegral, f"Diff XY (Mean: {XYintegral.mean():.2f})"),
        (YZintegral, f"Diff YZ (Mean: {YZintegral.mean():.2f})"),
        (XZintegral, f"Diff XZ (Mean: {XZintegral.mean():.2f})"),
    ]

    # --- 4. Loop through Data and Plot on Subplots ---
    for i, (matrix, title) in enumerate(plots):
        row = i // 3  # Integer division determines the row (0 or 1)
        col = i % 3   # Modulo determines the column (0, 1, or 2)
        ax = axes[row, col] # Select the current subplot axis
        
        # Plot the matrix using the 'viridis' colormap
        im = ax.imshow(matrix, cmap='viridis', origin='lower') # 'origin=lower' for standard math plots
        
        # Add the color bar specifically for this subplot
        # We create an instance of the colorbar next to the current axis (ax)
        plt.colorbar(im, ax=ax, label='Intensity / Differential Value', fraction=0.046, pad=0.04)
        
        # Set titles and labels
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("x (Column)")
        ax.set_ylabel("y (Row)")

    # Adjust layout to prevent plot titles and labels from overlapping
    plt.tight_layout()
    
    # Display the single figure containing all 6 plots
    plt.show()