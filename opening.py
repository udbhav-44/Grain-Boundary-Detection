import cv2 as cv
import numpy as np
from skimage.color import label2rgb

gseg=cv.ximgproc.segmentation.createGraphSegmentation()

img = cv.imread("0.jpeg", 0)
r,c = img.shape
color_dict = {}
img2 = img.copy()

img2 = cv.erode(img2, cv.getStructuringElement(cv.MORPH_CROSS, (3,3)))
img2 = cv.dilate(img, cv.getStructuringElement(cv.MORPH_CROSS, (3,3)))
# img2 = cv.erode(img, cv.getStructuringElement(cv.MORPH_CROSS, (3,3)))

cv.namedWindow("Graph cut", cv.WINDOW_GUI_NORMAL)
cv.createTrackbar("MinSize", "Graph cut", 100, 2000, lambda x:None)
cv.createTrackbar("ksize", "Graph cut", 1, 255, lambda x:None)
cv.createTrackbar("sigma", "Graph cut", 0, 1000, lambda x:None)
toggle = 'a'
old_MinSize = 0
old_ksize = 0
old_sigma=0
imgs = img.copy()
mask = np.ndarray(shape=(r,c,3), dtype=np.uint8)

while(1):
    ksize = cv.getTrackbarPos('ksize', "Graph cut")
    # ksize += 1-ksize%2
    sigma = cv.getTrackbarPos('sigma', "Graph cut")/10.0
    MinSize = cv.getTrackbarPos("MinSize", "Graph cut")

    # img_gb = cv.GaussianBlur(img, (ksize,ksize), sigma)

    if(ksize!=old_ksize or MinSize!=old_MinSize or old_sigma!=sigma):
        gseg.setK(ksize)
        gseg.setSigma(sigma)
        gseg.setMinSize(MinSize)
        imgs = gseg.processImage(img2).astype(int)
        r,c = imgs.shape
        mask = label2rgb(imgs, img)
        old_ksize = ksize
        old_sigma = sigma
        old_MinSize = MinSize

    # mask = cv.Canny(mask, 100, 200)
    # mask = cv.dilate(mask, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3)))

    # imgc = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    # imgc[mask!=0] = [0,0,255]
    
    if toggle == 'a':
        cv.imshow("Graph cut", mask)
    elif toggle == 's':
        cv.imshow("Graph cut", img)
    elif toggle == 'd':
        cv.imshow("Graph cut", img2)
    k = cv.waitKey(1) & 0xFF
    if k == 27:  ## Esc
        break
    else:
        toggle = chr(k)
cv.destroyAllWindows()


