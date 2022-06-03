from cgitb import reset
from colorsys import yiq_to_rgb
import cv2
import numpy as np


def harrisCornerDetector(img, alpha, t, dmin):
    result = np.copy(img)
    # filter image with gauss before harris corner detector
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, columns = img.shape

    # array with the detected corners
    corners = []

    # iterating through image
    for row in range(1, rows - 1):
        for col in range(1, columns - 1):

            # derivative  x
            gx = np.abs((int(img[row, col + 1]) - int(img[row, col - 1])) / 2)

            # derivative y
            gy = np.abs((int(img[row + 1, col]) - int(img[row - 1, col])) / 2)

            # corner-response-function
            crf = ((gx * gy) ** 2 - (gx * gy)) - (alpha * (gx + gy) ** 2)

            # thresholding the corner-response-function
            if crf > t:
                corners.append((row, col))

    # non-maximum-suppression
    # iterate through corners
    for curr_corner in corners:
        c_row, c_col = curr_corner
        # iterate through all leading corners
        for corner in corners[corners.index(curr_corner) + 1 : len(corners)]:
            row, col = corner
            # distance between the curr_corner and corner
            d = np.sqrt((c_row - row) ** 2 + (c_col - col) ** 2)
            # if the distance is smaller dmin delete the corner
            if d < dmin:
                corners.pop(corners.index(corner))

    # display a red x for every corner in the result image
    for corner in corners:
        result[corner] = (0, 0, 255)
        result[corner[0] - 1, corner[1]] = (0, 0, 255)
        result[corner[0], corner[1] - 1] = (0, 0, 255)
        result[corner[0] + 1, corner[1]] = (0, 0, 255)
        result[corner[0], corner[1] + 1] = (0, 0, 255)
    return result


# takes a reference and a template image
# return result image with red rectange around the match
def template_matching(ref, temp):
    rrows, rcols, rdims = ref.shape
    trows, tcols, tdims = temp.shape

    srows = rrows - trows
    scols = rcols - tcols
    ssd = np.full((srows, scols), np.infty)

    # (a)
    i = 0
    j = 0
    min = np.infty
    for x in range(0, srows):
        for y in range(0, scols):
            # ∑_(u=0)^(M-1)∑_(v=0)^(n-1) (g(x + u, y + v) − T(u, v))^2
            # calculate squared differences between the reference and the template
            # outgoing from the current pixel (x,y)
            diffs = (ref[x : x + trows, y : y + tcols] - temp) ** 2
            # get the sum of the squared differences
            ssd[x, y] = diffs.sum()
            # check if current sum of squared differences is the miniumum
            if diffs.sum() < min:
                # remember coordinates and new min
                i = x
                j = y
                min = diffs.sum()

    """
    # (b)
    cor = np.full((srows, scols), np.infty)

    rgray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    tgray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    i = 0
    j = 0
    min = np.infty
    for x in range(0, srows):
        for y in range(0, scols):
            for u in range(0, trows - 1):
                for v in range(0, tcols - 1):
                    guv = []
                    for k in range(u, trows):
                        for l in range(v, tcols):
                            guv.append(rgray[k, l])
                    if len(guv) > 0:
                        # 𝑔̅𝑢,𝑣
                        gmean = np.asarray(guv).mean()
                        # 𝑇̅
                        tmean = tgray.mean()
                        # (g(x + u, y + v) − 𝑔̅𝑢,𝑣)
                        calc1 = rgray[x + u, y + v] - gmean
                        # (T(u, v) − 𝑇̅)
                        calc2 = tgray[u, v] - tmean
                        # (g(x + u, y + v) − 𝑔̅𝑢,𝑣) ∙ (T(u, v) − 𝑇̅)
                        over = calc1 * calc2
                        # [(g(x + u, y + v) − 𝑔̅𝑢,𝑣)^2]^1/2 ∙ (T(u, v) − 𝑇̅)^2]^1/2
                        under = (calc1**2) ** (1 / 2) * (calc2**2) ** (1 / 2)
                        if under != 0:
                            res = over / under
                            if res < min:
                                i = x
                                j = y
                                min = res
    """
    # visualize match by drawing a red rectange around the match
    result = np.copy(ref)
    cv2.rectangle(result, (j - 1, i - 1), (j + trows + 1, i + tcols + 1), (0, 0, 255), 2)
    return result


# 1.
reference = cv2.imread("assets/p07_reference.png")
template = cv2.imread("assets/p07_template.png")

temp_match = template_matching(reference, template)

# 2.
img = cv2.imread("assets/p07_harris.png")

# harrisCornerDetector with alpha=0.04 CRF-Threshold=20000 dmin=10
harris = harrisCornerDetector(img, 0.04, 20000, 10)

EXPORT_IMAGES = False
SHOW_IMAGES = True

if EXPORT_IMAGES:
    cv2.imwrite("assets/export/hcd.png", harris)
    cv2.imwrite("assets/export/tm.png", temp_match)
if SHOW_IMAGES:
    cv2.imshow("HCD", harris)
    cv2.imshow("TM", temp_match)
    cv2.waitKey()
    cv2.destroyAllWindows()
