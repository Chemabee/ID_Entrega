import sys
from PyQt5 import uic,QtGui,QtCore
from PyQt5.QtWidgets import QApplication

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

        self.viewer_original = QtGui.RCDraw(720, 540, self.image_source, self.MainWindow.viewer_original)
        self.viewer_counter1 = QtGui.RCDraw(304, 130, self.image_counter1, self.MainWindow.viewer_counter1)
        self.viewer_counter2 = QtGui.RCDraw(304, 130, self.image_counter2, self.MainWindow.viewer_counter2)
        self.viewer_counter3 = QtGui.RCDraw(304, 130, self.image_counter3, self.MainWindow.viewer_counter3)

        self.MainWindow.Load_button.clicked.connect(self.loadImage)

def loadImage (self):
    #TODO terminar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.MainWindow.show()
    app.exec_()