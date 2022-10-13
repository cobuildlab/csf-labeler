from threading import Thread

import cups
from config import PRINTERS_CONFIG
from typing import Optional

conn = cups.Connection()
print("printer.py:conn.getJobs:", conn.getJobs())

current_printer = None


def get_printer_info():
    global current_printer

    if current_printer is not None:
        return current_printer

    printers = conn.getPrinters()
    for printer_config in PRINTERS_CONFIG:
        printer_name = printer_config["name"]
        if printer_name in printers:
            device_uri = printers[printer_name]['device-uri']
            state = printers[printer_name]['printer-state']
            serial = device_uri.split('=')[1]
            conn.cancelAllJobs(printer_name)
            current_printer = {"printer_name": printer_name, "device_uri": device_uri, "state": state, "serial": serial}
            return current_printer

    return {"printer_name": "", "device_uri": "", "state": 0, "serial": ""}


def get_printer_serial() -> Optional[str]:
    return get_printer_info()["serial"]


def is_printer_ready() -> Optional[bool]:
    printer_status = get_printer_info()["status"]
    if printer_status == 3:
        return True
    else:
        return False


def send_to_printer(filename):
    printer_name = get_printer_info()["name"]
    try:
        # conn.cancelAllJobs(printer_name)
        print("printer.py:send_to_printer:cancelAllJobs")
    except Exception as e:
        print("printer.py:send_to_printer:cancelAllJobs:", e)

    print("printer.py:send_to_printer:printFile:printer_name:", printer_name)
    print("printer.py:send_to_printer:printFile:filename:", filename)
    try:
        job_id = conn.printFile(printer_name, filename, "Printing " + filename, {})
        print("printer.py:send_to_printer:printFile:job_id:", job_id)
    except ValueError as e:
        print("printer.py:send_to_printer:printFile:error:It seems that the printer is OFF", e)


class Printer(Thread):
    def __init__(self, filename):
        Thread.__init__(self, name="Printer")
        self.filename = filename

    def run(self):
        printer_name = get_printer_info()["name"]
        print("Printer:run:printer_name:", printer_name)
        print("Printer:run:filename:", self.filename)
        try:
            job_id = conn.printFile(printer_name, self.filename, "Printing", {})
            print("Printer:run:job_id:", job_id)
        except ValueError as e:
            print("Printer:run:error:It seems that the printer is OFF", e)
