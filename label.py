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
text_2 = int(text_1 + vertical_padding + normal_fnt_size)
draw_1 = int(text_2 + vertical_padding * 2)
text_6 = int(label_length_px - 10)
text_5 = int(text_6 - vertical_padding - normal_fnt_size)
text_4 = int(text_5 - vertical_padding - normal_fnt_size)
text_3 = int(text_4 - vertical_padding - normal_fnt_size)

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

def generate_label(lot, count, weight_str, user_number):
    day_name = get_day_name()
    day_date = get_date()
    day_time = get_time()
    
    uniq_id = day_date.replace('/','') + '-' + str(lot) + '-' + str(count)
    
    img = Image.new('RGB', (label_width_px, label_length_px), color='white')
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('/home/pi/csf-labeler/arial.ttf', size=100)
    draw.text((406,150),str(weight_str) + " lb",fill='black', anchor="ms" ,font=fnt)
    fnt = ImageFont.truetype('/home/pi/csf-labeler/arial.ttf', size=50)
    draw.text((406, 225), uniq_id, fill='black', anchor="ms", font=fnt)
    draw.text((406, 820), day_name, fill='black', anchor="ms", font=fnt)
    draw.text((406, 880), day_date, fill='black', anchor="ms", font=fnt)
    draw.text((406, 940), day_time, fill='black', anchor="ms", font=fnt)
    draw.text((406, 1100), printer_serial + ' user #' + user_number, fill='black', anchor="ms", font=fnt)
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(str(weight_str))
    qr.make(fit= True)
    qr_bitmap = qr.make_image()

    pos = ((img.size[0] - qr_bitmap.size[0]) // 2, (img.size[1] - qr_bitmap.size[1]) // 2)
    print(pos)
    img.paste(qr_bitmap, pos)

    img_uniq_name = uniq_id + '.png'
    img.save(img_folder + img_uniq_name)
    
    return img_uniq_name
