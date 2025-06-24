# Robert Paugh - DSPW 

import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import requests
from open_ephys.control import OpenEphysHTTPServer
import json  

BASE_URL = "http://localhost:37497/api"

class OEControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Open Ephys Remote Control")
        self.gui = OpenEphysHTTPServer()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        btns = [
            ("Get Status", self.get_status),
            ("Idle", lambda: self.set_mode("IDLE")),  
            ("List Processors", self.list_processors),
            ("Acquire", lambda: self.set_mode("ACQUIRE")),
            ("Get Recording Info", self.get_recording),
            ("Record", lambda: self.set_mode("RECORD")),   
            ("Set Record Dir", self.set_record_dir),
            ("Broadcast Message", self.broadcast_message),
            ("Quit GUI", self.quit_gui),
        ]
        for i, (txt, cmd) in enumerate(btns):
            tk.Button(frame, text=txt, width=20, command=cmd).grid(row=i//2, column=i%2, padx=5, pady=5)

        self.log = scrolledtext.ScrolledText(self, width=60, height=15, state='disabled')
        self.log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def log_msg(self, msg):
        self.log.config(state='normal')
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state='disabled')

    def get_status(self):
        r = requests.get(f"{BASE_URL}/status")
        self.log_msg(f"Status: {r.json().get('mode')}")

    def set_mode(self, mode):
        r = requests.put(f"{BASE_URL}/status", json={"mode": mode})
        self.log_msg(f"Set mode to {mode}: {r.status_code}")

    def get_recording(self):
        r = requests.get(f"{BASE_URL}/recording")
        if r.status_code == 200:
            pretty = json.dumps(r.json(), indent=2)
            self.log_msg("Recording Info:\n" + pretty)
        else:
            self.log_msg(f"Error fetching recording info: {r.status_code}")
        
    def set_record_dir(self):
        d = simpledialog.askstring("Record Dir", "New parent_directory:")
        if d:
            r = requests.put(f"{BASE_URL}/recording", json={"parent_directory": d})
            self.log_msg(f"Set parent_directory to {d}: {r.status_code}")

    def list_processors(self):
        r = requests.get(f"{BASE_URL}/processors")
        self.log_msg("Processors:")
        for p in r.json().get("processors", []):
            self.log_msg(f"  ID {p['id']}: {p['name']}")

    def config_processor(self):
        pid = simpledialog.askinteger("Processor ID", "Enter processor ID:")
        cfg = simpledialog.askstring("Config", "Config text:")
        if pid and cfg:
            r = requests.put(f"{BASE_URL}/processors/{pid}/config", json={"text": cfg})
            self.log_msg(f"Config processor {pid}: {r.status_code}")

    def broadcast_message(self):
        txt = simpledialog.askstring("Broadcast", "Message text:")
        if txt:
            r = requests.put(f"{BASE_URL}/message", json={"text": txt})
            self.log_msg(f"Broadcast '{txt}': {r.status_code}")

    def quit_gui(self):
        r = requests.put(f"{BASE_URL}/window", json={"command": "quit"})
        self.log_msg(f"Quit GUI: {r.status_code}")

if __name__ == "__main__":
    app = OEControlApp()
    app.mainloop()
