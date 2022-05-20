from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from Worker1 import ImagePlayer
from Worker2 import HeaderBar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Project Starfish Prototype GUI")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(9, 40, 122);")

        self.cameraViewer = QtWidgets.QWidget(MainWindow)
        self.cameraViewer.setObjectName("cameraViewer")

        self.logo = QtWidgets.QLabel(self.cameraViewer)
        self.logo.setGeometry(QtCore.QRect(825, 20, 270, 42))
        pixmap = QPixmap('teleflex-logo.png')
        pixmap = pixmap.scaled(270, 42)        
        self.logo.setPixmap(pixmap)

        self.dateLabel = QtWidgets.QLabel(self.cameraViewer)
        self.dateLabel.setGeometry(QtCore.QRect(20, 15, 225, 50))
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        self.dateLabel.setStyleSheet("color : white")

        self.timeLabel = QtWidgets.QLabel(self.cameraViewer)
        self.timeLabel.setGeometry(QtCore.QRect(245, 15, 225, 50))
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        self.timeLabel.setStyleSheet("color : white")

        self.batteryLabel = QtWidgets.QLabel(self.cameraViewer)
        self.batteryLabel.setGeometry(QtCore.QRect(1820, 15, 100, 50))
        self.batteryLabel.setObjectName("batteryLabel")
        self.batteryLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        self.batteryLabel.setStyleSheet("color : white")

        self.batteryIcon = QtWidgets.QLabel(self.cameraViewer)
        self.batteryIcon.setGeometry(QtCore.QRect(1710, 15, 100, 50))
        self.batteryIcon.setObjectName("startBTN")

        self.cameraFeed = QtWidgets.QLabel(self.cameraViewer)
        self.cameraFeed.setGeometry(QtCore.QRect(320, 110, 1280, 960))
        self.cameraFeed.setObjectName("cameraFeed")

        self.startBTN = QtWidgets.QLabel(self.cameraViewer)
        self.startBTN.setPixmap(QPixmap("startButton.png").scaled(100,100))
        self.startBTN.setGeometry(QtCore.QRect(110, 490, 100, 100))
        self.startBTN.setObjectName("startBTN")
        self.startBTN.mousePressEvent = self.startButtonPress
        self.startBTN.mouseReleaseEvent = self.startButtonRelease

        self.stopBTN = QtWidgets.QLabel(self.cameraViewer)
        self.stopBTN.setPixmap(QPixmap("stopButton.png").scaled(100,100))
        self.stopBTN.setGeometry(QtCore.QRect(110, 610, 100, 100))
        self.stopBTN.setObjectName("stopBTN")
        self.stopBTN.mousePressEvent = self.stopButtonPress
        self.stopBTN.mouseReleaseEvent = self.stopButtonRelease

        self.saveImageBTN = QtWidgets.QLabel(self.cameraViewer)
        self.saveImageBTN.setPixmap(QPixmap("saveImageButton.png").scaled(100,100))
        self.saveImageBTN.setGeometry(QtCore.QRect(110, 720, 100, 100))
        self.saveImageBTN.setObjectName("saveImageBTN")
        self.saveImageBTN.mousePressEvent = self.saveImageButtonPress
        self.saveImageBTN.mouseReleaseEvent = self.saveImageButtonRelease

        self.startVideoBTN = QtWidgets.QLabel(self.cameraViewer)
        self.startVideoBTN.setPixmap(QPixmap("startVideoButton.png").scaled(100,100))
        self.startVideoBTN.setGeometry(QtCore.QRect(110, 820, 100, 100))
        self.startVideoBTN.setObjectName("startVideoBTN")
        self.startVideoBTN.mousePressEvent = self.startVideoButtonPress
        self.startVideoBTN.mouseReleaseEvent = self.startVideoButtonRelease

        self.stopVideoBTN = QtWidgets.QLabel(self.cameraViewer)
        self.stopVideoBTN.setPixmap(QPixmap("stopVideoButton.png").scaled(100,100))
        self.stopVideoBTN.setGeometry(QtCore.QRect(110, 930, 100, 100))
        self.stopVideoBTN.setObjectName("stopVideoBTN")
        self.stopVideoBTN.mousePressEvent = self.stopVideoButtonPress
        self.stopVideoBTN.mouseReleaseEvent = self.stopVideoButtonRelease

        MainWindow.setCentralWidget(self.cameraViewer)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ImagePlayer = ImagePlayer()
        self.ImagePlayer.start()
        self.ImagePlayer.CameraConnected.connect(self.isCameraConnected)
        self.ImagePlayer.ImageUpdate.connect(self.ImageUpdateSlot)

        self.HeaderBar = HeaderBar()
        self.HeaderBar.dateTrack.connect(self.updateDate)
        self.HeaderBar.timeTrack.connect(self.updateTime)
        self.HeaderBar.batteryTrack.connect(self.updateBattery)
        self.HeaderBar.start()

    def updateDate(self, date):
        self.dateLabel.setText(date)
    
    def updateTime(self, time):
        self.timeLabel.setText(time)
    
    def updateBattery(self, battery):
        self.batteryLabel.setText(battery + "%")
        battery = int(battery)
        if battery < 10:
            self.batteryIcon.setPixmap(QPixmap("batteryUltraLow.png").scaled(100,50))
        elif battery >= 10 and battery < 40:
            self.batteryIcon.setPixmap(QPixmap("batteryLow.png").scaled(100,50))
        elif battery >= 40 and battery < 60:
            self.batteryIcon.setPixmap(QPixmap("batteryMid.png").scaled(100,50))
        elif battery >=60 and battery < 90:
            self.batteryIcon.setPixmap(QPixmap("batteryHigh.png").scaled(100,50))
        else:
            self.batteryIcon.setPixmap(QPixmap("batteryUltraHigh.png").scaled(100,50))


    def isCameraConnected(self, camera):
        if not camera:
            self.startBTN.hide()
            self.stopBTN.hide()
            self.saveImageBTN.hide()
            self.startVideoBTN.hide()
            self.stopVideoBTN.hide()
        else: 
            self.startBTN.show()
            self.stopBTN.show()
            self.saveImageBTN.show()
            self.startVideoBTN.show()
            self.stopVideoBTN.show() 

    def ImageUpdateSlot(self, Image):
        self.cameraFeed.setPixmap(QPixmap.fromImage(Image))
    
    def StopVideo(self):
        self.ImagePlayer.stopVideo()

    def startButtonPress(self, event):
        self.startBTN.setPixmap(QPixmap("startButtonPressed.png").scaled(100,100))

    def startButtonRelease(self, event):
        self.startBTN.setPixmap(QPixmap("startButton.png").scaled(100,100))
        self.ImagePlayer.start()

    def stopButtonPress(self, event):
        self.stopBTN.setPixmap(QPixmap("stopButtonPressed.png").scaled(100,100))

    def stopButtonRelease(self, event):
        self.stopBTN.setPixmap(QPixmap("stopButton.png").scaled(100,100))
        self.ImagePlayer.stop()

    def saveImageButtonPress(self, event):
        self.saveImageBTN.setPixmap(QPixmap("saveImageButtonPressed.png").scaled(100,100))

    def saveImageButtonRelease(self, event):
        self.saveImageBTN.setPixmap(QPixmap("saveImageButton.png").scaled(100,100))
        self.ImagePlayer.saveImage()
    
    def startVideoButtonPress(self, event):
        self.startVideoBTN.setPixmap(QPixmap("startVideoButtonPressed.png").scaled(100,100))

    def startVideoButtonRelease(self, event):
        self.startVideoBTN.setPixmap(QPixmap("startVideoButton.png").scaled(100,100))
        self.ImagePlayer.startVideo()
        
    def stopVideoButtonPress(self, event):
        self.stopVideoBTN.setPixmap(QPixmap("stopVideoButtonPressed.png").scaled(100,100))

    def stopVideoButtonRelease(self, event):
        self.stopVideoBTN.setPixmap(QPixmap("stopVideoButton.png").scaled(100,100))
        self.ImagePlayer.stopVideo()
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate