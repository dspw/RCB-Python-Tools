# DSP Wireless, Inc. - DSPW - Robert Paugh - 04/24/25

# Using the OE GUI HTTP Server
# this UI sends Broadcast messages to a DSPW RCB Wi-Fi Plugin
# Event number and Timer value sent to the plugin when Press Start Button
# Requires that OE GUI acquisition has started OK.

import requests
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from time import sleep
from decimal import Decimal
from tkinter import messagebox

# === Tkinter Setup ===
geoWidth = 315
geoHeight = 140
geometry = "%dx%d" % (geoWidth,geoHeight)

root = tk.Tk()
root.title("DSPW RCB Wi-Fi  Bcast Event Timer")
#root.geometry('310x140')
root.geometry(geometry)
#root.minsize(310, 140)
#root.maxsize(310, 140)
root.minsize(geoWidth, geoHeight)
root.maxsize(geoWidth, geoHeight)

root.pack_propagate(False)
root.grid_propagate(False)

# === Variables ===
event_input = StringVar(value="1")
pulse_input = StringVar(value="500")
enable = IntVar()

eventNumStr = "1"
pulseTime = 0.5

# === Draw Line ===
#canvas = tk.Canvas(root, width=310, height=140)
canvas = tk.Canvas(root, width=geoWidth, height=geoHeight)
canvas.pack()
canvas.create_line(10, 63, 305, 63, width=2)

# === Labels ===
Label(text="Status", anchor="w").grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
Label(text="Event # ").grid(row=0, column=0, padx=10, sticky="w")
Label(text="Pulse (ms) ").grid(row=1, column=0, padx=10, sticky="w")

lblEventNum = Label(text="Event # 1", justify="left")
lblEventNum.grid(row=3, column=0, padx=10, sticky="w")

lblPulseNum = Label(text="Pulse 0.5s", justify="left", width=10)
lblPulseNum.grid(row=3, column=1, sticky="w")

lblTimerOnOff = Label(text="Timer Off")
lblTimerOnOff.grid(row=3, column=2, padx=10)

Label(text='Press "Return Key" to enter values.').grid(row=5, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# === Entry Widgets ===
event_box = Entry(root, textvariable=event_input, width=1)
event_box.grid(row=0, column=1, sticky="w")

pulse_box = Entry(root, textvariable=pulse_input, width=6)
pulse_box.grid(row=1, column=1, sticky="w")

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
    val = pulse_box.get()
    try:
        val = float(val)
        if 0.001 <= val <= 10000:
            val = Decimal(val).quantize(Decimal("0"))
        else:
            raise ValueError
    except ValueError:
        val = Decimal("500")
    
    pulse_box.delete(0, END)
    pulse_box.insert(0, str(val))
    pulseTime = int(val)
    lblPulseNum.config(text=f"Pulse {val}ms")
    #print("Pulse Time input:", val)
    return val

# Initial Input Updates
event_box.bind('<Return>', get_event)
pulse_box.bind('<Return>', get_pulseTime)

eventNumStr = get_event()
pulseNumStr = get_pulseTime()

# === Event Controls ===
def setEvent():
    get_event()
    get_pulseTime()
   
    try:
        response = requests.put("http://localhost:37497/api/message",
                 json={"text": f"DSPW RCB TIMER {eventNumStr} {pulseTime}"})
        response.raise_for_status()
        lblTimerOnOff.config(text="Timer On")
    except requests.exceptions.RequestException as e:
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An error occurred: {e}")
    except Exception as e:
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def clearEvent():
    try:
        response = requests.put("http://localhost:37497/api/message",
                 json={"text": f"DSPW RCB TIMER {eventNumStr} 0"})
        response.raise_for_status()
        lblTimerOnOff.config(text="Timer Off")
    except requests.exceptions.RequestException as e:
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An error occurred: {e}")
    except Exception as e:
        print("HTTP Server Error. Check Server is enabled in OE GUI")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
     
# === Buttons and Checkbox ===
Button(root, text='Start', width=5, command=setEvent).grid(row=0, column=2)
Button(root, text='Stop', width=5, command=clearEvent).grid(row=1, column=2)

# === Start UI Loop ===
root.mainloop()
