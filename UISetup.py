# Autor: Colin O'Dowd
# Project Starfish
# Function: UI Setup and Event Handling

from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Worker1 import ImagePlayer
from Worker2 import HeaderBar
import time

class UI_MainWindow(QMainWindow):
    def setupUI(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Project Starfish Prototype GUI")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1920, 1080)
        #self.setStyleSheet("background-color: rgb(9, 40, 122);") #navy blue (Teleflex color)
        self.setStyleSheet("background-color: rgb(0, 0, 0);") #black

        self.cameraViewer = QtWidgets.QWidget(self)
        self.cameraViewer.setObjectName("cameraViewer")

        self.logo = QtWidgets.QLabel(self.cameraViewer)
        self.logo.setGeometry(QtCore.QRect(825, 20, 270, 42))
        pixmap = QPixmap('Graphics/teleflex-logo-orange.png')
        pixmap = pixmap.scaled(270, 42)        
        self.logo.setPixmap(pixmap)

        self.dateLabel = QtWidgets.QLabel(self.cameraViewer)
        self.dateLabel.setGeometry(QtCore.QRect(20, 15, 300, 50))
        self.dateLabel.setObjectName("dateLabel")
        self.dateLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        self.dateLabel.setStyleSheet("color : rgb(255,165,0)")

        self.timeLabel = QtWidgets.QLabel(self.cameraViewer)
        self.timeLabel.setGeometry(QtCore.QRect(350, 15, 150, 50))
        self.timeLabel.setObjectName("timeLabel")
        self.timeLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        self.timeLabel.setStyleSheet("color : rgb(255,165,0)")

        self.batteryLabel = QtWidgets.QLabel(self.cameraViewer)
        self.batteryLabel.setGeometry(QtCore.QRect(1820, 15, 100, 50))
        self.batteryLabel.setObjectName("batteryLabel")
        self.batteryLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        self.batteryLabel.setStyleSheet("color : rgb(255,165,0)")

        self.batteryIcon = QtWidgets.QLabel(self.cameraViewer)
        self.batteryIcon.setGeometry(QtCore.QRect(1710, 15, 100, 50))
        self.batteryIcon.setObjectName("startBTN")

        self.cameraFeed = QtWidgets.QLabel(self.cameraViewer)
        self.cameraFeed.setGeometry(QtCore.QRect(320, 110, 1280, 960))
        self.cameraFeed.setObjectName("cameraFeed")

        self.patientNotesBTN = QtWidgets.QLabel(self.cameraViewer)
        self.patientNotesBTN.setPixmap(QPixmap("Graphics/patientNotesButton.png").scaled(100,100))
        self.patientNotesBTN.setGeometry(QtCore.QRect(110, 495, 100, 100))
        self.patientNotesBTN.setObjectName("patientNotesBTN")
        self.patientNotesBTN.installEventFilter(self)
        self.patientNotesBTN.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.patientNotesBTN.hide()

        self.saveImageBTN = QtWidgets.QLabel(self.cameraViewer)
        self.saveImageBTN.setPixmap(QPixmap("Graphics/saveImageButton.png").scaled(100,100))
        self.saveImageBTN.setGeometry(QtCore.QRect(110, 610, 100, 100))
        self.saveImageBTN.setObjectName("saveImageBTN")
        self.saveImageBTN.setMouseTracking(True)
        self.saveImageBTN.installEventFilter(self)
        self.saveImageBTN.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.saveImageBTN.hide()

        self.startVideoBTN = QtWidgets.QLabel(self.cameraViewer)
        self.startVideoBTN.setPixmap(QPixmap("Graphics/startVideoButton.png").scaled(100,100))
        self.startVideoBTN.setGeometry(QtCore.QRect(110, 720, 100, 100))
        self.startVideoBTN.setObjectName("startVideoBTN")
        self.startVideoBTN.installEventFilter(self)
        self.startVideoBTN.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.startVideoBTN.hide()

        self.stopVideoBTN = QtWidgets.QLabel(self.cameraViewer)
        self.stopVideoBTN.setPixmap(QPixmap("Graphics/stopVideoButton.png").scaled(100,100))
        self.stopVideoBTN.setGeometry(QtCore.QRect(110, 720, 100, 100))
        self.stopVideoBTN.setObjectName("stopVideoBTN")
        self.stopVideoBTN.installEventFilter(self)
        self.stopVideoBTN.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.stopVideoBTN.hide()

        self.fileExplorerBTN = QtWidgets.QLabel(self.cameraViewer)
        self.fileExplorerBTN.setPixmap(QPixmap("Graphics/fileExplorerButton.png").scaled(100,100))
        self.fileExplorerBTN.setGeometry(QtCore.QRect(110, 825, 100, 100))
        self.fileExplorerBTN.setObjectName("fileExplorerBTN")
        self.fileExplorerBTN.installEventFilter(self)
        self.fileExplorerBTN.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.fileExplorerBTN.hide()

        self.settingsBTN = QtWidgets.QLabel(self.cameraViewer)
        self.settingsBTN.setPixmap(QPixmap("Graphics/settingsButton.png").scaled(100,100))
        self.settingsBTN.setGeometry(QtCore.QRect(110, 940, 100, 100))
        self.settingsBTN.setObjectName("settingsBTN")
        self.settingsBTN.installEventFilter(self)
        self.settingsBTN.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.settingsBTN.hide()

        self.setCentralWidget(self.cameraViewer)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.ImagePlayer = ImagePlayer()
        self.ImagePlayer.start()
        self.ImagePlayer.CameraConnected.connect(self.isCameraConnected)
        self.ImagePlayer.ImageUpdate.connect(self.ImageUpdateSlot)

        self.HeaderBar = HeaderBar()
        self.HeaderBar.dateTrack.connect(self.updateDate)
        self.HeaderBar.timeTrack.connect(self.updateTime)
        self.HeaderBar.batteryTrack.connect(self.updateBattery)
        self.HeaderBar.start()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.TouchBegin or event.type() == QEvent.MouseButtonPress:
            match obj.objectName():
                case str("patientNotesBTN"):
                    self.patientNotesButtonPress()
                case str("startVideoBTN"):
                    self.startVideoButtonPress()
                case str("stopVideoBTN"):
                    self.stopVideoButtonPress()
                case str("saveImageBTN"):
                    self.saveImageButtonPress()
                case str("fileExplorerBTN"):
                    self.fileExplorerButtonPress()
                case str("settingsBTN"):
                    self.settingsButtonPress() 
        elif event.type() == QEvent.MouseButtonRelease:  # Catch the TouchBegin event.
            match obj.objectName():
                case str("patientNotesBTN"):
                    self.patientNotesButtonRelease()
                case str("startVideoBTN"):
                    self.startVideoButtonRelease()
                case str("stopVideoBTN"):
                    self.stopVideoButtonRelease()
                case str("saveImageBTN"):
                    self.saveImageButtonRelease()
                case str("fileExplorerBTN"):
                    self.fileExplorerButtonRelease()
                case str("settingsBTN"):
                    self.settingsButtonRelease()
                
        return super(UI_MainWindow, self).eventFilter(obj, event)

    def updateDate(self, date):
        self.dateLabel.setText(date)
    
    def updateTime(self, time):
        self.timeLabel.setText(time)
    
    def updateBattery(self, battery):
        self.batteryLabel.setText(battery + "%")
        battery = int(battery)
        if battery < 10:
            self.batteryIcon.setPixmap(QPixmap("Graphics/batteryUltraLow.png").scaled(100,50))
        elif battery >= 10 and battery < 40:
            self.batteryIcon.setPixmap(QPixmap("Graphics/batteryLow.png").scaled(100,50))
        elif battery >= 40 and battery < 60:
            self.batteryIcon.setPixmap(QPixmap("Graphics/batteryMid.png").scaled(100,50))
        elif battery >=60 and battery < 90:
            self.batteryIcon.setPixmap(QPixmap("Graphics/batteryHigh.png").scaled(100,50))
        else:
            self.batteryIcon.setPixmap(QPixmap("Graphics/batteryUltraHigh.png").scaled(100,50))

    def isCameraConnected(self, camera):
        if not camera:
            self.patientNotesBTN.hide()
            self.saveImageBTN.hide()
            self.startVideoBTN.hide()
            self.stopVideoBTN.hide()
            self.fileExplorerBTN.hide()
            self.settingsBTN.hide()
        else: 
            self.patientNotesBTN.show()
            self.saveImageBTN.show()
            self.startVideoBTN.show()
            self.fileExplorerBTN.show()
            self.settingsBTN.show()

    def ImageUpdateSlot(self, Image):
        self.cameraFeed.setPixmap(QPixmap.fromImage(Image))

    def patientNotesButtonPress(self):
        self.patientNotesBTN.setPixmap(QPixmap("Graphics/patientNotesButtonPressed.png").scaled(100,100))
        
    def patientNotesButtonRelease(self):
        self.patientNotesBTN.setPixmap(QPixmap("Graphics/patientNotesButton.png").scaled(100,100))

    def saveImageButtonPress(self):
        self.saveImageBTN.setPixmap(QPixmap("Graphics/saveImageButtonPressed.png").scaled(100,100))

    def saveImageButtonRelease(self):
        self.saveImageBTN.setPixmap(QPixmap("Graphics/saveImageButton.png").scaled(100,100))
        self.ImagePlayer.saveImage()
    
    def startVideoButtonPress(self):
        self.ImagePlayer.startVideo()
        self.startVideoBTN.setPixmap(QPixmap("Graphics/startVideoButtonPressed.png").scaled(100,100))

    def startVideoButtonRelease(self):
        self.startVideoBTN.hide()
        self.startVideoBTN.setPixmap(QPixmap("Graphics/startVideoButton.png").scaled(100,100))
        self.stopVideoBTN.show()
    
    def stopVideoButtonPress(self):
        self.ImagePlayer.stopVideo()

    def stopVideoButtonRelease(self):
        self.stopVideoBTN.hide()
        self.startVideoBTN.show()

    def fileExplorerButtonPress(self):
        self.fileExplorerBTN.setPixmap(QPixmap("Graphics/fileExplorerButtonPressed.png").scaled(100,100))

    def fileExplorerButtonRelease(self):
        self.fileExplorerBTN.setPixmap(QPixmap("Graphics/fileExplorerButton.png").scaled(100,100))

    def settingsButtonPress(self):
        self.settingsBTN.setPixmap(QPixmap("Graphics/settingsButtonPressed.png").scaled(100,100))

    def settingsButtonRelease(self):
        self.settingsBTN.setPixmap(QPixmap("Graphics/settingsButton.png").scaled(100,100))
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate