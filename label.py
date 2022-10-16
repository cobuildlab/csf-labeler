from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from qrcode import QRCode

from config import (IMG_FOLDER,
                    fnt_src,
                    label_width_px,
                    label_length_px,
                    header_fnt_size,
                    normal_fnt_size,
                    serial_fnt_size,
                    vertical_padding,
                    middle, LABEL_PATH
                    )

# QR and text dynamic positions.
text_1 = int(vertical_padding - 5 + header_fnt_size)
draw_1 = int(text_1 + vertical_padding - 5)
text_6 = int(label_length_px - 10)
text_5 = int(text_6 - vertical_padding - normal_fnt_size)
text_2 = int(text_5 - vertical_padding - normal_fnt_size)
text_4 = int(text_2 - vertical_padding - normal_fnt_size)
text_3 = int(text_4 - vertical_padding - normal_fnt_size)
text_7 = int(text_3 - vertical_padding - normal_fnt_size)
draw_2 = int(text_7 - 10 - normal_fnt_size)

# Font types initialization.
header_fnt = ImageFont.truetype(fnt_src, size=header_fnt_size)
body_fnt = ImageFont.truetype(fnt_src, size=normal_fnt_size)
serial_fnt = ImageFont.truetype(fnt_src, size=serial_fnt_size)


# Utility functions to get date and time.
def get_date():
    return datetime.today().strftime('%b/%d/%Y')


def get_date_for_id():
    return datetime.today().strftime('%m/%d/%Y')


def get_day_name():
    return datetime.today().strftime('%A')


def get_time():
    return datetime.today().strftime('%I:%M:%S %p')


# Main function to generate a label as an image.

def generate_label(lot, count, weight_str, barcode, unique_uuid):
    day_name = get_day_name()
    day_date = get_date()
    day_time = get_time()
    day_date_for_id = get_date_for_id()

    uniq_id = day_date_for_id.replace('/', '') + '-' + str(lot) + '-' + str(count)

    img = Image.new('RGB', (label_width_px, label_length_px), color='white')
    draw = ImageDraw.Draw(img)

    qr = QRCode(version=4, box_size=5, border=1)
    if barcode:
        qr.add_data(unique_uuid)
    else:
        qr.add_data(weight_str)
    qr.make(fit=True)
    qr_bitmap = qr.make_image(fill_color='black', back_color='white')

    draw.text((middle * 0.6, text_1), str(weight_str) + ' lb', fill='black', anchor='ms', font=header_fnt)
    img.paste(qr_bitmap, (50, draw_1))
    # draw.rectangle([((middle * 1.5) - 30, draw_2), ((middle * 1.5) + 30, draw_2 - 60)], fill=None, outline='black', width= 2)
    draw.text((middle * 1.5, text_7), day_name, fill='black', anchor='ms', font=serial_fnt)
    draw.line((((middle * 1.5) - 15), draw_2, ((middle * 1.5) + 15), (draw_2 - 30)), fill='black', width=3)
    draw.line((((middle * 1.5) + 15), draw_2, ((middle * 1.5) - 15), (draw_2 - 30)), fill='black', width=3)
    draw.text((middle * 1.5, text_3), day_date, fill='black', anchor='ms', font=serial_fnt)
    draw.text((middle * 1.5, text_4), day_time, fill='black', anchor='ms', font=serial_fnt)
    draw.text((middle * 1.5, text_2), uniq_id, fill='black', anchor='ms', font=serial_fnt)
    draw.text((middle * 1.5, text_5), barcode[-12:] if barcode else "No Barcode", fill='black', anchor='ms',
              font=serial_fnt)
    draw.text((middle * 1.5, text_6), unique_uuid[-12:], fill='black', anchor='ms', font=serial_fnt)
    img.save(LABEL_PATH)
