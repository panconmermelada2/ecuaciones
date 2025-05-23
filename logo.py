import pygame
import sys
import math

pygame.init()
W, H = 800, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flor Completa Ajustada")

BG    = (250, 248, 245)
PINK  = (255, 160, 170)
THICK = 6

def get_petal_outline(cx, cy, width, height, segments=80, taper=1.0):
    pts = []
    for i in range(segments+1):
        t = i / segments
        theta = math.pi * t
        w_loc = width * (1 - taper * (t**2))
        x = math.sin(theta) * w_loc
        y = (1 - math.cos(theta)) * height / 2
        pts.append((cx - x, cy + height - y))
    for i in range(segments, -1, -1):
        t = i / segments
        theta = math.pi * t
        w_loc = width * (1 - taper * (t**2))
        x = math.sin(theta) * w_loc
        y = (1 - math.cos(theta)) * height / 2
        pts.append((cx + x, cy + height - y))
    return pts

def rotate_points(points, center, angle_deg):
    ang = math.radians(angle_deg)
    ca, sa = math.cos(ang), math.sin(ang)
    cx, cy = center
    return [(cx + ( x-cx)*ca + ( y-cy)*sa,
             cy + -(x-cx)*sa + ( y-cy)*ca)
            for x, y in points]

def mirror_vertical(points, axis_x):
    return [(2*axis_x - x, y) for x, y in points]

pivot = (W//2, H//2)

outline_vert = get_petal_outline(pivot[0], pivot[1] - 50, 80, 200)
# HASTA AQUÍ YA JALA
outline_h  = rotate_points(outline_vert, pivot, -90)
outline_45 = rotate_points(outline_h,      pivot,  45)

base_ref = outline_h[0]
def align_to(src):
    bx, by = src[0]
    tx, ty = base_ref[0] - bx, base_ref[1] - by
    return [(x+tx, y+ty) for x, y in src]

outline_vert = align_to(outline_vert)
outline_h    = align_to(outline_h)
outline_45   = align_to(outline_45)

outline_h_m  = mirror_vertical(outline_h,  pivot[0])
outline_45_m = mirror_vertical(outline_45, pivot[0])

offset_m_x = -300 
outline_h_m  = [(x + offset_m_x, y) for x, y in outline_h_m]
outline_45_m = [(x + offset_m_x, y) for x, y in outline_45_m]

clock = pygame.time.Clock()
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)

    pygame.draw.lines(screen, PINK, True, outline_vert,   THICK)
    pygame.draw.lines(screen, PINK, True, outline_h,      THICK)
    pygame.draw.lines(screen, PINK, True, outline_45,     THICK)
    pygame.draw.lines(screen, PINK, True, outline_h_m,    THICK)
    pygame.draw.lines(screen, PINK, True, outline_45_m,   THICK)

    pygame.display.flip()
    clock.tick(30)

# profe parece simple pero me dí unos tirototes para poder acomodar los petalos y darles vuelta 😭
