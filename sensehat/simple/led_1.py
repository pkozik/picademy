#!/bin/python
'''
rotate the "1" on some not 
default background colour.

Don't forget to turn off all LEDs at the end    
'''

from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.low_light = True

for angle in (0, 90, 180, 270):
    sense.set_rotation(angle)
    sense.show_letter("1", text_colour=[
        255, 0, 128], back_colour=[5, 10, 5])
    sleep(1)

sense.clear()
