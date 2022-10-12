import cups
from config import PRINTERS_CONFIG
from typing import Optional

conn = cups.Connection()
print("printer.py:conn.getJobs:", conn.getJobs())


def __get_printer_info():
    printers = conn.getPrinters()
    for printer_config in PRINTERS_CONFIG:
        printer_name = printer_config["name"]
        if printer_name in printers:
            device_uri = printers[printer_name]['device-uri']
            state = printers[printer_name]['printer-state']
            serial = device_uri.split('=')[1]
            return printer_name, device_uri, state, serial
    return "", "", "", ""


def get_printer_serial() -> Optional[str]:
    return __get_printer_info()[3]


def is_printer_ready() -> Optional[bool]:
    printer_status = __get_printer_info()[2]
    if printer_status == 3:
        return True
    else:
        return False


def send_to_printer(filename):
    printer_name = __get_printer_info()[0]
    try:
        conn.cancelAllJobs(printer_name)
    except Exception as e:
        print("printer.py:send_to_printer:cancelAllJobs:", e)

    try:
        conn.printFile(printer_name, filename, "Printing " + filename, {})
    except ValueError as e:
        print("printer.py:send_to_printer:printFile:error:It seems that the printer is OFF", e)
