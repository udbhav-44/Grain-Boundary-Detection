import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('0.jpeg', cv.IMREAD_GRAYSCALE) #reads the original image, image converted to a single channel greyscale image
# _,img = cv.threshold(img, 155, 255, cv.THRESH_BINARY)

dft = cv.dft(np.float32(img),flags = cv.DFT_COMPLEX_OUTPUT) #discrete fourier transform of the image, to smoothen the image, DFT_COMPLEX: forward transformation of an array to get the 2D array with the real and complex components
dft_shift = np.fft.fftshift(dft) #shift the 0 frequency component to the centre of the spectrum
magnitude_spectrum = cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]) #calculate the magnitude of the pixel?
#plt.imshow(magnitude_spectrum, cmap = 'grey')
#plt.show()
mask = magnitude_spectrum>np.max(magnitude_spectrum)/3	#filter out all pixels with mag > maximum_mag/3 (Why 1/3?) (boolean condition)
# magnitude_spectrum[mask] = 0
#plt.imshow(mask, cmap = 'grey')
#plt.show()
fshift = dft_shift.copy() #copy the contents of dft_shift array
fshift2 = dft_shift.copy() #copy the contents of dft_shift array

#print(mask)
#plt.imshow(mask, cmap="gray")
#plt.show()

fshift[mask] = 0 #intensity value assigned to mask as 0?
f_ishift = np.fft.ifftshift(fshift) #inverse of the fftshift
img_back = cv.idft(f_ishift) #inverse discrete fourier transform of a 1D or 2D array
img_back = cv.magnitude(img_back[:,:,0],img_back[:,:,1]) #magnitude of each element of the 2D array

f_ishift2 = np.fft.ifftshift(fshift2)
img_back2 = cv.idft(f_ishift2)
img_back2 = cv.magnitude(img_back2[:,:,0],img_back2[:,:,1])
plt.imshow(img_back, cmap="gray")
plt.imsave("2.jpeg", img_back, cmap="gray")
plt.figure()
plt.imshow(img_back2, cmap="gray")
plt.show()

# rows, cols = img.shape

# cv.namedWindow("img", cv.WINDOW_NORMAL)
# cv.resizeWindow("img", 500, 300)

# cv.namedWindow("img1", cv.WINDOW_NORMAL)
# cv.resizeWindow("img1", 500, 300)

# cv.namedWindow("mask", cv.WINDOW_NORMAL)
# cv.resizeWindow("mask", 500, 300)

# cv.createTrackbar("Th", "img1", 0, min(rows,cols), lambda x:None)

# def get_mask(rows, cols, r):
#     mask = np.zeros((rows,cols,2), np.uint8)
#     rrows = rows//2
#     rcols = cols//2
#     for i in range(rows):
#         I = i-rrows
#         for j in range(cols):
#             J = j-rcols
#             if I*I+J*J<=r*r:
#                 mask[i,j,:] = 1
#     return mask
# flag =1

# while(1):
#     th1 = cv.getTrackbarPos('Th','img1')
#     mask = get_mask(rows, cols, th1)

#     fshift = dft_shift*mask
#     f_ishift = np.fft.ifftshift(fshift)
#     img_back = cv.idft(f_ishift)
#     img_back = cv.magnitude(img_back[:,:,0],img_back[:,:,1])
    
#     cv.imshow("img", img)
#     cv.imshow("img1", img_back)
#     cv.imshow("mask", 255*mask[:,:,0])

#     k = cv.waitKey(1) & 0xFF
#     if k == 27:
#         break
