#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep
from utils import Pixel
import atexit


class Reflect:
    """
    decorator class adding the Pixel reflection at the edge
    capabilities
    """

    def __init__(self, pixel):
        self.decorated = pixel
        self.factor = [1, 1]

    def __getattr__(self, name):
        return getattr(self.decorated, name)

    def move(self, dx, dy):
        if self.decorated.x in [0, 7]:
            self.factor[0] = -self.factor[0]
        if self.decorated.y in [0, 7]:
            self.factor[1] = -self.factor[1]

        self.decorated.move(dx * self.factor[0], dy * self.factor[1])


sense = SenseHat()
sense.low_light = True
sense.height = 8
sense.width = 8

atexit.register(sense.clear)


b = (0, 0, 155)
g = (0, 155, 0)
r = (155, 0, 0)

pixels = [Reflect(Pixel(5, 1, color=b)),
          Reflect(Pixel(4, 4, color=g)),
          Reflect(Pixel(1, 6, color=r))]

try:
    while True:
        for pixel in pixels:
            pixel.move(1, 1)
            pixel.refresh(sense)
        sleep(0.1)

except KeyboardInterrupt:
    exit(0)
