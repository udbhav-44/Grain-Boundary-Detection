import cv2 as cv
import numpy as np

img = cv.imread("2.jpeg", cv.IMREAD_GRAYSCALE)
img_col = cv.cvtColor(img, cv.COLOR_GRAY2BGR) #convert the grey image to color by assigning the greyscale intensity values to B, G, and R components as well

ddepth = cv.CV_16S
scale = 1
delta = 0

cv.namedWindow("img", cv.WINDOW_NORMAL)
cv.createTrackbar("th", "img", 0, 255, lambda x:None)
cv.createTrackbar("ksize", "img", 1, 255, lambda x:None)
cv.createTrackbar("sigma", "img", 0, 1000, lambda x:None)


while(1):
    ksize = cv.getTrackbarPos('ksize', 'img')
    ksize += 1-ksize%2
    sigma = cv.getTrackbarPos('sigma', 'img')/10.0
    img_gb = cv.GaussianBlur(img, (ksize,ksize), sigma)
    img_gb = cv.fastNlMeansDenoising(img_gb)

    grad_x = cv.Sobel(img_gb, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(img_gb, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    th = cv.getTrackbarPos('th','img')
    if th!=0:
        _, grad = cv.threshold(grad, th, 255, cv.THRESH_BINARY)
    # if(sigma!=0):
    #     img_col[:,:,2] = grad
    #     cv.imshow('img',img_col)
    # else:
    cv.imshow("img", grad)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        cv.imwrite("sobel_res.png", grad)
        break
cv.destroyAllWindows()
