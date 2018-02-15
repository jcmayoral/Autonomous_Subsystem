import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
img = cv2.imread('image.png')

#dst,thresh_img = cv2.threshold(img,0,150,cv2.THRESH_BINARY)
#blur = cv2.bilateralFilter(thresh_img,9,255,255)
#kernel = np.ones((5,5),np.float32)/25
#kst = cv2.filter2D(blur,-1,kernel)

lowerBound=np.array([1,1,1])
upperBound=np.array([45,45,45])
img=cv2.resize(img,(640,480))

mask=cv2.inRange(img,lowerBound,upperBound)


kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)


maskFinal=maskClose
_, conts, h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img,conts,-1,(255,0,0),3)
cv2.imshow("Without Noise",maskClose)
cv2.imshow("Object",img)
cv2.waitKey(10000)
