from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Camera_Frustum:
    def __init__(self, eyeX: float = 0,eyeY: float = 0, eyeZ: float = 0, cenX: float = 0, cenY: float = 0, cenZ: float = 0, vp_X: float = 0, vp_Y: float = 0, vp_Z: float = 0, alpha: GLdouble=0, aspect: GLdouble=0, zNear: GLdouble=0, zFar: GLdouble=0):
        self.eyeX, self.eyeY, self.eyeZ = eyeX, eyeY, eyeZ
        self.cenX, self.cenY, self.cenZ = cenX, cenY, cenZ
        self.vp_X, self.vp_Y, self.vp_Z = vp_X, vp_Y, vp_Z
        self.alpha, self.aspect, self.zNear, self.zFar = alpha, aspect, zNear, zFar

    def locateFrustum(self):
        gluPerspective(self.alpha, self.aspect, self.zNear,self.zFar)

    def locateCamera(self):
        gluLookAt(self.eyeX, self.eyeY, self.eyeZ, self.cenX, self.cenY, self.cenZ, self.vp_X, self.vp_Y, self.vp_Z)
