from tkinter import Tk, Label, Button, LEFT, Entry, TOP, BOTTOM, X
import socket
from random import randint
from struct import pack
import time


UDP_IP = "192.168.50.10"
UDP_PORT = 5050  # 5005

MESSAGE_SYN = b'\x01\xFF\x01'
MESSAGE_UART_SERVO = b'\x07\x0D\x00\x01\x01\x00'
MESSAGE_FIN = b'\x04\x00\x01'
MESSAGE_LCD_POS = b'\x08\x00\x01\x01\x02\x00\x02'

MESSAGE_LCD_POS_1 = b'\x08\x00\x01\x01\x02\x00\x02\x00\x00'
MESSAGE_LCD_POS_2 = b'\x08\x00\x01\x01\x02\x00\x02\x9f\x9f'


class MyFirstGUI:
    socket.setdefaulttimeout(5)
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    def __init__(self, master):
        self.master = master
        master.title("GUI for sending UDP packets")

        self.label = Label(master, text="Lets send some UDP Packets")
        self.label.pack()

        self.syn_button = Button(master, text="SYN", command=self.syn)
        self.syn_button.pack(side=LEFT)

        self.create_lcd_button = Button(master, text="Create a lcd at address 1 in package 1", command=self.create_lcd)
        self.create_lcd_button.pack(side=LEFT)

        self.fin_button = Button(master, text="FIN", command=self.fin)
        self.fin_button.pack(side=LEFT)

        self.set_eye_pos1_button = Button(master, text="Set eye at position 1", command=self.set_eye_pos_1)
        self.set_eye_pos1_button.pack(side=LEFT)

        self.set_eye_pos2_button = Button(master, text="Set eye at position 2", command=self.set_eye_pos_2)
        self.set_eye_pos2_button.pack(side=LEFT)

        self.set_eye_pos_button = Button(master, text="Set eye at random position", command=self.set_eye_pos)
        self.set_eye_pos_button.pack(side=LEFT)

        self.packet_input_text_box = Entry(master, width=100)
        #self.packet_input_text_box.grid(row=1, column=1)
        self.packet_input_text_box.bind('<Return>', func=self.packet_input_text)
        self.packet_input_text_box.pack(padx=5, pady=5)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(side=BOTTOM)

    def syn(self):
        print("SYN Packet")
        milliseconds = int(round(time.time() * 1000))
        print("{0} ms".format(milliseconds))
        self.sock.sendto(MESSAGE_SYN, (UDP_IP, UDP_PORT))
        self.print_response()

    def create_lcd(self):
        print("Create LCD Packet")
        milliseconds = int(round(time.time() * 1000))
        print("{0} ms".format(milliseconds))
        self.sock.sendto(MESSAGE_UART_SERVO, (UDP_IP, UDP_PORT))
        self.print_response()

    def fin(self):
        print("FIN Packet")
        milliseconds = int(round(time.time() * 1000))
        print("{0} ms".format(milliseconds))
        self.sock.sendto(MESSAGE_FIN, (UDP_IP, UDP_PORT))
        self.print_response()

    def set_eye_pos_1(self):
        print("set_eye_pos_1 Packet")
        milliseconds = int(round(time.time() * 1000))
        print("{0} ms".format(milliseconds))
        self.sock.sendto(MESSAGE_LCD_POS_1, (UDP_IP, UDP_PORT))
        self.print_response()

    def set_eye_pos_2(self):
        print("set_eye_pos_1 Packet")
        milliseconds = int(round(time.time() * 1000))
        print("{0} ms".format(milliseconds))
        self.sock.sendto(MESSAGE_LCD_POS_2, (UDP_IP, UDP_PORT))
        self.print_response()

    def set_eye_pos(self):
        x = pack("B", randint(0, 159))
        y = pack("B", randint(0, 159))

        print("Set eye position at {0},{1}".format(x, y))
        packet = MESSAGE_LCD_POS + x + y
        print(packet)
        milliseconds = int(round(time.time() * 1000))
        print("{0} ms".format(milliseconds))
        self.sock.sendto(packet, (UDP_IP, UDP_PORT))
        self.print_response()

    def print_response(self):
        try:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            milliseconds = int(round(time.time() * 1000))
            print("{0} ms Response:{1}".format(milliseconds, data))
        except Exception:
            print("Packet request sent but timed out after 5 seconds")

    def packet_input_text(self, input_info):
        # print(input_string)
        try:
            input_string = bytes.fromhex(self.packet_input_text_box.get())
            print(input_string)
            milliseconds = int(round(time.time() * 1000))
            print("{0} ms".format(milliseconds))
            self.sock.sendto(input_string, (UDP_IP, UDP_PORT))
            self.print_response()
        except Exception:
            print("Input not a valid hex byte stream, try again chief")


root = Tk()
my_gui = MyFirstGUI(root)

root.mainloop()