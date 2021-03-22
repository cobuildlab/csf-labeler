# import usb.core
# from usb.core import Device
#
# _devices = usb.core.find(find_all=True)
# devices = [device for device in _devices]
#
# if len(devices) == 0:
#     print("No devices connected")
#
# if devices[0] is None:
#     print("No devices connected")
#
# device:Device = devices[0]
# device.set_configuration()
#
# # get an endpoint instance
# cfg = device.get_active_configuration()
# intf = cfg[(0,0)]
#
# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_IN)
#
# assert ep is not None
#
# # write the data
# ep.read(ep, 7)


import usb.core
import usb.util
import time
from pykeyboard import PyKeyboard
import sys

# The number of times a number should be outputted by the scale
# before being output to the user.  This is to allow the scale
# to balance before output
BALANCE_THRESHOLD = 10

# These IDs can be found by using `lsusb`
VENDOR_ID = 0x0b67
PRODUCT_ID = 0x555e
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

k = PyKeyboard()

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
counts = {};

while True:
    try:
        data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        weight = float(data[4]) / 100
        weight_str = str(weight)

        if weight == 0.0:  # The scale goes back to zero, so we rest everything
            previous = []
            counts = {}
            continue

        # Duplicated reading
        if weight_str not in counts:
            counts[weight_str] = 0
        else:
            counts[weight_str] = counts[weight_str] + 1;

        if counts[weight_str] > BALANCE_THRESHOLD and weight not in previous:
            k.type_string(weight_str)
            previous.append(weight)

    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
