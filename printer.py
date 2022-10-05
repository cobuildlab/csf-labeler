import cups
from config import PRINTERS_CONFIG
from typing import Optional

conn = cups.Connection()

def check_printer_conn():
    for printer_config in PRINTERS_CONFIG:
        printer_device = printer_config["device"]()
        if printer_device is not None:
            return True
    return False

def __get_printer_info():
    printers = conn.getPrinters()
    for printer_config in PRINTERS_CONFIG:
        printer_name = printer_config["name"]
        if printer_name in printers:
            device_uri = printers[printer_name]['device-uri']
            state = printers[printer_name]['printer-state']
            serial = device_uri.split('=')[1]
            return printer_name, device_uri, state, serial
    return "", "","",""

print(PRINTERS_CONFIG)
print(__get_printer_info())
print(check_printer_conn())

def get_printer_serial()-> Optional[str]:
    return __get_printer_info()[3]

def get_printer_status()-> Optional[bool]:
    printer_status = __get_printer_info()[2]
    if printer_status == 3 and check_printer_conn():
        return True
    else:
        return False

def send_to_printer(filename):
    try: 
        conn.printFile(__get_printer_info()[0], filename, "Printing " + filename, {})
    except ValueError as e:
        print("It seems that the printer is OFF", e)

