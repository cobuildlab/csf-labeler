import brother_ql
from brother_ql.raster import BrotherQLRaster
from brother_ql.backends.helpers import send

# Using USB connected printer 
PRINTER_IDENTIFIER = 'usb://0x04f9:0x209c/L0Z645503'

def send_to_printer(filename):
    #filename = 'my_image2.png'
    printer = BrotherQLRaster('QL-810W')
    print_data = brother_ql.brother_ql_create.convert(printer, [filename], '62x100', red=False, lq=True)
    send(print_data, PRINTER_IDENTIFIER)

