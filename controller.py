from evdev import InputDevice, categorize, ecodes
from zebra_printer import send_to_printer, conn
from fairbanks_scale import init, current, check_scale_conn, check_scanner_conn
from label import generate_label
from threading import Thread
from math import ceil
from typing import Optional
from config import (
    buttons_pad_src,
    img_folder
)
from zebra_printer import get_printer_status
import urllib.request
import os

day_lot = None
count = None
pause = False

def get_day_lot()-> Optional[str]:
    global day_lot
    return day_lot
def get_count()-> Optional[str]:
    global count
    return count

def check_network_conn():
    try:
        urllib.request.urlopen('http://google.com')
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
        global day_lot, count
        count = count + 1                        
        label = generate_label(day_lot, count, str(rounded_weight))
        route = img_folder + label
        self.update_last_label(label)
        send_to_printer(route)
        
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
                                else:
                                    self.send_print_helper(ceil(float(format(float(weight), ".2f"))))
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
    