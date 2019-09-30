import cv2
import numpy as np

def default(image):
    return image


def hmap(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    heatmap_img = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return heatmap_img


def bilateral(image):
    bil = cv2.bilateralFilter(image,3,3,3)
    return bil

def fire(frame):
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)

    output = cv2.bitwise_and(frame, hsv, mask=mask)
    return output
def contour(frame):
    image = cv2.bilateralFilter(frame, 15, 75, 60)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    grad_x = cv2.Sobel(image, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(image, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    image = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_TRUNC)
    image = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    return image

def __color_segment__(image):
    image = cv2.bilateralFilter(image, 15, 75, 60)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hsv_image = image
    grad_x = cv2.Sobel(image, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(image, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    image = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    ret, thresh = cv2.threshold(image, 17, 255, cv2.THRESH_TOZERO_INV)
    msk_image = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    msk_image = cv2.cvtColor(msk_image, cv2.COLOR_GRAY2BGR)
    msk_image = cv2.bilateralFilter(msk_image, 15, 75, 60)
    image = cv2.bitwise_xor(msk_image, hsv_image)
    return image, msk_image

def color_segment(image):
    img, _ = __color_segment__(image)
    return img

def mask_segment(image):
    _, mask = __color_segment__(image)
    return mask