#!/usr/bin/python


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def clone(self):
        return Point(self.x, self.y)


class Pixel(Point):
    def __init__(self, x, y, color):
        Point.__init__(self, x, y)
        self.color = color

    def draw(self, screen):
        screen.set_pixel(self.x, self.y, self.color)

    def clear(self, screen):
        screen.set_pixel(self.x, self.y, (0, 0, 0))


class PixelSet:
    def __init__(self, *pixels):
        self.pixels = pixels

    def draw(self, screen):
        for pix in self.pixels:
            pix.draw(screen)

    def clear(self, screen):
        for pix in self.pixels:
            pix.clear(screen)


class LedBar:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen
        self.pixels = (
            Pixel(0, self.pos, self.blue),
            Pixel(1, self.pos, self.green),
            Pixel(2, self.pos, self.yellow),
            Pixel(3, self.pos, self.red),
            Pixel(4, self.pos, self.red),
            Pixel(5, self.pos, self.red),
            Pixel(6, self.pos, self.red),
        )
        self.current = 0

    def refresh(self):
        for pix in self.pixels:
            if pix.x < self.current:
                pix.draw(self.screen)
            else:
                pix.clear(self.screen)

    def up(self):
        if self.current < len(self.pixels):
            self.current += 1
            self.refresh()

    def down(self):
        if self.current > 0:
            self.current -= 1
            self.refresh()


# some helper methods
def x_in_range(point, screen):
    return (0 <= point.x < screen.width)


def y_in_range(point, screen):
    return (0 <= point.y < screen.height)


def point_in_range(point, screen):
    return (x_in_range(point, screen) and y_in_range(point, screen))
