from gpiozero import LED, Button
from time import sleep

# initialize button and LED
led = LED(4)
button = Button(15)


class ButtonPressAction:
    def __init__(self, _led):
        self.led = _led
        self.is_led_on = False

    def __call__(self, btn):
        print "+ button: pressed"
        if self.is_led_on:
            self.led.off()
        else:
            self.led.on()
        self.is_led_on = not self.is_led_on


button.when_pressed = ButtonPressAction(led)


def led_on_off():
    # blink the LED
    led.on()
    led.off()


if __name__ == "__main__":
    try:
        led_on_off()

        # wait till keypress
        while True:
            sleep(10)

    except KeyboardInterrupt:
        exit(0)
