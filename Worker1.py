import cv2
import numpy as np
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
        self.brightnessValue = 0
        self.videoFile = None

    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, self.frame = self.Capture.read()
            if ret:
                #self.FlippedImage = cv2.flip(frame, 1)
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(1280, 960, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                if self.videoCapture:
                    self.videoFile.write(self.frame)
            else:
                Pic = QPixmap('background.png')
                self.ImageUpdate.emit(Pic)
        self.Capture.release()
    def stop(self):
        self.ThreadActive = False
        self.quit()
    def saveImage(self):
        time = datetime.now()      
        img_name = "image_{}.png".format(time.strftime("%Hh%Mm%Ss"))
        if self.Capture.isOpened():
            cv2.imwrite(img_name, self.frame)
    def startVideo(self):
        time = datetime.now()         
        video_name = "video_{}.avi".format(time.strftime("%Hh%Mm%Ss"))
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        self.videoFile = cv2.VideoWriter(video_name, codec, 30.0, (640, 480))
        self.videoCapture = True
    def stopVideo(self):
        if self.videoCapture:
            self.videoFile.release()
        self.videoCapture = False
    def updateBrightness(self, value):
        self.brightnessValue = value