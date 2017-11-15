#!/usr/bin/python


class Pixel:
    def __init__(self, x, y, **kwargs):
        self.pos = [x, y]
        self.previous = [0, 0]
        self.color = kwargs["color"] if kwargs and "color" in kwargs else (
            0, 0, 128)
        self.bgcolor = kwargs["bgcolor"] if kwargs and "bgcolor" in kwargs else (
            0, 0, 0)

    @property
    def x(self):
        return self.pos[0] if self.pos else None

    @property
    def y(self):
        return self.pos[1] if self.pos else None

    def move(self, dx, dy):
        self.previous = list(self.pos)
        self.pos[0] += dx
        self.pos[1] += dy

    def set_color(self, color):
        self.color = color

    def clear(self, screen):
        if 0 <= self.previous[0] < screen.width and 0 <= self.previous[1] < screen.height:
            screen.set_pixel(self.previous[0], self.previous[1], self.bgcolor)

    def refresh(self, screen):
        if self.pos == self.previous:
            return

        # clear the pixel at old position
        self.clear(screen)
        # if we are still in the range of the screen
        if 0 <= self.x < screen.width and 0 <= self.y < screen.height:
            # draw new pixel
            screen.set_pixel(self.pos[0], self.pos[1], self.color)


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
