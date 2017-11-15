#!/bin/python
'''
Play with pixels on LED Matrix.

Turn on and off all pixels on the Matrix edge, 
one by one.

Hint: 
Numbering LEDs this way:
  0   1   2   3   4   5   6   7   
  8   9  10  11  12  13  14  15  
 16  17  18  19  20  21  22  23 
 24  25  26  27  28  29  30  31
 32  33  34  35  36  37  38  39
 40  41  42  43  44  45  46  47
 48  49  50  51  52  53  54  55
 56  57  58  59  60  61  62  63

LED at position 40 is:
  y = 40 // 8 = 5 
  x = 40 % 8  = 0
'''

from sense_hat import SenseHat
from time import sleep

off = (0, 0, 0)
pix_colour = (255, 0, 128)


class Pixel:
    def __init__(self, offset):
        self.y = offset // 8  # row
        self.x = offset % 8  # column


# all the pixels at the LED matrix edge
pixels = [4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61,
          60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2, 3]

sense = SenseHat()
sense.low_light = True

prev_pix = Pixel(0)
for pix in pixels:
    # turn off the previously lighted LED
    sense.set_pixel(prev_pix.x, prev_pix.y, off)
    # turn on the next one
    prev_pix = Pixel(pix)
    sense.set_pixel(prev_pix.x, prev_pix.y, pix_colour)
    sleep(0.1)

sense.clear()
