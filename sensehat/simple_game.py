#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep, time
from random import randint
from utils import Pixel, Gyro
import atexit

b = (0, 0, 155)
g = (100, 240, 60)
r = (155, 0, 0)
o = (0, 0, 0)
e = (0, 0, 0)


sad = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, b, e, e, b, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, r, r, r, r, e, e,
    e, r, e, e, e, e, r, e,
    e, e, e, e, e, e, e, e
]


class EdgeStop:
    """
    decorator class for Pixel to stop its movement 
    on the screen edge
    """

    def __init__(self, pixel, screen):
        self.decorated = pixel
        self.screen = screen

    def __getattr__(self, name):
        return getattr(self.decorated, name)

    def move(self, dx, dy):
        if not 0 <= self.decorated.x + dx < self.screen.width:
            dx = 0
        if not 0 <= self.decorated.y + dy < self.screen.height:
            dy = 0

        self.decorated.move(dx, dy)


class Scene:
    def __init__(self, **kwargs):
        self.count = kwargs["count"] if kwargs and "count" in kwargs else 5
        self.interval = kwargs["interval"] if kwargs and "interval" in kwargs else 1
        self.last_move = time()
        self.dots = []

    def clear(self):
        self.dots = []

    def move(self, dx=0, dy=1):
        now = time()
        if now - self.last_move < self.interval:
            return

        self.last_move = now
        for dot in self.dots:
            dot.move(dx, dy)

        # add new dots
        if len(self.dots) < self.count:
            self.dots.append(Pixel(randint(0, 7), 0, color=b))

    def refresh(self, screen):
        for dot in self.dots:
            dot.refresh(screen)

        # remove dots which moved out of the screen
        self.dots = [dot for dot in self.dots if dot.y < screen.height]

    def has_colision(self, obj):
        for dot in self.dots:
            if dot.x == obj.x and dot.y == obj.y:
                return True
        return False


def lost():
    # if hit the falling dot
    sense.set_pixels(sad)
    sleep(3)


sense = SenseHat()
atexit.register(sense.clear)

sense.low_light = True
sense.width = 8
sense.height = 8
scene = Scene(conunt=5, interval=0.5)
pad = EdgeStop(Pixel(4, 7, color=r), sense)
gyro = Gyro(sense, threshold=0.03)


try:
    for cnt in range(3):
        sense.clear()
        scene.clear()

        while True:
            so = gyro.get_orientation()

            scene.move()
            scene.refresh(sense)

            if scene.has_colision(pad):
                lost()
                break

            pad.move(so.pitch, so.roll)
            pad.refresh(sense)
            sleep(0.1)

except KeyboardInterrupt:
    exit(0)
