import pygame
import sys
import random

"""
Proyecto: Juego de Caída Libre - Ecuaciones Diferenciales

Modelo físico (ED real):
    d²y/dt² = -g 
    Solución:
        v(t) = v0 - g * t
        y(t) = y0 + v0 * t - 0.5 * g * t²
"""
game_width, game_height = 600, 800
pygame.init()
screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Juego: Caída Libre - ED")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

g = 9.81           # m/s²
dt = 1 / 60       # paso de tiempo (60 FPS)

# Jugador 
player_width, player_height = 60, 20
player_x = (game_width - player_width) // 2
player_y = game_height - player_height - 10
player_speed = 7

# Clase para objetos que caen
class FallingObject:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.v = 0  # velocidad inicial
        self.size = 20

    def update(self):
        # Integración de la ED: v += g*dt; y += v*dt
        self.v += g * dt
        self.y += self.v * dt * 50  # escala para visibilidad

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size,
                           self.size*2, self.size*2)

# Variables del juego
falling_objects = []
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 500)  # generar objeto cada 500 ms
score = 0
start_ticks = pygame.time.get_ticks()

font = pygame.font.SysFont('Arial', 24)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_event:
            x_pos = random.randint(20, game_width - 20)
            falling_objects.append(FallingObject(x_pos))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < game_width - player_width:
        player_x += player_speed

    # Actualizar objetos caídos
    for obj in falling_objects[:]:
        obj.update()
        if obj.y > game_height:
            falling_objects.remove(obj)
            score += 1

    # Checar colisiones
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obj in falling_objects:
        if player_rect.colliderect(obj.get_rect()):
            running = False  # fin del juego

    # Dibujar todo
    screen.fill(WHITE)
    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, player_rect)
    # Dibujar objetos
    for obj in falling_objects:
        obj.draw(screen)

    # Texto: ED y modelo
    eq_text = font.render("Ecuación: d²y/dt² = -g", True, BLACK)
    sol_text = font.render("Modelo: y = y0 + v0 t - 0.5 g t²", True, BLACK)
    screen.blit(eq_text, (20, 20))
    screen.blit(sol_text, (20, 50))

    # Texto: puntuación y tiempo
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    score_text = font.render(f"Score: {score}", True, BLACK)
    time_text = font.render(f"Tiempo: {seconds:.2f} s", True, BLACK)
    screen.blit(score_text, (20, 80))
    screen.blit(time_text, (20, 110))

    pygame.display.flip()

# Mensaje de fin
def_text = font.render("Juego terminado! D:" , True, RED)
screen.blit(def_text, (game_width//2 - 80, game_height//2))
pygame.display.flip()
pygame.time.delay(2000)

pygame.quit()
sys.exit()