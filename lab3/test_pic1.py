import pygame
import math
from pygame.draw import *

# Initialize Pygame
pygame.init()

# Constants
FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SKY_BLUE = (135, 206, 235)
WATER_BLUE = (0, 105, 200)
SAND_COLOR = (230, 230, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BEIGE = (200, 200, 170)
BROWN = (139, 69, 19)

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

def draw_sailboat(x, y, size):
    # Draw the hull as an inverted trapezoid
    hull_height = size // 4
    hull_top_width = size
    hull_bottom_width = size * 0.6
    hull_top_left = (x - hull_top_width // 2, y)
    hull_top_right = (x + hull_top_width // 2, y)
    hull_bottom_left = (x - hull_bottom_width // 2, y + hull_height)
    hull_bottom_right = (x + hull_bottom_width // 2, y + hull_height)
    hull_points = [hull_top_left, hull_top_right, hull_bottom_right, hull_bottom_left]
    polygon(screen, BROWN, hull_points)
    
    # Draw the mast
    mast_height = size // 2
    mast_width = size // 15
    rect(screen, BLACK, (x - mast_width // 2, y - mast_height, mast_width, mast_height))
    
    # Draw the sail as a light beige triangle
    sail_height = mast_height
    sail_width = size // 2
    sail_top = (x + mast_width // 2, y - sail_height)
    sail_bottom_left = (x + mast_width // 2, y - size // 15)
    sail_bottom_right = (x + sail_width +  + mast_width // 2, y - size // 15)
    polygon(screen, BEIGE, [sail_top, sail_bottom_left, sail_bottom_right])

# Draw everything
draw_background()
draw_sun()
draw_cloud(100, 50, 100, 40)  # Custom width and height for the cloud
draw_cloud(400, 150, 200, 70)
draw_umbrella(350, 400)
draw_umbrella(250, 500)
draw_sailboat(500, 350, 200) 
draw_sailboat(300, 320, 100)  # Custom size for the sailboat

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
