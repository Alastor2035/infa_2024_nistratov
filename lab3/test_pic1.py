import pygame
import math
from pygame.draw import *

# Initialize Pygame
pygame.init()

# Constants
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SKY_BLUE = (135, 206, 235)
WATER_BLUE = (0, 105, 148)
SAND_COLOR = (230, 230, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_background():
    # Draw the sky
    screen.fill(SKY_BLUE)
    
    # Draw the water
    wave_height = 15
    wave_length = 70
    rect(screen, WATER_BLUE, (0, SCREEN_HEIGHT // 2 + wave_height, SCREEN_WIDTH, SCREEN_HEIGHT // 2 - wave_height))

    # Draw the beach with a wavy border made of semicircles
    rect(screen, SAND_COLOR, (0, SCREEN_HEIGHT * 3 // 4, SCREEN_WIDTH, SCREEN_HEIGHT // 4))
    for x in range(0, SCREEN_WIDTH, wave_length*2):
        arc(screen, WATER_BLUE, (x, SCREEN_HEIGHT * 3 // 4 - wave_height, wave_length, wave_height * 2), math.pi, 2 * math.pi, 200)
    for x in range(wave_length, SCREEN_WIDTH, wave_length*2):
        arc(screen, SAND_COLOR, (x, SCREEN_HEIGHT * 3 // 4 -  wave_height, wave_length, wave_height * 2), 0, math.pi, 200)

def draw_sun():
    # Draw the sun
    sun_center = (700, 100)
    sun_radius = 50
    circle(screen, YELLOW, sun_center, sun_radius)
    
    # Draw rays of triangles
    num_rays = 24  # More frequent rays
    ray_length = 70
    for i in range(num_rays):
        angle = i * (360 / num_rays)
        end_x = sun_center[0] + ray_length * math.cos(math.radians(angle))
        end_y = sun_center[1] + ray_length * math.sin(math.radians(angle))
        polygon(screen, YELLOW, [sun_center, 
                                 (end_x, end_y), 
                                 (sun_center[0] + ray_length * math.cos(math.radians(angle + 7.5)), 
                                  sun_center[1] + ray_length * math.sin(math.radians(angle + 7.5)))])

def draw_cloud(x, y, width, height):
    # Draw a cloud consisting of two rows of circles with specified width and height
    num_circles = 5
    circle_radius = height // 2
    for row in range(2):
        for i in range(num_circles):
            offset_x = (i - num_circles // 2) * (width // num_circles)
            offset_y = row * circle_radius
            circle(screen, WHITE, (x + offset_x, y + offset_y), circle_radius)
            circle(screen, BLACK, (x + offset_x, y + offset_y), circle_radius, 1)

def draw_umbrella(x, y):
    # Draw the umbrella leg
    leg_height = 100
    leg_width = 5
    rect(screen, ORANGE, (x, y, leg_width, leg_height))
    
    # Draw the umbrella hat
    hat_height = 50
    hat_width = 100
    hat_top = (x + leg_width // 2, y - hat_height)
    hat_left = (x - hat_width // 2, y)
    hat_right = (x + hat_width // 2 + leg_width, y)
    polygon(screen, RED, [hat_top, hat_left, hat_right])
    
    # Draw the spokes
    num_spokes = 8
    for i in range(num_spokes):
        angle = i * (math.pi / (num_spokes - 1))
        end_x = hat_top[0] + (hat_width // 2) * math.cos(angle)
        end_y = y
        line(screen, BLACK, hat_top, (end_x, end_y))

def draw_sailboat(x, y):
    # Draw the sailboat
    rect(screen, BLACK, (x, y, 60, 20))  # Boat body
    polygon(screen, WHITE, [(x + 30, y - 30), (x + 60, y), (x, y)])  # Sail

# Draw everything
draw_background()
draw_sun()
draw_cloud(100, 50, 100, 40)  # Custom width and height for the cloud
draw_umbrella(350, 400)
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
