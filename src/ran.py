#!/usr/bin/env python

import rospy
import random
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from std_msgs.msg import Int32MultiArray

rospy.init_node('ram', anonymous=True)

pub1 = rospy.Publisher('/ran', Int32, queue_size = 10)
pub2 = rospy.Publisher('/ran/f', Float32, queue_size = 10)
pub3 = rospy.Publisher('/ran/M', Int32MultiArray, queue_size = 10)
rate = rospy.Rate(2)

while not rospy.is_shutdown():
    pub1.publish(random.randint(1, 100))
    pub2.publish(random.uniform(1, 100))
    pub_data = Int32MultiArray(data = [random.randint(1, 100), random.randint(1, 100)])
    pub3.publish(pub_data)
    rate.sleep()

