import pygame
from pygame.draw import *

# Initialize Pygame
pygame.init()

# Constants
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
GRAY = (130, 130, 130)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_background():
    rect(screen, GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_face():
    circle(screen, YELLOW, (200, 200), 150)
    circle(screen, BLACK, (200, 200), 150, 2)

def draw_mouth():
    rect(screen, BLACK, (110, 270, 170, 20))

def draw_eyes():
    left_eye = (110, 170)
    right_eye = (SCREEN_WIDTH - 110, 172)
    circle(screen, RED, left_eye, 30)
    circle(screen, BLACK, left_eye, 30, 2)
    circle(screen, BLACK, left_eye, 10)
    
    circle(screen, RED, right_eye, 30)
    circle(screen, BLACK, right_eye, 30, 2)
    circle(screen, BLACK, right_eye, 10)

def draw_eyebrows():
    left_eyebrow = [(2*30, 3*30), (2*30 + 8, 3*30 - 8), (5*30, 5*30), (5*30 - 8, 5*30 + 8)]
    right_eyebrow = [(SCREEN_WIDTH - 2*30, 3.5*30), (SCREEN_WIDTH - 2*30 - 8, 3.5*30 - 8), 
                     (SCREEN_WIDTH - 5*30, 5*30), (SCREEN_WIDTH - 5*30 + 8, 5*30 + 8)]
    polygon(screen, BLACK, left_eyebrow)
    polygon(screen, BLACK, right_eyebrow)

# Draw everything
draw_background()
draw_face()
draw_mouth()
draw_eyes()
draw_eyebrows()

pygame.display.update()

# Main loop
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
