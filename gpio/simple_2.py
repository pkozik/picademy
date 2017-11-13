'''
 LED connected to GPIO pin 4
 Button connected to the pin 15.
 
 turn the LED on/off on the button press.
 
 # option 1
 using global variables in callback
'''

from gpiozero import LED, Button
from time import sleep

# initialize button and LED
led = LED(4)
button = Button(15, pull_up=False)
is_led_on = False


def on_press(btn):
    global is_led_on
    global led

    print "+ button %d: pressed" % btn.pin.number
    led.off() if is_led_on else led.on()
    is_led_on = not is_led_on


button.when_pressed = on_press


if __name__ == "__main__":
    try:
        # wait till keypress
        while True:
            sleep(10)

    except KeyboardInterrupt:
        exit(0)
