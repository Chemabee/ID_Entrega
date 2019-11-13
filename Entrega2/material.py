from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Material:
    
    def __init__(self, mat_ambient, mat_specular, mat_emission, brillo):
        self.mat_ambient = mat_ambient
        self.mat_specular = mat_specular
        self.mat_emission = mat_emission
        self.brillo=brillo

    def putMaterial(self):
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.mat_ambient)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.mat_specular)
        glMaterialfv(GL_FRONT, GL_EMISSION, self.mat_emission)
        glMaterialf(GL_FRONT, GL_SHININESS, self.brillo)
