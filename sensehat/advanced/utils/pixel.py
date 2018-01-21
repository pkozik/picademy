#!/usr/bin/python


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def clone(self):
        return Point(self.x, self.y)


class Pixel:
    def __init__(self, x, y, **kwargs):
        self.pos = Point(x, y)
        self.previous = Point(0, 0)
        self.color = kwargs["color"] if kwargs and "color" in kwargs else (
            0, 0, 128)
        self.bgcolor = kwargs["bgcolor"] if kwargs and "bgcolor" in kwargs else (
            0, 0, 0)

    @property
    def x(self):
        return self.pos.x if self.pos else None

    @property
    def y(self):
        return self.pos.y if self.pos else None

    def move(self, dx, dy):
        self.previous = self.pos.clone()
        self.pos.x += dx
        self.pos.y += dy

    def set_color(self, color):
        self.color = color

    def clear(self, screen):
        if 0 <= self.previous.x < screen.width and 0 <= self.previous.y < screen.height:
            screen.set_pixel(self.previous.x, self.previous.y, self.bgcolor)

    def refresh(self, screen):
        # nothing happened
        if self.pos == self.previous:
            return

        # clear the pixel at old position
        self.clear(screen)
        # if we are still in the range of the screen
        if 0 <= self.x < screen.width and 0 <= self.y < screen.height:
            # draw new pixel
            screen.set_pixel(self.pos.x, self.pos.y, self.color)


class ReflectingPixel(Pixel):
    def __init__(self, x, y, **kwargs):
        Pixel.__init__(self, x, y, **kwargs)
        self.factor = [1, 1]

    def reflect_x(self):
        self.factor[0] = self.previous.x - self.pos.x

    def reflect_y(self):
        self.factor[1] = self.previous.y - self.pos.y

    def move(self, dx, dy):
        Pixel.move(self, dx * self.factor[0], dy * self.factor[1])
