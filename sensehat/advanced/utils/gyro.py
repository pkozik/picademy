#!/usr/bin/python

import math


class Data:
    pass


class Gyro:
    def __init__(self, sense, **kwargs):
        self.sense = sense
        self.threshold = kwargs["threshold"] if kwargs and "threshold" in kwargs else 0.1

    # return always values -1, 0, 1, depending on the device orientation.
    def __normalize(self, val):
        if abs(val) < self.threshold:
            return 0
        if val > 0:
            return 1
        return -1

    def get_orientation(self):
        os = self.sense.get_orientation_radians()
        out = Data()
        out.pitch = self.__normalize(-math.sin(os['pitch']))
        out.roll = self.__normalize(math.sin(os['roll']))
        return out
