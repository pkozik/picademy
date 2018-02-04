'''
 some code example demonstrating the observer pattern
'''

from sense_hat import SenseHat, ACTION_RELEASED
from point import Dot, LedBar
from signal import pause
import atexit

sense = SenseHat()
atexit.register(sense.clear)

#=====================================================
# some base class for our Devices, not to
# repeat the same code over and over again.
# Notice: the device doesn't know anything about the
# joystick implementation.


class Device:
    def __init__(self, idx):
        self.ledbar = LedBar(idx, sense)
        self.id = idx
        self.selected = False

    # callback called whenever the joystick changes
    # the slot selection
    def selectionRefresh(self, slot):
        self.selected = (slot == self.id)

    # must be overwritten in derived class
    # It will be called whenever the joystick changes the
    # value
    def adjust(self, direction):
        pass

    # method called by joystick whenever its state changes
    def update(self, **kwargs):
        if "slot" in kwargs:
            self.selectionRefresh(kwargs["slot"])

        if "value" in kwargs:
            if self.selected:
                self.adjust(kwargs["value"])


class Heating(Device):

    def adjust(self, direction):
        if direction == ">":
            self.heatUp()
        else:
            self.coolDown()

    def coolDown(self):
        self.ledbar.down()
        print("slot %d > Heating down" % self.id)

    def heatUp(self):
        if self.ledbar.current < 6:
            self.ledbar.up()
            print("slot %d > Heating up" % self.id)


class Lights(Device):
    def adjust(self, direction):
        if direction == ">":
            self.bright()
        else:
            self.dark()

    def dark(self):
        self.ledbar.down()
        print("slot %d > Light down" % self.id)

    def bright(self):
        if self.ledbar.current < 4:
            self.ledbar.up()
            print("slot %d > Light up" % self.id)


class Stereo(Device):
    def adjust(self, direction):
        if direction == ">":
            self.loud()
        else:
            self.silent()

    def silent(self):
        self.ledbar.down()
        print("slot %d > Stereo down" % self.id)

    def loud(self):
        if self.ledbar.current < 5:
            self.ledbar.up()
            print("slot %d > Stereo up" % self.id)


#====================================================
# this is our controller.
# You can use:
#   up/down - to select device
#   left/right - to customize settings on selected device
#
# Notice the loose coupling of the components. Joystick
# doesn't know anything abut the devices. Any device can
# be the observer. It only must have update(**kwargs) method
class Joystick:
    def __init__(self):

        # list of observers
        self.devices = []
        self.slot = 0
        self.slotSelector = Dot(7, 0, (255, 0, 100), sense)

        # just some senseHat joystick initialization
        sense.stick.direction_up = self.slotChanged
        sense.stick.direction_down = self.slotChanged
        sense.stick.direction_left = self.setValueDown
        sense.stick.direction_right = self.setValueUp

    # used by observers to register
    def registerDevice(self, device):
        self.devices.append(device)

    # notify all observers that internal change has changed.
    # kwargs contains subject of change
    def notify(self, **kwargs):
        for dev in self.devices:
            dev.update(**kwargs)

    def setValueUp(self, event):
        if event.action != ACTION_RELEASED:
            self.notify(value=">")

    def setValueDown(self, event):
        if event.action != ACTION_RELEASED:
            self.notify(value="<")

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

            self.notify(slot=self.slot)


if __name__ == '__main__':
    # subject
    joy = Joystick()

    # create devices (observers)
    light = Lights(0)
    stereo = Stereo(1)
    heat = Heating(2)
    # demonstrate adding yet another observer
    # light2 = Lights(3)

    # register observers
    joy.registerDevice(light)
    joy.registerDevice(stereo)
    joy.registerDevice(heat)
    # joy.registerDevice(light2)

    # send some notification to refresh the screen
    joy.notify(slot=0)
    pause()
