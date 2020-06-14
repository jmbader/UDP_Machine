from tkinter import *
import socket
import os
import platform
import subprocess
from random import randint
from struct import pack, unpack
import time
import pyperclip

UDP_IP = "192.168.50.10"
UDP_PORT = 5050

window_x = 400
window_y = 300


class XavierGUI(Frame):
    socket.setdefaulttimeout(5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.main_window()

    def main_window(self):
        self.master.title("XAVIER")

        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.exit_press)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)

        connection = Menu(menu)
        menu.add_cascade(label="Connection", menu=connection)

        # Sent Message Text Field

        # Recieved Message Text Field

        # Connect Button
        connect_button = Button(self, text="Connect", command=self.check_conn).grid(row=1, column=2)

        # IP Address Text Field
        ipAddr = Entry(self).grid(row=1, column=0)

        # Port Text Field
        port = Entry(self).grid(row=1, column=1)

    def exit_press(self):
        exit()

    def check_conn(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', UDP_IP]
        response = subprocess.call(command)

        if response:
            ping_status = "Device Connected"
        else:
            ping_status = "Device Not Connected"

        text_output = Label(self, text=ping_status)
        text_output.pack()


root = Tk()

geo = str(window_x) + "x" + str(window_y)
root.geometry(geo)

my_gui = XavierGUI(root)
root.mainloop()
