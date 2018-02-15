#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys, time
import rospy
import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
img = cv2.imread('image.png')

#dst,thresh_img = cv2.threshold(img,0,150,cv2.THRESH_BINARY)
#blur = cv2.bilateralFilter(thresh_img,9,255,255)
#kernel = np.ones((5,5),np.float32)/25
#kst = cv2.filter2D(blur,-1,kernel)

class ObjectDetection():
	"""Initializing ROS Subscriber"""
	def __init__(self):
	# subscribed Topic
		self.subscriber = rospy.Subscriber("/kinect2/qhd/image_depth_rect",Image, self.imagecallback,  queue_size = 1)
		#elf.test_pub = rospy.Publisher("/test/sd/object_detected",Image,  queue_size = 1000)
		self.image_pub = rospy.Publisher("/output/qhd/object_detected",Image,  queue_size = 1)

	def imagecallback(self,msg):

		bridge = CvBridge()
		msg.encoding = "mono16"
		img = bridge.imgmsg_to_cv2(msg,"bgr8")
		#imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


		lowerBound=np.array([5,5,5])
		upperBound=np.array([25,25,25])
		#img=cv2.resize(img,(640,480))

		mask=cv2.inRange(img,lowerBound,upperBound)


		kernelOpen=np.ones((5,5))
		kernelClose=np.ones((20,20))

		maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
		maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

		_, conts, h=cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		cv2.drawContours(img,conts,-1,(255,0,0),3)
		#cv2.imshow("Without Noise",maskClose)
		#cv2.imshow("Object",img)
		#cv2.waitKey(10000)
    	
		# Publish new image
		self.image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))

def main(args):
	'''Initializes and cleanup ros node'''
	ic = ObjectDetection()
	rospy.init_node('object_detection', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down ROS Image feature detector module")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
