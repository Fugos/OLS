import sys
import serial
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QLCDNumber, QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton

import Plot

# need to implement data storage architecture (trials inside of an experiment)


class DataReader:
    def __init__(self, address):
        # need to find a way to always find the correct serial port
        self.ser = serial.Serial(address)

    def read(self):
        return self.ser.readline().decode('utf-8').strip()

    def readall(self):
        # maybe need to implement this
        raise NotImplementedError

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
        self.reader = DataReader('/dev/cu.usbmodemFA131')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.active = False     # when true, update logic will run
        self.timer.start(500)   # 100 is the delay between each update
        self.plot = None
        self.data_readout_count = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # setup start and stop buttons
        start_button = QPushButton('Start', self)
        pause_button = QPushButton('Pause', self)
        start_button.setToolTip('This starts data collection')
        pause_button.setToolTip('This pauses data collection')
        start_button.clicked.connect(self.start)
        pause_button.clicked.connect(self.pause)

        # where the stop, start buttons live
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(start_button)
        button_layout.addWidget(pause_button)

        # setup the matplotlib figure
        self.plot = Plot.Plot(width=10, height=8)

        # where the figure and table eventually live
        main_layout = QHBoxLayout()
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

    def pause(self):
        print('pause')
        self.active = False

    def update(self):
        if self.active:
            data = float(self.reader.read())
            self.plot.updateDraw(newx=self.data_readout_count, newy=data)
            self.data_readout_count += 1
            print(data)
            sys.stdout.flush()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
