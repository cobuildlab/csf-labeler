import usb.core
import usb.util
import time
from threading import Thread
import sys
from typing import Optional

current_value = None

def current()-> Optional[str]:
    global current_value
    print("DEBUG:", current_value)   
    return current_value

class FairbanksScaleReader(Thread):
    def run(self):
        print("We started to read values")

        # The number of times a number should be outputted by the scale
        # before being output to the user.  This is to allow the scale
        # to balance before output
        BALANCE_THRESHOLD = 5

        # These IDs can be found by using `lsusb`
        VENDOR_ID = 0x0b67
        PRODUCT_ID = 0x555e
        device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        for cfg in device:
            for intf in cfg:
                if device.is_kernel_driver_active(intf.bInterfaceNumber):
                    try:
                        device.detach_kernel_driver(intf.bInterfaceNumber)
                    except usb.core.USBError as e:
                        sys.exit(
                            "Could not detatch kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber, str(e)))

        endpoint = device[0][(0, 0)][0]

        data = None

        # Thresholds - these are wiped each time the scale is back to ZERO
        # Archives each output, to not repeat itself indefinitely
        previous = [0]
        # Used as threshold to wait for scale to balance before outputting to the user (100 executions by default)
        counts = {}

        while True:
            try:
                global current_value
                data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                # print(data)
                # print("DEBUG",data[0],data[1],data[2],data[3],data[4], data[5], data[4] + (data[5]*256))
                if data[1] == 5:                    
                    previous = []
                    counts = {}
                    current_value = None
                    continue
                                
                weight = float(data[4] + (data[5]*256)) / 100
                weight_str = str(weight)
                # print("DEBUG:valid value:", weight_str)

                if weight == 0.0:  # The scale goes back to zero, so we rest everything
                    previous = []
                    counts = {}
                    current_value = None
                    continue

                # Duplicated reading
                if weight_str not in counts:
                    counts[weight_str] = 0
                else:
                    counts[weight_str] = counts[weight_str] + 1

                if counts[weight_str] > BALANCE_THRESHOLD and weight not in previous:
                    current_value = weight_str
                    previous.append(weight)
                                   

            except usb.core.USBError as e:
                data = None
                if e.args == ('Operation timed out',):
                    continue

def init():
    reader = FairbanksScaleReader()
    reader.start()
    reader.join()
