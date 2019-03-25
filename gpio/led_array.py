from gpiozero import LED, Button
from time import sleep

# initialize button and LED

up = Button(20)
down = Button(25)

leds = [
	LED(4),
	LED(17),
	LED(5),
	LED(6),
	LED(13)
]

speed = 0.5

def up_press(btn):
    global speed
    if speed < 2:
        speed += 0.2

up.when_pressed = up_press

def down_press(btn):
    global speed
    if speed > 0.2:
        speed -= 0.2

down.when_pressed = down_press


def turn_on_leds(leds, idx):
    for pos, led in enumerate(leds):
        if idx == pos:
		    led.on()
        else:
            led.off()


def led_off(leds):
    for led in leds:
        led.off()


def go():
    for ix in range(100000):
        print "iteration: %d, speed=%f" % (ix, speed)
        turn_on_leds(leds, ix % len(leds))
        sleep(speed)


if __name__ == "__main__":
    try:
        go()

    except KeyboardInterrupt:
        exit(0)


