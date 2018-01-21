#!/usr/bin/python


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def clone(self):
        return Point(self.x, self.y)


def x_in_range(point, screen):
    return (0 <= point.x < screen.width)


def y_in_range(point, screen):
    return (0 <= point.y < screen.height)


def point_in_range(point, screen):
    return (x_in_range(point, screen) and y_in_range(point, screen))
