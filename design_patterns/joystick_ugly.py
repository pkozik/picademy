from sense_hat import SenseHat, ACTION_RELEASED
from point import Pixel, LedBar
from signal import pause
import atexit

sense = SenseHat()
atexit.register(sense.clear)


# we have several devices to manage.
# we can smoothly set them up and down (e.g. volume up/down)
# To visualize, each is drawn on senseHat as colored led bar
class Device:
    def __init__(self, idx):
        self.ledbar = LedBar(idx, sense)


class Heating(Device):
    def coolDown(self):
        self.ledbar.down()

    def heatUp(self):
        if self.ledbar.current < 4:
            self.ledbar.up()


class Lights(Device):
    def dark(self):
        self.ledbar.down()

    def bright(self):
        if self.ledbar.current < 4:
            self.ledbar.up()


class Stereo(Device):
    def silent(self):
        self.ledbar.down()

    def loud(self):
        if self.ledbar.current < 4:
            self.ledbar.up()


#====================================================
# this is our controller.
# You can use:
#   up/down - to select device
#   left/right - to customize settings on selected device
#
# Notice the tight coupling of the components
class Joystick:
    def __init__(self):
        self.devices = (Stereo(0), Lights(1), Heating(2))
        self.selection = 0
        self.pix = Pixel(7, self.selection, (0, 200, 200))

        # draw elements
        self.pix.draw(sense)

        sense.stick.direction_up = self.selectionDown
        sense.stick.direction_down = self.selectionUp
        sense.stick.direction_left = self.setDown
        sense.stick.direction_right = self.setUp

    def refresh(self):
        self.pix.clear(sense)
        self.pix.y = self.selection
        self.pix.draw(sense)

    # joystick must know each device by name, and must
    # know the interface to manage each device
    def setUp(self, event):
        if event.action != ACTION_RELEASED:
            dev = self.devices[self.selection]
            if isinstance(dev, Stereo):
                dev.loud()
            elif isinstance(dev, Lights):
                dev.bright()
            elif isinstance(dev, Heating):
                dev.heatUp()

    def setDown(self, event):
        if event.action != ACTION_RELEASED:
            dev = self.devices[self.selection]
            if isinstance(dev, Stereo):
                dev.silent()
            elif isinstance(dev, Lights):
                dev.dark()
            elif isinstance(dev, Heating):
                dev.coolDown()

    def selectionUp(self, event):
        if event.action != ACTION_RELEASED:
            if self.selection < len(self.devices):
                self.selection += 1
                self.refresh()

    def selectionDown(self, event):
        if event.action != ACTION_RELEASED:
            if self.selection > 0:
                self.selection -= 1
                self.refresh()


if __name__ == '__main__':
    joy = Joystick()
    pause()
