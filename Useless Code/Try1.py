# To Perform Grain Boundary Detection

# ## 1. Grain Boundary Detection
# 1. Gray Scale Conversion
# 2. Gaussian Blur
# 3. Graph Segmentation
# 4. Color Mapping
# 5. Edge Detection
# 6. Morphological Operations
# 7. Overlaying Edges

# 1. Gray Scale Conversion

import cv2
import numpy as np

# Load the image
image = cv2.imread('0.jpeg')

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# 2. Gaussian Blur

# Apply Gaussian blur to the grayscale image
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# 3. Graph Segmentation
#segmented_image = cv2.ximgproc.segmentation.createGraphSegmentation(blurred_image)
#TypeError: Argument 'sigma' can not be treated as a double
# Apply graph segmentation to the blurred image
segmenter = cv2.ximgproc.segmentation.createGraphSegmentation(sigma=0.5, k=100, min_size=5000)
segmented_image = segmenter.processImage(blurred_image)

# Convert the segmented image to a suitable format for display
segmented_display = cv2.normalize(segmented_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Apply color mapping to the segmented image for better visualization
color_mapped = cv2.applyColorMap(segmented_display, cv2.COLORMAP_JET)

# 4. Color Mapping (already done in the previous step)

# 5. Edge Detection
edges = cv2.Canny(segmented_display, 100, 200)

# 6. Morphological Operations
kernel = np.ones((3,3), np.uint8)
dilated_edges = cv2.dilate(edges, kernel, iterations=1)

# 7. Overlaying Edges
result = cv2.addWeighted(image, 0.7, cv2.cvtColor(dilated_edges, cv2.COLOR_GRAY2BGR), 0.3, 0)

# Update the segmented_image variable to use the color-mapped version for display
segmented_image = color_mapped

# Save the processed images
cv2.imwrite('segmented_image.png', segmented_image)
cv2.imwrite('edges.png', edges)
cv2.imwrite('result.png', result)

# Display the images
cv2.imshow('Segmented Image', segmented_image)
cv2.imshow('Edges', edges)
cv2.imshow('Result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()

