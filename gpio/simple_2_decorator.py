'''
 LED connected to GPIO pin 4
 Button connected to the pin 15.
 
 turn the LED on/off on the button press.
 
 # version 2.
 decorated callback function with
 local variable holding LED state and 
 reference to the LED instance
'''

from gpiozero import LED, Button
from time import sleep

# initialize button and LED
led = LED(4)
button = Button(15)
is_led_on = False


# decorator
def setargs(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@setargs(is_led_on=False, led=led)
def on_press(btn):
    print "+ button %d: pressed" % btn.pin.number
    on_press.led.off() if on_press.is_led_on else on_press.led.on()
    on_press.is_led_on = not on_press.is_led_on


button.when_pressed = on_press


if __name__ == "__main__":
    try:
        # wait till keypress
        while True:
            sleep(10)

    except KeyboardInterrupt:
        exit(0)
