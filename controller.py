from evdev import InputDevice, categorize, ecodes
from printer import send_to_printer, conn
from fairbanks_scale import current, check_scale_conn
from scanner import get_scanner_device
from label import generate_label
from utils import custom_upper
from threading import Thread
from math import ceil
import uuid
from typing import Optional
from config import (
    buttons_pad_src,
    img_folder
)
from printer import get_printer_status
import os, time
import requests

unique_id = ""
day_lot = None
count = None
pause = False
scanned_code = ""
input_code = ""

# usb barcode scanner will match characters in this array based off keycode to verify correct string output due to different encoding
KEY_MAPPING = {'KEY_EQUAL': '+', 'KEY_SLASH': '/', 'KEY_SPACE': ' ', 'KEY_DOT': '.', 'KEY_MINUS': '-', 'KEY_Q': 'q',
               'KEY_W': 'w', 'KEY_E': 'e', 'KEY_R': 'r',
               'KEY_T': 't', 'KEY_Y': 'y',
               'KEY_U': 'u', 'KEY_I': 'i', 'KEY_O': 'o', 'KEY_P': 'p', 'KEY_A': 'a', 'KEY_S': 's', 'KEY_D': 'd',
               'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h',
               'KEY_J': 'j', 'KEY_K': 'k', 'KEY_L': 'l', 'KEY_Z': 'z', 'KEY_X': 'x', 'KEY_C': 'c', 'KEY_V': 'v',
               'KEY_B': 'b', 'KEY_N': 'n', 'KEY_M': 'm',
               'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4', 'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7',
               'KEY_8': '8', 'KEY_9': '9', 'KEY_0': '0'}


def code() -> Optional[str]:
    global scanned_code
    return scanned_code[-12:]


def get_day_lot() -> Optional[str]:
    global day_lot
    return day_lot


def get_count() -> Optional[str]:
    global count
    return count


def system_status():
    global pause
    if get_printer_status() and check_scale_conn():
        pause = False
        return True
    else:
        pause = True
        return False


KEY_UP = 0
KEY_DOWN = 1
LEFT_SHIFT = 42
KEY_ENTER = 28


class CodeScanner(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.code_scanner = None                      

    def run(self):
        # we check forever conections and disconections from the Scanner
        while True:
            self.code_scanner = get_scanner_device()  
            if self.code_scanner is None:
                print("CodeScanner:run:No scanner I'll try again in 5 seconds:")
                time.sleep(5)
                continue

            global input_code, scanned_code, keys, unique_id
            to_upper_case = False
            print("CodeScanner:run:code_scanner:", self.code_scanner)
            try:
                for event in self.code_scanner.read_loop():                    
                    if event.type == ecodes.EV_KEY:
                        data = categorize(event)
                        if data.scancode == LEFT_SHIFT:
                            to_upper_case = True
                            continue

                        if data.keystate != KEY_UP:
                            continue

                        # Each event is 1 character, have to store all events until code 28 which is enter/done.
                        # Store entire scan in global variable and reset the input.
                        if data.scancode == KEY_ENTER:
                            scanned_code = input_code                    
                            unique_id = str(uuid.uuid4())
                            input_code = ""
                        else:                
                            if data.keycode in KEY_MAPPING:
                                if to_upper_case:
                                    input_code += custom_upper(KEY_MAPPING[data.keycode])
                                    to_upper_case = False
                                else:
                                    input_code += KEY_MAPPING[data.keycode]
            except OSError:
                self.code_scanner = None
                print("CodeScanner:run:Scanner offline")




class ButtonsReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        global day_lot, count
        print("We started to read buttons values")

        # creates object 'gamepad' to store the data
        # you can call it whatever you like
        self.buttons_pad = InputDevice(buttons_pad_src)

        # print label
        self.blue_btn = 288

        # start new count new lot
        self.yellow_btn = 290

        # pause machine
        self.red_btn = 298

        # re-print last label
        self.green_btn = 292

        # reset machine
        self.white_btn = 294

        count = 0
        day_lot = 1
        self.last_label = ''

    def update_last_label(self, label):
        if self.last_label != '':
            myfile = img_folder + self.last_label
            if os.path.isfile(myfile):
                os.remove(myfile)
        self.last_label = label

    # Start new lot and count
    def start_new_lot(self):
        global day_lot, count
        day_lot = day_lot + 1
        count = 0

    def set_pause(self):
        global pause
        pause = not pause

    def send_print_helper(self, rounded_weight):
        global day_lot, count, unique_id, scanned_code
        count = count + 1
        print("this is unique_uuid: ", unique_id)
        label = generate_label(day_lot, count, str(rounded_weight), scanned_code, unique_id)
        route = img_folder + label
        self.update_last_label(label)
        send_to_printer(route)

    def send_url_request(self):
        global scanned_code, unique_id
        weight = current()
        if float(weight) <= 0.50:
            round_weight = str(0.5)
        else:
            round_weight = (ceil(float(format(float(weight), ".2f"))))
        url = "https://csfcouriersltd.com/ws/weighted_package"
        request_data = {"receipt_number": scanned_code, "packageId": unique_id, "weight": round_weight,
                        "username": "csfcourierltd", "password": "6Ld9y1saAAAAAFY5xdTG3bCjZ7jCnfhqztPdXKUL"}
        print("REQUEST DATA", request_data)
        try:
            x = requests.post(url, data=request_data)
            print("ButonReader:send_url_request:", x.text)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("API request: Something goes wrong", e)
        scanned_code = ""
        unique_id = ""

    def run(self):
        global pause
        # evdev takes care of polling the controller in a loop
        for event in self.buttons_pad.read_loop():            
            # filters by event type
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    print("ButtonReader:run:event:",event)
                    if event.code == self.blue_btn and not pause:
                        if conn.getJobs() == {}:
                            print("Let's print label")
                            weight = current()
                            if weight != None and float(weight) > 0:
                                if float(weight) <= 0.50:
                                    self.send_print_helper(str(0.5))
                                    self.send_url_request()
                                else:
                                    self.send_print_helper(ceil(float(format(float(weight), ".2f"))))
                                    self.send_url_request()
                                # print(event)
                        else:
                            print("Printer is busy")
                    if event.code == self.yellow_btn and not pause:
                        print("Let's start a new lot")
                        self.start_new_lot()                        
                    if event.code == self.red_btn:
                        if (pause):
                            print("CONTINUE")
                        else:
                            print("PAUSE")
                        self.set_pause()                        
                    if event.code == self.green_btn and not pause:
                        print("Green Btn pressed")
                        if self.last_label != '':
                            route = img_folder + self.last_label
                            send_to_printer(route)                            
                    if event.code == self.white_btn and not pause:
                        self.send_print_helper(str(0.5))