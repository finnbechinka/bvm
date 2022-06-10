import cv2
import numpy as np
from math import cos, sin, pi


def hough_circle_transformation(image, radius, hough_thresh):
    rows, cols = image.shape

    acc = np.zeros(image.shape)

    # iterate through the image
    for x in range(0, rows - radius):
        for y in range(0, cols - radius):
            # check if pixel is a edge pixel
            if image[x][y] == 255:
                # "draw" cricle around current edge pixel
                # and "vote" for the edge of that circle
                for theta in range(0, 360):
                    # calculate polar coordinate points
                    b = y - radius * sin(theta * pi / 180)
                    a = x - radius * cos(theta * pi / 180)

                    # vote for the edge
                    acc[int(a)][int(b)] += 1

    # get all center candidates from the accumulator matrix
    # meaning all points where the vote value exceeds the set threshold
    center_candidates = np.where(acc > hough_thresh)

    # image for the circles
    circles = np.zeros(image.shape)

    count = 0

    # iterate through the center candidates
    for i in range(0, center_candidates[0].size):

        alone = True
        # check if there is already a circle close by (within half a radius)
        for theta in range(0, 360):
            # calculate polar coordinate points
            y = center_candidates[1][i] - (2 * radius) * sin(theta * pi / 180)
            x = center_candidates[0][i] - (2 * radius) * cos(theta * pi / 180)

            # check there is already a circle inbetween the center and the edge
            if x < rows and y < cols:
                if np.sum(circles[center_candidates[0][i] : int(x), center_candidates[1][i] : int(y)]) > 0:
                    alone = False
        if alone:
            # increment coin count
            count += 1

            # draw the center
            cv2.circle(circles, (center_candidates[1][i], center_candidates[0][i]), 1, 255, 2)

            # draw circle around center
            cv2.circle(circles, (center_candidates[1][i], center_candidates[0][i]), radius, 255, 2)

    return count, circles


EXPORT_IMAGES = False
SHOW_IMAGES = True

# set radii for the different coins
RADIUS_1_CENT = 23
RADIUS_2_CENT = 27
RADIUS_5_CENT = 32

# min vote threshold
HOUGH_THRESH = 135

# base image
base_image = cv2.imread("assets/p08_muenzen.png", cv2.IMREAD_GRAYSCALE)

# smooth edges by applying a gaussian blur and
# use the canny edge detector to find the edges
blurred_img = cv2.GaussianBlur(base_image, (5, 5), 1)
edge_img = cv2.Canny(blurred_img, 150, 200)

# apply hough circle transformation to find the circles and cent counts
one_cent_count, one_cent_cricles = hough_circle_transformation(edge_img, RADIUS_1_CENT, HOUGH_THRESH)
two_cent_count, two_cent_cricles = hough_circle_transformation(edge_img, RADIUS_2_CENT, HOUGH_THRESH)
five_cent_count, five_cent_cricles = hough_circle_transformation(edge_img, RADIUS_5_CENT, HOUGH_THRESH)

# convert grayscale image to rgb image for drawing colored circles
color_image = cv2.cvtColor(base_image, cv2.COLOR_GRAY2RGB)

# draw colored circles
color_image[one_cent_cricles == 255] = [255, 0, 0]
color_image[two_cent_cricles == 255] = [0, 0, 255]
color_image[five_cent_cricles == 255] = [0, 255, 0]

# print inividual cent count and total
print(f"{one_cent_count} x 1 cent")
print(f"{two_cent_count} x 2 cent")
print(f"{five_cent_count} x 5 cent")
total = one_cent_count + two_cent_count * 2 + five_cent_count * 5
print(f"total: {total} cent")

if EXPORT_IMAGES:
    cv2.imwrite("assets/export/hough.png", color_image)
if SHOW_IMAGES:
    cv2.imshow("hough", color_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
