from evdev import InputDevice
import usb.core
from config import BARCODE_CONFIG


def check_scanner_conn():
    scanner_device = usb.core.find(idVendor=0x1eab, idProduct=0x9310)
    if scanner_device is not None:
        return True
    else:
        return False


def get_scanner_device():
    for barcode_config in BARCODE_CONFIG:
        code_scanner = InputDevice(barcode_config["src"])
        if code_scanner:
            return code_scanner
    return None
