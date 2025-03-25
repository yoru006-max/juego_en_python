import pygame
import os
import random
import time

# Desactiva el audio si hay problemas con ALSA
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Inicialización de pygame
pygame.init()

# Definición de constantes
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
pygame.display.set_caption("Juego Space Invaders")

# Carga de imágenes
fondo = pygame.image.load('background.webp')
inicio_fondo = pygame.image.load('inicio.webp')  # Carga la imagen de inicio
jugadorImg = pygame.image.load("player.png")

# Escalar la imagen del jugador
jugadorImg = pygame.transform.scale(jugadorImg, (64, 64))  # Cambia el tamaño a 64x64 píxeles

enemigoImg = pygame.image.load("enemi.png")  # Cambiado de ufo.png a enemi.png
laserImg = pygame.image.load("bullet.png")

# Carga de sonidos
explosion_sonido = pygame.mixer.Sound("explosion.wav")
laser_sonido = pygame.mixer.Sound("laser.wav")

# Variables del jugador
jugadorX = 370
jugadorY = 480
jugadorX_cambio = 0

# Variables del enemigo
num_enemigos = 7
enemigos = []

# Variables del láser
lasers = []
cooldown_disparo = 0.5  # Espera entre disparos en segundos
ultimo_disparo = 0

# Variables del juego
vidas = 3
score = 0
fuente = pygame.font.Font(None, 32)

# Velocidades
velocidad_jugador = 5
velocidad_enemigo = 2  # Velocidad de los enemigos
velocidad_laser = 5    # Velocidad de los láseres

# Función para reiniciar enemigos
def crear_enemigos():
    global enemigos
    enemigos = []
    for _ in range(num_enemigos):
        enemigos.append({
            "x": random.randint(50, 750),
            "y": random.randint(50, 150),
            "x_cambio": velocidad_enemigo,
            "y_cambio": 40
        })

# Función para dibujar al jugador
def jugador(x, y):
    pantalla.blit(jugadorImg, (x, y))

# Función para dibujar a los enemigos
def enemigo(x, y):
    pantalla.blit(enemigoImg, (x, y))

# Función para disparar el láser
def disparar_laser(x):
    global ultimo_disparo
    if time.time() - ultimo_disparo > cooldown_disparo:
        lasers.append({"x": x + 16, "y": 480})
        laser_sonido.play()
        ultimo_disparo = time.time()

# Función para detectar colisiones
def detectar_colision(x1, y1, x2, y2, distancia=27):
    return abs(x1 - x2) < distancia and abs(y1 - y2) < distancia

# Función para mostrar vidas y puntaje
def mostrar_info():
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
    texto_puntaje = fuente.render(f"Puntaje: {score}", True, (255, 255, 255))
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntaje, (10, 40))

# Pantalla de Game Over
def game_over():
    global vidas, score
    fuente_gameover = pygame.font.Font(None, 60)
    opciones = ["Reintentar", "Salir"]
    seleccion = 0

    while True:
        pantalla.blit(inicio_fondo, (0, 0))  # Dibuja la imagen de fondo
        texto_gameover = fuente_gameover.render("GAME OVER", True, (255, 0, 0))
        pantalla.blit(texto_gameover, (pantalla_ancho//2 - 150, 100))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "Reintentar":
                        vidas = 3
                        score = 0
                        crear_enemigos()
                        return "jugar"
                    else:
                        return "salir"

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (150, 150, 150)
            texto = fuente_gameover.render(opcion, True, color)
            pantalla.blit(texto, (pantalla_ancho//2 - 120, 250 + i*70))
        pygame.display.update()

# Menú de ajustes (placeholder)
def ajustes():
    fuente_ajustes = pygame.font.Font(None, 50)
    opciones = ["Ajuste 1", "Ajuste 2", "Volver"]
    seleccion = 0

    while True:
        pantalla.fill((0, 0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "Volver":
                        return "menu"

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (150, 150, 150)
            texto = fuente_ajustes.render(opcion, True, color)
            pantalla.blit(texto, (pantalla_ancho//2 - 100, 200 + i*70))

        pygame.display.update()

# Ciclo principal del juego
def juego():
    global jugadorX, jugadorX_cambio, vidas, score
    ejecutando = True
    crear_enemigos()
    while ejecutando:
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugadorX_cambio = -velocidad_jugador
                if evento.key == pygame.K_RIGHT:
                    jugadorX_cambio = velocidad_jugador
                if evento.key == pygame.K_SPACE:
                    disparar_laser(jugadorX)
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    jugadorX_cambio = 0

        # Movimiento del jugador
        jugadorX += jugadorX_cambio
        jugadorX = max(0, min(736, jugadorX))

        # Movimiento de los enemigos
        for enemigo_obj in enemigos:
            enemigo_obj["x"] += enemigo_obj["x_cambio"]
            if enemigo_obj["x"] <= 0 or enemigo_obj["x"] >= 736:
                enemigo_obj["x_cambio"] *= -1
                enemigo_obj["y"] += enemigo_obj["y_cambio"]
            enemigo(enemigo_obj["x"], enemigo_obj["y"])

            if detectar_colision(jugadorX, jugadorY, enemigo_obj["x"], enemigo_obj["y"], 50):
                vidas -= 1
                enemigo_obj["x"] = random.randint(50, 750)
                enemigo_obj["y"] = random.randint(50, 150)
                if vidas <= 0:
                    return game_over()

        # Movimiento de los láseres
        for laser in lasers[:]:  # Copia de la lista para evitar errores
            pantalla.blit(laserImg, (laser["x"], laser["y"]))
            laser["y"] -= velocidad_laser  # Usar la velocidad del láser
            if laser["y"] < 0:
                lasers.remove(laser)

            for enemigo_obj in enemigos:
                if detectar_colision(laser["x"], laser["y"], enemigo_obj["x"], enemigo_obj["y"]):
                    explosion_sonido.play()
                    score += 1
                    enemigo_obj["x"] = random.randint(50, 750)
                    enemigo_obj["y"] = random.randint(50, 150)
                    lasers.remove(laser)
                    break  # Evita errores de lista modificada

        jugador(jugadorX, jugadorY)
        mostrar_info()
        pygame.display.update()

# Menú principal
def menu_principal():
    fuente_menu = pygame.font.Font(None, 50)
    opciones = ["Jugar", "Ajustes", "Salir"]
    seleccion = 0

    while True:
        pantalla.blit(inicio_fondo, (0, 0))  # Dibuja la imagen de fondo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "Jugar":
                        return "jugar"
                    elif opciones[seleccion] == "Ajustes":
                        ajustes()  # Llama a la función de ajustes
                    else:
                        return "salir"

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (150, 150, 150)
            texto = fuente_menu.render(opcion, True, color)
            pantalla.blit(texto, (pantalla_ancho//2 - 100, 200 + i*70))

        pygame.display.update()

# Control del estado del juego
estado = "menu"
while estado != "salir":
    if estado == "menu":
        estado = menu_principal()
    elif estado == "jugar":
        estado = juego()

pygame.quit()
