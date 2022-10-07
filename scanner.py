from evdev import InputDevice
from config import BARCODE_CONFIG


def get_scanner_device():
    for barcode_config in BARCODE_CONFIG:
        try:
            code_scanner = InputDevice(barcode_config["src"])
        except FileNotFoundError:
            continue
        if code_scanner:
            return code_scanner
    return None
