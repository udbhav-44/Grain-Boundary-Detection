import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

img = cv.imread("0.jpeg", cv.IMREAD_GRAYSCALE)
img_gb = cv.GaussianBlur(img, (27,27),35)
y, x, _ = plt.hist(img_gb.flatten(), bins=100)
for i in range(1,99):
    if(y[i]>y[i-1]):
        img_gb[np.logical_and(img_gb>=x[i-1], img_gb<=x[i])] = (x[i]+x[i+1])/2

plt.figure()
y, x, _ = plt.hist(img_gb.flatten(), bins=100)
for i in range(1,99):
    if(y[i]<y[i-1]):
        img_gb[np.logical_and(img_gb>=x[i], img_gb<=x[i+1])] = (x[i]+x[i-1])/2

plt.figure()
plt.imshow(img_gb, cmap="gray")
plt.figure()
plt.hist(img_gb.flatten(), bins=100)
# plt.show()
cv.imwrite("5.png", img_gb)
