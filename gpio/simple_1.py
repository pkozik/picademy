'''
simple example blinking the LED connected to the 
pin 4 on GPIO.
'''

from gpiozero import LED
from time import sleep

# initialize button and LED
led = LED(4)


def led_on_off():
    for ix in range(10):
        print "iteration: %d" % ix
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)


if __name__ == "__main__":
    try:
        led_on_off()

    except KeyboardInterrupt:
        exit(0)
