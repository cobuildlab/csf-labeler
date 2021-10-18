import cups
from config import printer_name
from typing import Optional
from fairbanks_scale import check_printer_conn

conn = cups.Connection()
printers = conn.getPrinters()
device_uri = printers[printer_name]['device-uri']
printer_status = printers[printer_name]['printer-state']
printer_serial = device_uri.split('=')[1]
def get_printer_serial()-> Optional[str]:
    global printer_serial
    return printer_serial

def get_printer_status()-> Optional[bool]:
    global printer_status
    if printer_status == 3 and check_printer_conn():
        return True
    else:
        return False

def send_to_printer(filename):
    try: 
        conn.printFile (printer_name, filename, "Printing " + filename, {})
    except ValueError as e:
        print("It seems that the printer is OFF", e)

