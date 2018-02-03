from sense_hat import SenseHat
'''
This example presents how to apply the Object Oriented
Programming Principles to write more manageable, extensible
and reusable code.

Please refer to weather_station_ugly.py for initial code.

We used here:
* Open-closed Principle (WeatherStation)
* Dependency Inversion Principle (Sensors and WeatherStation)
* Composition over Inheritance 
* Program to Interfaces (Python uses duck typing, so interfaces
   are not "pythonic", but we tried to mimic this
* Loose coupling
'''

# sensors do not inherit from Sense but rather
# use composition to hold the Sense inplementation


class SensorBase():
    def __init__(self, impl):
        self.impl = impl

    # it is not needed needed (duck typing)
    # added just to mimic the interface
    def get_value(self):
        pass

    def get_name(self):
        pass

#============================================


class TemperatureSensor(SensorBase):
    def get_value(self):
        return self.impl.get_temperature()

    def get_name(self):
        return "Temperature"


#============================================
class HumiditySensor(SensorBase):
    def get_value(self):
        return self.impl.get_humidity()

    def get_name(self):
        return "Humidity"

#============================================


class PressureSensor(SensorBase):
    def get_value(self):
        return self.impl.get_pressure()

    def get_name(self):
        return "Pressure"


#============================================
class WeatherStation:
    def __init__(self):
        self.sensors = []

    def addSensor(self, sensor):
        self.sensors.append(sensor)

    def getInfo(self):
        info = ""
        for sensor in self.sensors:
            info += "%s: %0.2f " % (sensor.get_name(), sensor.get_value())
        return info


#==========================================
# some Mock classes to present the flexibility of new
# design
class SenseMock():
    def get_temperature(self):
        return 123.00

    def get_pressure(self):
        return 234.00

    def get_humidity(self):
        return 345.00

#=======================================
# new sensor we want to add to station


class SmogMetter():
    def get_value(self):
        return 100000.12

    def get_name(self):
        return "Smog"


if __name__ == '__main__':
    #sense = SenseMock()
    sense = SenseHat()

    wstation = WeatherStation()
    wstation.addSensor(HumiditySensor(sense))
    wstation.addSensor(PressureSensor(sense))
    wstation.addSensor(TemperatureSensor(sense))
    # adding new sensor is simple
    wstation.addSensor(SmogMetter())

    print wstation.getInfo()
