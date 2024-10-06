import cv2
import numpy as np
from skimage.segmentation import felzenszwalb
from skimage import io
from matplotlib import pyplot as plt

# Load the image
image_path = "0.jpeg"
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB as required by skimage

# Step 1: Preprocessing - Gaussian Blur to remove noise
blur = cv2.GaussianBlur(img_rgb, (5, 5), 0)

# Step 2: Edge Detection using Sobel or Canny (can try both and compare)
edges = cv2.Canny(blur, 100, 200)

# Step 3: Graph-based segmentation using Felzenszwalb's algorithm
segments = felzenszwalb(blur, scale=200, sigma=0.8, min_size=30)

# Step 4: Postprocessing - Morphological operations to clean up the segmentation
kernel = np.ones((3, 3), np.uint8)
segments_cleaned = cv2.morphologyEx(segments.astype(np.uint8), cv2.MORPH_CLOSE, kernel, iterations=2)

# Step 5: Optional - Overlay edges onto the segmented regions for clearer boundaries
overlay = cv2.addWeighted(img_rgb, 0.7, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB), 0.3, 0)

# Step 6: Visualization
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
plt.imshow(img_rgb)
plt.title("Original Image")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(blur)
plt.title("Blurred Image (Preprocessing)")
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(edges, cmap='gray')
plt.title("Edge Detection (Canny)")
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(segments, cmap='nipy_spectral')
plt.title("Graph-Based Segmentation")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(segments_cleaned, cmap='nipy_spectral')
plt.title("Cleaned Segmentation (Postprocessing)")
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(overlay)
plt.title("Overlay of Segments and Edges")
plt.axis("off")

plt.tight_layout()
plt.show()
