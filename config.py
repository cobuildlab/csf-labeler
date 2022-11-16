import os.path

import usb.core

# Printer Cups name
PRINTERS_CONFIG = [
    {
        "name": 'Zebra_Technologies_ZTC_ZD420-203dpi_ZPL',
        "device": lambda: usb.core.find(idVendor=0x0a5f, idProduct=0x0120)
    },
    {
        "name": 'Zebra_Technologies_ZTC_ZD410-203dpi_ZPL',
        "device": lambda: usb.core.find(idVendor=0x0a5f, idProduct=0x011c)
    },
]

# Input Pad source path.
buttons_pad_src = '/dev/input/by-id/usb-DragonRise_Inc._Generic_USB_Joystick-event-joystick'

# Barcode scanner source path.
BARCODE_CONFIG = [
    {
        "src": "/dev/input/by-id/usb-SuperMax_Imaging_2208_CM221A8K0092-event-kbd",
        "device": lambda: usb.core.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-Newland_Computer_KeyPos_SF-event-kbd",
        "device": lambda: usb.core.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperMax_Imaging_2208_CM221A4N1063-event-kbd",
        "device": lambda: usb.core.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperMax_Imaging_2208_CM221A8K0093-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperMax_Imaging_2600M_CM261A4N0068-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperMax_Imaging_2208_CM221A4N1061-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperLead_2208_SK220426012C8-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperLead_2208_SK22042601208-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperLead_2208_SK22042601209-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    },
    {
        "src": "/dev/input/by-id/usb-SuperLead_2208_SK22042601191-event-kbd",
        "device": lambda: usb.code.find(idVendor=0x2dd6, idProduct=0x2141)
    }
]
BASE_DIR = '/home/cobuild/csf-labeler'
# Label as image folder path.
IMG_PATH = BASE_DIR + '/images/'

# Font source path.
FONT_PATH = BASE_DIR + '/assets/arial.ttf'
# Label resolution - This should be set in pixels.
# label_width_px = 457
# label_length_px = 812
# Text font size - This should be set in pixels.
# header_fnt_size = 80
# normal_fnt_size = 40
# serial_fnt_size = 20

# Label resolution 1.25 x 2.25 in - This should be set in pixels.
label_width_px = 457
label_length_px = 254

# Text font size - This should be set in pixels.
header_fnt_size = 40
normal_fnt_size = 18
serial_fnt_size = 18

# Text Align variables. 
vertical_padding = 15
middle = int(label_width_px / 2)

LABEL_PATH = os.path.join(IMG_PATH, 'label.png')
