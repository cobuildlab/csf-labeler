import cups
from config import printer_name

conn = cups.Connection()
printers = conn.getPrinters()
device_uri = printers[printer_name]['device-uri']
printer_serial = device_uri.split('=')[1]

def send_to_printer(filename):
    try: 
        conn.printFile (printer_name, filename, "Printing " + filename, {})
    except ValueError as e:
        print("It seems that the printer is OFF", e)

