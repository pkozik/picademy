#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep
from utils import Pixel
import atexit


class Reflect:
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
atexit.register(sense.clear, (0, 0, 0))


b = (0, 0, 255)
g = (0, 255, 0)
r = (255, 0, 0)

pixels = [Reflect(Pixel(5, 1, b)),
          Reflect(Pixel(4, 4, g)),
          Reflect(Pixel(1, 6, r))]

sense.set_pixel(6, 2, (0, 120, 90))
try:
    dx = 1
    dy = 1
    while True:
        for pixel in pixels:
            pixel.move(1, 1)
            pixel.refresh(sense)
        sleep(0.1)

except KeyboardInterrupt:
    exit(0)
