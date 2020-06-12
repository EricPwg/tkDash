#!/usr/bin/env python2

import Tkinter as tk
from tkFrame import *
from rosPubSub import *
import rospy
from subprocess import Popen, PIPE
import os
import json

tkFList = []
topicDict = {}
tkSList = []
tkPList = []

win = tk.Tk()
win.title('main')
win.geometry('800x400')

frm_l = tk.Frame(win)
frm_r = tk.Frame(win)
frm_r.grid(row = 0, column = 0, padx = 20)
frm_l.grid(row = 0, column = 1, sticky = 'N')

def reorderCommand(id, command_num):
    global tkFList
    if command_num == 0:
        if id == 0:
            pass
        else:
            tkFList[id].regrid(id-1)
            tkFList[id-1].regrid(id)
            tkFList[id], tkFList[id-1] = tkFList[id-1], tkFList[id]
    elif command_num == 1:
        if id == len(tkFList)-1:
            pass
        else:
            tkFList[id].regrid(id+1)
            tkFList[id+1].regrid(id)
            tkFList[id], tkFList[id+1] = tkFList[id+1], tkFList[id]
    elif command_num == 2:
        if id == 0:
            pass
        else:
            tkFList[id].regrid(0)
            for i in range(0, id):
                tkFList[i].regrid(i+1)
            tt = tkFList.pop(id)
            tkFList.insert(0, tt)
    elif command_num == 3:
        if id == len(tkFList)-1:
            pass
        else:
            tkFList[id].regrid(len(tkFList)-1)
            for i in range(id+1, len(tkFList)):
                tkFList[i].regrid(i-1)
            tt = tkFList.pop(id)
            tkFList.append(tt)
    elif command_num == 4:
        PS = tkFList[id].getTopicPS()
        if PS == 's' or PS =='S':
            tkSList.pop(tkSList.index(tkFList[id].getTopicName()))
        elif PS == 'p' or PS =='P':
            tkPList.pop(tkSList.index(tkFList[id].getTopicName()))
        if id == len(tkFList)-1:
            tt = tkFList.pop(id)
        else:
            for i in range(id+1, len(tkFList)):
                tkFList[i].regrid(i-1)
            tt = tkFList.pop(id)
        tt.endTopic()

def loadC():
    global tkFList, topicDict, tkSList, tkPList
    lwin = tk.Tk()
    lwin.title('Load')

    l = tk.Label(lwin, text = '')
    l.grid(row = 0, column = 0, columnspan = 4)

    sbll = tk.Scrollbar(lwin)
    sbld = tk.Scrollbar(lwin, orient = 'horizontal')
    lbl = tk.Listbox(lwin, width=20, height=10, selectmode=tk.SINGLE, yscrollcommand = sbll.set, xscrollcommand = sbld.set)
    sbll.config(command = lbl.yview)
    sbld.config(command = lbl.xview)
    lbl.grid(row = 1, column = 0)
    sbll.grid(row = 1, column = 1, sticky = 'ns')
    sbld.grid(row = 2, column = 0, sticky = 'we')

    sbrl = tk.Scrollbar(lwin)
    sbrd = tk.Scrollbar(lwin, orient = 'horizontal')
    lbr = tk.Listbox(lwin, width=20, height=10, selectmode=tk.SINGLE, yscrollcommand = sbrl.set, xscrollcommand = sbrd.set)
    sbrl.config(command = lbr.yview)
    sbrd.config(command = lbr.xview)
    lbr.grid(row = 1, column = 2)
    sbrl.grid(row = 1, column = 3, sticky = 'ns')
    sbrd.grid(row = 2, column = 2, sticky = 'we')

    def listdir(p):
        #print(p)
        if os.path.isdir(p) == False:
            return
        for root, dirs, files in os.walk(p, topdown=True):
            break
        s = lbl.size()
        lbl.delete(0, s)
        s = lbr.size()
        lbr.delete(0, s)

        lbl.insert('end', '..')
        for i in dirs:
            lbl.insert('end', i)
        for i in files:
            if '.tkd' in i:
                lbr.insert('end', i)

    def enterC():
        cs = lbl.curselection()
        if len(cs) == 0:
            return
        cs = lbl.get(cs)
        pc = l.config()['text'][-1]
        p = pc+'/'+cs
        ap = os.path.abspath(p)
        l.config(text = ap)
        listdir(ap)
    
    def openC():
        global tkFList, topicDict, tkSList, tkPList
        cs = lbr.curselection()
        if len(cs) == 0:
            return
        cs = lbr.get(cs)
        pc = l.config()['text'][-1]
        p = pc+'/'+cs
        f = open(p)
        dic = json.load(f)
        print(dic)
        while len(tkFList) > 0:
            PS = tkFList[0].getTopicPS()
            if PS == 's' or PS =='S':
                tkSList.pop(tkSList.index(tkFList[0].getTopicName()))
            elif PS == 'p' or PS =='P':
                tkPList.pop(tkSList.index(tkFList[0].getTopicName()))
            tt = tkFList.pop(0)
            tt.__del__()

        for i in dic:
            tkF = tkFrame(frm_l, dic[i]['name'], dic[i]['type'], dic[i]['PS'], reorderCommand)
            tkF.grid(len(tkFList))
            tkF.startTopic()
            tkFList.append(tkF)
            tkSList.append(dic[i]['name'])
        lwin.destroy()

    cwd = os.getcwd()
    l.config(text = cwd)
    listdir(cwd)

    b = tk.Button(lwin, text = 'Enter', command = enterC)
    b.grid(row = 3, column = 0)
    sb = tk.Button(lwin, text = 'Load', command = openC)
    sb.grid(row = 3, column = 2)
        
    lwin.mainloop()

