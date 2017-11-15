#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep, time
from random import randint
from utils import Pixel


class ReflectingPixel(Pixel):
    def __init__(self, x, y, **kwargs):
        Pixel.__init__(self, x, y, **kwargs)
        self.factor = [1, 1]

    def reflect_x(self):
        self.factor[0] = self.previous[0] - self.pos[0]

    def reflect_y(self):
        self.factor[1] = self.previous[1] - self.pos[1]

    def move(self, dx, dy):
        Pixel.move(self, dx * self.factor[0], dy * self.factor[1])


class Scene:
    def __init__(self, **kwargs):
        self.count = kwargs["count"] if kwargs and "count" in kwargs else 5
        self.interval = kwargs["interval"] if kwargs and "interval" in kwargs else 1
        self.last_move = time()
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

    def has_colision(self, point):
        for dot in self.dots:
            if dot.x == point.x and dot.y == point.y:
                return True
        return False


sense = SenseHat()
sense.clear()

sense.low_light = True
sense.width = 8
sense.height = 8

b = (0, 0, 255)
g = (0, 255, 0)
r = (255, 0, 0)
o = (0, 0, 0)

scene = Scene(conunt=5, interval=0.5)
car = ReflectingPixel(4, 1, color=g)
dx = 1

while True:
    scene.move()
    scene.refresh(sense)

    if scene.has_colision(car):
        # if hit the falling dot
        car.reflect_x()
        car.reflect_y()
    else:
        # if at the screen edge
        if car.x <= 0 or car.x >= sense.width:
            car.reflect_x()
        if car.y <= 0 or car.y >= sense.height:
            car.reflect_y()

    car.move(1, 1)
    car.refresh(sense)

    sleep(0.05)
