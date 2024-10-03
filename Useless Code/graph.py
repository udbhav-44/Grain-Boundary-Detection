import cv2 as cv
import numpy as np

def graph_segmentation(image_path: str) -> None:
    """
    Perform graph segmentation on an image and display the segmented image.

    Args:
    image_path (str): The path to the input image.

    Returns:
    None

    Example:
    >>> graph_segmentation("0.jpeg")
    """

    sigma = 0.5
    k = 300
    # Create Graph Segmentation Object
    gseg = cv.ximgproc.segmentation.createGraphSegmentation(sigma= sigma, k = k, min_size=100)

    # Load the image
    img = cv.imread(image_path, 0)

    # Blurring the img using Gaussian Blur
    img = cv.GaussianBlur(img, (3, 3), 0)

    # Segment an image and store output in dst.
    imgs = gseg.processImage(img).astype(np.uint8)
    r, c = imgs.shape

    # Generating Mask for the image using segments
    mask = np.ndarray(shape=(r, c, 3), dtype=np.uint8)
    color_dict = {}
    for i in range(r):
        for j in range(c):
            if imgs[i, j] not in color_dict:
                color_dict[imgs[i, j]] = (255 * np.random.rand(1, 3)).astype(np.uint8)
            mask[i, j] = color_dict[imgs[i, j]]

    cv.namedWindow("Graph cut", cv.WINDOW_GUI_NORMAL)
    cv.createTrackbar("ksize", "Graph cut", 3, 255, lambda x: None)
    cv.createTrackbar("sigma", "Graph cut", int(sigma*10), 1000, lambda x: None)

    while (1):
        ksize = cv.getTrackbarPos('ksize', "Graph cut")
        ksize += 1 - ksize % 2
        sigma = cv.getTrackbarPos('sigma', "Graph cut") / 10.0

        img_gb = cv.GaussianBlur(img, (ksize, ksize), sigma)
        imgs = gseg.processImage(img_gb).astype(np.uint8)
        r, c = imgs.shape

        color_dict.clear()
        mask = np.ndarray(shape=(r, c, 3), dtype=np.uint8)
        for i in range(r):
            for j in range(c):
                if imgs[i, j] not in color_dict:
                    color_dict[imgs[i, j]] = (255 * np.random.rand(1, 3)).astype(np.uint8)
                mask[i, j] = color_dict[imgs[i, j]]

        cv.imshow("Graph cut", mask)
        cv.imwrite("segmented.png", mask)
        k = cv.waitKey(1) & 0xFF
        if k == 27:  ## Esc
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    graph_segmentation("0.jpeg")