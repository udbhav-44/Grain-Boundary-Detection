import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

for all_image in range(1, 38):
	original_image = str(all_image)+'.jpg'
	gseg=cv.ximgproc.segmentation.createGraphSegmentation()

	img = cv.imread(original_image, 0)
	img = cv.GaussianBlur(img, (3,3), 0)
	imgs = gseg.processImage(img).astype(int)
	# img = cv.Canny(img, 100, 255)
	r,c = imgs.shape

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
	#plt.plot(mask)
	#plt.show()
	segmented = str(all_image)+"_seg.png"
	cv.imwrite(segmented, mask)
	k = cv.waitKey(1) #& 0xFF
	if k == 27:  ## Esc
		break
	cv.destroyAllWindows()
	#print(segmented, " done")
	
	
	img_seg = cv.imread(segmented, cv.IMREAD_COLOR)
	img_org = cv.imread(original_image, cv.IMREAD_COLOR)
	img_blank = np.zeros((r,c,3))
	for i in range(len(img_blank)):
		for j in range(len(img_blank[0])):
			for k in range(len(img_blank[0][0])):
				img_blank[i][j][k] = 255

	#print(img)
	#print(len(img))
	#print(len(img[0]))
	#print(len(img[0][0]))

	#for i in range(len(img)):
	#	for j in range(len(img[0])):
	#		if i==100:
	#			img_org[i][j][0] = 0
	#			img_org[i][j][1] = 0
	#			img_org[i][i][2] = 255

	#cv.imshow("Image", img_org)
	#cv.waitKey(0)
	
	red = [0,0,255]
	red = np.array(red)

	def redify(array1, x, y):
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				array1[x+i][y+i] = red
	

	for i in range(len(img_seg)-1):
		for j in range(len(img_seg[0])-1):
			for k in [-1, 1]:
				compare = img_seg[i][j] == img_seg[i+k][j]
				if compare.all() == False:
					redify(img_org, i, j)
					redify(img_blank, i, j)
				compare = img_seg[i][j] == img_seg[i][j+k]
				if compare.all() == False:
					redify(img_org, i, j)
					redify(img_blank, i, j)
			
	#cv.imshow("Image", img_org)
	graph_cut_blank = str(segmented)+"_cut_blank.png"
	graph_cut = str(segmented)+"_cut.png"
	cv.imwrite(graph_cut_blank, img_blank)
	cv.imwrite(graph_cut, img_org)
	cv.waitKey(1)

	#trial_contour = [[100,100],[100,101],[100,102],[100,103],[100,104],[100,105],[100,106],[100,107],[100,108]]
	#trial_contour = np.array(trial_contour)
	#print(trial_contour)
	#thresh = cv.adaptiveThreshold(img, 127, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
	#print(thresh)
	
	#ret, thresh = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
	#print(thresh)
	#print(ret)
	#im2, contours = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	#print(im2)
	#print(contours)
	
	#img1 = cv.drawContours(img, contours, -1, (0,0,255), 3)
	#cv.imshow("Image", thresh)
	#cv.waitKey(0)
		
