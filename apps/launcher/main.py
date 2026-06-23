#!/usr/bin/env python

import os
import signal
import subprocess
import Tkinter as tk
import string, time
import json

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(REPO_ROOT, "config", "robot.local.json")
EXAMPLE_CONFIG_PATH = os.path.join(REPO_ROOT, "config", "robot.example.json")

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

webServer = "rosrun web_video_server web_video_server"
camera = "roslaunch astra_camera astra.launch"
rosBridge = "roslaunch rosbridge_server rosbridge_websocket.launch"
rosSerial = "rosrun rosserial_python serial_node.py /dev/ttyACM0"
thermalCamera = "roslaunch ros/launch/thermal_cam.launch"
thermalCameraId = None
audioServerlId = None
audioServer = "python apps/audio/server.py"
audioClientlId = None
audioClient = "python apps/audio/client.py"
webServerId = None
cameraId = None
rosBridgeId = None
rosSerialId = None

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
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

def loadconfig():
    global config
    try:
        config_path = CONFIG_PATH if os.path.exists(CONFIG_PATH) else EXAMPLE_CONFIG_PATH
        with open(config_path, 'r') as f:
            config = json.load(f)
            print(config)
            textentry.insert (0,str(config['robotIp']))
    except:
        pass

def kill (task):
    task.terminate()

def run (command):
    try:
        print(command.split(" "))
        return subprocess.Popen(command.split(" "), cwd=REPO_ROOT)
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

def runThermalCamera():
    global thermalCameraId
    global thermalCamera
    if thermalCameraId == None:

        thermalCameraId = run(thermalCamera)
        if thermalCameraId != None:
           label7.config(bg="#007bff",text="running")
        else:
            label7.config(bg="#ffc107",text="err")

def killThermalCamera():
    global thermalCameraId
    if thermalCameraId != None:
        label7.config(bg="#dc3545",text="stop")
        kill(thermalCameraId)
        thermalCameraId = None

def runCamera():
    global cameraId
    global camera
    if cameraId == None:

        cameraId = run(camera)
        if cameraId != None:
           label2.config(bg="#007bff",text="running")
        else:
            label2.config(bg="#ffc107",text="err")

def killCamera():
    global cameraId
    if cameraId != None:
        label2.config(bg="#dc3545",text="stop")
        kill(cameraId)
        cameraId = None

def runRosBridge():
    global rosBridgeId
    global rosBridge
    if rosBridgeId == None:

        rosBridgeId = run(rosBridge)
        if rosBridgeId != None:
            label3.config(bg="#007bff",text="running")
        else:
            label3.config(bg="#ffc107",text="err")

def killRosBridge():
    global rosBridgeId
    if rosBridgeId != None:
        label3.config(bg="#dc3545",text="stop")
        kill(rosBridgeId)
        rosBridgeId = None

def runRosSerial():
    global rosSerialId
    global rosSerial
    if rosSerialId == None:

        rosSerialId = run(rosSerial)
        if rosSerialId != None:
            label4.config(bg="#007bff",text="running")
        else:
            label4.config(bg="#ffc107",text="err")

def killRosSerial():
    global rosSerialId
    if rosSerialId != None:
        label4.config(bg="#dc3545",text="stop")
        kill(rosSerialId)
        rosSerialId = None

def runAudioServer():
    global audioServerlId
    global audioServer
    if audioServerlId == None:

        audioServerlId = run(audioServer)
        if audioServerlId != None:
            label5.config(bg="#007bff",text="running")
        else:
            label5.config(bg="#ffc107",text="err")

def killAudioServer():
    global audioServerlId
    if audioServerlId != None:
        label5.config(bg="#dc3545",text="stop")
        kill(audioServerlId)
        audioServerlId = None

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

