import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('image.png')


dst,thresh_img = cv2.threshold(img,0,150,cv2.THRESH_BINARY_INV)
blur = cv2.bilateralFilter(thresh_img,9,255,255)
plt.imshow(blur)
# plt.subplot(121),plt.imshow(img),plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
# plt.xticks([]), plt.yticks([])
plt.show()
