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
import os, time
import requests

day_lot = None
count = None

# usb barcode scanner will match characters in this array based off keycode to verify correct
# string output due to different encoding
KEY_MAPPING = {'KEY_EQUAL': '+', 'KEY_SLASH': '/', 'KEY_SPACE': ' ', 'KEY_DOT': '.', 'KEY_MINUS': '-', 'KEY_Q': 'q',
               'KEY_W': 'w', 'KEY_E': 'e', 'KEY_R': 'r',
               'KEY_T': 't', 'KEY_Y': 'y',
               'KEY_U': 'u', 'KEY_I': 'i', 'KEY_O': 'o', 'KEY_P': 'p', 'KEY_A': 'a', 'KEY_S': 's', 'KEY_D': 'd',
               'KEY_F': 'f', 'KEY_G': 'g', 'KEY_H': 'h',
               'KEY_J': 'j', 'KEY_K': 'k', 'KEY_L': 'l', 'KEY_Z': 'z', 'KEY_X': 'x', 'KEY_C': 'c', 'KEY_V': 'v',
               'KEY_B': 'b', 'KEY_N': 'n', 'KEY_M': 'm',
               'KEY_1': '1', 'KEY_2': '2', 'KEY_3': '3', 'KEY_4': '4', 'KEY_5': '5', 'KEY_6': '6', 'KEY_7': '7',
               'KEY_8': '8', 'KEY_9': '9', 'KEY_0': '0'}


def get_day_lot() -> Optional[str]:
    global day_lot
    return day_lot


def get_count() -> Optional[str]:
    global count
    return count


KEY_UP = 0
KEY_DOWN = 1
LEFT_SHIFT = 42
KEY_ENTER = 28


class CodeScanner(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.code_scanner = None
        self.scanned_code = ""

    def reset(self):
        self.scanned_code = ""

    def run(self):
        # we check forever connections and disconnections from the Scanner
        while True:
            self.code_scanner = get_scanner_device()
            if self.code_scanner is None:
                print("CodeScanner:run:No scanner I'll try again in 5 seconds:")
                time.sleep(5)
                continue

            to_upper_case = False
            input_code = ""
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
                            self.scanned_code = input_code
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
    def __init__(self, scanner_controller: CodeScanner):
        Thread.__init__(self)
        self.scanner_controller = scanner_controller
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
            my_file = img_folder + self.last_label
            if os.path.isfile(my_file):
                os.remove(my_file)
        self.last_label = label

    # Start new lot and count
    def start_new_lot(self):
        global day_lot, count
        day_lot = day_lot + 1
        count = 0

    def send_print_helper(self, rounded_weight, unique_id):
        print("ButtonsReader:send_print_helper")
        global day_lot, count
        count = count + 1
        print("ButtonsReader:send_print_helper:unique_id:", unique_id)
        label_path = generate_label(day_lot, count, str(rounded_weight), self.scanner_controller.scanned_code,
                                    unique_id)
        print("ButtonsReader:send_print_helper:label_path:", label_path)
        # route = img_folder + label
        # self.update_last_label(label_path)
        send_to_printer(label_path)

    def send_url_request(self, unique_id):
        print("ButtonsReader:send_url_request")
        if not self.scanner_controller.scanned_code:
            return

        weight = current()
        if float(weight) <= 0.50:
            rounded_weight = str(0.5)
        else:
            rounded_weight = (ceil(float(format(float(weight), ".2f"))))
        print("ButtonsReader:send_url_request:rounded_weight:", rounded_weight)
        url = "https://csfcouriersltd.com/ws/weighted_package"
        print("ButtonsReader:send_url_request:rounded_weight:url", url)
        request_data = {"receipt_number": self.scanner_controller.scanned_code, "packageId": unique_id,
                        "weight": rounded_weight,
                        "username": "csfcourierltd", "password": "6Ld9y1saAAAAAFY5xdTG3bCjZ7jCnfhqztPdXKUL"}
        print("ButtonsReader:send_url_request:request_data:", request_data)
        try:
            response = requests.post(url, data=request_data)
            print("ButtonReader:send_url_request:response:", response.text)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("ButtonReader:send_url_request:error: Something goes wrong", e)

    def run(self):
        while True:
            try:
                # evdev takes care of polling the controller in a loop
                for event in self.buttons_pad.read_loop():
                    # filters by event type
                    if event.type == ecodes.EV_KEY:
                        if event.value == 1:
                            print("ButtonReader:run:event:", event)
                            if event.code == self.blue_btn:
                                print("controller.py:ButtonsReader:run:blue_btn")
                                unique_id = str(uuid.uuid4())
                                weight = current()
                                if weight is not None and float(weight) > 0:
                                    weight_str = ""
                                    if float(weight) <= 0.50:
                                        weight_str = str(0.5)
                                    else:
                                        weight_str = ceil(float(format(float(weight), ".2f")))

                                    self.send_print_helper(weight_str, unique_id)
                                    self.send_url_request(unique_id)
                                    self.scanner_controller.reset()
                            if event.code == self.yellow_btn:
                                print("Let's start a new lot")
                                self.start_new_lot()
                            if event.code == self.green_btn:
                                print("Green Btn pressed")
                                if self.last_label != '':
                                    route = img_folder + self.last_label
                                    send_to_printer(route)
                            if event.code == self.white_btn:
                                self.send_print_helper(str(0.5))
            except Exception as e:
                print("controller.py:ButtonsReader:error: For some reason the buttons failed")
                print("controller.py:ButtonsReader:error: But we will try again, I promise:")
                print("controller.py:ButtonsReader:error:", e)
