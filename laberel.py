import cups

conn = cups.Connection()
printers = conn.getPrinters()
printer_name='Zebra_Technologies_ZTC_GK420t'
device_uri = printers[printer_name]['device-uri']
printer_serial = device_uri.split('=')[1]

def send_to_printer(filename):
    try: 
        conn.printFile (printer_name, filename, "Printing " + filename, {})
    except ValueError as e:
        print("It seems that the printer is OFF", e)

