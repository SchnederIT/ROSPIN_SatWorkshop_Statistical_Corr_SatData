import cv2
import numpy as np

#====================================================================================
#   Calculates the absolute difference between the gradient of 2 input images.
#
#   Inputs:
#       bitmap1: The Infrared image (as a 2D array).
#       bitmap2: The Ultraviolet image.
#
#   Output:
#       A 2D NumPy array representing the differential dynamics image (a numpy array).
#====================================================================================

def gradient_difference(bitmap1: np.ndarray, bitmap2: np.ndarray) -> np.ndarray:

    if not isinstance(bitmap1, np.ndarray) or not isinstance(bitmap2, np.ndarray):
        bitmap1 = np.array(bitmap1, dtype = np.float64)
        bitmap2 = np.array(bitmap2, dtype = np.float64)

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
        255, # normalize to values in range [0 .. 255]
        cv2.NORM_MINMAX
    )
    
    return np.uint8(gradient_difference_normalized)

#====================================================================================

if __name__ == '__main__':
    # a dummy test
    from dummy_bitmaps import X, Y
    print(gradient_difference(X, Y))
