from PIL import Image, ImageDraw, ImageFont
import datetime
import qrcode
#######################################################################
mach_id = "KH09"
uniq_id = "20210221-2-00032"
wgth = 8
transparency = 128        #0 means 100% transparency, 255 means 0% transparency
#######################################################################
img = Image.new('RGB', (696, 1109), color='white')
draw = ImageDraw.Draw(img)
img.putalpha(transparency)
draw.rectangle([10,10,686,1099],None,20)
fnt = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', size=100)
draw.text((260,40),str(wgth) + " lbs",fill='black' ,font=fnt)
fnt = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', size=50)
draw.text((140, 160), uniq_id, fill='black', font=fnt)
#draw.rectangle([100,250,600,700],None,3)
today = datetime.datetime.now()
draw.text((210, 730), today.strftime("%A"), fill='black', font=fnt)
draw.text((240, 800), today.strftime("%x"), fill='black', font=fnt)
draw.text((240, 900), today.strftime("%X"), fill='black', font=fnt)
draw.text((285, 1000), mach_id, fill='grey', font=fnt)
#qr = qrcode.make("12 lb")
qr = qrcode.QRCode(version=1, box_size=20, border=1)
qr.add_data(str(wgth) + " lb")
qr.make(fit= True)
qr_bitmap = qr.make_image(fill_color='black', back_color='white')
draw.bitmap((120,250),qr_bitmap, fill= 'black')
img.save('label.png')
