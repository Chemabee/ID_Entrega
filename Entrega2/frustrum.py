from OpenGL.GL import *

class Frustrum:

    def __init__(self, left: GLdouble=0, right: GLdouble=0, bottom: GLdouble=0, top: GLdouble=0, near: GLdouble=0, far: GLdouble=0):
        self.left=left
        self.right=right
        self.bottom=bottom
        self.top=top
        self.near=near
        self.far=far

    def getLeft(self):
        return self.left
    def setLeft(self, left):
        self.left=left
    
    def getRight(self):
        return self.right
    def setRight(self, right):
        self.right=right
    
    def getBottom(self):
        return self.bottom
    def setBottom(self, bottom):
        self.bottom=bottom

    def getTop(self):
        return self.top
    def setTop(self, top):
        self.top=top

    def getNear(self):
        return self.near
    def setNear(self, near):
        self.near=near

    def getFar(self):
        return self.far
    def setFar(self, far):
        self.far=far