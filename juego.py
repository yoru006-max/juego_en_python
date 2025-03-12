import pygame

# Inicialización de pygame
pygame.init()

# Definición de constantes
pantalla_ancho = 800
pantalla_alto = 600

# Tamaño de la pantalla
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))

# Título e ícono del juego
pygame.display.set_caption("Juego Space Invaders")
icono = pygame.image.load("ufo.png")
pygame.display.set_icon(icono)

# Configuración del fondo
fondo = pygame.image.load('background.png')

# Carga de imágenes
jugadorImg = pygame.image.load("player.png")

# Variables de posición y velocidad
jugadorX = 370
jugadorY = 480
jugadorX_cambio = 0

# Función para dibujar al jugador
def jugador(x, y):
    pantalla.blit(jugadorImg(x,y))