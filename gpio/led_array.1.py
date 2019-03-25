from gpiozero import LED, Button
from time import sleep

MAX_SPEED = 2
MIN_SPEED = 0.2
speed = 0.6
Button.delta = 0.2

def on_btn_press(btn):
    global speed
    new_val = speed + btn.delta
    if new_val > MIN_SPEED and new_val < MAX_SPEED:
        speed = new_val

up = Button(20)
up.delta = 0.2
up.when_pressed = on_btn_press

down = Button(25)
down.delta = -0.2
down.when_pressed = on_btn_press


leds = [
	LED(4),
	LED(17),
	LED(5),
	LED(6),
	LED(13)
]

def turn_on_leds(leds, value):
    for pos, led in enumerate(leds):
        if pos < len(value):
            if value[pos]:
                led.on()
            else:
                led.off()


def shift_left(arr):
    x = arr.pop(0)
    arr.append(x)


def go(onoff):
    while True:
        shift_left(onoff)
        print "speed=%f %s" % (speed, onoff)
        turn_on_leds(leds, onoff)        
        sleep(speed)


twins = [1,1,0,0,0]
blink = [0,1,0,1,0,1]
fill = [0,0,0,0,1,1,1,1,1]


if __name__ == "__main__":
    try:
        go(blink)

    except KeyboardInterrupt:
        exit(0)


