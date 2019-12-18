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
    cap = cv2.VideoCapture('M6MotorwayTraffic_cut.mp4')
    ret, originalFrame = cap.read()
    debug_ = False
    speed_ = 60
    pause = False

    RANGE = 7
    erode_range = 13 #50
    dilate_range = 30 #45
    kernel_range = 15

    sub = cv2.createBackgroundSubtractorMOG2()

    state = (1,1)   #(1,1): Dentro | (1,0): Saliendo | (0,1): Entrando | (0,0): Fuera
    counter = 1 #Se podria poner a none y que dependiendo por donde aparezca el primer centroide te lo ponga a 1 o 0 TODO

    def __init__(self):
        self.MainWindow = uic.loadUi('mainwindow.ui')
        self.MainWindow.setWindowTitle("Entrega 3 - Looking for something")


        self.MainWindow.counter.setText("Counter: " + str(self.counter))

        self.MainWindow.sliderBarrera.setRange(0, 350)
        self.MainWindow.spinBarrera.setRange(0, 350)

        self.MainWindow.spinBarrera.setValue(100)

        self.MainWindow.sliderBarrera.valueChanged.connect(self.change_barrier)

        self.MainWindow.sliderBarrera.setValue(175)

        self.MainWindow.buttonPause.clicked.connect(self.onPause)
        self.MainWindow.buttonRestart.clicked.connect(self.restart)
        self.MainWindow.buttonDebug.clicked.connect(self.debug)
        self.MainWindow.buttonCloseDebug.clicked.connect(self.closeWindows)
        self.MainWindow.spinSpeed.setValue(self.speed_)
        self.MainWindow.spinSpeed.valueChanged.connect(self.speed)

        self.MainWindow.spinRangeBarrier.setValue(self.RANGE)
        self.MainWindow.spinRangeBarrier.valueChanged.connect(self.changeRange)
        self.MainWindow.spinRangeErode.setValue(self.erode_range)
        self.MainWindow.spinRangeErode.valueChanged.connect(self.changeErodeRange)
        self.MainWindow.spinRangeDilate.setValue(self.dilate_range)
        self.MainWindow.spinRangeDilate.valueChanged.connect(self.changeDilateRange)
        self.MainWindow.spinRangeKernel.setValue(self.kernel_range)
        self.MainWindow.spinRangeKernel.valueChanged.connect(self.changeKernelRange)
        

        self.timer_frames = QtCore.QTimer(self.MainWindow)
        self.timer_frames.timeout.connect(self.gmg)#timer para refrescar la ventana
        self.timer_frames.start(self.speed_)

    def closeWindows(self):
        self.debug_ = False
        cv2.destroyAllWindows()

    def restart(self):
        self.closeWindows()
        self.counter = 1
        self.cap = cv2.VideoCapture('M6MotorwayTraffic_cut.mp4')
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
        self.MainWindow.spinBarrera.setValue((350-self.MainWindow.sliderBarrera.value())/350*100)

    def changeRange(self):
        self.RANGE = self.MainWindow.spinRangeBarrier.value()
    
    def changeErodeRange(self):
        self.erode_range = self.MainWindow.spinRangeErode.value()
    
    def changeDilateRange(self):
        self.dilate_range = self.MainWindow.spinRangeDilate.value()

    def changeKernelRange(self):
        self.kernel_range = self.MainWindow.spinRangeKernel.value()

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
            #refGreyImg = cv2.cvtColor(self.originalFrame, cv2.COLOR_BGR2GRAY)

            #Absolute Difference Image
            #diff = cv2.absdiff(currGreyImg, refGreyImg)

            diff = self.sub.apply(currGreyImg) 

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.kernel_range, self.kernel_range))
            kernelErode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.erode_range, self.erode_range))  # kernel to apply to the morphology
            kernelDilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.dilate_range, self.dilate_range))

            closing = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, kernel)
            
            opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
            
            dilation = cv2.dilate(opening, kernelDilate)

            erode = cv2.erode(dilation, kernelErode, iterations=1)
            
            #Thresholding Difference Image
            blurred = cv2.GaussianBlur(erode, (5, 5), 0)
            thImg = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)[1]

            #Centroid Image
            cnts = cv2.findContours(thImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            upperBarrier = int((35*self.MainWindow.spinBarrera.value()/10))

            if(len(cnts)!=0):
                for c in cnts:
                    #c = max(cnts, key = cv2.contourArea)
                    if cv2.contourArea(c) > 1500:
                        M = cv2.moments(c)
                        cX = int(M["m10"] / (M["m00"]+0.00005))
                        cY = int(M["m01"] / (M["m00"]+0.00005))
                        cv2.drawContours(finalImg, [c], -1, (0, 255, 0), 2)
                        cv2.circle(finalImg, (cX, cY), 7, (255, 255, 255), -1)
                
                        # draw the contour and center of the shape on the image
                        cv2.drawContours(finalImg, [c], -1, (0, 255, 0), 2)
                        cv2.circle(finalImg, (cX, cY), 7, (0, 0, 255), -1)

                        #Reescale point
                        #cY = int(cY/200 * 350)
                        #Process state of point
                        
                        self.changeState(cY, upperBarrier)

            finalImg = cv2.resize(finalImg, (500, 350))
            
            cv2.line(finalImg, (0,upperBarrier), (500,upperBarrier), (0,255,0), thickness=3)
            image = QtGui.QImage(finalImg, finalImg.shape[1], finalImg.shape[0], finalImg.shape[1] * 3,QtGui.QImage.Format_RGB888)

            pix = QtGui.QPixmap(image)

            self.MainWindow.video_source.setPixmap(pix)

            if self.debug_:
                cv2.imshow('Real video',frame)
                cv2.imshow('Current Grey Scale Image', currGreyImg)
                cv2.imshow('Absolute Difference Image', diff)
                cv2.imshow('Threshold Image', thImg)
        else:
            self.MainWindow.video_source.setText("The video has ended")
            self.closeWindows()
            self.timer_frames.stop()

    def changeState(self, cY, upperBarrier): 
        #if cY > upperBarrier and cY < lowerBarrier:
        if cY > (upperBarrier-self.RANGE) and cY < (upperBarrier + self.RANGE):
            self.counter += 1
            self.MainWindow.counter.setText("Counter: " + str(self.counter))
            print(self.counter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
