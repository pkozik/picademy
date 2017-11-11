from gpiozero import LED, Button
from time import sleep

# initialize button and LED
led = LED(4)
button = Button(15)


def button_press_action(button):
    print "Button %s pressed" % button.pin.number


button.when_pressed = button_press_action


def led_on_off():
    led.on()
    sleep(4)
    led.off()


if __name__ == "__main__":
    try:
        led_on_off()

        # wait till keypress
        while True:
            sleep(10)

    except KeyboardInterrupt:
        exit(0)
