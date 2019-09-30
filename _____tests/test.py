import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import os

def contour(image):
    image = cv2.bilateralFilter(image, 15, 75, 60)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    grad_x = cv2.Sobel(image, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(image, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    image = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    ret, thresh = cv2.threshold(image, 17, 255, cv2.THRESH_BINARY)
    image = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    return image

def rgb_plot(image):
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    pixel_colors = image.reshape((np.shape(image)[0] * np.shape(image)[1], 3))
    norm = colors.Normalize(vmin=-1., vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    r, g, b = cv2.split(image)
    axis.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    plt.show()

def hsv_plot(image):
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1, projection="3d")
    pixel_colors = image.reshape((np.shape(image)[0] * np.shape(image)[1], 3))
    norm = colors.Normalize(vmin=-1., vmax=1.)
    norm.autoscale(pixel_colors)
    pixel_colors = norm(pixel_colors).tolist()
    h, s, v = cv2.split(image)
    axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
    axis.set_xlabel("Hue")
    axis.set_ylabel("Saturation")
    axis.set_zlabel("Value")
    plt.show()

def segment(image):
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


path = "./data/data/img_data/train"
save_path = "./data/processed_data/img_data/train"
if True:
    for r, d, f, in os.walk(path):
        for dir in d:
            files = os.listdir(path+'/'+dir)
            for file in files:
                print(path+'/'+dir+'/'+file)
                frame = cv2.imread(path+'/'+dir+'/'+file)
                image, mask = segment(frame)
                ret, jpeg = cv2.imencode('.jpg',image)
                cv2.imshow("Frame Viewer", image)
                if cv2.waitKey(1) in [13, 27]:
                    cv2.destroyAllWindows()
                p = save_path+'/'+dir+'/'+file
                cv2.imwrite(p, image)

else:
    # cap = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #     image,mask = segment(frame)
    #     cv2.imshow("Frame Viewer", image)
    #     if cv2.waitKey(1) in [13, 27]:
    #         break
    #
    # cap.release()
    # cv2.destroyAllWindows()

    scale = 2
    directory = 'data/data/img_data/train/'
    frame = cv2.imread(directory+"default/img_8.jpg")
    w, h, p = frame.shape
    frame = cv2.resize(frame, (w*scale, h*scale))
    image, mask = segment(frame)
    cv2.imshow("Frame Viewer", image)
    if cv2.waitKey() in [13, 27]:
        cv2.destroyAllWindows()

