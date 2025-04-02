import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def load_ip_config():
    try:
        with open("ip.ini", "r") as f:
            ipbox.delete(0, tk.END)
            ipbox.insert(0, f.readline().strip())
            portbox.delete(0, tk.END)
            portbox.insert(0, f.readline().strip())
    except FileNotFoundError:
        pass

def save_ip_config():
    with open("ip.ini", "w") as f:
        f.write(ipbox.get() + "\n" + portbox.get() + "\n")
    messagebox.showinfo("Info", "Save IP")

def execute_socat(filename):
    batch_content = f"@echo off\nsocat.exe -t 99999999 - TCP:{ipbox.get()}:{portbox.get()} < {filename}\npause"
    with open("ps5.bat", "w") as f:
        f.write(batch_content)
    subprocess.run(["ps5.bat"], shell=True)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("ELF BIN Files", "*.elf;*.bin")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def send_payload():
    try:
        batch_content = f"@echo off\nsocat.exe -t 99999999 - TCP:{ipbox.get()}:{portbox.get()} < {file_entry.get()}\npause"
        with open("payload.bat", "w") as f:
            f.write(batch_content)
        subprocess.run(["payload.bat"], shell=True)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("PS Loaders")

tk.Label(root, text="IP:").grid(row=0, column=0)
ipbox = tk.Entry(root)
ipbox.grid(row=0, column=1)

tk.Label(root, text="Port:").grid(row=1, column=0)
portbox = tk.Entry(root)
portbox.grid(row=1, column=1)

tk.Button(root, text="Save IP", command=save_ip_config).grid(row=2, columnspan=2)

tk.Button(root, text="Send kstuff.elf", command=lambda: execute_socat("payloads/kstuff.elf")).grid(row=3, columnspan=2)
tk.Button(root, text="Send ftpsrv.elf", command=lambda: execute_socat("payloads/ftpsrv.elf")).grid(row=4, columnspan=2)
tk.Button(root, text="Send websrv.elf", command=lambda: execute_socat("payloads/websrv.elf")).grid(row=5, columnspan=2)
tk.Button(root, text="Send etaHEN2.0b.elf", command=lambda: execute_socat("payloads/etaHEN2.0b.elf")).grid(row=6, columnspan=2)

file_entry = tk.Entry(root, width=40)
file_entry.grid(row=7, column=0)
tk.Button(root, text="Browse", command=select_file).grid(row=7, column=1)
tk.Button(root, text="Send Custom Payload", command=send_payload).grid(row=8, columnspan=2)

load_ip_config()
root.mainloop()
