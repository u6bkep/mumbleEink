#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import io
from subprocess import Popen, PIPE
from datetime import datetime
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from calendar_get import update_cal
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont,ImageChops
import traceback
from cairosvg import svg2png

#logging.basicConfig(level=logging.DEBUG)

try:
#    logging.info("epd7in5_V2 Demo")

    font12 = ImageFont.truetype('Font.ttc', 12)

   # epd = epd7in5_V2.EPD()
   # logging.info("init and Clear")
   # epd.init()
   # epd.Clear()

#    imgOld = Image.open('mumble.bmp')
#    call("wkhtmltoimage --height 800 --width 480 --disable-smart-width -f bmp --javascript-delay 5000 http://mumble.gecko.network/mumble-widget/index.html mumble.bmp", shell=True)

    p = Popen("wkhtmltoimage --height 800 --width 480 --disable-smart-width -f bmp --javascript-delay 5000 http://mumble.gecko.network/mumble-widget/index.html -", shell=True, stdout=PIPE, close_fds=True)

#    logging.info(" update display")
#    Himage = Image.open('mumble.bmp')
#    Himage = Image.open(io.BytesIO(p.stdout.read()))
    try:
        Himage = p.communicate(input=None, timeout=20)
    except TimeoutExpired:
        p.kill()
        sys.exit("wkhtmltoimage timeout")
    Himage = Image.open(io.BytesIO(Himage[0]))

    svgOverlay = update_cal()

    #p = Popen("inkscape screen-output-cal.svg --without-gui -e -", shell=True, stdout=PIPE, close_fds=True)

    #calImage = Image.open(io.BytesIO(p.stdout.read()))
    calImage = svg2png(bytestring=svgOverlay)
    calImage = Image.open(io.BytesIO(calImage))

    Himage.paste(calImage, mask=calImage.split()[3])
 #   diff = ImageChops.difference(imgOld , Himage)
  #  if diff.getbbox() != None:
        
    epd = epd7in5_V2.EPD()
#    logging.info("init and Clear")
    epd.init()
#    logging.info(" updating image")
    Himage = Himage.convert('1', dither=None)
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 780), datetime.now().time().strftime('%I:%M %p'), font = font12, fill = 0)
    Himage = Himage.rotate(180)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

#    logging.info("Goto Sleep...")
    epd.sleep()
   # else:
   #     logging.info("server status not changed, not updating")
    
except IOError as e:
#    logging.info(e)
    print(e)
    
except KeyboardInterrupt:    
#    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
