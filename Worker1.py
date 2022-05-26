# Autor: Colin O'Dowd
# Project Starfish
# Function: Thread to handle the camera application

import cv2
import time
import os.path     
from PyQt5.QtGui import  QPixmap
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime

class ImagePlayer(QThread):
    def __init__(self):
        super(ImagePlayer, self).__init__()
        self.ThreadActive = None
        self.Capture = None
        self.frame = None
        self.videoCapture = None
        self.saveVideo = None
        self.brightnessValue = 0
        self.videoFile = None

    ImageUpdate = pyqtSignal(QImage)
    CameraConnected = pyqtSignal(bool)

    def run(self):
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, self.frame = self.Capture.read()
            if ret:
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1280, 960, Qt.KeepAspectRatio)
                self.CameraConnected.emit(True)
                self.ImageUpdate.emit(Pic)
                if self.videoCapture:
                    self.videoFile.write(self.frame)
            else:
                Pic = QImage(QPixmap('Graphics/undetected-camera.png').scaled(1280,960, Qt.KeepAspectRatio))
                self.CameraConnected.emit(False)
                self.ImageUpdate.emit(Pic)
                if self.saveVideo:
                    self.videoFile.release()
                    self.saveVideo = False
                self.Capture = cv2.VideoCapture(0)
        self.Capture.release()
    def stop(self):
        self.ThreadActive = False
        self.quit()
    def saveImage(self):     
        date = datetime.now().strftime("%B-%d-%Y")
        date_folder = "Saved/Images/" + date
        isdir = os.path.isdir(date_folder) 
        if not isdir:
            os.mkdir(date_folder)
        img_name = "image_{}.png".format(datetime.now().strftime("%Hh%Mm%Ss"))
        image_path = date_folder + "/" + img_name
        if self.Capture.isOpened():
            cv2.imwrite(image_path, self.frame)
    def startVideo(self):
        date = datetime.now().strftime("%B-%d-%Y")
        date_folder = "Saved/Videos/" + date
        isdir = os.path.isdir(date_folder) 
        if not isdir:
            os.mkdir(date_folder)        
        video_name = "video_{}.avi".format(datetime.now().strftime("%Hh%Mm%Ss"))
        video_path = date_folder + "/" + video_name
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        self.videoFile = cv2.VideoWriter(video_path, codec, 30.0, (640, 480))
        self.videoCapture = True
        self.saveVideo = True
    def stopVideo(self):
        self.videoCapture = False
        time.sleep(0.1) #delay to prevent main loop from writing frame to closed video file (run method always runs)
        if self.saveVideo:
            self.videoFile.release()
        self.saveVideo = False
    def updateBrightness(self, value):
        self.brightnessValue = value