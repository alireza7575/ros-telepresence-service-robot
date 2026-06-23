#!/usr/bin/env python

import os
import signal
import subprocess
import tkinter as tk
import string, time
import json

global config
global webServer
global camera
global thermalCamera
global rosBridge
global rosSerial
global audioServerlId
global audioServer
global audioClientlId
global audioClient
global webServerId
global cameraId
global thermalCameraId
global rosBridgeId
global rosSerialId

webServer = "python server.py"
audioClientlId = None
audioClient = "python client.py"
webServerId = None


root= tk.Tk()

canvas1 = tk.Canvas(root, width = 700, height = 600, bg = 'gray90', relief = 'raised')
canvas1.pack()


class Application(tk.Frame):

    def __init__(self, parent):
        loadconfig()
        self.parent = parent
        ### put HERE the "onLoad()" code ###
        
        tk.Frame.__init__(self, parent)
    #    self.create_widgets()
        
def saveconfig():
    global config
    config = {'robotIp': textentry.get()}
    print(config)
    with open('config.json', 'w') as f:
        json.dump(config, f)

def loadconfig():
    global config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            print(config)
            textentry.insert (0,str(config['robotIp']))
    except:
        pass

def kill (task):
    task.terminate()

def run (command):
    try:
        return subprocess.Popen(command.split(" "))
    except :
        return None

def runWebServer():
    global webServerId
    global webServer
    if webServerId == None:
        webServerId = run(webServer)
        if webServerId != None:
            label1.config(bg="#007bff",text="running")
        else:
            label1.config(bg="#ffc107",text="err")

def killWebServer():
    global webServerId

    if webServerId != None:
        label1.config(bg="#dc3545",text="stop")
        kill(webServerId)
        webServerId = None


def runAudioClient():
    global audioClientlId
    global audioClient
    if audioClientlId == None:

        audioClientlId = run(audioClient+" "+config['robotIp'])
        if audioClientlId != None:
            label6.config(bg="#007bff",text="running")
        else:
            label6.config(bg="#ffc107",text="err")

def killAudioClient():
    global audioClientlId
    if audioClientlId != None:
        label6.config(bg="#dc3545",text="stop")
        kill(audioClientlId)
        audioClientlId = None

label11 = tk.Label(width=10,text="Server", font=('helvetica', 20, 'bold'))
button1 = tk.Button(text='      Run      ', command=runWebServer, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button2 = tk.Button(text='      kill     ', command=killWebServer, bg='#dc3545',fg='white', font=('helvetica', 20, 'bold'))
label1 = tk.Label(width=10,height=2, text='not started',font=('helvetica', 20, 'bold') )



label16 = tk.Label(width=10,text="Audio client",font=('helvetica', 20, 'bold') )
button11 = tk.Button(text='      Run      ', command=runAudioClient, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button12 = tk.Button(text='      kill     ', command=killAudioClient, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label6 = tk.Label(width=10,height=2, text='not started',font=('helvetica', 20, 'bold'))




label20 = tk.Label(text="robot ip:",font=('helvetica', 20, 'bold'))
textentry = tk.Entry(font=('helvetica', 20, 'bold') )
button20 = tk.Button(text='      save the config      ', command=saveconfig, font=('helvetica', 20))

canvas1.create_window(90, 50, window=label11)
canvas1.create_window(270, 50, window=button1)
canvas1.create_window(430, 50, window=button2)
canvas1.create_window(600, 50, window=label1)

canvas1.create_window(90, 150, window=label16)
canvas1.create_window(270, 150, window=button11)
canvas1.create_window(430, 150, window=button12)
canvas1.create_window(600, 150, window=label6)

canvas1.create_window(70, 250, window=label20)
canvas1.create_window(290, 250, window=textentry)
canvas1.create_window(540, 250, window=button20)

app = Application(root)
app.mainloop()
