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

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont,ImageChops
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")

    font12 = ImageFont.truetype('Font.ttc', 12)

   # epd = epd7in5_V2.EPD()
   # logging.info("init and Clear")
   # epd.init()
   # epd.Clear()

#    imgOld = Image.open('mumble.bmp')
#    call("wkhtmltoimage --height 800 --width 480 --disable-smart-width -f bmp --javascript-delay 5000 http://mumble.gecko.network/mumble-widget/index.html mumble.bmp", shell=True)

    p = Popen("wkhtmltoimage --height 800 --width 480 --disable-smart-width -f bmp --javascript-delay 5000 http://mumble.gecko.network/mumble-widget/index.html -", shell=True, stdout=PIPE, close_fds=True)

    logging.info(" update display")
#    Himage = Image.open('mumble.bmp')
    Himage = Image.open(io.BytesIO(p.stdout.read()))

    
 #   diff = ImageChops.difference(imgOld , Himage)
  #  if diff.getbbox() != None:
        
    epd = epd7in5_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    logging.info(" updating image")
    Himage = Himage.convert('1', dither=None)
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 780), datetime.now().time().strftime('%I:%M %p'), font = font12, fill = 0)
    Himage = Himage.rotate(180)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    logging.info("Goto Sleep...")
    epd.sleep()
   # else:
   #     logging.info("server status not changed, not updating")
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
