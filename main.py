# Author: Colin O'Dowd

from PyQt5 import QtCore, QtGui, QtWidgets 
from types import FrameType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UISetup import Ui_MainWindow
import time
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow().setupUi(MainWindow)
    time.sleep(0.1) #delay for checking if camera is connected
    MainWindow.show()
    sys.exit(app.exec_())
