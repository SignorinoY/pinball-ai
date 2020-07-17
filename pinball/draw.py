import pygame

def draw_line(screen, p1, p2, color):
    pygame.draw.line(screen, color, p1.int(), p2.int(), 1)

def draw_circle(screen, color, center, radius):
    pygame.draw.circle(screen, color, center.int(), int(radius))