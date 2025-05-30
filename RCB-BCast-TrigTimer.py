# DSP Wireless, Inc. - DSPW - Robert Paugh - 04/26/25

# Using the OE GUI HTTP Server
# this UI sends Broadcast messages to a DSPW RCB Wi-Fi Plugin
# Press Clear Button - Event number and Pulse Timer = 0 is sent to the plugin.
# Press Pulse Button - Event number and Pulse Timer value(ms) is sent to the plugin,
# Loop Checkbox - When selected will send Pulse every Loop Time value.
# Requires that OE GUI acquisition has started OK.

import requests
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

from tkinter import ttk

from time import sleep
from decimal import Decimal
from tkinter import messagebox

# === Tkinter Setup ===
geoWidth = 405
geoHeight = 200
geometry = "%dx%d" % (geoWidth,geoHeight)

root = tk.Tk()
root.title("    DSPW RCB Wi-Fi    Bcast Event Trigger w/Timer")
root.geometry(geometry)
root.minsize(geoWidth, geoHeight)
root.maxsize(geoWidth, geoHeight)
root.pack_propagate(False)
root.grid_propagate(False)

# === Draw Line ===
canvas = tk.Canvas(root, width=geoWidth, height=geoHeight)
canvas.pack()
canvas.create_line(10, 105, 390, 105, width=2)

# === Variables ===
event_input = StringVar(value="1")
pulse_input = StringVar(value="0.5")
loop_input = StringVar(value="1.0")
enable = IntVar()

ipNumber = '127.0.0.1'   #"192.168.0.220"
eventNumStr = "1"
pulseTime = 0.5 #500
loopTime = 1.0

# === Labels ===
Label(text="Status", anchor="w").grid(row=3, column=0, padx=10, sticky="w")
Label(text="Event # ").grid(row=0, column=0, padx=10,sticky="w")
Label(text="Pulse Time(s)").grid(row=1, column=0, padx=10, sticky="w")
Label(text="Loop Time(s)").grid(row=2, column=0, padx=10, sticky="w")
Label(text='Press "Return Key" to enter values.').grid(row=6, column=0, columnspan=4, padx=10, pady=5, sticky="w")
Label(text='v0.1.0').grid(row=6,column=3, sticky="e")


Label(text="IP Number").grid(row=4, column=0, padx=10, sticky="w")
lblIpNum = Label(text= ipNumber, justify="left")
lblIpNum.grid(row=4, column=1, padx=00, sticky="w")

lblEventNum = Label(text="Event # 1", justify="left")
lblEventNum.grid(row=5, column=0, padx=10, sticky="w")

lblPulseNum = Label(text="Pulse 0.5s", justify="left", width=10)
lblPulseNum.grid(row=5, column=1, sticky="w")

lblLoopNum = Label(text="Loop 1s", justify="center")
lblLoopNum.grid(row=5, column=2)

lblLoopOnOff = Label(text="Loop is Off")
lblLoopOnOff.grid(row=5, column=3, padx=10)

# === Entry Widgets ===
event_box = Entry(root, textvariable=event_input, width=1)
event_box.grid(row=0, column=1, sticky="w")

pulse_box = Entry(root, textvariable=pulse_input, width=5)
pulse_box.grid(row=1, column=1, sticky="w")

loop_box = Entry(root, textvariable=loop_input, width=5)
loop_box.grid(row=2, column=1, sticky="w")

# === Functions ===
def get_event(event=None):
    global eventNumStr
    val = event_box.get()
    if not val.isdigit() or not (1 <= int(val) <= 8):
        val = "1"
        event_box.delete(0, END)
        event_box.insert(0, val)

    eventNumStr = val
    lblEventNum.config(text=f"Event # {val}")
    #print("Event input:", val)
    return val

def get_pulseTime(event=None):
    global pulseTime
    val = pulse_box.get()[:5]
    try:
        val = float(val)
        if 0.01 <= val <= 10000:
            val = Decimal(val).quantize(Decimal("0.000"))
        else:
            raise ValueError
    except ValueError:
        val = Decimal("0.5")
    
    pulse_box.delete(0, END)
    pulse_box.insert(0, str(val))
    pulseTime = float(val)
    lblPulseNum.config(text=f"Pulse {val}s")
    #print("Pulse Time input:", val)
    return val

def get_loopTime(event=None):
    global loopTime
    try:
        val = float(loop_box.get())
        if 0.5 <= val <= 2880:
            formatted = f"{val:.3f}"
        else:
            raise ValueError
    except ValueError:
        formatted = "1.000"

    loop_box.delete(0, END)
    loop_box.insert(0, formatted)
    loopTime = float(formatted)
    lblLoopNum.config(text=f"Loop {formatted}s")
    #print("Loop Time input:", formatted)
    return formatted

# Initial Input Updates
event_box.bind('<Return>', get_event)
pulse_box.bind('<Return>', get_pulseTime)
loop_box.bind('<Return>', get_loopTime)

eventNumStr = get_event()
pulseNumStr = get_pulseTime()
loopNumStr = get_loopTime()

# === Event Controls ===
def setEvent():  # used for Pulse Button
    get_event()
    pulseTimeMs = pulseTime * 1000
    ipFormatted = "http://" + ipNumber + ":37497/api/message"
    #print("IP Number input:", ipFormatted)
    #print("Pulse Time input (ms):", pulseTimeMs)
    try:
        response = requests.put("http://" + ipNumber + ":37497/api/message",
                # response = requests.put("http://localhost:37497/api/message",
                 json={"text": f"DSPW RCB TIMERPULSE {eventNumStr} {pulseTimeMs}"})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        enable.set(0)
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An error occurred: {e}")
    except Exception as e:
        enable.set(0)
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        
def clearEvent():
    get_event()
    
    try:
        response = requests.put("http://" + ipNumber + ":37497/api/message",
        #   response = requests.put("http://localhost:37497/api/message",
                 json={"text": f"DSPW RCB TRIGGER {eventNumStr} 0"})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        enable.set(0)
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An error occurred: {e}")
    except Exception as e:
        enable.set(0)
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
def enableLoop():
    get_loopTime()
    if enable.get() == 1:
        lblLoopOnOff.config(text="Loop is On")
        setEvent()
        
        root.after(int((loopTime * 1000) + (pulseTime * 1000)), enableLoop)
    else:
        lblLoopOnOff.config(text="Loop is Off")
        enable.set(0)
        

# === Buttons and Checkbox ===
#Button(root, text='Set', width=5, command=setEvent).grid(row=0, column=2)
Button(root, text='Clear', width=5, command=clearEvent).grid(row=0, column=2, padx=10, pady=0)
Button(root, text='Pulse', width=5, command=setEvent).grid(row=1, column=2, pady=5)

cBoxLoopEnable = Checkbutton(root, text="Loop", variable=enable, onvalue=1, offvalue=0, command=enableLoop)
cBoxLoopEnable.grid(row=2, column=2, pady=10)

# === Start UI Loop ===
#root.after(100, enableLoop)
root.mainloop()