def saveC():
    global tkFList, topicDict, tkSList, tkPList
    lwin = tk.Tk()
    lwin.title('Save')

    l = tk.Label(lwin, text = '')
    l.grid(row = 0, column = 0, columnspan = 4)
    se = tk.Entry(lwin)
    se.grid(row = 1, column = 0, columnspan = 2, sticky = 'e')
    tk.Label(lwin, text = '.tkd').grid(row = 1, column = 2, columnspan = 2, sticky = 'w')

    sbll = tk.Scrollbar(lwin)
    sbld = tk.Scrollbar(lwin, orient = 'horizontal')
    lbl = tk.Listbox(lwin, width=20, height=10, selectmode=tk.SINGLE, yscrollcommand = sbll.set, xscrollcommand = sbld.set)
    sbll.config(command = lbl.yview)
    sbld.config(command = lbl.xview)
    lbl.grid(row = 2, column = 0)
    sbll.grid(row = 2, column = 1, sticky = 'ns')
    sbld.grid(row = 3, column = 0, sticky = 'we')

    sbrl = tk.Scrollbar(lwin)
    sbrd = tk.Scrollbar(lwin, orient = 'horizontal')
    lbr = tk.Listbox(lwin, width=20, height=10, selectmode=tk.SINGLE, yscrollcommand = sbrl.set, xscrollcommand = sbrd.set)
    sbrl.config(command = lbr.yview)
    sbrd.config(command = lbr.xview)
    lbr.grid(row = 2, column = 2)
    sbrl.grid(row = 2, column = 3, sticky = 'ns')
    sbrd.grid(row = 3, column = 2, sticky = 'we')

    def listdir(p):
        #print(p)
        if os.path.isdir(p) == False:
            return
        for root, dirs, files in os.walk(p, topdown=True):
            break
        s = lbl.size()
        lbl.delete(0, s)
        s = lbr.size()
        lbr.delete(0, s)

        lbl.insert('end', '..')
        for i in dirs:
            lbl.insert('end', i)
        for i in files:
            if '.tkd' in i:
                lbr.insert('end', i)

    def enterC():
        cs = lbl.curselection()
        if len(cs) == 0:
            return
        cs = lbl.get(cs)
        pc = l.config()['text'][-1]
        p = pc+'/'+cs
        ap = os.path.abspath(p)
        l.config(text = ap)
        listdir(ap)

    def sC():
        global tkFList, topicDict, tkSList, tkPList
        ce = se.get()
        if len(ce) == 0:
            return
        dic = {}
        for i in tkFList:
            dd = {}
            dd['name'] = i.getTopicName()
            dd['type'] = i.getTopicType()
            dd['PS'] = i.getTopicPS()
            dic[i.getTopicName()] = dd
            print(dd)
        print(dic)
        pc = l.config()['text'][-1]
        p = pc+'/'+ce+'.tkd'
        c = open(p, 'w')
        json.dump(dic, c)
        c.close()
        lwin.destroy()
        
    
    cwd = os.getcwd()
    l.config(text = cwd)
    listdir(cwd)

    eb = tk.Button(lwin, text = 'Enter', command = enterC)
    eb.grid(row = 4, column = 0)
    sb = tk.Button(lwin, text = 'Save', command = sC)
    sb.grid(row = 4, column = 2)
        
    lwin.mainloop()

