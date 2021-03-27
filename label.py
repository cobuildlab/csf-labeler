from PIL import Image, ImageDraw, ImageFont
from numpy import random
#import datetime
from datetime import datetime
import qrcode
#######################################################################
mach_id = "KH09"
#uniq_id = "20210221-2-00032"
#wgth = 8
transparency = 128        #0 means 100% transparency, 255 means 0% transparency
img_folder = '/home/pi/csf-labeler/images/'
#######################################################################

def get_date():
    return datetime.today().strftime('%m/%d/%Y')
def get_day_name():
    return datetime.today().strftime("%A")
def get_time():
    return datetime.today().strftime('%I:%M:%S %p')
def get_weight():
    return random.randint(100)

def generate_label(lot, count, weight_str):
    day_name = get_day_name()
    day_date = get_date()
    day_time = get_time()
    uniq_id = day_date.replace('/','') + '-' + str(lot) + '-' + str(count)
    img = Image.new('RGB', (696, 1109), color='white')
    draw = ImageDraw.Draw(img)
    img.putalpha(transparency)
    #draw.rectangle([10,10,686,1099],None,20)
    fnt = ImageFont.truetype('arial.ttf', size=100)
    draw.text((348,110),str(weight_str) + " lb",fill='black', anchor="ms" ,font=fnt)
    fnt = ImageFont.truetype('arial.ttf', size=50)
    draw.text((348, 180), uniq_id, fill='black', anchor="ms", font=fnt)
    draw.text((348, 820), day_name, fill='black', anchor="ms", font=fnt)
    draw.text((348, 880), day_date, fill='black', anchor="ms", font=fnt)
    draw.text((348, 940), day_time, fill='black', anchor="ms", font=fnt)
    draw.text((348, 1100), mach_id, fill='black', anchor="ms", font=fnt)
    qr = qrcode.QRCode(version=1, box_size=20, border=1)
    qr.add_data(str(weight_str) + " lb")
    qr.make(fit= True)
    qr_bitmap = qr.make_image(fill_color='black', back_color='white')
    draw.bitmap((105,250),qr_bitmap, fill= 'black')
    img_uniq_name = uniq_id + '.png'
    img.save(img_folder + img_uniq_name)
    return img_uniq_name
