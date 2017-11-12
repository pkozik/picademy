#!/bin/python

from sense_hat import SenseHat

sense = SenseHat()
for angle in (0, 90, 180, 270):
    sense.set_rotation(angle)
    sense.show_message("Hello world!", text_colour=[
                       255, 0, 128], scroll_speed=0.1)
