#!/usr/bin/python3
from PIL import Image,ImageDraw,ImageFont
from subprocess import Popen, PIPE
from calendar_get import update_cal
import io

p = Popen("wkhtmltoimage --height 800 --width 480 --disable-smart-width -f bmp --javascript-delay 5000 http://mumble.gecko.network/mumble-widget/index.html -", shell=True, stdout=PIPE, close_fds=True)

mumbleImage = Image.open(io.BytesIO(p.stdout.read()))

update_cal()

p = Popen("inkscape screen-output-cal.svg --without-gui -e -", shell=True, stdout=PIPE, close_fds=True)

calImage = Image.open(io.BytesIO(p.stdout.read()))

mumbleImage.paste(calImage, mask=calImage.split()[3])

#mumbleImage.show()
mumbleImage = mumbleImage.convert('1', dither=None)
mumbleImage.save("screen-output.png")