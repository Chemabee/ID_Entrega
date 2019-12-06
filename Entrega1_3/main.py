import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
import cv2
import numpy as np
import math
import time
import imutils



class Window:
    cap = cv2.VideoCapture('video.wmv')
    ret, originalFrame = cap.read()
    debug_ = False
    speed_ = 60
    pause = False

    originState = 0
    lastState = 0
    counter = 1 #Se podria poner a none y que dependiendo por donde aparezca el primer centroide te lo ponga a 1 o 0 TODO

    def __init__(self):
        self.MainWindow = uic.loadUi('mainwindow.ui')
        self.MainWindow.setWindowTitle("Entrega 3 - Looking for something")

        self.MainWindow.sliderBarrera1.setRange(0, 350)
        self.MainWindow.spinBarrera1.setRange(0, 350)

        self.MainWindow.sliderBarrera2.setRange(0, 350)
        self.MainWindow.spinBarrera2.setRange(0, 350)

        self.MainWindow.spinBarrera1.setValue(100)
        self.MainWindow.spinBarrera2.setValue(100)

        self.MainWindow.sliderBarrera1.valueChanged.connect(self.change_barrier)
        self.MainWindow.sliderBarrera2.valueChanged.connect(self.change_barrier)

        self.MainWindow.sliderBarrera1.setValue(60)
        self.MainWindow.sliderBarrera2.setValue(160)

        self.MainWindow.buttonPause.clicked.connect(self.onPause)
        self.MainWindow.buttonRestart.clicked.connect(self.restart)
        self.MainWindow.buttonDebug.clicked.connect(self.debug)
        self.MainWindow.buttonCloseDebug.clicked.connect(self.closeWindows)
        self.MainWindow.spinSpeed.setValue(self.speed_)
        self.MainWindow.spinSpeed.valueChanged.connect(self.speed)

        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.gmg)#timer para refrescar la ventana
        self.timer_frames.start(self.speed_)

    def closeWindows(self):
        self.debug_ = False
        cv2.destroyAllWindows()

    def restart(self):
        self.closeWindows()
        self.cap = cv2.VideoCapture('video.wmv')
        self.timer_frames.start()

    def speed(self):
        self.timer_frames.setInterval(self.MainWindow.spinSpeed.value())

    def onPause(self):
        if not self.pause:
            self.timer_frames.stop()
            self.pause = True
        else:
            self.timer_frames.start()
            self.pause = False

    def debug(self):
        self.debug_ = True

    def change_barrier(self):
        b1 = 350 - self.MainWindow.sliderBarrera1.value()
        b2 = 350 - self.MainWindow.sliderBarrera2.value()
        if b1 > b2:
            self.MainWindow.spinBarrera1.setValue((350-self.MainWindow.sliderBarrera1.value())/350*100)
            self.MainWindow.spinBarrera2.setValue((350-self.MainWindow.sliderBarrera2.value())/350*100)

    def show(self):
        self.MainWindow.show()
    

    def gmg(self):
        ret, frame = self.cap.read()
        if(ret):
            #while ret:
            finalImg = frame

            #Current en GreyScale
            currGreyImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Reference Grey Image
            refGreyImg = cv2.cvtColor(self.originalFrame, cv2.COLOR_BGR2GRAY)

            #Absolute Difference Image
            diff = cv2.absdiff(currGreyImg, refGreyImg)

            #Thresholding Difference Image
            blurred = cv2.GaussianBlur(diff, (5, 5), 0)
            thImg = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

            #Centroid Image
            cnts = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            y1 = int((35*self.MainWindow.spinBarrera1.value()/10))
            y2 = int((35*self.MainWindow.spinBarrera2.value()/10))

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

                #Reescale point
                cY = int(cY/200 * 350)
                #Process state of point
                
                
                if cY < y2:
                    #print("0",cY)
                    #print("0",y1)
                    #Encima de la barrera alta
                    if self.lastState == 1:
                        #Pasa de estado 1 a estado 0 (medio a arriba)
                        print("cambiando estado origen")
                        self.lastState = 0
                        if self.originState == 2:
                            #Ha entrado en la habitacion
                            self.counter +=1
                            print(self.counter)
                        self.originState == 0
                elif cY > y2 and cY < y1:
                    #Entre ambas barreras
                    #print("1")
                    if self.lastState == 0:
                        #Pasa de estado 0 a estado 1 (arriba a medio)
                        self.lastState = 1
                    elif self.lastState == 2:
                        #Pasa de estado 2 a estado 1 (debajo a medio)
                        self.lastState = 1
                elif cY > y1:
                    #Debajo de la barrera baja
                    #print("2",cY)
                    #print("2",y1)
                    if self.lastState == 1:
                        #Pasa de estado 1 a estado 2 (medio a debajo)
                        print("cambiando estado origen")
                        self.lastState = 2
                        if self.originState == 0:
                            #Ha salido de la habitacion
                            
                            self.counter-=1
                            print(self.counter)
                        self.originState=2 

            finalImg = cv2.resize(finalImg, (500, 350))
            
            cv2.line(finalImg, (0,y1), (500,y1), (255,0,0), thickness=3)
            cv2.line(finalImg, (0,y2), (500,y2), (0,255,0), thickness=3)
            image = QtGui.QImage(finalImg, finalImg.shape[1], finalImg.shape[0], finalImg.shape[1] * 3,QtGui.QImage.Format_RGB888)

            pix = QtGui.QPixmap(image)

            self.MainWindow.video_source.setPixmap(pix)

            if self.debug_:
                cv2.imshow('Real video',frame)
                cv2.imshow('Current Grey Scale Image', currGreyImg)
                cv2.imshow('Reference Grey Image', refGreyImg)
                cv2.imshow('Absolute Difference Image', diff)
                cv2.imshow('Threshold Image', thImg)
        else:
            self.MainWindow.video_source.setText("The video has ended")
            self.closeWindows()
            self.timer_frames.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()