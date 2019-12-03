import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QPixmap
import cv2
import numpy as np
import math



class Window:
    cap = cv2.VideoCapture('video.wmv')
    ret, originalFrame = cap.read()

    def __init__(self):
        self.MainWindow = uic.loadUi('mainwindow.ui')
        self.MainWindow.setWindowTitle("Entrega 3 - Looking for something")

        self.MainWindow.sliderBarrera1.setRange(0, 350)
        self.MainWindow.spinBarrera1.setRange(0, 350)

        self.MainWindow.sliderBarrera2.setRange(0, 350)
        self.MainWindow.spinBarrera2.setRange(0, 350)

        self.MainWindow.sliderBarrera1.valueChanged.connect(self.change_barrier)
        self.MainWindow.sliderBarrera2.valueChanged.connect(self.change_barrier)


    def change_barrier(self):
        self.MainWindow.spinBarrera1.setValue(self.MainWindow.sliderBarrera1.value())
        self.MainWindow.spinBarrera2.setValue(self.MainWindow.sliderBarrera2.value())

    def show(self):
        self.MainWindow.show()
        self.gmg()
    

    def gmg(self):
        while(1):
            self.ret, frame = self.cap.read()
            finalImg = frame

            #Current
            ##cv2.imshow('Real video',frame)
            self.MainWindow.video_source.setPixmap(QPixmap(frame))

            #Current en GreyScale
            currGreyImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ##cv2.imshow('Current Grey Scale Image', currGreyImg)

            #Reference Grey Image
            refGreyImg = cv2.cvtColor(self.originalFrame, cv2.COLOR_BGR2GRAY)
            ##cv2.imshow('Reference Grey Image', refGreyImg)

            #Absolute Difference Image
            diff = cv2.absdiff(currGreyImg, refGreyImg)
            ##cv2.imshow('Absolute Difference Image', diff)

            #Thresholding Difference Image
            blurred = cv2.GaussianBlur(diff, (5, 5), 0)
            thImg = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
            ##cv2.imshow('Threshold Image', thImg)

            #Centroid Image
            cnts = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            if(len(cnts)!=0):
                c = max(cnts, key = cv2.contourArea)

                M = cv2.moments(c)
                cX = int(M["m10"] / (M["m00"]+0.00005))
                cY = int(M["m01"] / (M["m00"]+0.00005))
                cv2.drawContours(finalImg, [c], -1, (0, 255, 0), 2)
                cv2.circle(finalImg, (cX, cY), 7, (255, 255, 255), -1)
        
                # draw the contour and center of the shape on the image
                cv2.drawContours(finalImg, [c], -1, (0, 255, 0), 2)
                cv2.circle(finalImg, (cX, cY), 7, (0, 0, 255), -1)
            ##cv2.imshow('Centroide', finalImg)


            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()