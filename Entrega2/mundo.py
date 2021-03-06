import modelo as model
import camera_frustum as cf
import material
from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *
import random
import foco
import time
from PIL import Image
import numpy as np
import random

class Mundo:
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

    # Distintas opciones del menu.
    opcionesMenu = {
      "FONDO_1":0,
      "FONDO_2":1,
      "FONDO_3":2,
      "DIBUJO_1":3,
      "DIBUJO_2":4,
      "DIBUJO_3":5,
      "FORMA_1":6,
      "FORMA_2":7,
      "FORMA_3":8,
      "FORMA_4":9,
      "CAMARA_1":10,
      "CAMARA_2":11,
      "CAMARA_3":12
    }
    #Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    #Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores=[(0.00, 0.00, 0.00), (0.06, 0.25, 0.13), (0.10, 0.07, 0.33), (1.00, 1.00, 1.00), (0.12, 0.50, 0.26), (0.20, 0.14, 0.66)]

    #Cámaras diferentes.
    NUM_CAMARAS=None
    camaras=None
    camarasCargadas=[]
    cam=None

    #Astros diferentes
    planetas=None
    astros=[]
    lunas=[]
    NUM_ASTROS=None

    #Focos diferentes
    NUM_FOCOS=None
    focos=None
    focosCargados=[]

    #Materiales diferentes
    NUM_MATERIALES=None
    materiales=None
    materialesCargados=[]

    starting_time = time.time()

    staTexture=None

    H=800
    W=800
    im = None
    d = []
    fondo=False

    def __init__(self, data =None):
        #Inicializamos todo:
        self.im = Image.open("stars64.bmp")
        self.d = np.array(self.im).reshape(-1,1)
        self.im.close()

        #Variables de la clase
        self.width=800
        self.height=800
        self.aspect = self.width/self.height
        self.angulo = 0
        self.window=0

        #**Cargamos Materiales**
        self.materiales = data["materiales"]
        self.NUM_MATERIALES = len(self.materiales)
        for i in range (self.NUM_MATERIALES):
            self.materialesCargados.append(material.Material(self.materiales[i]["luzambiente"], self.materiales[i]["luzspecular"], self.materiales[i]["luzdifusa"], self.materiales[i]["brillo"]))
            print("&Material",i,"cargado desde JSON")

        #**Cargar Astros**
        numLunas=0
        self.planetas = data["planetas"]
        self.NUM_ASTROS = len(self.planetas)
            #Aqui cargamos los datos en modelos y los guardamos en una lista llamada astros
        for i in range(self.NUM_ASTROS):
            if(self.planetas[i]["l"]=="n"):
                numLunas=0
                self.astros.append(model.Modelo(self.planetas[i], self.materialesCargados[i]))
                print("&Planeta",i,"cargado desde JSON")
            elif(self.planetas[i]["l"]=="l"):
                numLunas+=1
                self.astros[i-numLunas].addLuna(model.Modelo(self.planetas[i], self.materialesCargados[i]))
                #self.lunas.append(model.Modelo(self.planetas[i], self.materialesCargados[i]))
                print("&Luna",numLunas,"del planeta",self.astros[i-numLunas].nombre,"cargado desde JSON")

        #**Cargar Camaras**
        self.camaras = data["camaras"]
        self.numCamaras = len(self.camaras)
            #Cargamos las camaras de data en objetos Camara_Frustum
        for i in range (self.numCamaras):
            self.camarasCargadas.append(cf.Camera_Frustum(self.camaras[i]["ejex"], self.camaras[i]["ejey"], self.camaras[i]["ejez"], 
            self.camaras[i]["centrox"], self.camaras[i]["centroy"], self.camaras[i]["centroz"],
            self.camaras[i]["upx"], self.camaras[i]["upy"], self.camaras[i]["upz"]))
            print("&Camara",i,"cargada desde JSON")

        #**Cargamos Focos**
        self.focos = data["focos"]
        self.NUM_FOCOS=len(self.focos)
        for i in range (self.NUM_FOCOS):
            self.focosCargados.append(foco.Foco(self.focos[i]["brillo"], self.focos[i]["luzdifusa"], self.focos[i]["luzambiente"], self.focos[i]["luzspecular"], self.focos[i]["posicion"]))
            print("&Foco",i,"cargado desde JSON")

        #Tamaño de los ejes y del alejamiento de Z.
        self.tamanio=0
        self.z0=0

        #Factor para el tamaño del modelo.
        self.escalaGeneral = 0.013
        self.multiplicadorVelocidad = 15

        #Rotacion de los modelos.
        self.alpha=0
        self.beta=0

        #Variables para la gestion del ratón.
        self.xold=0
        self.yold=0
        self.zoom=1.0

        #Vistas del Sistema Planetario.
        #modelo.tipoVista iForma
        self.iDibujo=3
        self.iFondo=0
        self.iForma=6
        self.iCamara=10

        

    def drawAxis(self):
        #Inicializamos
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glClearColor(0.0, 0.0, 0.0, 0.0)
	
        #Eje X Rojo
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.tamanio, 0.0, 0.0)

        #Eje Y Verde
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, self.tamanio, 0.0)

        #Eje Z Azul
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, self.tamanio)

        glClearColor(0.0, 0.0, 0.0, 0.0)

        glEnd()
        glEnable(GL_LIGHTING)

    def drawModel(self,forma, escala):
        forma.Draw_Model(self.iForma, escala)

    def loadTexture(self, image):
        glGenTextures(1, textureId)
        glBindTexture(GL_TEXTURE_2D, textureId)

    def chooseCamera(self):
        if(self.iCamara == 10):
            self.cam = self.camarasCargadas[0]
            self.cam.setFrustum(30.0, self.aspect, 1.0, 100.0)
        elif(self.iCamara == 11):
            self.cam = self.camarasCargadas[1]
            self.cam.setFrustum(30.0, self.aspect, 20.0, 100.0)
        elif(self.iCamara == 12):
            self.cam = self.camarasCargadas[2]
            self.cam.setFrustum(30.0, self.aspect, 10.0, 100.0)

    def display(self):
        glClearDepth(1.0)
        glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        #Cargando fondo
        if(self.fondo):
            glDisable(GL_DEPTH_TEST)
            glDrawPixels(self.W, self.H, GL_LUMINANCE, GL_UNSIGNED_BYTE, (GLubyte * len(self.d))(*self.d))
            glEnable(GL_DEPTH_TEST)

        #cam=cf.Camera_Frustum(1, 5, 5, 0, 0, 0, 0, 1, 0, 30.0, self.aspect, 1.0, 10.0)
        self.chooseCamera()
        self.cam.locateFrustum()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.cam.locateCamera(self.zoom)

        #TODO Poner rotacion y mirar ejemplo 3
        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)

        #Establecemos el color del Modelo.
        glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])
            
        #Pintamos el modelo.
        i=0
        for cuerpo in self.astros:
            glPushMatrix()
            tiempo = float(time.time() - self.starting_time)
            glRotatef(tiempo*cuerpo.wRotAstro*self.multiplicadorVelocidad, 0.0, 1.0, 0.0)
            glTranslated(cuerpo.getRadio()*self.escalaGeneral, 0.0, 0.0)
            glRotatef(tiempo*cuerpo.wRotProp*self.multiplicadorVelocidad, 0.0, 1.0, 0.0)
            self.drawModel(cuerpo,self.escalaGeneral)
            if(cuerpo.nombre=="Sol"):
                glRotatef(90.0, 1.0, 0.0, 0.0)
                for body in self.astros:
                    glutWireTorus(0.000, body.getRadio()*self.escalaGeneral, 100, 100)
            i+=1
            if(len(cuerpo.lunas)>0):
                for luna in cuerpo.lunas:
                    glRotatef(90.0, 1.0, 0.0, 0.0)
                    glutWireTorus(0.000, luna.getRadio()*self.escalaGeneral, 100, 100)
                    glRotatef(tiempo*luna.wRotAstro*self.multiplicadorVelocidad, 0.0, 0.0, -1.0)
                    glTranslated(luna.getRadio()*self.escalaGeneral, 0.0, 0.0)
                    glRotatef(tiempo*luna.wRotProp*self.multiplicadorVelocidad, 0.0, 1.0, 0.0)
                    self.drawModel(luna, self.escalaGeneral)
            glPopMatrix()

        for i in range (self.NUM_FOCOS):
            self.focosCargados[i].configurarFoco(i)
            
        
        glEnable(GL_LIGHTING)
        for i in range (self.NUM_FOCOS):
            self.focosCargados[i].habilitar_deshabilitarFoco(i)
 

        #Cerrando
        glFlush()
        glutSwapBuffers()


        
    #Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if (state == GLUT_UP):
                pass
            if(button==3):
                self.zoom=self.zoom-0.1
                #print("Zoom negativo...." + self.zoom)
            else:
                self.zoom=self.zoom+0.1
                #print("Zoom positivo...." + self.zoom)
        else:
            #Actualizamos los valores de x, y.
            self.xold = x
            self.yold = y 

    #Funcion que actualiza la posicion de los modelos en la pantalla segun los movimientos del raton.
    def onMotion(self, x, y):
        self.alpha = (self.alpha + (y - self.yold))
        self.beta = (self.beta + (x - self.xold))
        self.xold = x
        self.yold = y
        glutPostRedisplay()

    #Funcion que gestiona las pulsaciones en el teclado.
    def keyPressed(self, key):
        if(key == chr(27).encode()):  #Tecla Esc
            #Cerramos la ventana y salimos
            glutDestroyWindow(self.window)
            exit()
        elif(key == chr(114).encode() or key == chr(82).encode()):
            for i in range(len(self.randoms)):
                self.randoms[i]=random.random()
        elif(key == chr(49).encode()):  #Tecla 1
            self.focosCargados[0].cambiarEstado()
            self.focosCargados[0].habilitar_deshabilitarFoco(0)
        elif(key == chr(50).encode()):  #Tecla 2
            self.focosCargados[1].cambiarEstado()
            self.focosCargados[1].habilitar_deshabilitarFoco(1)
        elif(key == chr(51).encode()):  #Tecla 3
            self.focosCargados[2].cambiarEstado()
            self.focosCargados[2].habilitar_deshabilitarFoco(2)
        elif(key == chr(52).encode()):  #Tecla 4
            self.focosCargados[3].cambiarEstado()
            self.focosCargados[3].habilitar_deshabilitarFoco(3)
        elif(key == chr(53).encode()):  #Tecla 5
            self.focosCargados[4].cambiarEstado()
            self.focosCargados[4].habilitar_deshabilitarFoco(4)
        elif(key == chr(54).encode()):  #Tecla 6
            self.focosCargados[5].cambiarEstado()
            self.focosCargados[5].habilitar_deshabilitarFoco(5)
        elif(key == chr(55).encode()):  #Tecla 7
            self.focosCargados[6].cambiarEstado()
            self.focosCargados[6].habilitar_deshabilitarFoco(6)
        elif(key == chr(56).encode()):  #Tecla 8 para fondo
            if(self.fondo == True):
                self.fondo = False
            else:
                self.fondo = True

    def setVector4(self, v, v0, v1, v2, v3):
        v[0] = v0
        v[1] = v1
        v[2] = v2
        v[3] = v3
  
    #Funcion para activar las distintas opciones que permite el menu.
    def onMenu(self, opcion):
        if(opcion == self.opcionesMenu["FONDO_1"]):
            self.setIFondo(0)
        elif(opcion == self.opcionesMenu["FONDO_2"]):
            self.setIFondo(1)
        elif(opcion == self.opcionesMenu["FONDO_3"]):
            self.setIFondo(2)
        elif(opcion == self.opcionesMenu["DIBUJO_1"]):
            self.setIDibujo(3)
        elif(opcion == self.opcionesMenu["DIBUJO_2"]):
            self.setIDibujo(4)
        elif(opcion == self.opcionesMenu["DIBUJO_3"]):
            self.setIDibujo(5)
        elif(opcion == self.opcionesMenu["FORMA_1"]):
            self.setIForma(6)
        elif(opcion == self.opcionesMenu["FORMA_2"]):
            self.setIForma(7)
        elif(opcion == self.opcionesMenu["FORMA_3"]):
            self.setIForma(8)
        elif(opcion == self.opcionesMenu["FORMA_4"]):
            self.setIForma(9)
        elif(opcion == self.opcionesMenu["CAMARA_1"]):
            self.setICamara(10)
        elif(opcion == self.opcionesMenu["CAMARA_2"]):
            self.setICamara(11)
        elif(opcion == self.opcionesMenu["CAMARA_3"]):
            self.setICamara(12)

        glutPostRedisplay()
        return opcion
        

    #Aqui antes solo cargaba "Sol" ahora todos los modelos que queramos
    def cargarModelo(self, modelo):
        for cuerpo in self.astros:
            _, vertices, caras = cuerpo.load(modelo)
            cuerpo.setNVertices(len(vertices))
            cuerpo.setNCaras(len(caras))
            cuerpo.setCaras(caras)
            cuerpo.setVertices(vertices)
            if(len(cuerpo.lunas)>0):
                for luna in cuerpo.lunas:
                    _, vertices, caras = luna.load(modelo)
                    luna.setNVertices(len(vertices))
                    luna.setNCaras(len(caras))
                    luna.setCaras(caras)
                    luna.setVertices(vertices)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setIFondo(self, iFondo):
        self.iFondo = iFondo

    def getIFondo(self):
        return self.iFondo

    def setIDibujo(self, iDibujo):
        self.iDibujo = iDibujo

    def getIDibujo(self):
        return self.iDibujo
    
    def setIForma(self, iForma):
        self.iForma = iForma

    def getIForma(self):
        return self.iForma

    def setICamara(self, iCamara):
        self.iCamara = iCamara

    def getICamara(self):
        return self.iCamara