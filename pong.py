import pygame
import sys
from pygame.locals import *
from random import randint  # Importar randint para generar valores aleatorios

# Iniciar pygame
pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong")

# Definir colores
fondo = (0, 0, 0)
color_linea = (255, 255, 255)

# Crear lineas y bola
linea1 = pygame.Rect(50, 250, 10, 100)  # linea izquierda
linea2 = pygame.Rect(740, 250, 10, 100) # linea derecha
bola = pygame.Rect(390, 290, 20, 20)    # Bola

# Velocidad de las lineas
vel_linea = 5

# Velocidad de la bola
vel_bola_x = 2
vel_bola_y = 2

# Variables
juego_comenzado = False
puntuacion1 = 0
puntuacion2 = 0
modo_ia = False



# Función para reiniciar la bola
def reiniciar_bola():
    bola.x = 390  # Reiniciar en el centro
    bola.y = 290  

    vel_bola_x = randint(0, 1) * 2 - 1  # -1 o 1 aleatorio
    vel_bola_y = randint(0, 1) * 2 - 1  # -1 o 1 aleatorio
    return vel_bola_x, vel_bola_y

# Inicializar la velocidad de la bola
vel_bola_x, vel_bola_y = reiniciar_bola()

def main():
    font = pygame.font.SysFont("Arial", 20)
    titulo = font.render("Pong Game", True, color_linea)
    mensaje_iniciar = font.render("Presiona 1 para comenzar (2 players)", True, color_linea)
    mensaje_vsmaquina = font.render("Presiona 2 para comenzar (1 player)", True, color_linea)
    mensaje_salir = font.render("Presiona ESC para salir", True, color_linea)
    
    pantalla.fill(fondo)
    pantalla.blit(titulo, (250, 150))
    pantalla.blit(mensaje_iniciar, (160, 250))
    pantalla.blit(mensaje_vsmaquina, (160, 390))
    pantalla.blit(mensaje_salir, (160, 460))

    pygame.display.update()

#Juego
while True:
    pantalla.fill(fondo)


    # Capturar eventos
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()

    # Detectar teclas presionadas
    pulsado = pygame.key.get_pressed()


    # Mostrar mensaje de inicio si el juego no ha comenzado
    if not juego_comenzado:
        main()

    if pulsado[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    if pulsado[pygame.K_1] and not juego_comenzado:
        modo_ia = False  # Modo 2 jugadores
    if pulsado[pygame.K_2] and not juego_comenzado:
        modo_ia = True  # Modo jugador vs robot



    if pulsado[pygame.K_1] or pulsado[pygame.K_2] and not juego_comenzado:
        juego_comenzado = True
        puntuacion_jugador1 = 0
        puntuacion_jugador2 = 0
        vel_bola_x, vel_bola_y = reiniciar_bola()

    # Dibujar objetos solo si el juego ha comenzado
    if juego_comenzado:
        pygame.draw.rect(pantalla, color_linea, linea1)
        pygame.draw.rect(pantalla, color_linea, linea2)
        pygame.draw.ellipse(pantalla, color_linea, bola)
        font = pygame.font.SysFont("Arial", 30)
        puntuacion = font.render(f"{puntuacion2} : {puntuacion1}", True, color_linea)
        pantalla.blit(puntuacion, (350, 20))




    # Mover la bola
        bola.x += vel_bola_x * 2  # Aumentamos la velocidad en X
        bola.y += vel_bola_y * 2  # Aumentamos la velocidad en Y
        # Colisión contra objetos o paredes
        if bola.top <= 0:
            bola.top = 0
            vel_bola_y = -vel_bola_y 
        if bola.bottom >= 600:
            bola.bottom = 600
            vel_bola_y = -vel_bola_y




        # Reiniciar bola cuando toca las paredes laterales
        if bola.left <= 0:
            vel_bola_x, vel_bola_y = reiniciar_bola()
            puntuacion1 += 1
        elif bola.right >= 800:
            vel_bola_x, vel_bola_y = reiniciar_bola()    
            puntuacion2 += 1





        # Colisión con las lineas
        if bola.colliderect(linea1) or bola.colliderect(linea2):
            vel_bola_x = -vel_bola_x  # Cambiar dirección en X
            #Incrementar velocidad al tocar lineas
            vel_bola_x += 1
            vel_bola_y += 1

    # Movimiento de la linea izquierda (jugador 1) con W y S
    if pulsado[pygame.K_w] and linea1.top > 0:
        linea1.y -= vel_linea
    if pulsado[pygame.K_s] and linea1.bottom < 600:
        linea1.y += vel_linea


    if modo_ia:
        # Movimiento robot
        if bola.centery < linea2.centery and linea2.top > 0:
            linea2.y -= vel_linea
        if bola.centery > linea2.centery and linea2.bottom < 600:
            linea2.y += vel_linea

    else:
        # Movimiento de la linea derecha (jugador 2) con flechas
        if pulsado[pygame.K_UP] and linea2.top > 0:
            linea2.y -= vel_linea
        if pulsado[pygame.K_DOWN] and linea2.bottom < 600:
            linea2.y += vel_linea
    # Iniciar el juego cuando se presiona la barra espaciadora
    if pulsado[pygame.K_SPACE] and not juego_comenzado:
        juego_comenzado = True

    pygame.display.update()

    pygame.time.delay(10)
