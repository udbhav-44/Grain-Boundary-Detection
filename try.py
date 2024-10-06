import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the image
image_path = "0.jpeg"
img = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a Gaussian Blur to reduce noise and improve thresholding
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Adaptive thresholding to handle different lighting conditions
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 2)

# Remove small noise through morphological operations (opening)
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# Dilate to get sure background area
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Distance transform to get sure foreground area (grains)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# Finding unknown region (those areas that are neither sure foreground nor background)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

# Marker labelling
_, markers = cv2.connectedComponents(sure_fg)

# Add one to all markers to ensure the background is not marked as zero
markers = markers + 1

# Mark the unknown region with zero
markers[unknown == 0] = 0

# Apply the Watershed algorithm
markers = cv2.watershed(img, markers)

# Mark the boundaries of the segmented regions
img[markers == -1] = [255, 0, 0]

# Display the original and segmented images side by side
plt.figure(figsize=(10, 10))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Segmented Image with Grain Boundaries')
plt.axis('off')

plt.show()
