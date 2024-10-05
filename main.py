import cv2
import numpy as np
import os
from datetime import datetime
##################################
# Work Update :
# Grayscale
# Gaussian Blur (dynamic kernel size and sigma)
# Morphological Operations (dynamic kernel size and iterations)

##################################

# Load the image
image = cv2.imread('0.jpeg')

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Create a window to control the Gaussian Blur
cv2.namedWindow('Gaussian Blur')
cv2.namedWindow('Morphological Operations')
cv2.createTrackbar('Kernel Size', 'Gaussian Blur', 5, 25, lambda x: None)
cv2.createTrackbar('Sigma', 'Gaussian Blur', 0, 1000, lambda x: None)
cv2.createTrackbar('Kernel for Erosion Operation', 'Morphological Operations', 5, 25, lambda x: None)
cv2.createTrackbar('Iterations for Erosion Operation', 'Morphological Operations', 1, 10, lambda x: None)
cv2.createTrackbar('Kernel for Dilation Operation', 'Morphological Operations', 5, 25, lambda x: None)
cv2.createTrackbar('Iterations for Dilation Operation', 'Morphological Operations', 1, 10, lambda x: None)

gray_image = convert_to_grayscale(image)

def apply_gaussian_blur(image):
    
    kernel_size = cv2.getTrackbarPos('Kernel Size', 'Gaussian Blur')
    sigma = cv2.getTrackbarPos('Sigma', 'Gaussian Blur')
    
    # Ensure kernel size is odd and at least 1
    kernel_size = max(1, kernel_size)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Create a tuple for kernel size
    kernel_size = (kernel_size, kernel_size)
    sigma = max(0, sigma)
    
    return cv2.GaussianBlur(image, kernel_size, sigma)


#Morphological Operations
# Type of kernel : Rectangular (can be changed to elliptical or cross shaped)
def apply_erosion(image):
    kernel_size = cv2.getTrackbarPos('Kernel for Erosion Operation', 'Morphological Operations')
    iterations = cv2.getTrackbarPos('Iterations for Erosion Operation', 'Morphological Operations')
    
    kernel_size = max(1, kernel_size)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def apply_dilation(image):
    kernel_size = cv2.getTrackbarPos('Kernel for Dilation Operation', 'Morphological Operations')
    iterations = cv2.getTrackbarPos('Iterations for Dilation Operation', 'Morphological Operations')
    
    kernel_size = max(1, kernel_size)
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)
    

# Create a window to control the Canny Edge Detection
cv2.namedWindow('Canny Edge Detection')
cv2.createTrackbar('Threshold 1', 'Canny Edge Detection', 100, 1000, lambda x: None)
cv2.createTrackbar('Threshold 2', 'Canny Edge Detection', 200, 1000, lambda x: None)

def apply_canny_edge_detection(image):
    threshold1 = cv2.getTrackbarPos('Threshold 1', 'Canny Edge Detection')
    threshold2 = cv2.getTrackbarPos('Threshold 2', 'Canny Edge Detection')
    return cv2.Canny(image, threshold1, threshold2)




while True:
    # Apply Gaussian blur with current trackbar settings
    blurred_image = apply_gaussian_blur(gray_image)
    eroded_image = apply_erosion(blurred_image)
    dilated_image = apply_dilation(eroded_image)
    
    canny_image = apply_canny_edge_detection(dilated_image)
    cv2.imshow('Dilation', canny_image)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        #create a folder to store the images
        os.makedirs('results', exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(f'results/results_{timestamp}')
        
        cv2.imwrite(f'results/results_{timestamp}/dilated_image.png', dilated_image)
        cv2.imwrite(f'results/results_{timestamp}/eroded_image.png', eroded_image)
        cv2.imwrite(f'results/results_{timestamp}/blurred_image.png', blurred_image)
        cv2.imwrite(f'results/results_{timestamp}/gray_image.png', gray_image)
        cv2.imwrite(f'results/results_{timestamp}/original_image.png', image)
        cv2.imwrite(f'results/results_{timestamp}/canny_image.png', canny_image)
        print("Images saved successfully.")
        # save the values of the trackbars in a text file with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f"results/results_{timestamp}/trackbar_values.txt", "w") as f:
            f.write(f"Kernel Size: {cv2.getTrackbarPos('Kernel Size', 'Gaussian Blur')}\n")
            f.write(f"Sigma: {cv2.getTrackbarPos('Sigma', 'Gaussian Blur')}\n")
            f.write(f"Kernel for Erosion Operation: {cv2.getTrackbarPos('Kernel for Erosion Operation', 'Morphological Operations')}\n")
            f.write(f"Iterations for Erosion Operation: {cv2.getTrackbarPos('Iterations for Erosion Operation', 'Morphological Operations')}\n")
            f.write(f"Kernel for Dilation Operation: {cv2.getTrackbarPos('Kernel for Dilation Operation', 'Morphological Operations')}\n")
            f.write(f"Iterations for Dilation Operation: {cv2.getTrackbarPos('Iterations for Dilation Operation', 'Morphological Operations')}\n")
            f.write(f"Threshold 1: {cv2.getTrackbarPos('Threshold 1', 'Canny Edge Detection')}\n")
            f.write(f"Threshold 2: {cv2.getTrackbarPos('Threshold 2', 'Canny Edge Detection')}\n")
        break

cv2.destroyAllWindows()




