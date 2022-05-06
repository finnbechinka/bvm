import cv2
import numpy as np
import math


def display(img, name="image", wait=False):
    cv2.imshow(name, img)
    if wait:
        cv2.waitKey()
        cv2.destroyAllWindows()


def calc_gaussian(n, sigma):
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


img = cv2.imread("assets/p04_apfelbaum.png", cv2.IMREAD_GRAYSCALE)

display(cv2.filter2D(img, -1, calc_gaussian(1, 5.5)), "blurred", True)
