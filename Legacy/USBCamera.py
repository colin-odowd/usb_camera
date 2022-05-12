import sys
from types import FrameType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import datetime

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.StartBTN = QPushButton("Start")
        self.StartBTN.clicked.connect(self.StartFeed)
        self.VBL.addWidget(self.StartBTN)

        self.StopBTN = QPushButton("Stop")
        self.StopBTN.clicked.connect(self.StopFeed)
        self.VBL.addWidget(self.StopBTN)

        self.SaveImageBTN = QPushButton("Save Image")
        self.SaveImageBTN.clicked.connect(self.SaveImage)
        self.VBL.addWidget(self.SaveImageBTN)

        self.StartVideoBTN = QPushButton("Start Video")
        self.StartVideoBTN.clicked.connect(self.StartVideo)
        self.VBL.addWidget(self.StartVideoBTN)
        
        self.StopVideoBTN = QPushButton("Stop Video")
        self.StopVideoBTN.clicked.connect(self.StopVideo)
        self.VBL.addWidget(self.StopVideoBTN)

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def StartFeed(self):
        self.Worker1.start()

    def StopFeed(self):
        self.Worker1.stop()

    def SaveImage(self):
        self.Worker1.saveImage()

    def StartVideo(self):
        self.Worker1.startVideo()
    
    def StopVideo(self):
        self.Worker1.stopVideo()

class Worker1(QThread):
    def __init__(self):
        super(Worker1, self).__init__()
        self.ThreadActive = None
        self.Capture = None
        self.FlippedImage = None
        self.videoCapture = None
        self.videoFile = None

    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = self.Capture.read()
            if ret:
                self.FlippedImage = cv2.flip(frame, 1)
                Image = cv2.cvtColor(self.FlippedImage, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                if self.videoCapture:
                    self.videoFile.write(self.FlippedImage)
        self.Capture.release()
    def stop(self):
        self.ThreadActive = False
        self.quit()
    def saveImage(self):
        time = datetime.datetime.now()      
        img_name = "image_{}.png".format(time.strftime("%Hh%Mm%Ss"))
        if self.Capture.isOpened():
            cv2.imwrite(img_name, self.FlippedImage)
    def startVideo(self):
        time = datetime.datetime.now()      
        video_name = "video_{}.avi".format(time.strftime("%Hh%Mm%Ss"))
        codec = cv2.VideoWriter_fourcc(*'MJPG')
        self.videoFile = cv2.VideoWriter(video_name, codec, 30.0, (640, 480))
        self.videoCapture = True
    def stopVideo(self):
        self.videoCapture = False
        self.videoFile.release()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())