label11 = tk.Label(width=10,text="WebServer", font=('helvetica', 20, 'bold'))
button1 = tk.Button(text='      Run      ', command=runWebServer, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button2 = tk.Button(text='      kill     ', command=killWebServer, bg='#dc3545',fg='white', font=('helvetica', 20, 'bold'))
label1 = tk.Label(width=10,height=2, text='not started',font=('helvetica', 20, 'bold') )

label12 = tk.Label(width=10,text="Camera",font=('helvetica', 20, 'bold') )
button3 = tk.Button(text='      Run      ', command=runCamera, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button4 = tk.Button(text='      kill     ', command=killCamera, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label2 = tk.Label(width=10,height=2, text='not started' ,font=('helvetica', 20, 'bold'))

label13 = tk.Label(width=10,text="RosBridge" ,font=('helvetica', 20, 'bold'))
button5 = tk.Button(text='      Run      ', command=runRosBridge, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button6 = tk.Button(text='      kill     ', command=killRosBridge, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label3 = tk.Label(width=10,height=2, text='not started',font=('helvetica', 20, 'bold') )

label14 = tk.Label(width=10,text="RosSerial" ,font=('helvetica', 20, 'bold'))
button7 = tk.Button(text='      Run      ', command=runRosSerial, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button8 = tk.Button(text='      kill     ', command=killRosSerial, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label4 = tk.Label(width=10,height=2, text='not started' ,font=('helvetica', 20, 'bold'))

label15 = tk.Label(width=12,text="Audio server",font=('helvetica', 20, 'bold') )
button9 = tk.Button(text='      Run      ', command=runAudioServer, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button10 = tk.Button(text='      kill     ', command=killAudioServer, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label5 = tk.Label(width=10,height=2, text='not started',font=('helvetica', 20, 'bold'))

label16 = tk.Label(width=12,text="Audio client",font=('helvetica', 20, 'bold') )
button11 = tk.Button(text='      Run      ', command=runAudioClient, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button12 = tk.Button(text='      kill     ', command=killAudioClient, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label6 = tk.Label(width=10,height=2, text='not started',font=('helvetica', 20, 'bold'))

label17 = tk.Label(width=14,text=" Thermal camera",font=('helvetica', 18, 'bold') )
button13 = tk.Button(text='      Run      ', command=runThermalCamera, bg='#007bff', fg='white', font=('helvetica', 20, 'bold'))
button14 = tk.Button(text='      kill     ', command=killThermalCamera, bg='#dc3545', fg='white', font=('helvetica', 20, 'bold'))
label7 = tk.Label(width=10,height=2, text='not started' ,font=('helvetica', 20, 'bold'))


label20 = tk.Label(text="robot ip:",font=('helvetica', 20, 'bold'))
textentry = tk.Entry(font=('helvetica', 20, 'bold') )
button20 = tk.Button(text='      save the config      ', command=saveconfig, font=('helvetica', 20))

canvas1.create_window(90, 50, window=label11)
canvas1.create_window(270, 50, window=button1)
canvas1.create_window(430, 50, window=button2)
canvas1.create_window(600, 50, window=label1)

canvas1.create_window(90, 110, window=label12)
canvas1.create_window(270, 110, window=button3)
canvas1.create_window(430, 110, window=button4)
canvas1.create_window(600, 110, window=label2)

canvas1.create_window(90, 170, window=label13)
canvas1.create_window(270, 170, window=button5)
canvas1.create_window(430, 170, window=button6)
canvas1.create_window(600, 170, window=label3)

canvas1.create_window(90, 230, window=label14)
canvas1.create_window(270, 230, window=button7)
canvas1.create_window(430, 230, window=button8)
canvas1.create_window(600, 230, window=label4)

canvas1.create_window(90, 290, window=label15)
canvas1.create_window(270, 290, window=button9)
canvas1.create_window(430, 290, window=button10)
canvas1.create_window(600, 290, window=label5)

canvas1.create_window(90, 350, window=label16)
canvas1.create_window(270, 350, window=button11)
canvas1.create_window(430, 350, window=button12)
canvas1.create_window(600, 350, window=label6)

canvas1.create_window(90, 410, window=label17)
canvas1.create_window(270, 410, window=button13)
canvas1.create_window(430, 410, window=button14)
canvas1.create_window(600, 410, window=label7)

canvas1.create_window(70, 470, window=label20)
canvas1.create_window(290, 470, window=textentry)
canvas1.create_window(540, 470, window=button20)

app = Application(root)
app.mainloop()
