import cv2
from random import randrange
import numpy as np

def display(image, name = "image"):
    cv2.imshow(name, image)
    cv2.waitKey()
    cv2.destroyAllWindows()

# takes two paths to images base_img and filler_img
# replace n x n big tiles of base_img with n x n big tiles from random position of filler_img
# displays resulting image
def tile_fill(base_img, filler_img, n):
    base = cv2.imread(base_img)
    filler = cv2.imread(filler_img)
    b_rows, b_cols, b_dims = base.shape
    f_rows, f_cols, f_dims = filler.shape

    for row in range(0, b_rows - n, n * 2):
        for col in range(0, b_cols - n, n * 2):
            
            x1 = randrange(0, f_rows - n)
            print(x1)
            y1 = randrange(0, f_cols - n)
            print(y1)
            
            base[row: row + n, col: col + n] = filler[x1: (x1 + n), y1: (y1 + n)]
    cv2.imwrite("result.jpg", base)
    display(base)

# takes path to an image
# returns histogram list
def histogram(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    rows, cols = img.shape
    
    hist = [0 for y in range(0,255)]

    # iterate through all pixels 
    # and sum up all occurances of each grayscale value
    for row in range(0, rows):
        for col in range(0, cols):

            pixel = img[row, col]
            grayscale = pixel
            hist[grayscale] += 1
    
    return hist

# takes path to an image
# returns cumulative histogram list
def histogram_cumulative(img_path):
    hist = histogram(img_path)

    cum_hist = [0 for y in range(0,255)]

    # iterage thorugh hist 
    # and sum up prev cum_hist value with the current hist value
    for i in range(0, len(hist)):
        if(i == 0):
            cum_hist[i] = hist[i]
        else:
            cum_hist[i] = cum_hist[i - 1] + hist[i]
    
    return cum_hist

# takes path to an image
# returns equalized histogram list
def histogram_equalized(img_path):
    eq_hist = [0 for y in range(0, 255)]

    cum_hist = histogram_cumulative(img_path)

    # iterate through cum_hist 
    # and calculate the equalized value
    for i in range (0, 255):
        eq_hist[i] = round(cum_hist[i] * (255 / max(cum_hist)))
    
    return eq_hist

minden = "assets/p02_teil1_minden.jpg"
sonne = "assets/p02_teil1_sonne.jpg"
steine = "assets/p02_teil2_steine.jpg"

tile_fill(minden, sonne, 50)
print("(a):\n" + str(histogram(steine)) + "\n\n")
print("(b):\n" + str(histogram_cumulative(steine)) + "\n\n")
print("(c):\n" + str(histogram_equalized(steine)) + "\n\n")