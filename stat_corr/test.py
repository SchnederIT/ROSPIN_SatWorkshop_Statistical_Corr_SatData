if __name__ == '__main__':
    
    from grad_analysis import gradient_difference
    import cv2

    try:
        # Load images as grayscale (0 flag)
        ir_img = cv2.imread('ir_image.tif', 0)
        uv_img = cv2.imread('uv_image.tif', 0)
        
        if ir_img is None or uv_img is None:
            raise FileNotFoundError("One or both image files not found or corrupted.")

        # Ensure images have the same dimensions before processing
        if ir_img.shape != uv_img.shape:
             raise ValueError("Input images must have the same dimensions.")
        
        # Call the function
        result_diff_image = gradient_difference(ir_img, uv_img)
        
        # Display the result (requires a GUI environment like a desktop or a notebook)
        cv2.imshow('Differential Dynamics Image (I_DIFF)', result_diff_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have valid image files named 'ir_image.tif' and 'uv_image.tif' in the same directory, and that you have installed opencv-python and numpy.")
        