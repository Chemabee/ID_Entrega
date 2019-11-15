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

    #GL_LIGHT
    lights = {
        0 : GL_LIGHT0,
        1 : GL_LIGHT1,
        2 : GL_LIGHT2,
        3 : GL_LIGHT3,
        4 : GL_LIGHT4,
        5 : GL_LIGHT5,
        6 : GL_LIGHT6,
        7 : GL_LIGHT7,
    }

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
    def getBrillo(self):
        return self.brillo

    def estaActivo(self):
        return self.activo
    
    def cambiarEstado(self):
        if self.activo:
            self.activo = False
        else:
            self.activo = True

    def configurarFoco(self, i):
        glLightfv(self.lights[i], GL_DIFFUSE, self.luzdifusa)
        glLightfv(self.lights[i], GL_AMBIENT, self.luzambiente)
        glLightfv(self.lights[i], GL_SPECULAR, self.luzspecular)
        glLightfv(self.lights[i], GL_POSITION, self.posicion)

    def habilitar_deshabilitarFoco(self, i):
        if(self.estaActivo()):
            glEnable(self.lights[i])
        else:
            glDisable(self.lights[i]) 