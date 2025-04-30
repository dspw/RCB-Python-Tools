# DSP Wireless, Inc. - DSPW - Robert Paugh - 04/28/25

import requests

# import tkinter module 
from tkinter import *

# Following will import tkinter.ttk module and 
# automatically override all the widgets 
# which are present in tkinter module. 
from tkinter.ttk import *

from time import sleep

# Create Object
root = Tk() 

# Initialize tkinter window
root.title("DSPW RCB Wi-Fi Event Trigger")
root.geometry('420x180')

# Variables
timeOut = float(2.5) # HTTP POST timout
tglTime = float(0.5) # time(sec) between toggle event high/low
loopTime = int(1500) # loop time in msec

#RCB-WiFi Events start at 0. In OE Events start at 1
eventNumStr = "7" # Event 6 is = Event 7 in OE GUI

dataSet ='__SL_P_UDI,S6' # Post message to SET Event 6 (OE event 7)
dataClr = '__SL_P_UDI,C6' # Post message to CLEAR Event 6  (OE event 7)

# If only have 1 RCB WiFi device, edit/delete things not used to simplify the script
numRcb = 2 # Set to 2 or 4 depending on number of RCB WiFi devices.

# variable used in the checkbox
enable = IntVar()

# Button Functions
#Function is named using the last 2 digits of IP number, ex. .93
def toggle91():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.91:80', headers=headers, data=dataSet, timeout=timeOut)
    sleep(tglTime) # minimum time length of event toggle
    response = requests.post('http://192.168.0.91:80', headers=headers, data=dataClr, timeout=timeOut)
    
def toggle92():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataSet, timeout=timeOut)
    sleep(tglTime) 
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataClr, timeout=timeOut)

def toggle93():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataSet, timeout=timeOut)
    sleep(tglTime) 
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataClr, timeout=timeOut)

def toggle94():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.94:80', headers=headers, data=dataSet, timeout=timeOut)
    sleep(tglTime) 
    response = requests.post('http://192.168.0.94:80', headers=headers, data=dataClr, timeout=timeOut)    

   
def toggleBoth():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataSet, timeout=timeOut)
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataSet, timeout=timeOut)
    sleep(tglTime) # minimum time length of event toggle
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataClr, timeout=timeOut)
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataClr, timeout=timeOut)    

def set92():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataSet, timeout=timeOut)

def clear92():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataClr, timeout=timeOut)

def set93():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataSet, timeout=timeOut)

def clear93():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }  
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataClr, timeout=timeOut)

def setBoth():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataSet, timeout=timeOut)
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataSet, timeout=timeOut)


def clearBoth():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataClr, timeout=timeOut)
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataClr, timeout=timeOut)

def setFour():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataSet, timeout=timeOut)
    response = requests.post('http://192.168.0.94:80', headers=headers, data=dataSet, timeout=timeOut)
    response = requests.post('http://192.168.0.91:80', headers=headers, data=dataSet, timeout=timeOut)
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataSet, timeout=timeOut)

def clearFour():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post('http://192.168.0.93:80', headers=headers, data=dataClr, timeout=timeOut)
    response = requests.post('http://192.168.0.94:80', headers=headers, data=dataClr, timeout=timeOut)
    response = requests.post('http://192.168.0.91:80', headers=headers, data=dataClr, timeout=timeOut)
    response = requests.post('http://192.168.0.92:80', headers=headers, data=dataClr, timeout=timeOut)
    

def enableLoop():
    if enable.get() == 1: # get checkbox on/off
        if numRcb == 2:
            setBoth()
            sleep(tglTime)
            clearBoth()
        elif numRcb == 4:
            setFour()
            sleep(tglTime)
            clearFour()
            
        root.after('loopTime', enableLoop)
         #root.after(1500, enableLoop)
        
    #else:
     #   cBoxEnable.config(text = "Loop Off")

# Create and Configure UI
btn10 = Button(root, text='Set 93', command = set93)
btn10.grid(row=1,column=0, padx=0, pady=0)
btn20 = Button(root, text = 'Set 92 ', command = set92)
btn20.grid(row=2,column=0, padx=0, pady=0)
btn30 = Button(root, text = 'Set All', command = setBoth)
btn30.grid(row=3,column=0, padx=0, pady=0)

btn11 = Button(root, text='Clear 93', command = clear93)
btn11.grid(row=1,column=1, padx=0, pady=0)
btn21 = Button(root, text = 'Clear 92 ', command = clear92)
btn21.grid(row=2,column=1, padx=0, pady=0)
btn31 = Button(root, text = 'Clear All', command = clearBoth)
btn31.grid(row=3,column=1, padx=0, pady=0)

btn12 = Button(root, text='Toggle 93', command = toggle93)
btn12.grid(row=1,column=2, padx=30, pady=10)
btn22 = Button(root, text = 'Toggle 92 ', command = toggle92)
btn22.grid(row=2,column=2, padx=30, pady=10)
btn32 = Button(root, text = 'Toggle All', command = toggleBoth)
btn32.grid(row=3,column=2, padx=30, pady=10)

lblEventNum = Label(text="Event# " + eventNumStr + " - Time "+ str(tglTime) +" sec")
lblEventNum.grid(row=0, column=0,padx=5, pady=5)

cBoxEnable = Checkbutton(root, text="Loop", variable = enable, onvalue=1, offvalue = 0, command=enableLoop)
cBoxEnable.grid(row=0, column=2, padx=5, pady=5)

root.after(100, enableLoop)


root.mainloop() 
