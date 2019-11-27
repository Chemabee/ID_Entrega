import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
import cv2
import numpy as np
import math

NUM_LADOS=4

rectangleAreas=[                #x, y, ancho, alto
        (1030,564,400,140),
        (1030,850,400,140),
        (1030,1144,400,140)
    ]

class Window:

    def __init__(self):
        #Cargamos la pantalla principal
        self.MainWindow = uic.loadUi('mainwindow.ui')
        #Establecemos un título a la pantalla principal
        self.MainWindow.setWindowTitle("Looking for something")

        #Inicializamos la imagen fuente y las de los contadores
        self.image_source = QtGui.QImage(720, 540, QtGui.QImage.Format_RGB888)
        self.image_counter1 = QtGui.QImage(304, 130, QtGui.QImage.Format_Indexed8)
        self.image_counter2 = QtGui.QImage(304, 130, QtGui.QImage.Format_Indexed8)
        self.image_counter3 = QtGui.QImage(304, 130, QtGui.QImage.Format_Indexed8)

        #viewers
        self.MainWindow.viewer_original.setPixmap(QtGui.QPixmap(self.image_source))
        self.MainWindow.viewer_counter1.setPixmap(QtGui.QPixmap(self.image_counter1))
        self.MainWindow.viewer_counter2.setPixmap(QtGui.QPixmap(self.image_counter2))
        self.MainWindow.viewer_counter3.setPixmap(QtGui.QPixmap(self.image_counter3))
        
        #conexión del botón
        self.MainWindow.Load_button.clicked.connect(self.loadImage)

    def loadImage (self):
        directory = "capturas"
        fn = QFileDialog.getOpenFileName(self.MainWindow, "Choose a frame to download", directory, "Images (*.png *.xpm *.jpg)")
        
        original_image = cv2.imread(str(fn[0]), cv2.IMREAD_COLOR)
        self.mat_original = cv2.resize(original_image, (720, 540), cv2.INTER_CUBIC)

        w, h = rectangleAreas[0][2], rectangleAreas[0][3]
        #self.make_filter()
        image = QtGui.QImage(self.mat_original, 720, 540, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.MainWindow.viewer_original.setPixmap(pixmap)
        

    def make_filter(self):
        self.image_gray = cv2.cvtColor(self.mat_original, cv2.COLOR_BGR2GRAY)
        #Asignamos al vídeo 1 la imagen con filtro gaussiano y canny
        img = cv2.GaussianBlur(self.image_gray, (5,5),10)
        tempV = cv2.Canny(img, 1, 1)

        cv2.imshow("Imagen gris", self.image_gray)

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
            """if len(cnt) == NUM_LADOS and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                #Calcula el coseno máximo de entre los 4 puntos de cada silueta, el % es para iterar dando la vuelta a la lista de los 4 puntos
                max_cos = np.max([self.angle_cos( cnt[i], cnt[(i+1) % NUM_LADOS], cnt[(i+2) % NUM_LADOS] ) for i in range(NUM_LADOS)])
                #Comprueba que el angulo sea de 90 grados, con holgura para poder pillarlo en diagonal
                if max_cos < 0.2:"""
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