import pygame
from pygame.locals import QUIT

WIDTH, HEIGHT = 700, 500
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# constants

# variables
cuadrado = pygame.Rect(0, HEIGHT/2, 60, 60)
velocidad = 1
aceleracion = 0.3

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

    # code here
    cuadrado.x += velocidad
    velocidad += aceleracion
    pygame.draw.rect(screen, (255, 255, 255), cuadrado)

    pygame.display.update()
    screen.fill((0, 0, 0))
    clock.tick(30)