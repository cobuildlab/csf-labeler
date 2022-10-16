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
        name = printer_config["name"]
        if name in printers:
            device_uri = printers[name]['device-uri']
            state = printers[name]['printer-state']
            serial = device_uri.split('=')[1]
            conn.cancelAllJobs(name)
            current_printer = {"name": name, "device_uri": device_uri, "state": state, "serial": serial}
            return current_printer

    return {"name": "", "device_uri": "", "state": 0, "serial": ""}


def get_printer_serial() -> Optional[str]:
    return get_printer_info()["serial"]


def is_printer_ready() -> Optional[bool]:
    printer_state = get_printer_info()["state"]
    if printer_state == 3:
        return True
    else:
        return False


def send_to_printer(filename):
    name = get_printer_info()["name"]
    try:
        conn.cancelAllJobs(name)
        print("printer.py:send_to_printer:cancelAllJobs")
    except Exception as e:
        print("printer.py:send_to_printer:cancelAllJobs:", e)

    print("printer.py:send_to_printer:printFile:name:", name)
    print("printer.py:send_to_printer:printFile:filename:", filename)
    try:
        job_id = conn.printFile(name, filename, "Printing " + filename, {})
        print("printer.py:send_to_printer:printFile:job_id:", job_id)
    except ValueError as e:
        print("printer.py:send_to_printer:printFile:error:It seems that the printer is OFF", e)


# TODO: We need a local queue to moderate printer communication
class Printer(Thread):
    def __init__(self, filename):
        Thread.__init__(self, name="Printer")
        self.filename = filename

    def run(self):
        name = get_printer_info()["name"]
        print("Printer:run:name:", name)
        print("Printer:run:filename:", self.filename)
        try:
            job_id = conn.printFile(name, self.filename, "Printing", {})
            print("Printer:run:job_id:", job_id)
        except ValueError as e:
            print("Printer:run:error:It seems that the printer is OFF", e)
