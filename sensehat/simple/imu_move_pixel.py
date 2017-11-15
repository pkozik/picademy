#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep
import atexit
import math

r = (255, 0, 0)
o = (255, 127, 0)
y = (255, 255, 0)
g = (0, 255, 0)
b = (0, 0, 255)
i = (75, 0, 130)
v = (159, 0, 255)
e = (0, 0, 0)

image = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, g, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e
]

sense = SenseHat()
sense.low_light = True
atexit.register(sense.clear, e)


class Pixel:
    def __init__(self, x, y, color=g):
        self.x = x
        self.y = y
        self.color = color

    def __set_color(self):
        self.color = g
        if self.get_x() <= 0 or self.get_x() >= 7 or self.get_y() <= 0 or self.get_y() >= 7:
            self.color = r

    def move(self, dx, dy):
        if 0 <= self.x + dx <= 7:
            self.x += dx

        if 0 <= self.y + dy <= 7:
            self.y += dy

        self.__set_color()

    def get_x(self):
        return int(round(self.x, 0))

    def get_y(self):
        return int(round(self.y, 0))

    def __str__(self):
        return "[%d, %d, %s]" % (self.x, self.y, self.color)


pix = Pixel(4, 4)
sense.set_pixel(pix.x, pix.y, b)

speed = 1
try:
    while True:
        for event in sense.stick.get_events():
            if event.direction == "right":
                speed += 1
            elif event.direction == "left":
                if speed > 1:
                    speed -= 1

        os = sense.get_orientation_radians()
        pitch = - math.sin(os['pitch']) * speed
        roll = math.sin(os['roll']) * speed

        sense.set_pixel(pix.get_x(), pix.get_y(), e)
        pix.move(pitch, roll)
        sense.set_pixel(pix.get_x(), pix.get_y(), pix.color)

except KeyboardInterrupt:
    exit(0)
