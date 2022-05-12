from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtGui import QIcon, QPixmap
import sys
from types import FrameType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
from datetime import datetime
import numpy as np
import time
import psutil
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class HeaderBar(QThread):
    dateTrack = pyqtSignal(str)
    timeTrack = pyqtSignal(str)
    batteryTrack = pyqtSignal(str)
    
    def __init__(self):
        super(HeaderBar, self).__init__()

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            time.sleep(0.1)
            cur_date = datetime.now().strftime("%B %d, %Y")
            cur_time = datetime.now().strftime("%H:%M:%S")
            curr_battery = str(psutil.sensors_battery().percent)
            self.dateTrack.emit(cur_date)
            self.timeTrack.emit(cur_time)
            self.batteryTrack.emit(curr_battery)