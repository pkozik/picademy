#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep, time
from random import randint
from utils import Pixel, ReflectingPixel
import atexit


class Scene:
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self.color = kwargs["color"] if kwargs and "color" in kwargs else (
            0, 0, 250)
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
            self.dots.append(Pixel(randint(0, 7), 0, color=self.color))

    def refresh(self):
        for dot in self.dots:
            dot.refresh(self.screen)

        # remove dots which moved out of the screen
        self.dots = [dot for dot in self.dots if dot.y < self.screen.height]

    def check_colision(self, obj):
        # check if hit falling dots
        for dot in self.dots:
            if dot.x == obj.x and dot.y == obj.y:
                obj.reflect_x()
                obj.reflect_y()
                return
        # check the screen edge colision
        if obj.x <= 0 or obj.x >= self.screen.width - 1:
            obj.reflect_x()
        if obj.y <= 0 or obj.y >= self.screen.height - 1:
            obj.reflect_y()


sense = SenseHat()
atexit.register(sense.clear)
sense.clear()

sense.low_light = True
sense.width = 8
sense.height = 8
scene = Scene(sense, color=(0, 0, 250), conunt=5, interval=0.5)
car = ReflectingPixel(4, 1, color=(250, 0, 0))

try:
    while True:
        scene.move()
        scene.refresh()
        scene.check_colision(car)
        car.move(1, 1)
        car.refresh(sense)
        sleep(0.1)

except KeyboardInterrupt:
    exit(0)
