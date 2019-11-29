import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
import cv2
import numpy as np
import math
import matchTemplate as mt

NUM_LADOS=4

rectangleAreas=[                #x, y, ancho, alto
        (1030,564,400,140),
        (1030,850,400,140),
        (1030,1144,400,140)
    ]
auxNameImg = ""

class Window:

    def __init__(self):
        f = open("out.txt", "w")
        f.close()
        #Cargamos la pantalla principal
        self.MainWindow = uic.loadUi('mainwindow.ui')
        #Establecemos un título a la pantalla principal
        self.MainWindow.setWindowTitle("Looking for something")

        #clipping button
        self.MainWindow.Clip_button.clicked.connect(self.clipping)
        
        #load button
        self.MainWindow.Load_button.clicked.connect(self.loadImage)
        
        #extract number button and windows
        self.MainWindow.OCR_button.clicked.connect(self.extractNumbers)
        self.res1 = self.MainWindow.resultado1
        self.res2 = self.MainWindow.resultado2
        self.res3 = self.MainWindow.resultado3

        #global process button
        self.MainWindow.GLOBAL_button.clicked.connect(self.globalProcess)

    def globalProcess(self):
        for i in range(12):
            self.loadImage("capturas/capturas_{}.jpg".format(i+1))
            self.clipping()
            self.extractNumbers()
        
        self.MainWindow.viewer_original.setText("GLOBAL PROCESS COMPLETE, CHECK out.txt")
        self.cleanLabels()


    def extractNumbers(self):
        num1 = self.nums[0][0][1]+self.nums[0][1][1]+self.nums[0][2][1]+'.'+self.nums[0][3][1]
        num2 = self.nums[1][0][1]+self.nums[1][1][1]+self.nums[1][2][1]+'.'+self.nums[1][3][1]
        num3 = self.nums[2][0][1]+self.nums[2][1][1]+self.nums[2][2][1]+'.'+self.nums[2][3][1]
        self.res1.setText(num1)
        self.res2.setText(num2)
        self.res3.setText(num3)

        f = open("out.txt", "a+")
        f.write(self.auxNameImg+" "+num1+" "+num2+" "+num3+"\n")
        f.close()


    def clipping(self):
        self.nums = []
        for i in range(len(rectangleAreas)):
            x, y, w, h = rectangleAreas[i][0], rectangleAreas[i][1], rectangleAreas[i][2], rectangleAreas[i][3]
            self.cropped = self.original_image[y:y+h, x:x+w]
            self.cropped, aux = mt.MatchTemplate().doMatch(self.cropped)
            self.nums.append(aux)

            self.cropped = cv2.resize(self.cropped, (304, 130), cv2.INTER_CUBIC)

            if i == 0:
                self.image_counter1 = QtGui.QImage(self.cropped, 304, 130, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(self.image_counter1.rgbSwapped())
                self.MainWindow.viewer_counter1.setPixmap(pixmap)
            elif i == 1:
                self.image_counter2 = QtGui.QImage(self.cropped, 304, 130, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(self.image_counter2.rgbSwapped())
                self.MainWindow.viewer_counter2.setPixmap(pixmap)
            elif i == 2:
                self.image_counter3 = QtGui.QImage(self.cropped, 304, 130, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap()
                pixmap.convertFromImage(self.image_counter3.rgbSwapped())
                self.MainWindow.viewer_counter3.setPixmap(pixmap)


    def loadImage (self, dir=None):
        if not dir:
            directory = "capturas"
            fn = QFileDialog.getOpenFileName(self.MainWindow, "Choose a frame to download", directory, "Images (*.png *.xpm *.jpg)")
            img_fn = str(fn[0])
        else:
            img_fn = dir
        
        self.auxNameImg = img_fn
        
        self.original_image = cv2.imread(img_fn, cv2.IMREAD_COLOR)
        self.mat_original = cv2.resize(self.original_image, (720, 540), cv2.INTER_CUBIC)

        self.cleanLabels()

        image = QtGui.QImage(self.mat_original, 720, 540, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.MainWindow.viewer_original.setPixmap(pixmap)

    def cleanLabels(self):
        self.MainWindow.viewer_counter1.clear()
        self.MainWindow.viewer_counter2.clear()
        self.MainWindow.viewer_counter3.clear()
        self.res1.clear()
        self.res2.clear()
        self.res3.clear()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.MainWindow.show()
    app.exec_()