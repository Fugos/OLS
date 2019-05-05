from PyQt5.QtWidgets import QApplication, QLCDNumber, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

class Plot(FigureCanvas):
    def __init__(self, title="", xlabel="", ylabel="", parent=None, axes_params=None, width=1, height=1, dpi=65, x=[], y=[]):
        self.name = 'plot_' + xlabel + '_' + ylabel
        self.x = np.array(x)
        self.y = np.array(y)

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.plot_data, = self.axes.plot(x, y, 'r-')

    def updateDraw(self, newx, newy):
        self.x = np.append(self.x, np.array(newx))
        self.y = np.append(self.y, np.array(newy))

        if self.x.size and self.y.size:
            ymin = round(np.min(self.y), 0) - 1
            ymax = round(np.max(self.y), 0) + 1
            xmin = round(np.min(self.x), 0) - 1
            xmax = round(np.max(self.x), 0) + 1
            self.axes.set_xbound(lower=xmin, upper=xmax)
            self.axes.set_ybound(lower=ymin, upper=ymax)

        self.plot_data.set_xdata(self.x)
        self.plot_data.set_ydata(self.y)

        try:
            self.draw()
        except ValueError:
            print('Woops!\nSome drawing SNAFU happened.\n')

    def clear(self):
        self.x = np.array([])
        self.y = np.array([])
        self.plot_data.set_xdata(self.x)
        self.plot_data.set_ydata(self.y)
        try:
            self.draw()
        except ValueError:
            print('Woops!\nSome drawing SNAFU happened.\n')

    def getData(self):
        return np.vstack((self.x,self.y))

    

