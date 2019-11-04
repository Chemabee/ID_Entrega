import modelo
import OpenGL as gl

class Mundo:

    #Distintas opciones del menu.
    opcionesMenu=["FONDO_1", "FONDO_2", "FONDO_3", "FONDO_4",
				"DIBUJO_1", "DIBUJO_2", "DIBUJO_3", "DIBUJO_4",
				"FORMA_1", "FORMA_2", "FORMA_3", "FORMA_4"]

    #Número de vistas diferentes.
    numCamaras=3

    #Definimos los distintos colores que usaremos para visualizar nuestro Sistema Planetario.
    #Negro, Verde oscuro, Azul oscuro, Blanco, Verde claro, Azul claro
    colores=[{0.00, 0.00, 0.00}, { 0.06, 0.25, 0.13}, { 0.10, 0.07, 0.33}, { 1.00, 1.00, 1.00}, { 0.12, 0.50, 0.26}, { 0.20, 0.14, 0.66}]

    def __init__(self):
        #Inicializamos todo:

        #Variables de la clase
        width=800
        height=800
        aspect = width/height
        angulo = 0
        window=0
        Sol=modelo()

        #Tamaño de los ejes y del alejamiento de Z.
        tamanio=0
        z0=0

        #Factor para el tamaño del modelo.
        escalaGeneral = 0.005

        #Rotacion de los modelos.
        alpha=0
        beta=0

        #Variables para la gestion del ratón.
        xold=0
        yold=0
        zoom=1.0

        #Vistas del Sistema Planetario.
        #modelo.tipoVista iForma
        iDibujo=4
        iFondo=0

    def drawAxis(self):
        #Inicializamos
        gl.glDisable(gl.GL_LIGHTING)
        gl.glBegin(gl.GL_LINES)
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)
	
        #Eje X Rojo
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(self.tamanio, 0.0, 0.0)

        #Eje Y Verde
        gl.glColor3f(0.0, 1.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, self.tamanio, 0.0)

        #Eje Z Azul
        gl.glColor3f(0.0, 0.0, 1.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, self.tamanio)

        gl.glClearColor(0.0, 0.0, 0.0, 0.0)

        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)

    def drawModel(self, escala):
        gl.glDisable(gl.GL_LIGHTING)
        modelo.Draw_Model(modelo.wired,escala,self.zoom)
        gl.glEnable(gl.GL_LIGHTING)

    def display(self):
        gl.glClearDepth(1.0)
        gl.glClearColor(colores[self.getIFondo()][0], colores[self.getIFondo()][1], colores[self.getIFondo()][2], 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        gl.glRotatef(self.alpha, 1.0, 0.0, 0.0)
        gl.glRotatef(self.beta, 0.0, 1.0, 0.0)

        #Establecemos el color del Modelo.
        gl.glColor3f(self.colores[self.getIDibujo()][0], self.colores[self.getIDibujo()][1], colores[self.getIDibujo()][2])
            
        #Pintamos el modelo.
        drawModel(self.Sol,self.escalaGeneral)

        gl.glFlush()
        gl.glutSwapBuffers()

        
    #Funcion para gestionar los movimientos del raton.
    def onMouse(self, button, state, x, y):
        if (button == 3) or (button == 4):
            if (state == gl.GLUT_UP):
                pass
            if(button==3):
                self.zoom=self.zoom-0.1
                print("Zoom negativo...." + zoom)
            else:
                self.zoom=self.zoom+0.1
                print("Zoom positivo...." + zoom)
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
        gl.glutPostRedisplay()

    #Funcion que gestiona las pulsaciones en el teclado.
    def keyPressed(self, key, x, y):
        if(key == 27):  #Tecla Esc
            #Cerramos la ventana y salimos
            gl.glutDestroyWindow(self.window)
            exit(self, 0)

    def setVector4(self, v, v0, v1, v2, v3):
        v[0] = v0
        v[1] = v1
        v[2] = v2
        v[3] = v3
  
    #Funcion para activar las distintas opciones que permite el menu.
    def onMenu(self, opcion):
        if(opcion == self.opcionesMenu[0]):
            setIFondo(self, 0)
        elif(opcion == self.opcionesMenu[1]):
            setIFondo(self, 1)
        elif(opcion == self.opcionesMenu[2]):
            setIFondo(self, 2)
        elif(opcion == self.opcionesMenu[4]):
            setIDibujo(self, 3)
        elif(opcion == self.opcionesMenu[5]):
            setIDibujo(self, 4)
        elif(opcion == self.opcionesMenu[6]):
            setIDibujo(self, 5)
        gl.glutPostRedisplay()
        


    def cargarModelo(self, nombre):
        self.Sol.Load_Model(nombre)

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