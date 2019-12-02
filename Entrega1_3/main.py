import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
import cv2
import numpy as np
import math

class Window:
    def __init_(self):
        self.MainWindow = uic.loadUi('mainwindow.ui')
        self.MainWindow.setWindowTitle("Entrega 3 - Looking for something")

        self.MainWindow.slider_barrera1.setRange(0, 350)
        self.MainWindow.spinBarrera1.setRange(0, 350)

        self.MainWindow.slider_barrera2.setRange(0, 350)
        self.MainWindow.spinBarrera2.setRange(0, 350)

        self.MainWindow.sliderBarrera1.valueChanged.connect(self.change_barrier)
        self.MainWindow.sliderBarrera2.valueChanged.connect(self.change_barrier)

    def change_barrier(self):
        self.MainWindow.spinBarrera1.setValue(self.MainWindow.slider_barrera1.value())
        self.MainWindow.spinBarrera2.setValue(self.MainWindow.slider_barrera2.value())

    def show(self):
        self.MainWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()