import sys
import serial
import numpy as np
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QLCDNumber, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton

import Plot
import Table

class DataReader:
    def __init__(self, address):
        # need to find a way to always find the correct serial port
        self.ser = serial.Serial(address)

    def read(self):
        return self.ser.readline().decode('utf-8').strip()

    def readall(self):
        # maybe need to implement this eventually?
        raise NotImplementedError
    
    def flush(self):
        self.ser.read_all()

    def __del__(self):
        self.ser.__exit__()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'QLS'
        self.width = 780
        self.height = 400
        self.reader = DataReader('/dev/cu.usbmodemFA131')   #needs to change to appropriate serial port
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.active = False     # when true, update logic will run
        self.timer.start(500)   # the delay between each update, should actually sync with the baud rate and the arduino sample rate, but this works for now
        self.plot = None
        self.table = None
        self.data_readout_count = 0     #used as replacement for time series in data right now, can be converted by multiplying by delay between collections
        self.initUI()

    def initUI(self):
        # init window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # setup start and stop buttons
        start_button = QPushButton('Start', self)
        pause_button = QPushButton('Pause', self)
        clear_button = QPushButton('Clear', self)
        export_button = QPushButton('Export', self)
        start_button.setToolTip('This starts data collection')
        pause_button.setToolTip('This pauses data collection')
        clear_button.setToolTip('This clears all collected data')
        export_button.setToolTip('This generates a csv of currently collected data')
        start_button.clicked.connect(self.start)
        pause_button.clicked.connect(self.pause)
        clear_button.clicked.connect(self.clear)
        export_button.clicked.connect(self.export)

        # where the stop, start buttons live
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(start_button)
        button_layout.addWidget(pause_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(export_button)

        # setup the matplotlib figure
        self.plot = Plot.Plot(width=10, height=8)

        # setup the table
        self.table = Table.Table()

        # where the figure and table eventually live
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.plot)

        # putting all the layouts together
        full_layout = QVBoxLayout()
        full_layout.addStretch(1)
        full_layout.addLayout(main_layout)
        full_layout.addLayout(button_layout)
        self.setLayout(full_layout)

    def start(self):
        print('start')
        self.active = True
        self.reader.flush()

    def pause(self):
        print('pause')
        self.active = False

    def clear(self):
        print('clear')
        self.active = False
        self.plot.clear()
        self.table.clear()

    def export(self):
        print('export')
        self.active = False
        output = self.plot.getData()
        print(output)   #just for testing
        np.savetxt("output.csv", output, delimiter=",")

    def update(self):
        if self.active:
            try:
                data = float(self.reader.read())
                self.table.addData(newx=self.data_readout_count, newy=data)
                self.plot.updateDraw(newx=self.data_readout_count, newy=data)
                self.data_readout_count += 1
                print(data)
                sys.stdout.flush()
            except:
                print('error updating, probably just no new data')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
