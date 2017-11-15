#!/bin/python
'''
get the humidity, temperature and pressure from the
sensors and display it on the LED matrix 

'''

from sense_hat import SenseHat

sense = SenseHat()
sense.low_light = True

humidity = sense.get_humidity()
temp = sense.get_temperature()
pressure = sense.get_pressure()


info = "Humidity: %.1f %%rH, Temperature: %.1f C, Pressure: %.1f Millibars" % (
    humidity, temp, pressure)
sense.show_message(info, text_colour=(0, 100, 100), scroll_speed=0.1)
sense.clear()
