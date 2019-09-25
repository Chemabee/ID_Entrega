#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication
#from PyQt4 import QtCore, QtGui, uic
import cv2
import numpy as np


MAX_IMG=2
IDCAM=0

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
        self.MainWindow.canny_slide.setRange(0,150)
        self.MainWindow.canny.setRange(0,150)
        #Conectamos los sliders con sus cajitas
        self.MainWindow.canny_slide.valueChanged.connect(self.change_canny)

        #Timer para refrescar el filtro e imagen
        self.timer_filter = QtCore.QTimer(self.MainWindow);
        self.timer_filter.timeout.connect(self.make_filter)#timer para los filtros de cv2 funcion que ejecuta
        self.timer_filter.start(3);
        
        self.timer_frames = QtCore.QTimer(self.MainWindow);
        self.timer_frames.timeout.connect(self.show_frames)#timer para refrescar la ventana
        self.timer_frames.start(3);

    #Métodos para conectar los sliders con los números en la cajita
    def change_canny(self):
        self.MainWindow.canny.setValue(self.MainWindow.canny_slide.value())

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
        self.cv_video[1] = cv2.Canny(self.cv_video[1], self.MainWindow.canny.value(), self.MainWindow.canny_slide.value())

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