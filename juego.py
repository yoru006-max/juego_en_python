import pygame
import os
import random

# Desactiva el audio si hay problemas con ALSA
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Inicialización de pygame
pygame.init()

# Definición de constantes
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))
pygame.display.set_caption("Juego Space Invaders")
icono = pygame.image.load("ufo.png")
pygame.display.set_icon(icono)

# Cargar y escalar la imagen de fondo
fondo = pygame.image.load('background.webp')
fondo = pygame.transform.scale(fondo, (pantalla_ancho, pantalla_alto))

# Carga de imágenes
jugadorImg = pygame.image.load("player.png")
enemigoImg = pygame.image.load("ufo.png")
laserImg = pygame.image.load("bullet.png")
explosion_sonido = pygame.mixer.Sound("explosion.wav")
laser_sonido = pygame.mixer.Sound("laser.wav")

# Variables del jugador
jugadorX = 370
jugadorY = 480
jugadorX_cambio = 0

# Variables del enemigo
num_enemigos = 7
enemigos = []
for i in range(num_enemigos):
    enemigos.append({
        "x": random.randint(50, 750),
        "y": random.randint(50, 150),
        "x_cambio": 3,
        "y_cambio": 40
    })

# Variables del láser
laserX = 0
laserY = 480
laserY_cambio = 5
laser_visible = False
ultimo_disparo = 0  
cooldown_disparo = 0.001  # Control del tiempo entre disparos (en milisegundos)

# Variables del juego
vidas = 3
score = 0
fuente = pygame.font.Font(None, 32)

# Función para dibujar al jugador
def jugador(x, y):
    pantalla.blit(jugadorImg, (x, y))

# Función para dibujar a los enemigos
def enemigo(x, y):
    pantalla.blit(enemigoImg, (x, y))

# Función para disparar el láser
def disparar_laser(x, y):
    global laser_visible
    laser_visible = True
    pantalla.blit(laserImg, (x + 16, y + 10))

# Función para detectar colisiones
def detectar_colision(x1, y1, x2, y2, distancia=27):
    return abs(x1 - x2) < distancia and abs(y1 - y2) < distancia

# Función para mostrar vidas y puntaje
def mostrar_info():
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (255, 255, 255))
    texto_puntaje = fuente.render(f"Puntaje: {score}", True, (255, 255, 255))
    pantalla.blit(texto_vidas, (10, 10))
    pantalla.blit(texto_puntaje, (10, 40))

# Ciclo principal del juego
def juego():
    global jugadorX, jugadorX_cambio, laserX, laserY, laser_visible, score, vidas, ultimo_disparo, cooldown_disparo
    clock = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        pantalla.fill((0, 0, 0))
        pantalla.blit(fondo, (0, 0))

        tiempo_actual = pygame.time.get_ticks()  # Obtener tiempo actual en ms

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugadorX_cambio = -5
                if evento.key == pygame.K_RIGHT:
                    jugadorX_cambio = 5
                if evento.key == pygame.K_SPACE:
                    # Verifica si ha pasado suficiente tiempo desde el último disparo
                    print(f"Tiempo actual: {tiempo_actual}, Último disparo: {ultimo_disparo}, Cooldown: {cooldown_disparo}")  # Depuración
                    if not laser_visible and (tiempo_actual - ultimo_disparo > cooldown_disparo):
                        laser_sonido.play()
                        laserX = jugadorX
                        disparar_laser(laserX, laserY)
                        ultimo_disparo = tiempo_actual  # Guarda el tiempo del disparo
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    jugadorX_cambio = 0

        # Movimiento del jugador
        jugadorX += jugadorX_cambio
        if jugadorX <= 0:
            jugadorX = 0
        elif jugadorX >= 736:
            jugadorX = 736

        # Movimiento de los enemigos
        for enemigo_obj in enemigos:
            enemigo_obj["x"] += enemigo_obj["x_cambio"]
            if enemigo_obj["x"] <= 0 or enemigo_obj["x"] >= 736:
                enemigo_obj["x_cambio"] *= -1
                enemigo_obj["y"] += enemigo_obj["y_cambio"]
            enemigo(enemigo_obj["x"], enemigo_obj["y"])
            
            # Colisión con el jugador
            if detectar_colision(jugadorX, jugadorY, enemigo_obj["x"], enemigo_obj["y"], 50):
                vidas -= 1
                enemigo_obj["x"] = random.randint(50, 750)
                enemigo_obj["y"] = random.randint(50, 150)
                if vidas <= 0:
                    return "menu"
            
            # Colisión con el láser
            if detectar_colision(laserX, laserY, enemigo_obj["x"], enemigo_obj["y"]):
                explosion_sonido.play()
                score += 1
                enemigo_obj["x"] = random.randint(50, 750)
                enemigo_obj["y"] = random.randint(50, 150)
                laser_visible = False
                laserY = 480
        
        # Movimiento del láser
        if laser_visible:
            disparar_laser(laserX, laserY)
            laserY -= laserY_cambio
            if laserY <= 0:
                laser_visible = False
                laserY = 480

        # Dibujar elementos en pantalla
        jugador(jugadorX, jugadorY)
        mostrar_info()
        pygame.display.update()

        clock.tick(60)  # Limita la velocidad a 60 FPS

# Control del estado del juego
estado = "menu"
while estado != "salir":
    if estado == "menu":
        estado = "jugar"  # Se inicia el juego directamente para pruebas
    elif estado == "jugar":
        estado = juego()

pygame.quit()
