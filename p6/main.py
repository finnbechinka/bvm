import cv2
import numpy as np


# takes image and structural element
# return result image after dilatation
def dilatate(image, h):
    # ensure only symmetrical structural element
    if len(h) % 2 == 0:
        return

    # h radius
    dist = int((len(h) - 1) / 2)

    rows, cols = image.shape
    result = np.zeros((rows, cols), np.uint8)

    # iterate through image
    for row in range(dist, rows - dist):
        for col in range(dist, cols - dist):
            # superimpose kernel onto image for each pixel with the value 255
            # with said pixel at its center
            if image[row, col] == 255:
                for x in range(-dist, dist + 1):
                    for y in range(-dist, dist + 1):
                        # set each surrounding pixel to the corresponding kernel value
                        result[row + x, col + y] = h[x + dist, y + dist]
    return result


# takes image and structural element
# return result image after erosion
def erode(image, h):
    # ensure only symmetrical structural element
    if len(h) % 2 == 0:
        return

    # h radius
    dist = int((len(h) - 1) / 2)

    rows, cols = image.shape
    result = np.zeros((rows, cols), np.uint8)

    # iterate through image
    for row in range(0, rows):
        for col in range(0, cols):
            # handle edge cases
            # make sure kernal doesnt leave image
            if row - dist + 1 < 0 or row + dist + 1 > rows or col - dist + 1 < 0 or col + dist + 1 > cols:
                result[row, col] = 0
                continue
            # superimpose kernel on image
            # check if the kernel is contained in image
            # with the current pixel at its center
            contained = True
            for x in range(-dist, dist + 1):
                for y in range(-dist, dist + 1):
                    if image[row + x, col + y] != h[x + dist, y + dist]:
                        contained = False
            if contained:
                # retain pixel if kernel is contained in image
                result[row, col] = 255
            else:
                # erode pixel if kernel is not contained in image
                result[row, col] = 0
    return result


def watershed(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply otsu's binarization to approximate the objects
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # find sure background area
    kernel = np.ones((3, 3), np.uint8)
    sure_bg = cv2.dilate(thresh, kernel, iterations=3)

    # find sure foreground area
    ret, sure_fg = cv2.threshold(thresh, 0, 255, 0)

    # find unknown region
    unknown = cv2.subtract(sure_bg, sure_fg)

    # label markers
    ret, markers = cv2.connectedComponents(sure_fg)

    # add one to all labels so that sure background is not 0, but 1
    markers = markers + 1

    # mark the region of unknown with zero
    markers[unknown == 255] = 0

    # apply watershed
    markers = cv2.watershed(img, markers)

    # make background black
    img[markers == 1] = [0, 0, 0]

    # make boundary region blue
    img[markers == -1] = [255, 0, 0]

    # color all objects
    steps = 255 / markers.max()
    for i in range(2, markers.max() + 1):
        img[markers == i] = [i * steps, i * steps, i * steps]
    return img


zahn = cv2.imread("assets/p06_zahnrad.png", cv2.IMREAD_GRAYSCALE)
gummi = cv2.imread("assets/p06_gummitiere.png")

# 1.
# structural element
H = np.full((7, 7), 255, np.uint8)

# closing
d = dilatate(zahn, H)
e = erode(d, H)

# 2.
w = watershed(gummi)

EXPORT_IMAGES = True
SHOW_IMAGES = True

if EXPORT_IMAGES:
    cv2.imwrite("assets/export/closing.png", e)
    cv2.imwrite("assets/export/watershed.png", w)
if SHOW_IMAGES:
    cv2.imshow("closing", e)
    cv2.imshow("water", w)
    cv2.waitKey()
    cv2.destroyAllWindows()
