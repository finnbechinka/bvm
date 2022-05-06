import cv2
import numpy as np


EXPORT_IMAGES = True  # sets if images should be saved to file (in working directory)
SHOW_IMAGES = True  # sets if images should be shown in windows

img_bgr = cv2.imread("assets/praktikum_01_schatten.jpg")
img_rgb = img_bgr[:, :, [2, 1, 0]]


def name_colors(img):
    print("(0,0,0): " + str(img[0, 0, 0] / 256))
    print("(1,0,0): " + str(img[1, 0, 0] / 256))
    print("(0,1,0): " + str(img[0, 1, 0] / 256))
    print("(0,0,1): " + str(img[0, 0, 1] / 256))
    print("(1,1,0): " + str(img[1, 1, 0] / 256))
    print("(1,0,1): " + str(img[1, 0, 1] / 256))
    print("(0,1,1): " + str(img[0, 1, 1] / 256))
    # print("(0.6,0.6,0.6): " + str(img[0.6,0.6,0.6]/256))


# takes an rgb image and returns it coverted to the yuv format
def rgb_to_yuv(img):
    rows, cols, dims = img.shape

    img_yuv = np.zeros((rows, cols, dims))

    for row in range(0, rows):
        for col in range(0, cols):

            pixel = img[row, col]

            r = (pixel[0] / 255) ** (1 / 2.2)
            g = (pixel[1] / 255) ** (1 / 2.2)
            b = (pixel[2] / 255) ** (1 / 2.2)

            y = (0.299 * r) + (0.587 * g) + (0.114 * b)
            u = 0.493 * (b - y)
            v = 0.877 * (r - y)

            img_yuv[row, col] = (y, u, v)

    return img_yuv


# takes an rgb image and
# depending on if EXPORT_IMAGES and/or SHOW_IMAGES is set saves and/or shows the images resulting in the shadow detection
def shadow_detection(img):
    yuv = rgb_to_yuv(img)

    us_mean = np.mean(yuv[:, :, 1])
    us_stddev = np.std(yuv[:, :, 1])

    vs_mean = np.mean(yuv[:, :, 2])
    vs_stddev = np.std(yuv[:, :, 2])

    rows, cols, dims = img.shape

    s = np.zeros((rows, cols))
    t1 = np.zeros((rows, cols))
    t2 = np.zeros((rows, cols))

    for row in range(0, rows):
        for col in range(0, cols):

            if yuv[row, col, 1] > (us_mean + us_stddev):
                t1[row, col] = 255
            else:
                t1[row, col] = 0

            if yuv[row, col, 2] > (vs_mean - vs_stddev):
                t2[row, col] = 0
            else:
                t2[row, col] = 255

            s[row, col] = t1[row, col] * t2[row, col]

    if EXPORT_IMAGES:
        cv2.imwrite("t1.jpg", t1)
        cv2.imwrite("t2.jpg", t2)
        cv2.imwrite("s.jpg", s)

    if SHOW_IMAGES:
        cv2.imshow("s", s)
        cv2.imshow("t1", t1)
        cv2.imshow("t2", t2)
        cv2.waitKey()
        cv2.destroyAllWindows()


name_colors(img_rgb)
shadow_detection(img_rgb)
