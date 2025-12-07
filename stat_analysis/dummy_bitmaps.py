import numpy as np

L = 500
noise_intensity = 10

def generate_dummy_bitmaps(L: int):
    # Generates three L x L NumPy matrices (X, Y, Z) with distinct patterns
    # for testing gradient calculation and noise robustness

    if L < 5:
        L = 5
        
    # 1. Create coordinate grids (X_coord and Y_coord)
    # The 'linspace' creates L points between 0 and 1, used for grid coordinates.
    # The 'meshgrid' creates two 2D arrays representing the x and y coordinates 
    # at every point in the L x L grid.
    x_coords, y_coords = np.meshgrid(np.linspace(0, 1, L), np.linspace(0, 1, L))

    # --- Matrix X: Linear Diagonal Gradient (Simulates simple intensity slope) ---
    X = (x_coords + y_coords) * (255 / 2)
    
    # --- Matrix Y: Radial (Concentric) Gradient (Simulates a heat/pollution plume) ---
    center_x = x_coords - 0.5
    center_y = y_coords - 0.5
    distance_r = np.sqrt(center_x**2 + center_y**2)
    Y = (np.cos(0.5 * distance_r * 20) * 0.5 + 0.5) * 255
    
    # --- Matrix Z: Linear Gradient + High-Frequency Noise ---
    # Z = X.copy()
    # noise = np.random.normal(0, noise_intensity, size=(L, L))
    # Z += noise
    
    Z = 250 - (x_coords + y_coords) * (255 / 2)

    X = np.clip(X, 0, 255)
    Y = np.clip(Y, 0, 255)
    Z = np.clip(Z, 0, 255)
    
    return X.astype(np.float64), Y.astype(np.float64), Z.astype(np.float64)

X, Y, Z = generate_dummy_bitmaps(L) 

# if __name__ == '__main__':
    
#     X_matrix, Y_matrix, Z_matrix = generate_dummy_bitmaps(L)
    
#     print(f"--- Generated Dummy Matrices ({L}x{L}) ---")
#     print(f"X (Diagonal Gradient) Shape: {X_matrix.shape} | Mean: {X_matrix.mean():.2f}")
#     print(f"Y (Radial Gradient) Shape: {Y_matrix.shape} | Mean: {Y_matrix.mean():.2f}")
#     print(f"Z (Noisy Gradient) Shape: {Z_matrix.shape} | Mean: {Z_matrix.mean():.2f}")