import modelo as model
from OpenGL.GLUT import * 
from OpenGL.GLU import *
from OpenGL.GL import *

class Mundo:

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
      "FORMA_4":9
    }

    #Número de vistas diferentes.
    numCamaras=3

    #Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    #Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores=[(0.00, 0.00, 0.00), (0.06, 0.25, 0.13), (0.10, 0.07, 0.33), (1.00, 1.00, 1.00), (0.12, 0.50, 0.26), (0.20, 0.14, 0.66)]

    def __init__(self):
        #Inicializamos todo:

        #Variables de la clase
        self.width=800
        self.height=800
        self.aspect = self.width/self.height
        self.angulo = 0
        self.window=0
        self.Sol=model.Modelo()

        #Tamaño de los ejes y del alejamiento de Z.
        self.tamanio=0
        self.z0=0

        #Factor para el tamaño del modelo.
        self.escalaGeneral = 0.005

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
        
        self.material_difuso=[None, None, None, None]
        self.material_ambiente=[None, None, None, None]
        self.material_specular=[None, None, None, None]
        self.material_emission=[None, None, None, None]
        self.luzdifusa=[None, None, None, None]
        self.luzambiente=[None, None, None, None]
        self.luzspecular=[None, None, None, None]
        self.posicion0=[None, None, None, None]
        self.rotacion=[None, None, None, None]

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
        forma.Draw_Model(self.iForma, escala, self.zoom)

    def display(self):
        glClearDepth(1.0)
        glClearColor(self.colores[self.getIFondo()][0], self.colores[self.getIFondo()][1], self.colores[self.getIFondo()][2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(self.alpha, 1.0, 0.0, 0.0)
        glRotatef(self.beta, 0.0, 1.0, 0.0)

        #Establecemos el color del Modelo.
        glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], self.colores[self.getIDibujo()][2])
            
        #Pintamos el modelo.
        self.drawModel(self.Sol,self.escalaGeneral)

        brillo = 10
        self.setVector4(self.luzdifusa, 1.0, 1.0, 1.0, 1.0)
        self.setVector4(self.luzambiente, 0.50, 0.50, 0.50, 1.0)
        self.setVector4(self.luzspecular, 0.20, 0.20, 0.20, 1.0)
        self.setVector4(self.posicion0, 5.0, 5.0, 6.0, 0.0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.luzdifusa)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.luzambiente)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.luzspecular)
        glLightfv(GL_LIGHT0, GL_POSITION, self.posicion0)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glFlush()
        glutSwapBuffers()

        
    #Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if (state == GLUT_UP):
                pass
            if(button==3):
                self.zoom=self.zoom-0.1
                print("Zoom negativo...." + self.zoom)
            else:
                self.zoom=self.zoom+0.1
                print("Zoom positivo...." + self.zoom)
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
    def keyPressed(self, key, x, y):
        if(key == 27):  #Tecla Esc
            #Cerramos la ventana y salimos
            glutDestroyWindow(self.window)
            exit(self, 0)

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
        glutPostRedisplay()
        return opcion
        


    def cargarModelo(self, nombre):
        _, vertices, caras = self.Sol.load(nombre)
        self.Sol.setNVertices(len(vertices))
        self.Sol.setNCaras(len(caras))
        self.Sol.setCaras(caras)
        self.Sol.setVertices(vertices)

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