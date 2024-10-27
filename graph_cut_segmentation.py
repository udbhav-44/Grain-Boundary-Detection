import cv2
import numpy as np
from skimage.segmentation import felzenszwalb
from skimage.color import label2rgb

def graph_cut_segment(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(img_rgb, (5, 5), 0)
    
    # Apply morphological operations with elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    eroded = cv2.erode(blurred, kernel, iterations=1)
    dilated = cv2.dilate(eroded, kernel, iterations=1)
    
    # Apply Felzenszwalb segmentation
    segments = felzenszwalb(dilated, scale=100, sigma=0.5, min_size=50)
    
    # Create colored segmentation
    segmented = label2rgb(segments, img_rgb, kind='avg')
    
    # Convert back to BGR for OpenCV
    segmented_bgr = cv2.cvtColor(np.uint8(segmented*255), cv2.COLOR_RGB2BGR)
    
    # Enhance edges
    edges = cv2.Canny(cv2.cvtColor(segmented_bgr, cv2.COLOR_BGR2GRAY), 50, 150)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Overlay edges on segmented image
    result = cv2.addWeighted(segmented_bgr, 0.7, edges_colored, 0.3, 0)
    
    return result

if __name__ == "__main__":
    # Process image
    result = graph_cut_segment('0.jpeg')
    
    # Display results
    cv2.imshow('Original', cv2.imread('0.jpeg'))
    cv2.imshow('Graph Cut Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save result
    cv2.imwrite('graph_cut_result.png', result)
