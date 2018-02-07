from sense_hat import SenseHat, ACTION_RELEASED
from point import LedBar, Dot
from signal import pause
import atexit

sense = SenseHat()
atexit.register(sense.clear)

#=================================================
# Receivers

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


#=============================================
# Commands

'''added here only to mimic the interface'''


class Command:
    def execute(self):
        pass


''' commands to manage the Heating device '''


class HeatWarmUpCommand(Command):
    def __init__(self, reciver):
        self.heating = reciver

    def execute(self):
        self.heating.heatUp()


class HeatCoolDownCommand(Command):
    def __init__(self, reciver):
        self.heating = reciver

    def execute(self):
        self.heating.coolDown()


''' commands to manage the Light device'''


class LightBrightCommand(Command):
    def __init__(self, reciver):
        self.light = reciver

    def execute(self):
        self.light.bright()


class LightDarkCommand(Command):
    def __init__(self, reciver):
        self.light = reciver

    def execute(self):
        self.light.dark()


'''commands to manage the Stereo device'''


class StereoLoudCommand(Command):
    def __init__(self, reciver):
        self.stereo = reciver

    def execute(self):
        self.stereo.loud()


class StereoSilentCommand(Command):
    def __init__(self, reciver):
        self.stereo = reciver

    def execute(self):
        self.stereo.silent()


''' some bonus command to run several different commands'''


class MacroCommand(Command):
    def __init__(self, *args):
        self.commands = args

    def execute(self):
        for cmd in self.commands:
            cmd.execute()


#====================================================
#  Invoker.

class Joystick:
    def __init__(self):
        self.slotCommands = []
        self.slot = 0
        self.slotSelector = Dot(7, 0, (255, 0, 100), sense)

        # some senseHat joystick initialization
        sense.stick.direction_up = self.slotChanged
        sense.stick.direction_down = self.slotChanged
        sense.stick.direction_left = self.setDown
        sense.stick.direction_right = self.setUp

    # assign the commend to invoker
    def addActions(self, up_cmd, down_cmd):
        self.slotCommands.append((up_cmd, down_cmd))

    # execute appropriate command on key press
    def setUp(self, event):
        if event.action != ACTION_RELEASED:
            cmd = self.slotCommands[self.slot]
            cmd[0].execute()

    def setDown(self, event):
        if event.action != ACTION_RELEASED:
            cmd = self.slotCommands[self.slot]
            cmd[1].execute()

    # select different device
    def slotChanged(self, event):
        if event.action != ACTION_RELEASED:
            if event.direction == "down":
                if self.slot < len(self.slotCommands) - 1:
                    self.slot += 1
                    self.slotSelector.move(0, 1)
            if event.direction == "up":
                if self.slot > 0:
                    self.slot -= 1
                    self.slotSelector.move(0, -1)


if __name__ == '__main__':
    # create devices (Receivers)
    light = Lights(0)
    stereo = Stereo(1)
    heat = Heating(2)

    all_up = MacroCommand(LightBrightCommand(light),
                          StereoLoudCommand(stereo),
                          HeatWarmUpCommand(heat))

    all_down = MacroCommand(LightDarkCommand(light),
                            StereoSilentCommand(stereo),
                            HeatCoolDownCommand(heat))

    joy = Joystick()
    # create and assign commands
    joy.addActions(LightBrightCommand(light), LightDarkCommand(light))
    joy.addActions(StereoLoudCommand(stereo), StereoSilentCommand(stereo))
    joy.addActions(HeatWarmUpCommand(heat), HeatCoolDownCommand(heat))
    joy.addActions(all_up, all_down)

    pause()
