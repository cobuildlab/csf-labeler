from evdev import InputDevice, categorize, ecodes

from network import RequestSender
from printer import send_to_printer, Printer
from label import generate_label
from threading import Thread
from math import ceil
import uuid
from config import (
    buttons_pad_src,
    img_folder
)
import os


class ButtonsReader(Thread):
    def __init__(self, scanner_controller, scale_controller):
        Thread.__init__(self, name="ButtonsReader")
        self.scanner_controller = scanner_controller
        self.scale_controller = scale_controller
        self.day_lot = 1
        self.count = 0
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
        self.last_label = ''

    def update_last_label(self, label):
        if self.last_label != '':
            my_file = img_folder + self.last_label
            if os.path.isfile(my_file):
                os.remove(my_file)
        self.last_label = label

    # Start new lot and count
    def start_new_lot(self):
        self.day_lot = self.day_lot + 1
        self.count = 0

    def send_print_helper(self, rounded_weight, unique_id):
        print("ButtonsReader:send_print_helper")
        self.count = self.count + 1
        print("ButtonsReader:send_print_helper:unique_id:", unique_id)
        label_path = generate_label(self.day_lot, self.count, str(rounded_weight), self.scanner_controller.scanned_code,
                                    unique_id)
        print("ButtonsReader:send_print_helper:label_path:", label_path)
        # route = img_folder + label
        # self.update_last_label(label_path)
        # send_to_printer(label_path)
        Printer(label_path).start()
        print("ButtonsReader:send_print_helper:Printer:sent")

    def send_url_request(self, weight_str, unique_id):
        print("ButtonsReader:send_url_request")
        scanned_code = self.scanner_controller.scanned_code
        if not scanned_code:
            print("ButtonsReader:send_url_request:NO CODE, NO REQUEST")
            return

        print("ButtonsReader:send_url_request:send_request:", unique_id, scanned_code, weight_str)
        RequestSender(unique_id, scanned_code, weight_str).start()
        print("ButtonsReader:send_url_request:sent:")

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
                                weight = self.scale_controller.current_value
                                if weight is not None and float(weight) > 0:
                                    if float(weight) <= 0.50:
                                        weight_str = str(0.5)
                                    else:
                                        weight_str = ceil(float(format(float(weight), ".2f")))

                                    self.send_print_helper(weight_str, unique_id)
                                    self.send_url_request(weight_str, unique_id)
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
