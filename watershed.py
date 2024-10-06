import numpy as np
import cv2
# from main import apply_gaussian_blur , apply_erosion , apply_dilation , apply_canny_edge_detection 

image = cv2.imread('0.jpeg')

def watershed(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5,5), 2)

    # Threshold the image to get a binary image
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
   #noise removal
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

   #sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

   #Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

   #Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

   #Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

   #Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

   #Mark the region of unknown with zero
    markers[unknown==255] = 0   

    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255,0,0]

    return image

# blur = apply_gaussian_blur(image)
# eroded_image = apply_erosion(blur)
# dilated_image = apply_dilation(eroded_image)
# canny_image = apply_canny_edge_detection(dilated_image)

cv2.imshow('Watershed', watershed(image))
cv2.waitKey(0)

cv2.destroyAllWindows()




    