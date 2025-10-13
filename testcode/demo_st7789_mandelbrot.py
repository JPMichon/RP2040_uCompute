"""
based on https://github.com/alastairhm/micropython-st7735/blob/main/mandelbrot_tft.py
240x240 ST7789 SPI LCD
using MicroPython library:


"""

import uos
import machine
import st7789py as st7789

import random
from math import cos, pi, sin

#SPI(1) default pins
spi1_sck=2
spi1_mosi=3
spi1_miso=8     #not use
st7789_res = 4
st7789_dc  = 5
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)

HALF_WIDTH = int(disp_width/2)
HALF_HEIGHT = int(disp_height/2)
CENTER_X = int(disp_width/2)-1
CENTER_Y = int(disp_height/2)-1

def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB (based on colorsys.py).

        Args:
            h (float): Hue 0 to 1.
            s (float): Saturation 0 to 1.
            v (float): Value 0 to 1 (Brightness).
    """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

    
print(uos.uname())
spi0 = machine.SPI(0,62500000,sck=machine.Pin(2,machine.Pin.OUT),mosi=machine.Pin(3,machine.Pin.OUT), polarity=1,phase=0)
print(spi0)
display = st7789.ST7789(spi0, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT), 
                          xstart=0, ystart=0, rotation=0)

minX = -2.0
maxX = 1.0
width = 240
height = 240
aspectRatio = 1

chars = " .,-:;i+hHM$*#@ "
clen = len(chars)
colours = [
    st7789.color565(0xF0, 0x20, 0x20),
    st7789.RED,
    st7789.MAROON,
    st7789.GREEN,
    st7789.FOREST,
    st7789.BLUE,
    st7789.NAVY,
    st7789.CYAN,
    st7789.YELLOW,
    st7789.PURPLE,
    st7789.WHITE,
    st7789.GRAY,
    st7789.RED,
    st7789.MAROON,
    st7789.GREEN,
    st7789.FOREST,
    st7789.BLACK,
]

rangeX = maxX - minX
yScale = (rangeX) * (float(height) / width) * aspectRatio

for y in range(height):
    line = ""
    ytemp = y * yScale / height - yScale / 2
    for x in range(width):
        c = complex(minX + x * (rangeX) / width, ytemp)
        z = c
        colour = 0
        while abs(z) <= 2 and colour < clen:
            colour += 1
            z = z * z + c
        display.pixel(y, x, colours[colour])
        line += chars[colour % clen]
   # print(line)




