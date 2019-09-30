import random
import serial


class Sensor:
    def __init__(self, no_port='0'):
        self._port = no_port
        self.data = random.randrange(50) + 10


    def _read_data(self):
        self.data += random.randrange(3) - 1

    def get_data(self):
        self._read_data()
        return self.data


class HumiditySensor(Sensor):
    def __init__(self):
        Sensor.__init__(self)


class TempSensor(Sensor):
    def __init__(self):
        Sensor.__init__(self)


