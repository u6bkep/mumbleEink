#!/usr/bin/python3
from PIL import Image,ImageDraw,ImageFont

Himage = Image.open('mumble.bmp')
#Himage.rotate(180)
Himage =  Himage.convert('1', dither=None)
Himage.save("mode1.bmp")
