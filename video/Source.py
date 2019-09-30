import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from matplotlib.figure import Figure
import matplotlib as mplt
from matplotlib.backends.backend_agg import FigureCanvasAgg as Canvas
import video.effects as eff
from data import DataSource as ds
IMG_SIZE = 224

class Video(object):
    def __init__(self,device=0,effect=eff.default):
        self.__feed__ = cv2.VideoCapture(device)
        self.__effect__ = effect
        self.__current_bytes__ = None
        self.__temp_path = '../data/viewer_temp.jpg'
        self.shape = (640, 480, 3)
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        self.__class__.__call__ = lambda x:x

    def __del__(self):
        self.__feed__.release()

    def read(self,resize=0):
        success, image = self.__feed__.read()
        if not success:
            return cv2.imencode('.jpeg', np.zeros(self.shape))
        cv2.imwrite(self.__temp_path, image)
        try:
            if resize != 0:
                image = cv2.resize(image, (resize,resize))

            if not isinstance(self.__effect__, (list, tuple)):
                return self.__effect__(image)
            else:
                self.__effect__.reverse()
                for e in self.__effect__:
                    image = e(image)

                return image
        except:
            return image

    def buffer_image(self):
        try:
            image = cv2.imread(self.__temp_path)
            print(image.shape)
        except:
            image = np.zeros(shape=(IMG_SIZE, IMG_SIZE, 3))

        return image

    def snapshot(self):
        image = self.read()
        try:
            ret, jpeg = cv2.imencode('.jpeg', image)
            jpeg = cv2.cvtColor(jpeg, cv2.COLOR_BGR2RGB)
            return jpeg
        except:
            ret, jpeg = cv2.imencode('.jpeg', np.zeros(self.shape))
            return jpeg

    def get_frame(self, write_temp_file=False):
        image = self.read()
        try:
            ret, jpeg = cv2.imencode('.jpeg', image)
            self.shape = image.shape
            self.__current_bytes__ = jpeg.tobytes()

        except:
            if self.__current_bytes__ is None:
                ret, jpeg = cv2.imencode('.jpeg', np.zeros(self.shape))
                self.__current_bytes__ = jpeg.tobytes()

        return self.__current_bytes__

    def from_current_bytes(self):
        try:
            return cv2.imdecode(np.frombuffer(self.__current_bytes__, np.uint8), -1)
        except:
            return


class Plot(object):
    def __init__(self, X="Time", Y="Temperature", title='', bufSize = 10, color="red", datasource=None):
        if datasource is None:
            self.dataSource = ds.RealTimeData()
        else:
            self.dataSource = datasource
        self.x = [X]
        self.y = [Y]
        self.inputX = [self.dataSource.to_dict()[X]]*(bufSize+1)
        #self.inputX.append(self.dataSource.to_dict()[X])
        self.inputY = [self.dataSource.to_dict()[Y]]*(bufSize+1)
        #self.inputY.append(self.dataSource.to_dict()[Y])
        self.history = [time.strftime('%M:%S', time.gmtime())] * len(X)
        self.__bufSize = bufSize + 1
        self.__title = title
        self.trace = plt.plot
        self.plot = None
        self.__fig = None
        self.__canvas = None
        self.fig = None
        self.color = color
        self.__freq = 10

    def __acquire(self, x_axis="Time", y_axis="Time"):
        rtd = self.dataSource.to_dict()
        xval = rtd[x_axis]
        yval = rtd[y_axis]


        maxx = self.inputX[-1] +1
        self.inputX.append(xval)
        self.inputY.append(yval)

        return

    def add_plot(self,x,y,label):
        self.plot.plot(x, y, color=self.color, label=label)

    def __draw(self, n=10):

        if(self.__bufSize > len(self.inputX)):
            x = self.inputX
        else:
            x = self.inputX[-self.__bufSize:-1]

        if (self.__bufSize > len(self.inputY)):
            y = self.inputY
        else:
            y = self.inputY[-self.__bufSize:-1]

        self.plot = self.__fig.add_subplot(111)
        #p.spines['left'].set_position('center')
        #p.spines['bottom'].set_position('center')
        self.plot.spines['right'].set_color('none')
        self.plot.spines['top'].set_color('none')
        self.plot.margins(0, 0)
        self.plot.set_xlim([np.min(x), np.max(x)])

        colors = mplt.cm.cool(np.linspace(0,1,n))
        self.plot.set_ylim([0, np.max(y)*1.1])
        self.plot.set_xticks([])


        #Adding funtion plots
        self.add_plot(x,y,self.y[0])
        self.plot.legend(self.y[0], loc="upper right")

    def __render(self):
        self.__fig = Figure(figsize=(8, 4.5), dpi=150)
        self.__canvas = Canvas(figure=self.__fig)
        self.__draw()
        
        self.__canvas.draw()
        s, (width, height) = self.__canvas.print_to_buffer()
        self.fig = np.fromstring(s, np.uint8).reshape((height, width, 4))

    def get_frame(self, x_axis, y_axis):
        self.__render()
        try:
            self.__acquire(x_axis, y_axis)
        except:
            pass

        try:
            img = cv2.cvtColor(self.fig, cv2.COLOR_BGR2RGB)
            ret, jpeg = cv2.imencode('.jpeg', img)
            self.shape = self.fig.shape
            return jpeg.tobytes()
        except:
            ret, jpeg = cv2.imencode('.jpeg', np.zeros(self.shape))
            return jpeg.tobytes()

