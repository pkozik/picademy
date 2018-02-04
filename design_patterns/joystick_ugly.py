from sense_hat import SenseHat, ACTION_RELEASED
from point import Pixel, LedBar, Dot
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
        self.id = idx


class Heating(Device):
    def coolDown(self):
        self.ledbar.down()
        print("slot: %d > Heating down" % self.id)

    def heatUp(self):
        if self.ledbar.current < 5:
            self.ledbar.up()
            print("slot: %d > Heating up" % self.id)


class Lights(Device):
    def dark(self):
        self.ledbar.down()
        print("slot: %d > Lights down" % self.id)

    def bright(self):
        if self.ledbar.current < 5:
            self.ledbar.up()
            print("slot: %d > Lights up" % self.id)


class Stereo(Device):
    def silent(self):
        self.ledbar.down()
        print("slot: %d > Music down" % self.id)

    def loud(self):
        if self.ledbar.current < 5:
            self.ledbar.up()
            print("slot: %d > Music up" % self.id)


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
        self.slot = 0
        self.slotSelector = Dot(7, 0, (255, 0, 100), sense)

        sense.stick.direction_up = self.slotChanged
        sense.stick.direction_down = self.slotChanged
        sense.stick.direction_left = self.setDown
        sense.stick.direction_right = self.setUp

    # joystick must know each device by name, and must
    # know the interface to manage each device
    def setUp(self, event):
        if event.action != ACTION_RELEASED:
            dev = self.devices[self.slot]
            if isinstance(dev, Stereo):
                dev.loud()
            elif isinstance(dev, Lights):
                dev.bright()
            elif isinstance(dev, Heating):
                dev.heatUp()

    def setDown(self, event):
        if event.action != ACTION_RELEASED:
            dev = self.devices[self.slot]
            if isinstance(dev, Stereo):
                dev.silent()
            elif isinstance(dev, Lights):
                dev.dark()
            elif isinstance(dev, Heating):
                dev.coolDown()

    def slotChanged(self, event):
        if event.action != ACTION_RELEASED:
            if event.direction == "down":
                if self.slot < len(self.devices) - 1:
                    self.slot += 1
                    self.slotSelector.move(0, 1)
            if event.direction == "up":
                if self.slot > 0:
                    self.slot -= 1
                    self.slotSelector.move(0, -1)


if __name__ == '__main__':
    joy = Joystick()
    pause()
