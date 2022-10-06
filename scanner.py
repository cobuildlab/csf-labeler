from evdev import InputDevice
import usb.core
from config import BARCODE_CONFIG


def check_scanner_conn():
    for barcode_config in BARCODE_CONFIG:
        code_scanner = barcode_config["device"]()
        if code_scanner is not None:
            return True        
    return False


def get_scanner_device():
    for barcode_config in BARCODE_CONFIG:
        code_scanner = InputDevice(barcode_config["src"])
        if code_scanner:
            return code_scanner
    return None
