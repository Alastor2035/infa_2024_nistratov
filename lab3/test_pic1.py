

import pygame
from pygame.draw import *

# Initialize Pygame
pygame.init()

# Constants
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SKY_BLUE = (135, 206, 235)
WATER_BLUE = (0, 105, 148)
SAND_COLOR = (194, 178, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_background():
    # Draw the sky
    screen.fill(SKY_BLUE)
    # Draw the water
    rect(screen, WATER_BLUE, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    # Draw the beach
    rect(screen, SAND_COLOR, (0, SCREEN_HEIGHT * 3 // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 4))

def draw_sun():
    # Draw the sun
    circle(screen, YELLOW, (700, 100), 50)

def draw_cloud(x, y, width, height):
    # Draw a cloud consisting of circles with specified width and height
    num_circles = 5
    circle_radius = height // 2
    for i in range(num_circles):
        offset_x = (i - num_circles // 2) * (width // num_circles)
        circle(screen, WHITE, (x + offset_x, y), circle_radius)
        circle(screen, BLACK, (x + offset_x, y), circle_radius, 1)

def draw_umbrella(x, y):
    # Draw the umbrella
    arc(screen, BLACK, (x, y, 100, 50), 3.14, 0, 5)  # Umbrella top
    rect(screen, BLACK, (x + 40, y + 10, 5, 50))  # Umbrella stick

def draw_sailboat(x, y):
    # Draw the sailboat
    rect(screen, BLACK, (x, y, 60, 20))  # Boat body
    polygon(screen, WHITE, [(x + 30, y - 30), (x + 60, y), (x, y)])  # Sail

# Draw everything
draw_background()
draw_sun()
draw_cloud(100, 50, 100, 40)  # Custom width and height for the cloud
draw_umbrella(350, 500)
draw_sailboat(400, 400)

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
