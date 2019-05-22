################################
#        Space Invaders        #
################################

#cosas que se importan
import pygame,sys
from pygame.locals import *  
from random import randint

#variables globales
ancho = 900
alto  = 700
listaEnemigos = []

#Cambio de icono
icono = pygame.image.load("imagenes_juego/space_invader.png")
pygame.display.set_icon(icono)  

#clases
class NaveEspacial(pygame.sprite.Sprite):
    """ crea la clase de las naves """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenNave = pygame.image.load('imagenes_juego/nave.jpg') 
        self.ImagenExplosion = pygame.image.load("imagenes_juego/explosion.jpg")  

        self.rect = self.ImagenNave.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30

        self.listaDisparo= []
        self.Vida = True 

        self.velocidad = 20

    """Nuevos cambios"""

    def movimientoDerecha(self):
    	self.rect.right += self.velocidad
    	self.__movimiento()

    def movimientoIzquierda(self):
    	self.rect.left -= self.velocidad
    	self.__movimiento()

    def __movimiento(self):
    	if self.Vida == True:
    		if self.rect.left <= 0:
    			self.rect.left = 0

    		elif self.rect.right > 900:
    			self.rect.right = 900

    """Fin de los nuevos cambios"""

    def disparar(self,x,y):
        miProyectil = proyectil(x,y, "imagenes_juego/disparoa.jpg", True)
        self.listaDisparo.append(miProyectil)

    def destruccion(self):
        self.Vida = False
        self.velocidad = 0
        self.ImagenNave = self.ImagenExplosion

    def dibujar(self, superficie):
        superficie.blit(self.ImagenNave, self.rect)

    def Ganador(self):
    	self.Vida = False
    	self.velocidad = 0

class proyectil(pygame.sprite.Sprite):
	"""crea la clase de los proyectiles"""

	def __init__(self, posx, posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)

		self.ImagenProyectil = pygame.image.load(ruta)

		self.rect = self.ImagenProyectil.get_rect()

		self.velocidadDisparo = 5

		self.rect.top = posy-50
		self.rect.left = posx-5

		self.disparoPersonaje = personaje

	def Trayectoria(self):
		if self.disparoPersonaje == True:
			self.rect.top = self.rect.top - self.velocidadDisparo

		else:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def Dibujar(self, superficie):
		superficie.blit(self.ImagenProyectil, self.rect)

