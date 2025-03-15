import pygame
import os

# Desactiva el audio si hay problemas con ALSA
os.environ['SDL_AUDIODRIVER'] = 'dummy'

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
    pantalla.blit(jugadorImg, (x, y))  # Corregido: se usa (x, y) en una tupla

# Ciclo principal del juego
ejecutando = True
while ejecutando:
    pantalla.fill((0, 0, 0))
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugadorX_cambio = -5
            if evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 5

        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugadorX_cambio = 0

    # Validación de los límites del jugador
    jugadorX += jugadorX_cambio
    if jugadorX <= 0:
        jugadorX = 0
    elif jugadorX >= 736:
        jugadorX = 736

    # Dibuja el jugador
    jugador(jugadorX, jugadorY)

    # Actualiza la pantalla
    pygame.display.update()