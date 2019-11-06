from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Camera:
    def __init__(self, eyeX: float = 0,eyeY: float = 0, eyeZ: float = 0, cenX: float = 0, cenY: float = 0, cenZ: float = 0, vp_X: float = 0, vp_Y: float = 0, vp_Z: float = 0):
        self.eyeX, self.eyeY, self.eyeZ = eyeX, eyeY, eyeZ
        self.cenX, self.cenY, self.cenZ = cenX, cenY, cenZ
        self.vp_X, self.vp_Y, self.vp_Z = vp_X, vp_Y, vp_Z
    
    def setEyeX(self, new):
        self.eyeX = new
    
    def setEyeY(self, new):
        self.eyeY = new
    
    def setEyeZ(self, new):
        self.eyeZ = new
    
    def setCenX(self, new):
        self.cenX = new

    def setCenY(self, new):
        self.cenY = new

    def setCenZ(self, new):
        self.cenZ = new
    
    def setVp_X(self, new):
        self.vp_X = new
    
    def setVp_Y(self, new):
        self.vp_Y = new
    
    def setVp_Z(self, new):
        self.vp_Z = new
    
    def getEyeX(self):
        return self.eyeX

    def getEyeY(self):
        return self.eyeY
    
    def getEyeZ(self):
        return self.eyeZ
    
    def getCenX(self):
        return self.cenX
    
    def getCenY(self):
        return self.cenY
    
    def getCenZ(self):
        return self.cenZ

    def getVp_X(self):
        return self.vp_X

    def getVp_Y(self):
        return self.vp_Y

    def getVp_Z(self):
        return self.vp_Z
    
        