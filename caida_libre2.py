import pygame
import sys
import random
import os

# Proyecto: Juego de Caída Libre - Dificultad Progresiva + Records
# Modelo físico modificado: 
# d²y/dt² = -(g0 + α * incremento)

game_width, game_height = 600, 800
pygame.init()
screen = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Juego: Caída Libre - Dificultad Progresiva")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

g0 = 9.81       # gravedad inicial (m/s²)
alpha = 2.0     # incremento de gravedad cada aumento
dt = 1 / 60     # paso de tiempo (60 FPS)

player_width, player_height = 60, 20
player_x = (game_width - player_width) // 2
player_y = game_height - player_height - 10
player_speed = 7

# Variables del juego
falling_objects = []
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 500)  # generar objeto cada 500 ms
score = 0
start_ticks = pygame.time.get_ticks()

font = pygame.font.SysFont('Arial', 24)

# Archivo de records
records_file = "records.txt"

# Leer records existentes
def load_records():
    if os.path.exists(records_file):
        with open(records_file, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

# Guardar records
def save_records(records):
    with open(records_file, "w") as f:
        for rec in records:
            f.write(f"{rec}\n")

# Clase para objetos que caen
class FallingObject:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.v = 0  # velocidad inicial
        self.size = 20
        self.color = self.random_pastel_color()

    def random_pastel_color(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        return (r, g, b)

    def update(self, current_time):
        # Aumentar gravedad cada 2 segundos
        incremento = int(current_time // 2)
        g_dynamic = g0 + alpha * incremento
        g_dynamic = min(g_dynamic, 50)  # limitar para no volverse imposible

        # dv/dt = - (g0 + α * incremento)
        self.v += g_dynamic * dt    
        # dy/dt = v
        self.y += self.v * dt * 50  

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size,
                           self.size*2, self.size*2)

# Cargar records al inicio
records = load_records()

running = True
while running:
    clock.tick(60)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # tiempo en segundos

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
        obj.update(seconds)
        if obj.y > game_height:
            falling_objects.remove(obj)
            score += 1

    # Checar colisiones
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for obj in falling_objects:
        if player_rect.colliderect(obj.get_rect()):
            running = False

    # Dibujar todo
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player_rect)
    for obj in falling_objects:
        obj.draw(screen)

    # Mostrar información
    eq_text = font.render("Ecuación: d²y/dt² = -(g0 + α * incremento)", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    time_text = font.render(f"Tiempo: {seconds:.2f} s", True, BLACK)

    screen.blit(eq_text, (20, 20))
    screen.blit(score_text, (20, 80))
    screen.blit(time_text, (20, 110))

    pygame.display.flip()

# Fin del juego
nombre = ""
if len(records) < 3 or any(int(rec.split(":")[1]) < score for rec in records):
    pygame.time.delay(500)
    screen.fill(WHITE)
    input_font = pygame.font.SysFont('Arial', 36)
    input_text = input_font.render("Nuevo récord! Escribe tu nombre:", True, BLACK)
    screen.blit(input_text, (50, game_height//2 - 100))
    pygame.display.flip()

    # Capturar nombre
    capturing = True
    input_name = ""
    while capturing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                capturing = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    nombre = input_name.strip()
                    capturing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    input_name += event.unicode

        # Mostrar entrada
        screen.fill(WHITE)
        screen.blit(input_text, (50, game_height//2 - 100))
        name_surface = input_font.render(input_name, True, BLUE)
        screen.blit(name_surface, (50, game_height//2))
        pygame.display.flip()

    # Guardar nuevo récord
    if nombre:
        records.append(f"{nombre}:{score}")
        # Mantener solo los mejores 3
        records = sorted(records, key=lambda x: int(x.split(":")[1]), reverse=True)[:3]
        save_records(records)

# Mostrar mensaje final
screen.fill(WHITE)
final_text = font.render("Juego terminado! D:", True, RED)
screen.blit(final_text, (game_width//2 - 100, game_height//2 - 20))

# Mostrar records
y_offset = game_height//2 + 30
records_title = font.render("Records:", True, BLACK)
screen.blit(records_title, (game_width//2 - 80, y_offset))
for i, rec in enumerate(records):
    rec_text = font.render(f"{i+1}. {rec}", True, BLACK)
    screen.blit(rec_text, (game_width//2 - 80, y_offset + 30 + i*30))

pygame.display.flip()
pygame.time.delay(4000)

pygame.quit()
sys.exit()