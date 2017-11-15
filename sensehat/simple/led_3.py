#!/bin/python
'''
demo of senseHat.set_pixels.

Define the matrix of pixels to show
some simple image, e.g. a smile face

Don't forget to clear matrix at the end.

'''

from sense_hat import SenseHat
from time import sleep

# define some colors
r = (255, 0, 0)
b = (0, 0, 255)
e = (0, 0, 0)

# define the image (smile)
image = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, b, e, e, b, e, e,
    e, e, e, e, e, e, e, e,
    e, r, e, e, e, e, r, e,
    e, e, r, r, r, r, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e
]

sense = SenseHat()
sense.low_light = True

sense.set_pixels(image)
sleep(5)
sense.clear()
