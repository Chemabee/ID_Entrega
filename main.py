#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication
#from PyQt4 import QtCore, QtGui, uic
import cv2
import numpy as np


MAX_IMG=2
IDCAM=2
NUM_LADOS=4

class Webcam:

    def __init__(self):
        #Array de los videos
        self.cv_video=[]
        #Cargamos la pantalla principal
        self.MainWindow = uic.loadUi('mainwindow.ui')
        #Establecemos un título a la pantalla principal
        self.MainWindow.setWindowTitle("Entrega 1")

        #Array de las ventanas de los vídeos
        self.qt_video = [self.MainWindow.video,self.MainWindow.video1]
        #Capturamos la webcam
        self.webcam = cv2.VideoCapture(IDCAM)
        
        #Preparamos la cámara en caso de BGR
        blue_image = np.zeros((640,480,3), np.uint8)
        blue_image[:] = (255,0,0)
        for i in range(MAX_IMG):
            self.cv_video.append(blue_image)
        
        #TODO asignar el minimo del canny mas alto para que no haya tanto ruido
        
        #Establecemos los rangos de las sliders
        self.MainWindow.canny_slide.setRange(30,150)
        self.MainWindow.canny.setRange(30,150)

        self.MainWindow.canny_slide1.setRange(30,150)
        self.MainWindow.canny1.setRange(30,150)

        #Conectamos los sliders con sus cajitas
        self.MainWindow.canny_slide.valueChanged.connect(self.change_canny)
        self.MainWindow.canny_slide1.valueChanged.connect(self.change_canny)


        #Timer para refrescar el filtro e imagen
        self.timer_filter = QtCore.QTimer(self.MainWindow);
        self.timer_filter.timeout.connect(self.make_filter)#timer para los filtros de cv2 funcion que ejecuta
        self.timer_filter.start(3);
        
        self.timer_frames = QtCore.QTimer(self.MainWindow);
        self.timer_frames.timeout.connect(self.show_frames)#timer para refrescar la ventana
        self.timer_frames.start(3);

    #Métodos para conectar los sliders con los números en la cajita
    def change_canny(self, num):
        self.MainWindow.canny.setValue(self.MainWindow.canny_slide.value())
        self.MainWindow.canny1.setValue(self.MainWindow.canny_slide1.value())
    def make_filter(self):
        #Lee la cámara
        ok,entrada=self.webcam.read()
        #Establece un tamaño
        self.height, self.width = entrada.shape[:2]
        
        #Asignamos al vídeo 0 la imagen sin filtro
        self.cv_video[0] = entrada.copy()

        #Asignamos al vídeo 1 la imagen con filtro gaussiano y canny
        #self.cv_video[1] = cv2.cvtColor(entrada, cv2.COLOR_BGR2GRAY)
        self.cv_video[1] = cv2.GaussianBlur(entrada, (5,5),0)
        tempV = cv2.Canny(self.cv_video[1], self.MainWindow.canny_slide.value(), self.MainWindow.canny_slide1.value())

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
        cv2.drawContours( self.cv_video[1], squares, -1, (0, 255, 0), 4 )

    def angle_cos(self, p0, p1, p2):
        d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
        return abs( np.dot(d1, d2) / (np.sqrt(np.dot(d1,d1)) * np.sqrt(np.dot(d2,d2))))


    def show_frames(self):
        for i in range(len(self.qt_video)):
            self.convertCV2ToQimage(self.cv_video[i],self.qt_video[i])

    def convertCV2ToQimage(self,cv_vid,qt_vid):
        gray_color_table = [QtGui.qRgb(i, i, i) for i in range(256)]
        if cv_vid is None:
            return
        if cv_vid.dtype!=np.uint8:
            return
        if len(cv_vid.shape)==2:
            image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_Indexed8)
            image.setColorTable(gray_color_table)
        if len(cv_vid.shape)==3:
            if cv_vid.shape[2]==3:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_RGB888)
            elif cv_vid.shape[2]==4:
               image = QtGui.QImage(cv_vid, cv_vid.shape[1], cv_vid.shape[0], cv_vid.strides[0], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        qt_vid.setPixmap(pixmap)

    def convertQImageToCV(self,incomingImage):
        incomingImage = incomingImage.convertToFormat(4)
        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)
        return arr

if __name__ == "__main__":
    app = QApplication(sys.argv)
    webcam = Webcam()
    webcam.MainWindow.show()
    app.exec_()