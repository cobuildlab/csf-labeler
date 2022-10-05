from evdev import InputDevice
import usb.core
from config import     barcode_scanner_src


def check_scanner_conn():
    scanner_device = usb.core.find(idVendor=0x1eab, idProduct=0x9310)
    if scanner_device is not None:
        return True
    else:
        return False

def get_scanner_device():
    code_scanner = InputDevice(barcode_scanner_src)
    if code_scanner:
        return code_scanner
    return None