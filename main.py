# Autor: Colin O'Dowd
# Project Starfish
# Function: Main Application

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UISetup import UI_MainWindow

def main():
    app = QApplication(sys.argv)
    win = UI_MainWindow()
    win.setupUI()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
