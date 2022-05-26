# Autor: Colin O'Dowd
# Project Starfish
# Function: Thread to handle the header bar

import time
import psutil
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

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