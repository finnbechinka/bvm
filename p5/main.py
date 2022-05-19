from unittest import result
import cv2
import numpy as np


# takes path to an image
# returns histogram list
def histogram(img):
    rows, cols = img.shape

    hist = [0 for y in range(0, 255)]

    # iterate through all pixels
    # and sum up all occurances of each grayscale value
    for row in range(0, rows):
        for col in range(0, cols):

            pixel = img[row, col]
            grayscale = pixel
            hist[grayscale] += 1

    return hist


# takes img
# returns image after otsu thresholding
def otsu(img):
    rows, cols = img.shape
    result = np.zeros((rows, cols), np.uint8)
    pixel_count = rows * cols

    k = 255

    # get histogram of image
    hist = histogram(img)

    # C_1 pixel counts for all possible T
    t_n1 = [0 for i in range(k)]
    # C_2 pixel counts for all possible T
    t_n2 = [0 for i in range(k)]

    sum_n1 = 0
    for i in range(k):
        # sum up the histogram from 0 to T for all possible T
        sum_n1 += hist[i]
        t_n1[i] = sum_n1

        # sum up the histogram from T+1 to k-1 for all possible T
        sum_n2 = 0
        for j in range(i + 1, k):
            sum_n2 += hist[j]

        t_n2[i] = sum_n2

    # mean values for all possible C_1
    c1_mean = [0 for i in range(k)]
    # mean values for all possible C_2
    c2_mean = [0 for i in range(k)]

    # calculate mean values for all C_1 and C_2 classes
    c1_mean_sum = 0
    for i in range(k):
        # if pixel count is  0 set mean to 0
        if t_n1[i] == 0:
            c1_mean[i] = 0
        else:
            # calculate mean
            c1_mean_sum += i * hist[i]
            c1_mean[i] = c1_mean_sum / t_n1[i]

        # if pixel count is 0 set mean to 0
        if t_n2[i] == 0:
            c2_mean[i] = 0
        else:
            # calculate mean
            c2_mean_sum = 0
            for j in range(i + 1, k):
                c2_mean_sum += j * hist[j]
            c2_mean[i] = c2_mean_sum / t_n2[i]

    # variance values of all possible T values
    variance = [0 for i in range(k)]

    # T_Otsu
    t_otsu = 0
    # max variance value
    max_var = 0

    # calculate the variance values
    for i in range(k):
        # 1/MN^2 * n1(T) * n2(T) * [μ1(T) - μ2(T)]^2
        variance[i] = (1 / (pixel_count**2)) * t_n1[i] * t_n2[i] * ((c1_mean[i] - c2_mean[i]) ** 2)

        # check is current variance is new max var
        if variance[i] > max_var:
            t_otsu = i
            max_var = variance[i]

    # iterate through the image
    for row in range(rows):
        for col in range(cols):
            # apply threshold
            if img[row, col] > t_otsu:
                result[row, col] = 0
            else:
                result[row, col] = 255

    return result


# takes img, seed coordinates and gray value variance limit
# return processed img
def region_growing(img, seed, var=40):
    print("region growing (it will take some time)")
    rows, cols = img.shape
    result = np.full((rows, cols, 3), (255, 0, 0)).astype(np.uint8)
    checked = []
    queue = []
    queue.append((seed[0], seed[1]))
    # for homogeneity criterion
    seed_val = img[seed[0], seed[1]]

    while len(queue) > 0:
        pix = queue[0]
        # iterate through neighbors of current queue pixel/seed
        for i in range(-1, 2):
            for j in range(-1, 2):
                # check if neighbor value passes homogeneity criterion/gray value difference
                if seed_val - var < img[pix[0] + i, pix[1] + j] < seed_val + var:
                    # make neighbor red
                    result[pix[0] + i, pix[1] + j] = (0, 0, 255)

                    # add neighbor to queue if not already checked
                    if not (pix[0] + i, pix[1] + j) in checked:
                        queue.append((pix[0] + i, pix[1] + j))

                    # mark neighbor as checked
                    checked.append((pix[0] + i, pix[1] + j))
        # remove pixel/seed from queue
        queue.pop(0)

    # make 3x3 square around initial seed greed
    for i in range(-1, 2):
        for j in range(-1, 2):
            result[seed[0] + i, seed[1] + j] = (0, 255, 0)
    print("region growing finished")
    return result


img = cv2.imread("assets/p05_gummibaeren.png", cv2.IMREAD_GRAYSCALE)


EXPORT_IMAGES = True  # sets if images should be saved to file (into assets/export/)


def listener(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        result = region_growing(img, (y, x))
        cv2.imshow("region_growing", result)
        if EXPORT_IMAGES:
            cv2.imwrite("assets/export/region_growing.png", result)


img_otsu = otsu(img)

cv2.imshow("otsu", img_otsu)
cv2.imshow("region_growing", img)
cv2.setMouseCallback("region_growing", listener)
cv2.waitKey()
cv2.destroyAllWindows()

if EXPORT_IMAGES:
    cv2.imwrite("assets/export/otsu.png", img_otsu)
