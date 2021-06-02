from PIL import Image, ImageDraw, ImageFont
from zebra_printer import printer_serial
from datetime import datetime
from qrcode import QRCode
from config import (
    img_folder,
    fnt_src, 
    label_width_px, 
    label_length_px, 
    header_fnt_size,
    normal_fnt_size, 
    serial_fnt_size, 
    vertical_padding, 
    middle 
)

# QR and text dynamic positions.
text_1 = int(vertical_padding + header_fnt_size)
draw_1 = int(text_1 + vertical_padding)
text_2 = int(label_length_px - 20)
text_6 = int(label_length_px - 10)
text_5 = int(text_6 - vertical_padding - normal_fnt_size)
text_4 = int(text_5 - vertical_padding - normal_fnt_size)
text_3 = int(text_4 - vertical_padding - normal_fnt_size)
draw_2 = int(text_3 - vertical_padding - normal_fnt_size)

# Font types inicialitation.
header_fnt = ImageFont.truetype(fnt_src, size=header_fnt_size)
body_fnt = ImageFont.truetype(fnt_src, size=normal_fnt_size)
serial_fnt = ImageFont.truetype(fnt_src, size=serial_fnt_size)

# Utility functions to get date and time.
def get_date():
    return datetime.today().strftime('%m/%d/%Y')
def get_day_name():
    return datetime.today().strftime('%A')
def get_time():
    return datetime.today().strftime('%I:%M:%S %p')

# Main function to generate a label as an image.
def generate_label(lot, count, weight_str):
    day_name = get_day_name()
    day_date = get_date()
    day_time = get_time()
    
    uniq_id = day_date.replace('/','') + '-' + str(lot) + '-' + str(count)
    
    img = Image.new('RGB', (label_width_px, label_length_px), color='white')
    draw = ImageDraw.Draw(img)

    qr = QRCode(version=1, box_size=6, border=1)
    qr.add_data(str(weight_str))
    qr.make(fit= True)
    qr_bitmap = qr.make_image(fill_color='black', back_color='white')

    draw.text((middle * 0.5, text_1), str(weight_str) + ' lb', fill='black', anchor='ms', font=header_fnt)
    draw.text((middle * 0.5, text_2), uniq_id, fill='black', anchor='ms', font=body_fnt)
    draw.bitmap((50, draw_1), qr_bitmap, fill= 'black')
    draw.rectangle([((middle * 1.5) - 30, draw_2), ((middle * 1.5) + 30, draw_2 - 60)], fill=None, outline='black', width= 2)
    draw.text((middle * 1.5, text_3), day_name, fill='black', anchor='ms', font=body_fnt)
    draw.text((middle * 1.5, text_4), day_date, fill='black', anchor='ms', font=body_fnt)
    draw.text((middle * 1.5, text_5), day_time, fill='black', anchor='ms', font=body_fnt)
    draw.text((middle * 1.5, text_6), printer_serial, fill='black', anchor='ms', font=serial_fnt)
    
    img_uniq_name = uniq_id + '.png'
    img.save(img_folder + img_uniq_name)
    
    return img_uniq_name
