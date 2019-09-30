import pymongo as mongo
import subprocess
import time
import random
import json
from data.sensors import *
from video import effects as eff
from video import Source as src
from video import DataVisualizer as dv
from data.models.ImageClassifier import predict
DEFAULT_ADDRESS = "127.0.0.1"
euc_d = 0
class RealTimeData(object):
    def __init__(self, video_source=0, server=None):
        self.server = server
        self.start_time = time.time()
        self.time = 0
        self.temperature = TempSensor()
        self.humidity = HumiditySensor()

        self._interval = 1
        self.source = src.Video(video_source, effect=eff.bilateral)
        self.state = {}
        self.sensor_plot = dv.Plot(buffer=30, datasource=self, vtype='bar')
        self.sensor_plot.DEFAULT_Y = ["Temperature", "Humidity"]
        self.state_plot = dv.Plot(buffer=10, datasource=self, vtype='bar')
        self.state_plot.DEFAULT_Y = ["none", "Fire"]

        self.state = dict((k, 0.01*random.randint(0, 100)) for k in self.state_plot.DEFAULT_Y)

    def __get(self):
        global euc_d
        self.time = self.time + self._interval
        try:
            self.server.system.step()
        except:
            pass
        frame = self.source.from_current_bytes()
        if frame is not None:
            self.state = predict([frame])
        #time.sleep(self._interval)


    def to_dict(self):
        self.__get()
        d = {"Time": self.time,
             "Temperature": self.temperature.get_data(),
             "Humidity": self.humidity.get_data(),
            }
        d.update(self.state)
        return d

    def json(self):
        return json.dumps(self.to_dict())


class DBSource(object):
    def __init__(self, address=DEFAULT_ADDRESS, column_name="Default"):
        self.__mongod = subprocess.Popen("mongod", shell=False)
        self.__client = mongo.MongoClient("mongodb://"+address+":27017/", connect=False)
        self.__db = self.__client["FireDetector"]
        self._col_name = column_name
        self.__col = self.__db[self._col_name]

    def insert(self, d):
        x = self.__col.insert_many(d)
        return x.inserted_ids

    def insertRealTime(self, rtd=None):
        if rtd is None:
            rtd = RealTimeData()
        rtd.get()
        d = rtd.to_dict()
        x = self.__col.insert_one(d)
        return d

    def get(self, history=0):
        find = self.__col.find()
        x =[]
        for f in find:
            x.append(f)
        #x = x.sort()
        if history == 0:
            return x
        return x[-history:]

    def reset(self):
        self.__col.drop()
        self.__col = self.__db[self._col_name]

    def terminate(self):
        self.__mongod.terminate()


