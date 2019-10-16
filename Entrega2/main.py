import mundo as m
import OpenGL as gl

class Main:

    def display(self):
        self.mundo.display()

    def onMenu(self, opcion):
        self.mundo.onMenu(opcion)

    #Funcion que crea las distintas opciones que se pueden activar en los menus.
    def creacionMenu(self):
        menuFondo = gl.glutCreateMenu(onMenu)
        gl.glutAddMenuEntry("Negro", self.mundo.opcionesMenu[0])
        gl.glutAddMenuEntry("Verde oscuro", self.mundo.opcionesMenu[1])
        gl.glutAddMenuEntry("Azul oscuro", self.mundo.opcionesMenu[2])

        menuDibujo = gl.glutCreateMenu(onMenu)
        gl.glutAddMenuEntry("Blanco", self.mundo.opcionesMenu[4])
        gl.glutAddMenuEntry("Verde claro", self.mundo.opcionesMenu[5])
        gl.glutAddMenuEntry("Azul claro", self.mundo.opcionesMenu[6])

        menuPrincipal = gl.glutCreateMenu(onMenu)
        gl.glutAddSubMenu("Color de fondo", menuFondo)
        gl.glutAddSubMenu("Color del dibujo", menuDibujo)
        #Carga el menú con el boton derecho.
        gl.glutAttachMenu(gl.GLUT_RIGHT_BUTTON)

    def onMotion(self, x, y):
        self.mundo.onMotion(x, y)

    def onMouse(self, button, state, x, y):
        self.mundo.onMouse(button, state, x, y)

    def keyPressed(self, key, x, y):
        self.mundo.keyPressed(key, x, y)

    def InitGL(self):
        #Activamos los buffers
        gl.glutInitDisplayMode(gl.GLUT_DOUBLE | gl.GLUT_RGB | gl.GLUT_RGBA | gl.GLUT_DEPTH | gl.GLUT_ALPHA)	
        #Eestablece el tamaño de la ventana.
        gl.glutInitWindowSize(self.mundo.getWidth(), self.mundo.getHeight())	
        #Establece la posicion inicial (esquina superior izquierda de la ventana).
        gl.glutInitWindowPosition(100, 100)
        gl.glutCreateWindow("Mundo")
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_NORMALIZE)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glDepthFunc(gl.GL_LESS)

    def main(self, argc, argv):
        self.mundo = m.Mundo()

        self.mundo.cargarModelo(argv[1])

        gl.glutInit(argc, argv)

        #Declaraciones Globales
        gl.InitGL()

        #Gestion de los botones del raton
        gl.glutMouseFunc(self.onMouse())
        #Gestion de los movimientos del raton	
        gl.glutMotionFunc(self.onMotion())	
        #Dibujo e Idle
        gl.glutDisplayFunc(self.display())
        gl.glutIdleFunc(self.display())
        #Menús
        self.creacionMenu()
        #Pulsaciones del teclado
        gl.glutKeyboardFunc(self.keyPressed)
            
        #Repeat.
        gl.glutMainLoop()