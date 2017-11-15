#!/usr/bin/python

from sense_hat import SenseHat
from time import sleep
from utils import Pixel
import atexit
from random import randint


class Scene:
    '''
    falling dots from the top of the LED matrix to the
    bottom. 
    '''

    def __init__(self, count):
        self.count = count
        self.dots = []

    def move(self):
        for dot in self.dots:
            dot.move(0, 1)

        # add new dots
        if len(self.dots) < self.count:
            self.dots.append(Pixel(randint(0, 7), 0, color=(0, 0, 100)))

    def refresh(self, screen):
        for dot in self.dots:
            dot.refresh(screen)

        # remove dots which moved out of the screen
        self.dots = [dot for dot in self.dots if dot.y < screen.height]


sense = SenseHat()
sense.low_light = True
atexit.register(sense.clear, (0, 0, 0))

sense.height = 8
sense.width = 8

g = (0, 255, 0)
r = (255, 0, 0)
scene = Scene(5)

try:
    while True:
        scene.move()
        scene.refresh(sense)
        sleep(0.2)

except KeyboardInterrupt:
    exit(0)
