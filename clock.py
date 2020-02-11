#!/usr/bin/env python

import colorsys
import time
import datetime
import threading
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd

def start():
    threading.Timer(3.0, start).start()
    FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 12)
    width, height = unicornhathd.get_shape()
    text_x = width
    text_y = 2
    font_file, font_size = FONT

    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = width, 0

    lines = str(datetime.datetime.now())[10:-10]
    colours = [tuple([int(n * 255) for n in colorsys.hsv_to_rgb(x / float(len(lines)), 1.0, 1.0)]) for x in range(len(lines))]
    
    unicornhathd.rotation(90)
    if (int(lines[:3])>=21 or int(lines[:3])<9):
        unicornhathd.brightness(0.01)
    else:
        unicornhathd.brightness(1)

    for line in lines:
        w, h = font.getsize(line)
        text_width += w + width
        text_height = max(text_height, h)

    text_width += width + text_x + 1

    image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    offset_left = 0

    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, colours[index], font=font)

        offset_left += font.getsize(line)[0] + 1

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x + scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

        unicornhathd.show()
        
start()


        


