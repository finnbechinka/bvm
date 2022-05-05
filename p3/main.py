import cv2
import numpy as np

# outputs 2*n+1 x 2*n+1 mean blur filter matrix 
# example n = 1:
# [[1, 1, 1],
#  [1, 1, 1],
#  [1, 1, 1]]
def mean_blur_matrix(n):
    matrix = []
    for i in range(2*n+1):
        row = []
        for j in range(2*n+1):
            row.append(1)
        matrix.append(row)
    return matrix

# outputs 2*n+1 x 2*n+1 binomial filter matrix 
# example n = 1:
# [[1, 2, 1],
#  [2, 4, 2],
#  [1, 2, 1]]
def binomial_matrix(n):
    # create 1d binomial filter with p = 2*n
    vector = (np.poly1d([0.5, 0.5])**(2*n)).coeffs
    
    # calculate scalar
    s = 1 / (vector[0] * vector[0])

    # create 2d binomial filter by multiplying the 1d matrix
    matrix = []
    for i in range(2*n+1):
        row = []
        for j in range(2*n+1):
            # multiply values by s in oder to have interger values instead of float values in the matrix
            row.append(int((vector[i] * vector[j]) * s))
        matrix.append(row)
    return matrix


def linear_filter(input, filter):
    # create input image clone to write result values into as not to change pixel values needed for calculations
    output = input.copy()
    rows, cols = input.shape
    # calculate n, where n is the distance between the middle of the matrix and the edge of the matrix 
    n = int((len(filter) / 2))

    # iterate throgh the input image starting with the nth pixel 
    # as to not go out of bounds with the matrix
    for row in range(n, rows - n):
        for col in range(n , cols - n):
            values = []

            # iterate through the surrounding pixels according to the matrix
            for x in range(-n, n+1):
                for y in range(-n, n+1):
                    values.append(input[row + x][col + y] * filter[x][y])
            
            
            # set output pixel to the sum of the values devided by the sum of the filter matrix values
            output[row][col] = sum(values) / sum(sum(filter, []))
   
    return output


def weighted_median_filter(input, filter):
    # create input image clone to write result values into as not to change pixel values needed for calculations
    output = input.copy()
    rows, cols = input.shape
    # calculate n, where n is the distance between the middle of the matrix and the edge of the matrix 
    n = int((len(filter) / 2))

    # iterate throgh the input image starting with the nth pixel 
    # as to not go out of bounds with the matrix
    for row in range(n, rows - n):
        for col in range(n , cols - n):
            values = []
            
            # iterate through the surrounding pixels according to the matrix
            for x in range(-n, n+1):
                for y in range(-n, n+1):
                    for w in range(0, filter[x][y]):
                        # add pixel value to the list as often as the weighting says
                        values.append(input[row + x][col + y])
            
            # set weighted median as new pixel value in output image
            values.sort()
            output[row][col] = values[int(len(values)/2)]
   
    return output

img = cv2.imread("assets/p03_nilpferd.jpg", cv2.IMREAD_GRAYSCALE)

# 1. (a)
# N = 1
a = linear_filter(img, mean_blur_matrix(1))

# 1. (b)
# N = 1
b = linear_filter(img, binomial_matrix(1))

# N = 2
c = linear_filter(img, binomial_matrix(2))

# 2.
# weight matrix
W = [[1,2,1],
     [2,3,2],
     [1,2,1]]
d = weighted_median_filter(img, W)

EXPORT_IMAGES = False # sets if images should be saved to file (in working directory)
SHOW_IMAGES = True # sets if images should be shown in windows

if EXPORT_IMAGES:
    cv2.imwrite("assets/export/mean_blur.jpg", a)
    cv2.imwrite("assets/export/binomial_filter_1.jpg", b)
    cv2.imwrite("assets/export/binomial_filter_2.jpg", c)
    cv2.imwrite("assets/export/weighted_median_filter.jpg", d)
if SHOW_IMAGES:
    cv2.imshow("mean blur (N = 1)", a)
    cv2.imshow("binomial filter (N = 1)", b)
    cv2.imshow("binomial filter (N = 2)", c)
    cv2.imshow("weighted median filter", d)
    cv2.waitKey()
    cv2.destroyAllWindows()