from gpiozero import LED, Button
from time import sleep

# initialize button and LED
led = LED(4)
button = Button(15)

button.when_pressed = led.toggle


if __name__ == "__main__":
    try:
        # wait till keypress
        while True:
            sleep(10)

    except KeyboardInterrupt:
        exit(0)
