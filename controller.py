# import evdev
from evdev import InputDevice, categorize, ecodes
from laberel import send_to_printer, conn
from label import generate_label
from fairbanks_scale import init, current
from threading import Thread
from fairbanks_scale import current
from math import ceil

class ButtonsReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("We started to read buttons values")
        #creates object 'gamepad' to store the data
        #you can call it whatever you like
        self.buttons_pad = InputDevice('/dev/input/by-id/usb-DragonRise_Inc._Generic_USB_Joystick-event-joystick')
        self.img_folder = '/home/pi/csf-labeler/images/'
        
        #print label
        self.blue_btn = 288
        
        #start new count new lot
        self.yellow_btn = 289
        
        #pause machine
        self.red_btn = 298
        
        #re-print last label
        self.green_btn = 290
        
        #reset machine
        self.white_btn = 299
        
        self.pause = False
        self.count = 0
        self.day_lot = 1
        self.last_label = ''

            
    def update_last_label(self, label):
        self.last_label = label

    #Start new lot and count
    def start_new_lot(self):
        self.day_lot = self.day_lot + 1
        self.count = 0
        
    def set_pause(self):
        self.pause = not self.pause

    def send_print_helper(self, rounded_weight):
        self.count = self.count + 1                        
        label = generate_label(self.day_lot, self.count, str(rounded_weight))
        route = self.img_folder + label
        self.update_last_label(label)
        send_to_printer(route)
        
    def run(self):
        #evdev takes care of polling the controller in a loop
        for event in self.buttons_pad.read_loop():
            #print(categorize(event))
                # filters by event type
            if event.type == ecodes.EV_KEY:
                if event.value == 1:
                    # print(event)
                    if event.code == self.blue_btn and not self.pause:
                        if conn.getJobs() == {}:
                            print("Let's print label")
                            weight = current()
                            if weight != None and float(weight) > 0:
                                if float(weight) <= 0.5:
                                    self.send_print_helper(str(0.5))
                                else:
                                    self.send_print_helper(ceil(float(weight)))
                                #print(event)
                        else:
                            print("Printer is busy")
                    if event.code == self.yellow_btn and not self.pause:
                        print("Let's start a new lot")
                        self.start_new_lot()
                        #   print(event)
                    if event.code == self.red_btn:
                        if(self.pause):
                            print("CONTINUE")
                        else:
                            print("PAUSE")
                        self.set_pause()
                        #print(event)
                    if event.code == self.green_btn and not self.pause:
                        print("Green Btn pressed")
                        if self.last_label != '':
                            route = self.img_folder + self.last_label
                            send_to_printer(route)
                            # print(current())
                    if event.code == self.white_btn:
                        print("Restarting machine...")


def init_buttons():
    reader = ButtonsReader()
    reader.start()
    

init_buttons()
init()