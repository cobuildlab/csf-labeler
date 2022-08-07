from evdev import InputDevice, categorize, ecodes
from zebra_printer import send_to_printer, conn, printer_serial
from fairbanks_scale import init, current, check_scale_conn, check_scanner_conn
from label import generate_label
from threading import Thread
from math import ceil
import uuid
from typing import Optional
from config import (
    buttons_pad_src,
    barcode_scanner_src,
    img_folder
)
from zebra_printer import get_printer_status
import urllib.request
import os
import json
import requests
import time

unique_id = ""
day_lot = None
count = None
pause = False
scanned_code = ""
input_code = ""

#usb barcode scanner will match characters in this array based off keycode to verify correct string output due to different encoding
keys = "X^1234567890-XXXqwertzuiopXXXXasdfghjkl:'XXXyxcvbnm,.XXXX XXXXXXXXXXXXXXXX"

def code()-> Optional[str]:
    global scanned_code
    return scanned_code[-12:]
def get_day_lot()-> Optional[str]:
    global day_lot
    return day_lot
def get_count()-> Optional[str]:
    global count
    return count

def check_network_conn():
    try:
        urllib.request.urlopen('https://google.com')
        return True
    except:
        return False

def system_status():
    global pause
    if get_printer_status() and check_scale_conn():
        pause = False
        return True
    else:
        pause = True
        return False

class CodeScanner(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.code_scanner = InputDevice(barcode_scanner_src)
    def run(self):
        global input_code, scanned_code, keys, unique_id
        for event in self.code_scanner.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.keystate == 1 and data.scancode != 42:
                #Each event is 1 character, have to store all events until code 28 which is enter/done. 
                #Store entire scan in global variable and reset the input.
                    if data.scancode == 28:
                        scanned_code = input_code.replace("X","")
                        unique_id = str(uuid.uuid4())
                        input_code = ""
                    else:
                        input_code += keys[data.scancode].upper()

def init_scanner():
    reader2 = CodeScanner()
    reader2.start()
    init()  

class ButtonsReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        global day_lot, count
        print("We started to read buttons values")
        
        #creates object 'gamepad' to store the data
        #you can call it whatever you like
        self.buttons_pad = InputDevice(buttons_pad_src)
        
        #print label
        self.blue_btn = 288
        
        #start new count new lot
        self.yellow_btn = 290
        
        #pause machine
        self.red_btn = 298
        
        #re-print last label
        self.green_btn = 292
        
        #reset machine
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

    #Start new lot and count
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
        print("this is unique_uuid: ",unique_id)
        label = generate_label(day_lot, count, str(rounded_weight), scanned_code, unique_id)
        route = img_folder + label
        self.update_last_label(label)
        send_to_printer(route)
        
    def send_url_request(self):
        global scanned_code, unique_id
        weight = current()
        round_weight = (ceil(float(format(float(weight), ".2f"))))
        url = "https://csfcouriersltd.com/ws/weighted_package"
        request_data = {"receipt_number": scanned_code,"packageId": unique_id,"weight": round_weight, "username":"csfcourierltd","password":"6Ld9y1saAAAAAFY5xdTG3bCjZ7jCnfhqztPdXKUL"}
        try:
            x = requests.post(url, data = request_data)
            print(x.text)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("API request: Something goes wrong",e)
        scanned_code = ""
        unique_id = ""
 
    def run(self):
        global pause
        #evdev takes care of polling the controller in a loop
        for event in self.buttons_pad.read_loop():
            #print(categorize(event))
            # filters by event type
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    print(event)
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
                                #print(event)
                        else:
                            print("Printer is busy")
                    if event.code == self.yellow_btn and not pause:
                        print("Let's start a new lot")
                        self.start_new_lot()
                        #   print(event)
                    if event.code == self.red_btn:
                        if(pause):
                            print("CONTINUE")
                        else:
                            print("PAUSE")
                        self.set_pause()
                        #print(event)
                    if event.code == self.green_btn and not pause:
                        print("Green Btn pressed")
                        if self.last_label != '':
                            route = img_folder + self.last_label
                            send_to_printer(route)
                            # print(current())
                    if event.code == self.white_btn and not pause:
                        self.send_print_helper(str(0.5))
    
def init_buttons():
    reader = ButtonsReader()
    reader.start()
    init()
    
