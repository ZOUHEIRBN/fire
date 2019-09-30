import random
import serial
import time
SKEYS = {"DHT": ["Humidity", "Temperature"]}
class Sensor:
    def __init__(self, no_port='0', sensor_type=None):
        self._port = no_port
        #self._arduino = serial.Serial('com15', 9600)
        __class__._arduino = serial.Serial('com15', 9600)
        time.sleep(2)
        self.sensor_data = {}
        if not sensor_type:
            self._sensor_keys = ["Humidity", "Temperature"]
        else:
            try:
                self._sensor_keys = SKEYS[sensor_type]
            except:
                self._sensor_keys = ["Humidity", "Temperature"]


    def _read_data(self):
        b = self._arduino.readline()
        result = b.decode().rstrip()
        result = str(result)
        for k in self._sensor_keys:
            if result.startswith(k):
                value = float(result.replace(k + ": ", ''))
                if value > -999:
                    self.sensor_data[k] = value

        time.sleep(1)

    def get_data(self):
        self._read_data()
        return self.sensor_data


class HumiditySensor(Sensor):
    def __init__(self):
        Sensor.__init__(self, sensor_type="DHT")

    def get_data(self):
        self._read_data()
        return self.sensor_data["Humidity"]

class TempSensor(Sensor):
    def __init__(self):
        Sensor.__init__(self, sensor_type="DHT")

    def get_data(self):
        self._read_data()
        return self.sensor_data["Temperature"]

