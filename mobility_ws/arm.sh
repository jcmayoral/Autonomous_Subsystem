#!/bin/bash
source devel/setup.bash
export ROS_IP=10.42.0.37
export ROS_MASTER_URI=http://10.42.0.1:11311
roslaunch arm_openloop actuator_run.launch
