import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

img = cv.imread("5.png", cv.IMREAD_GRAYSCALE)
img_col = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

cv.namedWindow("img", cv.WINDOW_NORMAL)
cv.resizeWindow("img", 1000, 800)
cv.createTrackbar("Th", "img", 0, 255, lambda x:None)
cv.createTrackbar("Th1", "img", 0, 255, lambda x:None)
cv.createTrackbar("Th2", "img", 0, 255, lambda x:None)

cv.createTrackbar("ksize", "img", 1, 100, lambda x:None)
cv.createTrackbar("sigma", "img", 1, 100, lambda x:None)
toggle = 0
count = 1
seg = np.zeros_like(img)
while(1):
    ksize = cv.getTrackbarPos('ksize', 'img')
    ksize += 1-ksize%2
    sigma = cv.getTrackbarPos('sigma', 'img')/10.0
    img_gb = cv.GaussianBlur(img, [ksize,ksize], sigma)
    img_gb = cv.GaussianBlur(img, [ksize,ksize], sigma)
    img_gb = cv.GaussianBlur(img, [ksize,ksize], sigma)
    img_gb = cv.GaussianBlur(img, [ksize,ksize], sigma)

    th = cv.getTrackbarPos('Th','img')
    # _, img_th = cv.threshold(img_gb, th, 255, cv.THRESH_BINARY)
    # _, img_th = cv.threshold(img_gb, th, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV)
    th1 = cv.getTrackbarPos('Th1','img')
    th2 = cv.getTrackbarPos('Th2','img')

    can = cv.Canny(img_gb, th1, th2)

    
    # sob = cv.Sobel(img_gb, )
    can = cv.cvtColor(can, cv.COLOR_GRAY2BGR)
    can[:,:,[0,2]]=0
    if toggle=='a':
        cv.imshow('img',cv.addWeighted(can, 1, img_col, 1, 0))
    elif toggle=='s':
        cv.imshow('img', can)
    elif toggle=='d':
        cv.imshow('img',cv.addWeighted(can, 1, cv.cvtColor(img_gb, cv.COLOR_GRAY2BGR), 1, 0))
    else:
        cv.imshow('img', img_gb)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    if(k==ord('a')):
        toggle = 'a'
    if(k==ord('s')):
        toggle = 's'
    if(k==ord('d')):
        toggle = 'd'
    if(k==ord('w')):
        toggle = 'w'
    #if(k==ord(' ')):
        #seg[np.logical_and(seg==0,img_th==0)] = count
        #count += 1
cv.destroyAllWindows()
#plt.imshow(seg)
#plt.show()
