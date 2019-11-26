import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication
import cv2
import numpy as np
import math

rng = CV_RNG(12345)     #¿?

hierarchy = []
contours = []

def MainWindow(self, parent):
    QMainWindow(parent)
    ui(uic.MainWindow)
    ui.setup(self)

    self.Image_source = QImage(720,540, Format_RGB888)
    self.image_counter = QImage(304,130, Format_Indexed8)
