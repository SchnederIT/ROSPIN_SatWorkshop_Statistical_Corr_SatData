import numpy as np

L = 500
noise_intensity = 30

def generate_dummy_bitmaps(L: int):

    if L < 50:
        L = 50

    x_coords, y_coords = np.meshgrid(np.linspace(0, 1, L), np.linspace(0, 1, L))

    # --- Matrix X: Linear Diagonal Gradient (Simulates simple intensity slope) ---
    X = (x_coords + y_coords) * (255 / 2)
    
    # --- Matrix Y: Radial (Concentric) Gradient (Simulates a heat/pollution plume) ---
    center_x = x_coords - 0.5
    center_y = y_coords - 0.5
    distance_r = np.sqrt(center_x**2 + center_y**2)
    Y = (np.cos(0.75 * distance_r * 20) * 0.5 + 0.5) * 255
    
    # --- Matrix Z: Linear Gradient + High-Frequency Noise ---
    Z = X.copy()
    noise = np.random.normal(0, noise_intensity, size=(L, L))
    Z += noise
    
    # Z = 250 - (x_coords + y_coords) * (255 / 2) # X in inverse direction 

    X = np.clip(X, 0, 255)
    Y = np.clip(Y, 0, 255)
    Z = np.clip(Z, 0, 255)
    
    return X.astype(np.float64), Y.astype(np.float64), Z.astype(np.float64)

X, Y, Z = generate_dummy_bitmaps(L)