# Printer Cups name
# if printer version 410
# printer_name = 'Zebra_Technologies_ZTC_ZD410-203dpi_ZPL'
printer_name = 'ZTC-ZD420-203dpi-ZPL'

# Input Pad source path.
buttons_pad_src = '/dev/input/by-id/usb-DragonRise_Inc._Generic_USB_Joystick-event-joystick'

# Barcode scanner source path.
barcode_scanner_src ='/dev/input/by-id/usb-Jieli_Technology_USB_PHY_2.0-event-kbd'

# Label as image folder path.
img_folder = '/home/pi/csf-labeler/images/'

# Font source path.
fnt_src = '/home/pi/csf-labeler/arial.ttf'

# Label resolution - This should be set in pixels.
#label_width_px = 457
#label_length_px = 812
# Text font size - This should be set in pixels.
#header_fnt_size = 80
#normal_fnt_size = 40
#serial_fnt_size = 20

# Label resolution 1.25 x 2.25 in - This should be set in pixels.
label_width_px = 457
label_length_px = 254


# Text font size - This should be set in pixels.
header_fnt_size = 40
normal_fnt_size = 18
serial_fnt_size = 18

# Text Align variables. 
vertical_padding = 15
middle = int(label_width_px/2)
