from evdev import InputDevice, categorize, ecodes
from config import BARCODE_CONFIG
from threading import Thread
import time

from utils import custom_upper

KEY_UP = 0
KEY_DOWN = 1
LEFT_SHIFT = 42
KEY_ENTER = 28

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


def get_scanner_device():
    for barcode_config in BARCODE_CONFIG:
        try:
            code_scanner = InputDevice(barcode_config["src"])
        except FileNotFoundError:
            continue
        if code_scanner:
            return code_scanner
    return None


class CodeScanner(Thread):
    def __init__(self):
        Thread.__init__(self, name="CodeScanner")
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
            except OSError as e:
                print("CodeScanner:run:Scanner offline:error:", e)
                self.code_scanner = None
