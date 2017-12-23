#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ROS Node for handling GPS data stream from the APM planner module.  
Package under construction.

Copyright © 2017 by Pranay Agarwal
The IIT-B Mars Rover Team
"""

import rospy
import math
from std_msgs.msg import String
import mavros
from sensor_msgs.msg import NavSatFix
import numpy as np

array = []
# gps data rate is 2 readings in 1 second


def callback(data):
    global array
    if (data.status == -1):
        rospy.logerr("error in gps data")
    else:
        gps_pub.publish(data)
        # target = (19.13179, 72.918155)
        # current = (data.latitude, data.longitude)
        # array.append(current)
        # if(len(array) == 10):  # change parameter 10 depending on speed and accuracy
        #     dist = get_distance(target, current)
        #     theta_motor = navigate(target, current)
        #     rospy.loginfo("Distance to target %s, with %s and rotation %s",
        #                   dist, data.status, theta_motor)     # rospy.get_caller_id()
        #     array = []


def get_distance(point1, point2):    # tuple objects
    R = 6371  # Radius of the earth in km
    dLat = math.pi * (point2[0] - point1[0]) / 180
    dLon = math.pi * (point2[1] - point1[1]) / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.pi * (point1[0]) / 180) * math.cos(
        math.pi * (point2[0]) / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # Distance in km
    return d


def navigate(target, current_position):
    global array

    current_direction = np.polyfit([array[i][1] for i in range(len(array))], [
                                   array[i][0] for i in range(len(array))], 1)
    # linear polynomial fit
    curr_slope = current_direction[0]
    # treating longitude as x and latitude as y
    destination_slope = (target[0] - current_position[0]) / \
        (target[1] - current_position[1])
    theta_motor = np.arctan(
        (curr_slope - destination_slope) / (1 + curr_slope * destination_slope))
    return theta_motor * 180 / np.pi


def listener():
    rospy.init_node('gps_listener', anonymous=True)
    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, callback)
    # spin() simply keeps python from exiting until this node is stopped
    gps_pub = rospy.Publisher("/nav_sensors/apm/gps", NavSatFix, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    listener()
