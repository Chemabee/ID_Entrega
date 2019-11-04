import mundo as m
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

class Main:

    def display(self):
        self.mundo.display()

    def onMenu(self, opcion):
        self.mundo.onMenu(opcion)

    #Funcion que crea las distintas opciones que se pueden activar en los menus.
    def creacionMenu(self):
        menuFondo = glutCreateMenu(self.onMenu)
        glutAddMenuEntry("Negro", self.mundo.opcionesMenu[0])
        glutAddMenuEntry("Verde oscuro", self.mundo.opcionesMenu[1])
        glutAddMenuEntry("Azul oscuro", self.mundo.opcionesMenu[2])

        menuDibujo = glutCreateMenu(self.onMenu)
        glutAddMenuEntry("Blanco", self.mundo.opcionesMenu[4])
        glutAddMenuEntry("Verde claro", self.mundo.opcionesMenu[5])
        glutAddMenuEntry("Azul claro", self.mundo.opcionesMenu[6])

        menuPrincipal = glutCreateMenu(self.onMenu)
        glutAddSubMenu("Color de fondo", menuFondo)
        glutAddSubMenu("Color del dibujo", menuDibujo)
        #Carga el menú con el boton derecho.
        glutAttachMenu(GLUT_RIGHT_BUTTON)

    def onMotion(self, x, y):
        self.mundo.onMotion(x, y)

    def onMouse(self, button, state, x, y):
        self.mundo.onMouse(button, state, x, y)

    def keyPressed(self, key, x, y):
        self.mundo.keyPressed(key, x, y)

    def InitGL(self):
        #Activamos los buffers
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_RGBA | GLUT_DEPTH | GLUT_ALPHA)	
        #Eestablece el tamaño de la ventana.
        glutInitWindowSize(self.mundo.getWidth(), self.mundo.getHeight())	
        #Establece la posicion inicial (esquina superior izquierda de la ventana).
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Mundo")
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)

    def main(self, argc, argv):
        self.mundo = m.Mundo()

        self.mundo.cargarModelo(argv[1])

        glutInit(argc, argv)

        #Declaraciones Globales
        self.InitGL()

        #Gestion de los botones del raton
        glutMouseFunc(self.onMouse)
        #Gestion de los movimientos del raton	
        glutMotionFunc(self.onMotion)	
        #Dibujo e Idle
        glutDisplayFunc(self.display())
        glutIdleFunc(self.display())
        #Menús
        self.creacionMenu()
        #Pulsaciones del teclado
        glutKeyboardFunc(self.keyPressed)
            
        #Repeat.
        glutMainLoop()