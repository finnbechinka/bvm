import cv2
from cv2 import filter2D
from cv2 import imwrite
import numpy as np
import math


def progress_bar(progress, total, msg="doing stuff:"):
    percent = 100 * (progress / float(total))
    bar = "█" * int(percent / 2) + "-" * (50 - int(percent / 2))
    msg = (msg[:25] + "..") if len(msg) > 75 else msg
    clear = "                                                            "
    print(f"\rworking: [{bar}] {percent:.2f}% ({msg}){clear}", end="\r")
    if progress == total:
        print("\ndone")


def display(img, name="image", wait=False):
    cv2.imshow(name, img)
    if wait:
        cv2.waitKey()
        cv2.destroyAllWindows()


# takes in n = matrix size (must be odd or n = 1 will be used by default)
# and sigma for the calculation of the gaussian filter
# returns gaussian filter kernel of size (2 * n + 1)x(2 * n + 1)
def calc_gaussian(n, sigma):
    if n % 2 == 0:
        n = 1

    matrix = []

    # distance between middle of the matrix and the edge
    d = int((2 * n + 1) / 2)

    for x in range(-d, d + 1):
        row = []
        for y in range(-d, d + 1):
            scalar = 1 / (2 * math.pi * sigma**2)
            exp = -(x**2 + y**2) / (2 * sigma**2)
            row.append(scalar * math.e**exp)
        matrix.append(row)

    # normalize filter sum to 1
    msum = sum(sum(matrix, []))
    for x in range(0, 2 * n + 1):
        for y in range(0, 2 * n + 1):
            matrix[x][y] *= 1 / msum

    return np.array(matrix)


# takes in an image and gaussian filter kernel
# returns new blurred image
def gaussian(img, kernel=calc_gaussian(1, 5.5)):
    return cv2.filter2D(img, -1, kernel)


# takes grayscale image
# returns gradient magnitute and direction
def sobel(input):
    # sobel filter matrices
    S_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    S_Y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # apply sobel x and y filter to input image
    resultx = cv2.filter2D(input, cv2.CV_32F, S_X)
    resulty = cv2.filter2D(input, cv2.CV_32F, S_Y)

    # calculate gradient magnitute
    magnitute = np.hypot(resultx, resulty)  # Equivalent to sqrt(x1**2 + x2**2)
    magnitute = magnitute / magnitute.max() * 255  # normalize values
    magnitute = np.uint8(magnitute)  # convert to 8 bit

    # calcutae gradient direction
    direction = np.arctan2(resulty, resultx)

    return (magnitute, direction)


# takes in gradient magnitute and direction
# returns non maxima suppression result
def non_maxima_suppression(mag, dir):
    rows, cols = mag.shape
    result = np.zeros((rows, cols), np.uint8)
    deg = np.rad2deg(dir)  # convert gadient direction to degrees

    # iterate through gradient magnitute
    # find neighbor a and b
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            a = 0
            b = 0

            # horizontal
            if (
                (0 <= deg[row, col] < 22.5)
                or (157.5 <= deg[row, col] <= 180)
                or (-22.5 <= deg[row, col] < 0)
                or (-180 <= deg[row, col] < -157.5)
            ):
                a = mag[row, col + 1]
                b = mag[row, col - 1]
            # diagonal 45
            elif (22.5 <= deg[row, col] < 67.5) or (-157.5 <= deg[row, col] < -112.5):
                a = mag[row + 1, col + 1]
                b = mag[row - 1, col - 1]
            # vertical
            elif (67.5 <= deg[row, col] < 112.5) or (-112.5 <= deg[row, col] < -67.5):
                a = mag[row + 1, col]
                b = mag[row - 1, col]
            # diogonal 135
            elif (112.5 <= deg[row, col] < 157.5) or (-67.5 <= deg[row, col] < -22.5):
                a = mag[row + 1, col - 1]
                b = mag[row - 1, col + 1]

            # check if local maxima is bigger than neighbors
            if (mag[row, col] > a) and (mag[row, col] > b):
                result[row, col] = mag[row, col]
            else:
                result[row, col] = 0

    return result


# takes gradient magnitute, low and high threshold
# returns gradient magnitute with thinned out edges
def hysteresis(mag, t_low, t_high):
    rows, cols = mag.shape
    result = np.zeros((rows, cols), np.uint8)

    # iterate thorugh image and set values acording to threshold values
    for row in range(0, rows):
        for col in range(0, cols):
            if mag[row, col] > t_high:
                result[row, col] = 255
            if mag[row, col] < t_low:
                result[row, col] = 0
            if (mag[row, col] >= t_low) & (mag[row, col] <= t_high):
                result[row, col] = 128

    # check for all weak edges if they are adjacent to a strong edge
    # if a weak edge is adjacent to a strong edge elevate it (set value to 255)
    # otherwise suppress it (set value to 0)
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if result[row, col] == 128:
                connected = False
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if result[row + i, col + j] == 255:
                            connected = True
                if connected:
                    result[row, col] = 255
                else:
                    result[row, col] = 0

    return result


progress_bar(0, 6, "reading img")
img = cv2.imread("assets/p04_apfelbaum.png", cv2.IMREAD_GRAYSCALE)

# (a)
progress_bar(1, 6, "calculating gauss kernel")
gauss_kernel = calc_gaussian(1, 5.5)
progress_bar(2, 6, "applying gauss kernel")
blurred_img = gaussian(img, gauss_kernel)

progress_bar(3, 6, "calculating magnitute and direction of edges")
# (b)
sobel_mag, sobel_dir = sobel(blurred_img)

# (c)
progress_bar(4, 6, "applying nms")
nms_img = non_maxima_suppression(sobel_mag, sobel_dir)

# (d)
progress_bar(5, 6, "applying hysteresis")
canny = hysteresis(nms_img, 25, 50)
progress_bar(6, 6)

EXPORT_IMAGES = True  # sets if images should be saved to file (into assets/export/)
SHOW_IMAGES = True  # sets if images should be shown in windows

if EXPORT_IMAGES:
    cv2.imwrite("assets/export/blurred_img.png", blurred_img)
    cv2.imwrite("assets/export/sobel_mag.png", sobel_mag)
    cv2.imwrite("assets/export/nms_img.png", nms_img)
    cv2.imwrite("assets/export/canny.png", canny)
if SHOW_IMAGES:
    display(blurred_img, "gaussian blur")
    display(sobel_mag, "sobel filter")
    display(nms_img, "nms")
    display(canny, "canny", True)
