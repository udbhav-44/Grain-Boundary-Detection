import cv2 as cv
import numpy as np
import argparse

# Global variables
src = None
max_elem = 2
max_kernel_size = 21
title_trackbar_element_shape = 'Element:\n 0: Rect \n 1: Cross \n 2: Ellipse'
title_trackbar_kernel_size = 'Kernel size:\n 2n +1'
title_erosion_window = 'Erosion Demo'
title_dilation_window = 'Dilation Demo'

def main(image):
    global src
    src = cv.imread(cv.samples.findFile(image))
    if src is None:
        print('Could not open or find the image: ', image)
        exit(0)
    
    cv.namedWindow(title_erosion_window)
    cv.createTrackbar(title_trackbar_element_shape, title_erosion_window, 0, max_elem, erosion)
    cv.createTrackbar(title_trackbar_kernel_size, title_erosion_window, 0, max_kernel_size, erosion)
    
    cv.namedWindow(title_dilation_window)
    cv.createTrackbar(title_trackbar_element_shape, title_dilation_window, 0, max_elem, dilation)
    cv.createTrackbar(title_trackbar_kernel_size, title_dilation_window, 0, max_kernel_size, dilation)
    
    erosion(0)
    dilation(0)
    cv.waitKey()

def morph_shape(val):
    shapes = [cv.MORPH_RECT, cv.MORPH_CROSS, cv.MORPH_ELLIPSE]
    return shapes[val]

def check_kernel_size(size):
    max_size = 100
    if size < 0 or size > max_size:
        raise ValueError(f"Kernel size must be between 0 and {max_size}")

def apply_morphology(operation, window_title):
    kernel_size = cv.getTrackbarPos(title_trackbar_kernel_size, window_title)
    shape = morph_shape(cv.getTrackbarPos(title_trackbar_element_shape, window_title))
    
    try:
        check_kernel_size(kernel_size)
        element = cv.getStructuringElement(shape, (2 * kernel_size + 1, 2 * kernel_size + 1),
                                           (kernel_size, kernel_size))
        result = operation(src, element)
        cv.imshow(window_title, result)
        cv.imwrite(f"{window_title.lower().replace(' ', '_')}.png", result)
        cv.waitKey(1)
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Please adjust the kernel size using the trackbar for {window_title}.")
    except cv.error as e:
        print(f"OpenCV Error: {e}")
        print(f"An error occurred during the {window_title} operation.")

def erosion(val):
    apply_morphology(cv.erode, title_erosion_window)

def dilation(val):
    apply_morphology(cv.dilate, title_dilation_window)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code for Eroding and Dilating tutorial.')
    parser.add_argument('--input', help='Path to input image.', default='0.jpeg')
    args = parser.parse_args()
    
    try:
        main(args.input)
    except cv.error as e:
        print(f"OpenCV Error: {e}")
        print("Please check if the input image exists and is valid.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

 