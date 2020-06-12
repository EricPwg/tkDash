import rospy
from std_msgs.msg import *

'''
class rosPub:
    def __init__(self):

'''

class rosSub:
    def __init__(self, tname, type, cb):
        self.topicName = str(tname)
        self.topicType = type
        self.cb = cb
        self.subFlag = False

    def start(self):
        if self.subFlag == False:
            self.topicSub = rospy.Subscriber(self.topicName, self.topicType, self.cb)
            self.subFlag = True

    def end(self):
        if self.subFlag == True:
            self.topicSub.unregister()
            self.subFlag = False

    def __del__(self):
        self.end()
