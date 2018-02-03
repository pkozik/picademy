from sense_hat import SenseHat

sense = SenseHat()


# we have several weather sensors which are
# used by WatherStation. Each sensor has different
# API do get measurements
class TemperatureSensor():
    def get_temperature(self):
        return sense.get_temperature()


class HumiditySensor():
    def get_humidity(self):
        return sense.get_humidity()


class PressureSensor():
    def get_pressure(self):
        return sense.get_pressure()

# we have the WeatherStation, which is
# tightly coupled with Sensors


class WeatherStation:
    def __init__(self):
        self.sensors = [HumiditySensor(), PressureSensor(),
                        TemperatureSensor()]

    # WeaterStation must know all Sensors by name
    # and know which method must be call for each
    def getInfo(self):
        info = ""
        for sensor in self.sensors:
            if isinstance(sensor, TemperatureSensor):
                info += " temp: %0.2f" % sensor.get_temperature()
            elif isinstance(sensor, HumiditySensor):
                info += " hum: %0.2f" % sensor.get_humidity()
            elif isinstance(sensor, PressureSensor):
                info += " press: %0.2f" % sensor.get_pressure()
            else:
                info += " not supported"

        return info


if __name__ == '__main__':

    wstation = WeatherStation()
    print wstation.getInfo()
