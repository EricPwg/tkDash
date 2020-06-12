import Tkinter as tk
from rosPubSub import *
import rospy
from std_msgs.msg import *

FRAME_BUTTON_NUM = 5
FRAME_BUTTON_TEXT = ['^', 'v', 'Top', 'Buttom', 'Delete', 'Restart']

typeMap = {'std_msgs/Int32':Int32, 'std_msgs/Float32':Float32, 'std_msgs/Int32MultiArray':Int32MultiArray, 'std_msgs/Float32MultiArray':Float32MultiArray, 'std_msgs/Int64':Int64, 'std_msgs/Float64':Float64}
singletypeList = ['std_msgs/Int32', 'std_msgs/Float32', 'std_msgs/Int64', 'std_msgs/Float64']
multitypeList = ['std_msgs/Int32MultiArray', 'std_msgs/Float32MultiArray', 'std_msgs/Int64MultiArray', 'std_msgs/Float64MultiArray']

class tkFrame:
    def __init__(self, win, name, type, PS, reorderCommand):
        self.win = win
        self.frm = tk.Frame(win)
        self.topic_name = name
        self.topic_type = type
        self.PS = PS
        self.RC = reorderCommand
        self.liveFlag = False
        tk.Button(self.frm, text = FRAME_BUTTON_TEXT[0], command = lambda: self.Frame_Button_Command(0)).grid(row = 0, column = 0)
        tk.Button(self.frm, text = FRAME_BUTTON_TEXT[1], command = lambda: self.Frame_Button_Command(1)).grid(row = 1, column = 0)
        tk.Button(self.frm, text = FRAME_BUTTON_TEXT[2], command = lambda: self.Frame_Button_Command(2)).grid(row = 0, column = 1)
        tk.Button(self.frm, text = FRAME_BUTTON_TEXT[3], command = lambda: self.Frame_Button_Command(3)).grid(row = 1, column = 1)
        tk.Button(self.frm, text = FRAME_BUTTON_TEXT[4], command = lambda: self.Frame_Button_Command(4)).grid(row = 0, column = 2)
        tk.Button(self.frm, text = FRAME_BUTTON_TEXT[5], command = lambda: self.Frame_Button_Command(5)).grid(row = 1, column = 2)
        
        self.L = tk.Label(self.frm, text = self.topic_name)
        self.L.grid(row = 0, column = 3, padx = 5)
        self.L2 = tk.Label(self.frm, text = self.topic_type)
        self.L2.grid(row = 1, column = 3, padx = 5)
        self.L3 = tk.Label(self.frm, text = '')
        self.L3.grid(row = 0, column = 4, rowspan = 2)
        

        #self.Sub = rosSub('/ran', Int32, self.cb)
        #self.Sub.start()

    def __del__(self):
        self.endTopic()
        self.frm.destroy()
        

    def Frame_Button_Command(self, commandNum):
        if commandNum <=4:
            self.RC(self.order, commandNum)
            if commandNum == 4:
                self.frm.destroy()
        elif commandNum == 5:
            self.restart()

    def grid(self, r):
        self.order = r
        #self.L2.config(text=str(r))
        self.frm.grid(row = r, column = 0, pady = 5, sticky = 'W')

    
    def regrid(self, r):
        self.frm.grid_forget()
        self.order = r
        #self.L2.config(text=str(r))
        self.frm.grid(row = r, column = 0, pady = 5, sticky = 'W')

    def cb(self, data):
        if self.topic_type in singletypeList:
            self.L3.config(text=str(data.data))
        if self.topic_type in multitypeList:
            data = [str(i) for i in data.data]
            data = '\n'.join(data)
            self.L3.config(text=str(data))

    def getTopicName(self):
        return self.topic_name
    def getTopicType(self):
        return self.topic_type
    def getTopicPS(self):
        return self.PS

    def startTopic(self):
        if self.liveFlag == True:
            return
        if self.PS == 'P' or self.PS == 'p':
            self.Topic = rosPub(name, type)
            self.liveFlag = True
        elif self.PS == 'S' or self.PS == 's':
            self.Topic = rosSub(self.topic_name, typeMap[self.topic_type], self.cb)
            self.Topic.start()
            self.liveFlag = True

    def endTopic(self):
        if self.liveFlag == False:
            return
        self.Topic.end()
        self.liveFlag == False

    def restart(self):
        if self.PS == 'S' or self.PS == 's':
            if self.liveFlag == True:
                self.Topic.end()
            self.Topic = rosSub(self.topic_name, typeMap[self.topic_type], self.cb)
            self.Topic.start()
            self.liveFlag = True
