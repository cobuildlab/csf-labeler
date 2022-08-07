import usb.core
import usb.util
from threading import Thread
import sys
from typing import Optional

current_value = None

def current()-> Optional[str]:
    global current_value
    return current_value

def check_scale_conn():
    scale_device = usb.core.find(idVendor=0x0b67, idProduct=0x555e)
    if scale_device != None:
        return True
    else:
        return False

def check_scanner_conn():
    scanner_device = usb.core.find(idVendor=0xe851, idProduct=0x1000)
    if scanner_device != None:
        return True
    else:
        return False

def check_printer_conn():
    printer_device = usb.core.find(idVendor=0x0a5f, idProduct=0x0120)
    if printer_device != None:
        return True
    else:
        return False
class FairbanksScaleReader(Thread):
    def run(self):
    
        print("We started to read values")

        # The number of times a number should be outputted by the scale
        # before being output to the user.  This is to allow the scale
        # to balance before output
        BALANCE_THRESHOLD = 10



        # These IDs can be found by using `lsusb`
        device = usb.core.find(idVendor=0x0b67, idProduct=0x555e)

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
        # Used as threshold to wait for scale to balance before outputting to the user (100 executions by default)
        counts = {}

        while True:
            try:
                global current_value
                data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                # print(data)
                # print("DEBUG",data[0],data[1],data[2],data[3],data[4], data[5], data[4] + (data[5]*256))
                if data[1] == 5:                    
                    counts = {}
                    current_value = None
                    continue
                    
                weight = float(data[4] + (data[5]*256)) / 100
                weight_str = str(weight)

                if weight == 0.0:  # The scale goes back to zero, so we rest everything
                    counts = {}
                    current_value = None
                    continue

                # Duplicated reading
                if weight_str not in counts:
                    counts[weight_str] = 0
                else:
                    counts[weight_str] = counts[weight_str] + 1

                if counts[weight_str] > BALANCE_THRESHOLD :
                    current_value = weight_str
                    counts = {}

            except usb.core.USBError as e:
                data = None
                if e.args == ('Operation timed out',):
                    continue

def init():
    reader = FairbanksScaleReader()
    reader.start()

