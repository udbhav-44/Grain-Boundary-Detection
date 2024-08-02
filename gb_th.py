import cv2 as cv
import numpy as np

img = cv.imread("0.jpeg", cv.IMREAD_GRAYSCALE)

cv.namedWindow("img", cv.WINDOW_NORMAL)
cv.resizeWindow("img", 1000, 800)
cv.createTrackbar("Th", "img", 0, 255, lambda x:None)
cv.createTrackbar("ksize", "img", 1, 100, lambda x:None)
cv.createTrackbar("sigma", "img", 1, 100, lambda x:None)

while(1):
    ksize = cv.getTrackbarPos('ksize', 'img')
    ksize += 1-ksize%2
    sigma = cv.getTrackbarPos('sigma', 'img')/10.0
    img_gb = cv.GaussianBlur(img, [ksize,ksize], sigma)
    # th = cv.getTrackbarPos('Th','img')
    # _, img_th = cv.threshold(img_gb, th, 255, cv.THRESH_BINARY)
    cv.imshow('img',img_gb)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
