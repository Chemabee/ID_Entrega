#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication
#from PyQt4 import QtCore, QtGui, uic
import cv2
import numpy as np
import image_process as mcv2

class Webcam:
    def __init__(self):
        self.cv_video=[]
        self.MainWindow = uic.loadUi('webcam.ui')
        self.MainWindow.setWindowTitle("Esto es una entrega...")
