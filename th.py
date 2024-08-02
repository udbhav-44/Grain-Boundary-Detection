import cv2 as cv
import numpy as np

img = cv.imread("1.jpeg", cv.IMREAD_GRAYSCALE)

cv.namedWindow("img", cv.WINDOW_NORMAL)
cv.resizeWindow("img", 1000, 800)
cv.createTrackbar("Th", "img", 0, 255, lambda x:None)
while(1):
    th = cv.getTrackbarPos('Th','img')
    _, img_th = cv.threshold(img, th, 255, cv.THRESH_BINARY)
    cv.imshow('img',img_th)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()