
import re

class Modelo:    
    def __init__(self, ncaras=None, nvertices=None):
        NumCaras = ncaras
        NumVertices = nvertices
        self.inicializarParametros()


    def setVector4(v, v0, v1, v2, v3):
        v[0]=v0
        v[1]=v1
        v[2]=v2
        v[3]=v3

    def inicializarParametros():
        alpha=0
        beta=0

    def getNCaras():
        return NumCaras

    def setNCaras(val):
        NumCaras = val
    def getNVertices():
        return NumVertices

    def setNVertices(val):
        NumVertices = val

    def Load_Model(fileName):
        file = open(filename,"r")
        lines = file.readlines()
        for line in lines:
            if "Tri-mesh," in line:
                m = re.search('Vertices: (*) Faces: (*)', line)#ni idea tampoco
                self.setNCaras(m.group(2))
                self.setNVertices(m.group(1))
            ListaCaras.resize(self.getNCaras())
            ListaPuntos3D.resize(self.getNVertices())
            if "Vertex [0..*]: " in line:#ni idea
                l = line.split(" ")
                numVert = l[0]




                

    def Draw_Model(iForma, scale_from_editor, zoom):
        pass
