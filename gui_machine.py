from tkinter import *
import socket
from random import randint
from struct import pack, unpack
import time
import pyperclip


UDP_IP = "192.168.50.10"
UDP_PORT = 5050  # 5005

MESSAGE_SYN = b'\x01\xFF\x01'
MESSAGE_LCD = b'\x07\x0D\x00\x00\x00\x00'
MESSAGE_FIN = b'\x04\x00\x01'
MESSAGE_LCD_POS = b'\x08\x00\x00\x00\x02\x00\x04'

MESSAGE_XYZa_ONE = b'\x07\x03\x00\x01\x01\x01\x01'
MESSAGE_XYZs_ONE = b'\x07\x0b\x00\x01\x01\x01\x01'
MESSAGE_XYZa_TWO = b'\x07\x03\x00\x02\x02\x01\x02'
MESSAGE_XYZs_TWO = b'\x07\x0b\x00\x02\x02\x01\x02'
MESSAGE_XYZa_THREE = b'\x07\x03\x00\x03\x03\x01\x03'
MESSAGE_XYZs_THREE = b'\x07\x0b\x00\x03\x03\x01\x03'
MESSAGE_XYZa_FOUR = b'\x07\x03\x00\x04\x04\x01\x04'
MESSAGE_XYZs_FOUR = b'\x07\x0b\x00\x04\x04\x01\x04'

MESSAGE_LCD_POS_1 = b'\x08\x00\x00\x00\x02\x00\x04\x00\x00\x00\x00'
MESSAGE_LCD_POS_2 = b'\x08\x00\x00\x00\x02\x00\x04\x78\x78\x78\x78'


class MyFirstGUI:
    socket.setdefaulttimeout(5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, master):
        self.master = master

        button_width = 20
        button_height = 0
        master.option_add("*Font", "-*-lucidatypewriter-medium-r-*-*-*-160-*-*-*-*-*-*")
        master.configure(background='#92B2E5')

        master.title("GUI for sending UDP packets")
        master.geometry('600x685')

        self.syn_button = Button(master, text="SYN", command=self.syn, height=button_height, width=button_width)
        self.syn_button.grid(row=1, column=1, padx=5, pady=5)

        self.create_lcd_button = Button(master, text="LCD ADR:1 PKG:1", command=self.create_lcd, height=button_height, width=button_width)
        self.create_lcd_button.grid(row=2, column=1, columnspan=1, padx=5, pady=5)

        self.create_xyz_button = Button(master, text="XYZ Servos", command=self.create_xyz, height=button_height, width=button_width)
        self.create_xyz_button.grid(row=2, column=2, columnspan=1, padx=5, pady=5)

        self.fin_button = Button(master, text="FIN", command=self.fin, height=button_height, width=button_width)
        self.fin_button.grid(row=3, column=1, padx=5, pady=5)

        self.set_eye_pos1_button = Button(master, text="Set eye at position 1", command=self.set_eye_pos_1, height=button_height, width=button_width)
        self.set_eye_pos1_button.grid(row=4, column=1, padx=5, pady=5)

        self.set_eye_pos2_button = Button(master, text="Set eye at position 2", command=self.set_eye_pos_2, height=button_height, width=button_width)
        self.set_eye_pos2_button.grid(row=4, column=2, padx=5, pady=5)

        self.set_eye_pos_button = Button(master, text="Set eye at rand position", command=self.set_eye_pos, height=button_height, width=button_width)
        self.set_eye_pos_button.grid(row=4, column=3, padx=5, pady=5)

        self.label_frame = LabelFrame(master, bg='#92B2E5', text="Send Raw Data")
        self.label_frame.grid(row=5, column=1, columnspan=4, pady=20)

        self.packet_input_text_box = Entry(self.label_frame, width=50)
        self.packet_input_text_box.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        self.packet_input_text_box.bind('<Return>', func=self.packet_input_text)

        self.clear_button = Button(self.label_frame, text="Clear", width=13, command=self.clear)
        self.clear_button.grid(row=5, column=3)

        self.float_to_hex_input = Entry(self.label_frame, width=24)
        self.float_to_hex_input.grid(row=6, column=1, columnspan=1, padx=5, pady=5)

        self.float_to_hex_output = Entry(self.label_frame, width=24)
        self.float_to_hex_output.grid(row=6, column=2, columnspan=1, padx=5, pady=5)

        self.convert_button = Button(self.label_frame, text="Convert", command=self.convert, width=13)
        self.convert_button.grid(row=6, column=3)

        self.text_output = Text(self.label_frame, width=65)
        self.text_output.grid(row=7, column=1, columnspan=4, padx=5, pady=5)

        self.close_button = Button(master, text="Close", command=master.quit, height=button_height, width=button_width)
        self.close_button.grid(row=1, column=3, padx=5, pady=5)

    def convert(self):
        input_float = float(self.float_to_hex_input.get())
        output_hex = hex(unpack('<I', pack('<f', input_float))[0])[2:]
        output_hex = " ".join(output_hex[i:i + 2] for i in range(0, len(output_hex), 2))
        pyperclip.copy(output_hex)
        self.float_to_hex_output.delete(0, END)
        self.float_to_hex_output.insert(0, output_hex)

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
        self.sock.sendto(MESSAGE_LCD, (UDP_IP, UDP_PORT))
        self.print_response()

    def create_xyz(self):
        print("XYZ Packet")
        self.sock.sendto(MESSAGE_XYZa_ONE, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZs_ONE, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZa_TWO, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZs_TWO, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZa_THREE, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZs_THREE, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZa_FOUR, (UDP_IP, UDP_PORT))
        self.print_response()
        self.sock.sendto(MESSAGE_XYZs_FOUR, (UDP_IP, UDP_PORT))
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
        x1 = pack("B", randint(0, 159))
        y1 = pack("B", randint(0, 159))
        x2 = pack("B", randint(0, 159))
        y2 = pack("B", randint(0, 159))

        print("Set eye position at {0},{1}".format(x1, y1))
        packet = MESSAGE_LCD_POS + x1 + y1 + x2 + y2
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
            self.text_output.insert('1.0', str(data) + '\n')
        except Exception:
            print("Packet request sent but timed out after 5 seconds")
            self.text_output.insert('1.0', "Packet request sent but timed out after 5 seconds\n")

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

    def clear(self):
        try:
            self.sock.settimeout(0.1)
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
        except Exception:
            self.text_output.insert('1.0', "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            self.sock.settimeout(5)



root = Tk()
my_gui = MyFirstGUI(root)

root.mainloop()
