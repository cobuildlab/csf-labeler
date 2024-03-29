import usb.core
import usb.util
from threading import Thread
import sys
from typing import Optional


def check_scale_conn():
    scale_device = usb.core.find(idVendor=0x0b67, idProduct=0x555e)
    if scale_device is not None:
        return True
    else:
        return False


BALANCE_THRESHOLD = 10


class FairbanksScaleReader(Thread):
    def __init__(self):
        Thread.__init__(self, name="FairbanksScaleReader")
        self.current_value = None

    def run(self):
        # The number of times a number should be outputted by the scale
        # before being output to the user.  This is to allow the scale
        # to balance before output

        # These IDs can be found by using `lsusb`
        device = usb.core.find(idVendor=0x0b67, idProduct=0x555e)
        for cfg in device:
            for intf in cfg:
                if device.is_kernel_driver_active(intf.bInterfaceNumber):
                    try:
                        device.detach_kernel_driver(intf.bInterfaceNumber)
                    except usb.core.USBError as e:
                        sys.exit(
                            "Could not detatch kernel driver from interface({0}): {1}".format(intf.bInterfaceNumber,
                                                                                              str(e)))

        endpoint = device[0][(0, 0)][0]

        # Thresholds - these are wiped each time the scale is back to ZERO
        # Archives each output, to not repeat itself indefinitely
        # Used as threshold to wait for scale to balance before outputting to the user (100 executions by default)
        counts = {}

        while True:
            try:
                data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
                # print(data)
                # print("DEBUG",data[0],data[1],data[2],data[3],data[4], data[5], data[4] + (data[5]*256))
                if data[1] == 5:
                    counts = {}
                    self.current_value = None
                    continue

                weight = float(data[4] + (data[5] * 256)) / 100
                weight_str = str(weight)

                if weight == 0.0:  # The scale goes back to zero, so we rest everything
                    counts = {}
                    self.current_value = None
                    continue

                # Duplicated reading
                if weight_str not in counts:
                    counts[weight_str] = 0
                else:
                    counts[weight_str] = counts[weight_str] + 1

                if counts[weight_str] > BALANCE_THRESHOLD:
                    self.current_value = weight_str
                    counts = {}

            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    continue