class Invasor(pygame.sprite.Sprite):
	"""crea la clase de los proyectiles"""
	
	def __init__(self, posx, posy, distancia, imagenUno, imagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.ImagenExplosion = pygame.image.load("imagenes_juego/explosion.jpg") 
		self.imagenA = pygame.image.load(imagenUno)
		self.imagenB = pygame.image.load(imagenDos)

		self.listaImagenes = [self.imagenA, self.imagenB]
		self.posImagen = 0

		self.imagenInvasor = self.listaImagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()

		self.listaDisparo = []
		self.velocidad = 10
		self.rect.top = posy-50
		self.rect.left = posx-5

		self.rangoDisparo = 1
		self.tiempoCambio = 1

		self.conquista = False

		self.derecha = True
		self.contador = 0
		self.Maxdescenso = self.rect.top + 40

		self.limiteDerecha   = posx + distancia
		self.limiteIzquierda = posx - distancia

	def Dibujar(self, superficie):
		self.imagenInvasor = self.listaImagenes[self.posImagen]
		superficie.blit(self.imagenInvasor, self.rect)

	def Comportamiento(self, tiempo):
		#algoritmo de comportamiento

		if self.conquista == False:
			self.__movimientos()
			self.__ataque()

			if self.tiempoCambio == tiempo:
				self.posImagen += 1
				self.tiempoCambio += 1

				if self.posImagen > len(self.listaImagenes)-1:
					self.posImagen = 0

	def __movimientos(self):
		if self.contador < 3:
			self.__movimientoLateral()

		else:
			self.__descenso()

	def __descenso(self):
		if self.Maxdescenso == self.rect.top:
			self.contador = 0
			self.Maxdescenso = self.rect.top + 40

		else:
			self.rect.top += 1

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left = self.rect.left + self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False
				self.contador += 1

		else:
			self.rect.left = self.rect.left - self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True

	def __ataque(self):
		if (randint(0,100) < self.rangoDisparo):
			self.__disparo()

	def __disparo(self):
		x,y = self.rect.center
		miProyectil = proyectil(x,y+65, "imagenes_juego/disparob.jpg", False)
		self.listaDisparo.append(miProyectil)

#funciones

def DetenerTodo():
	for enemigo in listaEnemigos:
		for disparo in enemigo.listaDisparo:
			enemigo.listaDisparo.remove(disparo)

		enemigo.conquista = True

def cargarEnemigos():
	enemigo = Invasor(100,50,100,"imagenes_juego/marcianoA.jpg","imagenes_juego/MarcianoB.jpg")
	listaEnemigos.append(enemigo)
	
	enemigoA = Invasor(300,50,100,"imagenes_juego/marcianoA.jpg","imagenes_juego/MarcianoB.jpg")
	listaEnemigos.append(enemigoA)

	enemigoB = Invasor(500,50,100,"imagenes_juego/marcianoA.jpg","imagenes_juego/MarcianoB.jpg")
	listaEnemigos.append(enemigoB)

	enemigoC = Invasor(700,50,100,"imagenes_juego/marcianoA.jpg","imagenes_juego/MarcianoB.jpg")
	listaEnemigos.append(enemigoC)
	
	"""Segundo marciano"""

	enemigo2 = Invasor(100,150,100,"imagenes_juego/Marciano2A.jpg","imagenes_juego/Marciano2B.jpg")
	listaEnemigos.append(enemigo2)

	enemigo2A = Invasor(300,150,100,"imagenes_juego/Marciano2A.jpg","imagenes_juego/Marciano2B.jpg")
	listaEnemigos.append(enemigo2A)

	enemigo2B = Invasor(500,150,100,"imagenes_juego/Marciano2A.jpg","imagenes_juego/Marciano2B.jpg")
	listaEnemigos.append(enemigo2B)

	enemigo2C = Invasor(700,150,100,"imagenes_juego/Marciano2A.jpg","imagenes_juego/Marciano2B.jpg")
	listaEnemigos.append(enemigo2C)

	"""Tercer marciano"""

	enemigo3 = Invasor(100,250,100,"imagenes_juego/Marciano3A.jpg","imagenes_juego/Marciano3B.jpg")
	listaEnemigos.append(enemigo3)

	enemigo3A = Invasor(300,250,100,"imagenes_juego/Marciano3A.jpg","imagenes_juego/Marciano3B.jpg")
	listaEnemigos.append(enemigo3A)

	enemigo3B = Invasor(500,250,100,"imagenes_juego/Marciano3A.jpg","imagenes_juego/Marciano3B.jpg")
	listaEnemigos.append(enemigo3B)

	enemigo3C = Invasor(700,250,100,"imagenes_juego/Marciano3A.jpg","imagenes_juego/Marciano3B.jpg")
	listaEnemigos.append(enemigo3C)

def SpaceInvader():
	pygame.init()  
	venta = pygame.display.set_mode((ancho,alto)) 
	pygame.display.set_caption("Space Invaders") 
	ImagenFondo = pygame.image.load("imagenes_juego/Fondo.jpg")

	mi_fuenteSistema = pygame.font.SysFont("Arial",30)
	Texto = mi_fuenteSistema.render("Fin del Juego",0,(255,255,255))
	Texto2 = mi_fuenteSistema.render("Has Ganado :D",0,(255,255,255))

	jugador = NaveEspacial()
	cargarEnemigos()

	enJuego = True

	#Nuevo cambio

	reloj = pygame.time.Clock()

	#bucle infinito
	while True:
	    
	    #Nuevo Cambio
	    reloj.tick(30)
	    
	    tiempo = pygame.time.get_ticks()//1000

	    for evento in pygame.event.get():  
	        if evento.type == QUIT:
	            pygame.QUIT  
	            sys.exit()

	        if evento.type == pygame.KEYDOWN:
	            if evento.key == K_ESCAPE:
	            	pygame.QUIT  
	            	sys.exit() 

	        if enJuego == True:
	        	if evento.type == pygame.KEYDOWN:
	        		
	        		if evento.key == K_LEFT:
	        			jugador.movimientoIzquierda()

	        		elif evento.key == K_RIGHT:
	        			jugador.movimientoDerecha()

	        		elif evento.key == K_SPACE:
	        			x,y = jugador.rect.center
	        			jugador.disparar(x,y)

	    venta.blit(ImagenFondo,(0,0))

	    jugador.dibujar(venta)

	    if len(jugador.listaDisparo)>0:
	    	for x in jugador.listaDisparo:
	    		x.Dibujar(venta)
	    		x.Trayectoria()

	    		if x.rect.top < -10:
	    			jugador.listaDisparo.remove(x)

	    		else:
	    			for enemigo in listaEnemigos:
	    				if x.rect.colliderect(enemigo.rect):
	    					listaEnemigos.remove(enemigo) 

	    if len(listaEnemigos) > 0:
	    	for enemigo in listaEnemigos:
	    		enemigo.Comportamiento(tiempo)
	    		enemigo.Dibujar(venta)

	    		if enemigo.rect.colliderect(jugador.rect):
	    			jugador.destruccion()
	    			enJuego = False
	    			DetenerTodo()

	    		if len(enemigo.listaDisparo)>0:
			    	for x in enemigo.listaDisparo:
			    		x.Dibujar(venta)
			    		x.Trayectoria()

			    		if x.rect.colliderect(jugador.rect):
			    			jugador.destruccion()
			    			enJuego = False
			    			DetenerTodo()

			    		if x.rect.top > 900:
			    			enemigo.listaDisparo.remove(x)

			    		else:
			    			for disparo in jugador.listaDisparo:
			    				if x.rect.colliderect(disparo.rect):
			    					jugador.listaDisparo.remove(disparo)
			    					enemigo.listaDisparo.remove(x)

	    if enJuego == False:
	    	pygame.mixer.music.fadeout(3000)
	    	venta.blit(Texto,(400,400))

	    if len(listaEnemigos) == 0:
	    	venta.blit(Texto2,(375,400))
	    	jugador.Ganador()
	    	pygame.mixer.fadeout(3000)

	    	

	    pygame.display.update()  

SpaceInvader()
