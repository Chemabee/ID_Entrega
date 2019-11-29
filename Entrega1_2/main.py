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
        self.MainWindow.viewer_counter1.clear()
        self.MainWindow.viewer_counter2.clear()
        self.MainWindow.viewer_counter3.clear()
        self.res1.clear()
        self.res2.clear()
        self.res3.clear()


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
        self.make_filter()

        self.MainWindow.viewer_counter1.clear()
        self.MainWindow.viewer_counter2.clear()
        self.MainWindow.viewer_counter3.clear()
        self.res1.clear()
        self.res2.clear()
        self.res3.clear()

        image = QtGui.QImage(self.mat_original, 720, 540, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.MainWindow.viewer_original.setPixmap(pixmap)
        

    def make_filter(self):
        self.image_gray = cv2.cvtColor(self.mat_original, cv2.COLOR_BGR2GRAY)
        #Asignamos al vídeo 1 la imagen con filtro gaussiano y canny
       # img = cv2.GaussianBlur(self.image_gray, (5,5),0)
       # tempV = cv2.threshold(img, 10, 250, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
        self.image_gray = cv2.medianBlur(self.image_gray, 5)
        tempV = cv2.adaptiveThreshold(self.image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        #tempV = cv2.Canny(thres, 1, 1)

        #Adquirimos el vector con los puntos de los contornos
        contours, _hierarchy = cv2.findContours(tempV, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        squares = []
        #Para cada contorno
        for cnt in contours:
            #Calcula la longitud total del contorno
            cnt_len = cv2.arcLength(cnt, True)
            #Aproxima a la silueta mas simple posible
            cnt = cv2.approxPolyDP(cnt, 0.05*cnt_len, True)
            #Primero comprueba que tiene 4 puntos, es decir 4 vértices, 4 lados. Despues establece el minimo de tamaño, a menor mas sensible.
            #Por ultimo comprueba si la silueta es convexa, es decir, no tiene angulos internos > 180 y no tiene diagonales interiores
            if len(cnt) == NUM_LADOS and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                #Calcula el coseno máximo de entre los 4 puntos de cada silueta, el % es para iterar dando la vuelta a la lista de los 4 puntos
                max_cos = np.max([self.angle_cos( cnt[i], cnt[(i+1) % NUM_LADOS], cnt[(i+2) % NUM_LADOS] ) for i in range(NUM_LADOS)])
                #Comprueba que el angulo sea de 90 grados, con holgura para poder pillarlo en diagonal
                if max_cos < 0.2:
                    squares.append(cnt)
        self.isSquare(squares)

    def angle_cos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / (np.sqrt(np.dot(d1,d1)) * np.sqrt(np.dot(d2,d2))))

    def isSquare(self, squares):
        rectangulos = []
        for cnt in squares:
            rectangulos.append(cnt)
        cv2.drawContours( self.mat_original, rectangulos, -1, (0, 0, 255), 1 )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.MainWindow.show()
    app.exec_()