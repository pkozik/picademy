#!/bin/python

'''
use sense_hat joystick to move the pixel around 
the LED matrix. 
when middle button is pressed, exit the program
  
'''


from sense_hat import SenseHat, ACTION_RELEASED
from time import sleep

x = 3
y = 3
keep_go = True
sense = SenseHat()
sense.low_light = True

# make sure we are not go out of the edges of the LED matirx


def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))


def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y - 1)


def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y + 1)


def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x - 1)


def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x + 1)


def bye():
    global keep_go
    keep_go = False

# redraw the pixel


def refresh():
    sense.clear()
    sense.set_pixel(x, y, 0, 120, 50)


# initialize the joystick with appropriate callback functions
sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_any = refresh
sense.stick.direction_middle = bye

refresh()
while keep_go:
    sleep(2)

sense.clear()
print "Bye!"