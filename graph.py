import cv2 as cv
import numpy as np

# explain the code
# 1. Load the image
# 2. Apply Gaussian Blur to the image
# 3. Create a GraphSegmentation object


# Create Graph Segementation Object
gseg=cv.ximgproc.segmentation.createGraphSegmentation() #

# Load the image
img = cv.imread("0.jpeg", 0)

# Blurring the img using Gaussian Blur
img = cv.GaussianBlur(img, (3,3), 0)

# Segment an image and store output in dst.
imgs = gseg.processImage(img).astype(int)
# img = cv.Canny(img, 100, 255)
r,c = imgs.shape

# Generating Mask for the image using segments
mask = np.ndarray(shape=(r,c,3), dtype=np.uint8)
color_dict = {}
for i in range(r):
    for j in range(c):
        if imgs[i,j] not in color_dict:
            color_dict[imgs[i,j]] = (255*np.random.rand(1,3)).astype(np.uint8)
        mask[i,j] = color_dict[imgs[i,j]]



cv.namedWindow("Graph cut", cv.WINDOW_GUI_NORMAL)
cv.createTrackbar("ksize", "Graph cut", 1, 255, lambda x:None)
cv.createTrackbar("sigma", "Graph cut", 0, 1000, lambda x:None)

while(1):
    ksize = cv.getTrackbarPos('ksize', "Graph cut")
    ksize += 1-ksize%2
    sigma = cv.getTrackbarPos('sigma', "Graph cut")/10.0

    img_gb = cv.GaussianBlur(img, (ksize,ksize), sigma)
    imgs = gseg.processImage(img_gb).astype(int)
    r,c = imgs.shape

    mask = np.ndarray(shape=(r,c,3), dtype=np.uint8)
    for i in range(r):
        for j in range(c):
            if imgs[i,j] not in color_dict:
                color_dict[imgs[i,j]] = (255*np.random.rand(1,3)).astype(np.uint8)
            mask[i,j] = color_dict[imgs[i,j]]

    # mask = cv.Canny(mask, 100, 200)
    # mask = cv.dilate(mask, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3)))

    # imgc = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    # imgc[mask!=0] = [0,0,255]

    cv.imshow("Graph cut", mask)
    cv.imwrite("segmented.png", mask)
    k = cv.waitKey(1) & 0xFF
    if k == 27:  ## Esc
        break
cv.destroyAllWindows()


