from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Foco:
    brillo=None
    luzdifusa=[]
    luzambiente=[]
    luzspecular=[]
    posicion=[]
    activo=False

    def __init__(self, brillo=None, luzdifusa=None, luzambiente=None, luzspecular=None, posicion=None):
        self.brillo = brillo
        self.luzdifusa=luzdifusa
        self.luzambiente=luzambiente
        self.luzspecular=luzspecular
        self.posicion=posicion
        self.activo=True
    
    def getLuzDifusa(self):
        return self.luzdifusa
    def getLuzAmbiente(self):
        return self.luzambiente
    def getLuzSpecular(self):
        return self.luzspecular
    def getPosicion(self):
        return self.posicion
        
    def cambiarEstado(self):
        if self.activo:
            self.activo = False
        else:
            self.activo = True