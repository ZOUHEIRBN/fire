import pandas as pd
import matplotlib as mplt
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as Canvas
from data import DataSource as ds
import tensorflow as tf
if tf.__version__ >= '2.0.0':
    from data.models.ImageClassifier import LABELS
else:
    from data.models.ImageClassifier_legacy import LABELS

DEFAULT_STEP = 5
PLOT_GRAD = [(0, 1, 0), (.5, .5, 0), (1, 0, 0)]
PLOT_META = {
    "none": {'color': (0, 0, 0), 'unit': '°C', 'plot_method': 'bar', 'boundaries': [0, 100]},
    "Fire": {'color': (1, .5, 0), 'unit': '°C', 'plot_method': 'bar', 'boundaries': [0, 100]},
    "Temperature": {'color': (1, 0, 0), 'unit': '°C', 'plot_method': 'plot', 'boundaries': [10, 30]},
    "Humidity": {'color': (0, 0, .5), 'unit': '%', 'plot_method': 'plot', 'boundaries': [0, 100]},
}
def generate_gradient():
    global PLOT_GRAD
    arr = np.array([p for p in PLOT_GRAD])
    arr = arr.transpose()
    linsp = []
    for a in arr:
        steps = 100//(len(a)-1)
        sub = []
        for i in range(1, len(a)):
            sub.extend(np.linspace(a[i-1], a[i], steps))
        linsp.append(sub)

    return np.array(linsp).transpose()
PLOT_GRAD = generate_gradient()
class Plot(object):
    def __init__(self, datasource=None, buffer=25, vtype='plot'):
        if datasource is None:
            self.datasource = ds.RealTimeData()
        else:
            self.datasource = datasource
        self.DEFAULT_X = ["Time"]
        self.DEFAULT_Y = list(PLOT_META.keys())
        self.DEFAULT_VIEWTYPE = vtype
        self.figure, self.ax = plt.subplots()
        self.__bounds = [0, 100]
        self.plt_method = {}
        self._buffer_size = buffer
        L = []
        for i in range(buffer):
            L.append(datasource.to_dict())
        self.data = pd.DataFrame(L)
        self.color = {}
        Y = list(self.data.columns.values)
        for e in Y:
            if e not in PLOT_META.keys():
                self.plt_method[e] = "plot"
                self.color[e] = tuple([random.randrange(255)/255 for i in range(3)])
                continue

            if PLOT_META[e]["plot_method"]:
                self.plt_method[e] = PLOT_META[e]["plot_method"]
            else:
                self.plt_method[e] = "plot"

            if PLOT_META[e]["color"]:
                self.color[e] = PLOT_META[e]["color"]
            else:
                self.color[e] = tuple([random.randrange(255)/255 for i in range(3)])

    def refresh(self, datasource=None, vtype=None):
        if  datasource==None:
            datasource = self.datasource

        if vtype:
            self.DEFAULT_VIEWTYPE = vtype

        L = self.data.to_dict('records')
        d = datasource.to_dict()
        keys = self.DEFAULT_Y
        for k in keys:
            if k in d.keys():
                try:
                    v1 = L[-1][k]
                    v2 = L[-2][k]
                    der = v1-v2
                    d[k+'_drv'] = der + 0
                except:
                    d[k + '_drv'] = 0

        L.append(d)

        self.data = pd.DataFrame(L)
        cols = list(self.data.columns)
        for c in cols:
            #Fill null values with 0 and convert all to int for plotting
            self.data[c] = self.data[c].fillna(0)
            self.data[c] = pd.to_numeric(self.data[c]).astype(np.int64)

    def line_plot(self, Y=None):
        X = self.DEFAULT_X
        if not Y:
            Y = [t for t in self.DEFAULT_Y if t not in X]

        data = self.data.to_dict('list')

        leg = []
        for x in X:
            if len(self.data[x].values) > self._buffer_size:
                self.ax.set_xlim([self.data[x].values[-self._buffer_size], self.data[x].values[-1]])
                pass
            self.ax.set_xticks([])
            for y in Y:
                try:
                    try:
                        c = PLOT_META[y]['color']
                    except:
                        c = (0, 0, 0)

                    if min(data[y]) < 0:
                        self.__bounds[0] = min(data[y])
                    else:
                        self.__bounds[0] = 0


                    self.ax.plot(data[x], data[y], color=c)
                    leg.append(y)
                except:
                    continue

        self.ax.legend(leg, loc='upper left')

    def derived_line_plot(self, Y=None):
        X = self.DEFAULT_X
        if not Y:
            Y = [t for t in self.DEFAULT_Y if t not in X]

        data = self.data.to_dict('list')

        leg = []
        for x in X:
            if len(self.data[x].values) > self._buffer_size:
                self.ax.set_xlim([self.data[x].values[-self._buffer_size], self.data[x].values[-1]])
                pass
            self.ax.set_xticks([])
            for y in Y:
                try:
                    try:
                        c = PLOT_META[y]['color']
                    except:
                        c = (0, 0, 0)

                    self.__bounds[0] = -self.__bounds[1]

                    drvname = ''.join([y, '_drv'])
                    self.ax.plot(data[x], data[y], color=c)
                    leg.append(y)
                    self.ax.plot(data[x], data[drvname], color=c, linestyle="dashed")
                    leg.append(drvname.replace('_drv',' difference'))
                except:
                    continue

        self.ax.legend(leg, loc='upper left')

    def bar_plot(self, Y=None):
        X = self.DEFAULT_X
        if not Y:
            Y = [t for t in self.DEFAULT_Y if t not in X]

        lastdata = self.data.to_dict('records')[-1]
        self.__bounds[0] = 0
        try:
            dic = dict((k, int(float(lastdata[k]))) for k in Y)
        except:
            dic = dict((k, 1 / len(Y)) for k in Y)

        for y in Y:
            try:
                c = PLOT_META[y]['color']
            except:
                c = PLOT_GRAD[int(dic[y])]

            self.ax.bar(y, dic[y], color=c)

    def __render(self,X=None, Y=None):
        if not X:
            X = self.DEFAULT_X
        if not Y:
            Y = self.DEFAULT_Y


        self.ax.set_ylim(self.__bounds)
        if self._buffer_size < 12:
            self.ax.set_yticks(np.linspace(self.__bounds[0], self.__bounds[1], self._buffer_size - 1))
        else:
            self.ax.set_yticks(np.linspace(self.__bounds[0], self.__bounds[1], 11))

        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')

        if self.DEFAULT_VIEWTYPE.lower() == 'bar':
            self.bar_plot(Y)
        elif self.DEFAULT_VIEWTYPE.lower() == 'derived':
            self.derived_line_plot(Y)
        else:
            self.line_plot(Y)

        canvas = Canvas(figure=self.figure)
        canvas.draw()
        s, (width, height) = canvas.print_to_buffer()
        img = np.fromstring(s, np.uint8).reshape((height, width, 4))
        self.ax.clear()
        return img

    def get_frame(self,X=None, Y=None):
        image = self.__render(X, Y)
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ret, jpeg = cv2.imencode('.jpeg', image)
            return jpeg.tobytes()
        except:
            ret, jpeg = cv2.imencode('.jpeg', np.zeros(shape=(1, 1, 3)))
            return jpeg.tobytes()



