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

# Variables de juego
vidas = 3
score = 0

# Función para dibujar al jugador
def jugador(x, y):
    pantalla.blit(jugadorImg, (x, y))

# Función para dibujar texto
def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    pantalla.blit(img, (x, y))

# Función para mostrar vidas y puntuación
def mostrar_info():
    fuente = pygame.font.Font(None, 32)
    dibujar_texto(f"Vidas: {vidas}", fuente, (255, 255, 255), 10, 10)
    dibujar_texto(f"Puntuación: {score}", fuente, (255, 255, 255), 10, 50)

# Función para el menú principal
def menu_principal():
    fuente = pygame.font.Font(None, 50)
    opciones = ["Jugar", "Configuración", "Opciones", "Salir"]
    seleccion = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    return opciones[seleccion].lower()

        pantalla.blit(fondo, (0, 0))
        
        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (150, 150, 150)
            dibujar_texto(opcion, fuente, color, pantalla_ancho//2 - 100, 200 + i*70)

        pygame.display.update()

# Ciclo principal del juego
def juego():
    global jugadorX, jugadorX_cambio, vidas, score

    ejecutando = True
    while ejecutando:
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
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

        # Muestra la información de vidas y puntuación
        mostrar_info()

        # Actualiza la pantalla
        pygame.display.update()

        # Aquí puedes agregar lógica para aumentar la puntuación
        # Por ejemplo:
        # score += 1  # Aumenta la puntuación en cada frame

        # Aquí puedes agregar lógica para perder vidas
        # Por ejemplo:
        # if colision_con_enemigo:
        #     vidas -= 1
        #     if vidas <= 0:
        #         return "menu"  # Vuelve al menú principal si se pierden todas las vidas

# Ciclo principal del programa
estado = "menu"
while estado != "salir":
    if estado == "menu":
        estado = menu_principal()
    elif estado == "jugar":
        estado = juego()
    elif estado == "configuración":
        # Aquí puedes agregar la lógica para la pantalla de configuración
        print("Configuración")
        estado = "menu"
    elif estado == "opciones":
        # Aquí puedes agregar la lógica para la pantalla de opciones
        print("Opciones")
        estado = "menu"

pygame.quit()
