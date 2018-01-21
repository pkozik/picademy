from sense_hat import SenseHat
import atexit
from time import sleep
from point import Point, x_in_range, y_in_range, point_in_range
from _collections import deque


def from_kwargs(kwargs, key, dflt):
    return kwargs[key] if kwargs and key in kwargs else dflt


class Pixel:
    '''
    Simple Pixel class which can be moved 
    on the Sense Hat LED Matrix.

    You can provide the pixel position, color,
    background color, and reference to the
    screen, where it shall be drawn.

    This class an example of using Template Method
    design pattern.
    '''

    def __init__(self, x, y, **kwargs):
        self.pos = Point(x, y)
        self.previous = Point(0, 0)
        self.color = from_kwargs(kwargs, "color", (0, 0, 128))
        self.bgcolor = from_kwargs(kwargs, "bgcolor", (0, 0, 0))
        self.screen = from_kwargs(kwargs, "screen", None)

    def move(self, dx, dy):
        '''
        This is our template method, defining some steps required
        to draw the pixel on the LED matrix.
        These steps can be easily redefined in the derived classes
        '''
        # 1) calculate the new position of the pixel
        npos = self.calc_new_pos(dx, dy)
        if npos == self.pos:
            return
        # 2) store the previous position in the history
        self.store_history()
        # 3) move the pixel to new position
        self.change_position(npos)
        # 4) draw the pixel on the screen
        self.draw_pixel()
        # clear the pixel at old position
        self.clear()

    def draw_pixel(self):
        if point_in_range(self.pos, self.screen):
            self.screen.set_pixel(self.pos.x, self.pos.y, self.color)

    def change_position(self, npos):
        self.pos = npos

    def store_history(self):
        self.previous = self.pos.clone()

    def calc_new_pos(self, dx, dy):
        return Point(self.pos.x + dx, self.pos.y + dy)

    def clear(self):
        if point_in_range(self.previous, self.screen):
            self.screen.set_pixel(
                self.previous.x, self.previous.y, self.bgcolor)


class EdgeReflectPixel(Pixel):
    '''
    Pixel reflecting from the screen edges.

    Re-implement only the calc_new_pos() step, to 
    change the direction when the pixel is on the screen
    edge
    '''

    def __init__(self, x, y, **kwargs):
        Pixel.__init__(self, x, y, **kwargs)
        self.xfactor = 1
        self.yfactor = 1

    def x_edge_hit(self):
        self.xfactor *= -1

    def y_edge_hit(self):
        self.yfactor *= -1

    # redefine the step 1)
    def calc_new_pos(self, dx, dy):
        npos = Pixel.calc_new_pos(self, dx * self.xfactor, dy * self.yfactor)

        if not x_in_range(npos, self.screen):
            self.x_edge_hit()
        if not y_in_range(npos, self.screen):
            self.y_edge_hit()

        return Pixel.calc_new_pos(self, dx * self.xfactor, dy * self.yfactor)


class EdgeStopPixel(EdgeReflectPixel):
    '''
    Pixel stopping at the screen edge.
    '''

    def x_edge_hit(self):
        self.xfactor = 0

    def y_edge_hit(self):
        self.yfactor = 0


class TailedPixel(EdgeReflectPixel):
    def __init__(self, x, y, **kwargs):
        EdgeReflectPixel.__init__(self, x, y, **kwargs)
        self.tail = from_kwargs(kwargs, "tail", 3)
        self.history = deque(maxlen=self.tail)

    # step 2 redefined
    def store_history(self):
        self.history.appendleft(self.pos.clone())

    # step 5 redefined
    def clear(self):
        for idx, point in enumerate(self.history):
            color = self.__fade_out_color(self.color, idx)
            self.screen.set_pixel(point.x, point.y, color)

    def __fade_out_color(self, color, step):
        hsize = len(self.history)
        return (
            color[0] - (color[0] * (step + 1)) // hsize,
            color[1] - (color[1] * (step + 1)) // hsize,
            color[2] - (color[2] * (step + 1)) // hsize
        )


# main
sense = SenseHat()
atexit.register(sense.clear)

sense.low_light = True
sense.width = 8
sense.height = 8


dot = TailedPixel(4, 1, color=(0, 0, 250), screen=sense, tail=3)


while True:
    dot.move(1, 1)
    sleep(0.1)
