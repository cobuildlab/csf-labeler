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
imgFolder = '/home/pi/csf-labeler/Imaging/'
#######################################################################

def getDate():
    return datetime.today().strftime('%m/%d/%Y')
def getDayName():
    return datetime.today().strftime("%A")
def getTime():
    return datetime.today().strftime('%I:%M:%S %p')
def getWeight():
    return random.randint(100)

def generateLabel(lot, count):
    wgth = getWeight()
    day_name = getDayName()
    day_date = getDate()
    day_time = getTime()
    uniq_id = day_date.replace('/','') + '-' + str(lot) + '-' + str(count)
    img = Image.new('RGB', (696, 1109), color='white')
    draw = ImageDraw.Draw(img)
    img.putalpha(transparency)
    draw.rectangle([10,10,686,1099],None,20)
    fnt = ImageFont.truetype('arial.ttf', size=100)
    draw.text((260,40),str(wgth) + " lb",fill='black' ,font=fnt)
    fnt = ImageFont.truetype('arial.ttf', size=50)
    draw.text((140, 160), uniq_id, fill='black', font=fnt)
    draw.text((210, 730), day_name, fill='black', font=fnt)
    draw.text((240, 800), day_date, fill='black', font=fnt)
    draw.text((240, 900), day_time, fill='black', font=fnt)
    draw.text((285, 1000), mach_id, fill='grey', font=fnt)
    qr = qrcode.QRCode(version=1, box_size=20, border=1)
    qr.add_data(str(wgth) + " lb")
    qr.make(fit= True)
    qr_bitmap = qr.make_image(fill_color='black', back_color='white')
    draw.bitmap((120,250),qr_bitmap, fill= 'black')
    img_uniq_name = uniq_id + '.png'
    img.save(imgFolder + img_uniq_name)
    return img_uniq_name