def tlistC():
    global lb, topicDict, tkFList, tkSList, tkPList
    s = lb.size()
    lb.delete(0, s)
    proc = Popen('rostopic list', stdout = PIPE, shell = True)
    tmp = proc.stdout.read()
    tmp = tmp.split()

    for i in range(len(tmp)):
        proc = Popen('rostopic type '+tmp[i], stdout = PIPE, shell = True)
        g = proc.stdout.read()
        topicN = g.split()[0]
        if topicN in typeMap:
            tL = [topicN]
            topicDict[tmp[i]] = tL
    #print(topicDict)
    for i in topicDict:
        s = '['
        if i in tkSList:
            s = s+'s'
        else:
            s = s+'-'
        if i in tkPList:
            s = s+'p'
        else:
            s = s+'-'
        s = s+'] '
        s = s+i+' {'
        s = s+topicDict[i][0]+'}'
        #print(s)
        lb.insert('end', s)

def sC():
    global tkFList, lb, topicDict, tkSList
    cs = lb.curselection()
    if len(cs) == 0:
        return
    cs = lb.get(cs)
    tn = cs.split()[1]
    #print(tn)
    if tn in tkSList:
        return
    tkF = tkFrame(frm_l, tn, topicDict[tn][0], 'S', reorderCommand)
    tkF.grid(len(tkFList))
    tkF.startTopic()
    tkFList.append(tkF)
    tkSList.append(tn)
    #print(tkFList)

rospy.init_node('tkDash', anonymous=True)

loadB = tk.Button(frm_r, text = 'Load', command = loadC)
loadB.grid(row = 0, column = 0, sticky="nsew")
saveB = tk.Button(frm_r, text = 'Save', command = saveC)
saveB.grid(row = 0, column = 1, sticky="nsew")
tlistB = tk.Button(frm_r, text = 'List topics', command = tlistC)
tlistB.grid(row = 1, column = 0, columnspan = 2, sticky="nsew")
sB = tk.Button(frm_r, text = 'Subscribe >>', command = sC)
sB.grid(row = 2, column = 3)
sB = tk.Button(frm_r, text = 'Publish >>')
sB.grid(row = 3, column = 3)

sb1 = tk.Scrollbar(frm_r)
sb2 = tk.Scrollbar(frm_r)
lb = tk.Listbox(frm_r, width=20, height=10, selectmode=tk.SINGLE, yscrollcommand = sb1.set, xscrollcommand = sb2.set)
sb1.config(command = lb.yview)
sb2.config(command = lb.xview, orient = 'horizontal')
lb.grid(row = 2, column = 0, rowspan = 2, columnspan = 2, sticky = tk.E)
sb1.grid(row = 2, column = 2, rowspan = 2, sticky = tk.N+tk.S)
sb2.grid(row = 4, column = 0, columnspan = 2, sticky = tk.E+tk.W)

'''
num = 5
for i in range(num):
    tkF = tkFrame(frm_l, i, reorderCommand)
    tkF.grid(i)
    tkFList.append(tkF)
'''

win.mainloop()
