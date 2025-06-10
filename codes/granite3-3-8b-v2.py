import pygame
import math
from pygame.locals import *

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 30
SPEED = 5
TRIANGLE_ROTATION_SPEED = 0.01

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_triangle(center, angle):
    points = [
        (center[0] + math.cos(angle) * 150, center[1] - math.sin(angle) * 150),
        (center[0] + math.cos(angle + 120) * 150, center[1] - math.sin(angle + 120) * 150),
        (center[0] + math.cos(angle + 240) * 150, center[1] - math.sin(angle + 240) * 150)
    ]
    pygame.draw.polygon(screen, BLACK, points)

def check_collision(ball_rect, triangle):
    for point in triangle:
        if ball_rect.colliderect(pygame.Rect(point[0] - BALL_SIZE, point[1] - BALL_SIZE, BALL_SIZE * 2, BALL_SIZE * 2)):
            return True
    return False

# Ball position and velocity
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [SPEED, SPEED]

# Triangle center and rotation angle
triangle_center = [WIDTH // 2, HEIGHT // 2]
angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Rotate triangle
    global angle
    angle += TRIANGLE_ROTATION_SPEED
    draw_triangle(triangle_center, angle)

    # Move ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball bounces off edges
    if ball_pos[0] < 0 or ball_pos[0] > WIDTH - BALL_SIZE:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] < 0 or ball_pos[1] > HEIGHT - BALL_SIZE:
        ball_vel[1] = -ball_vel[1]

    # Check for collision with triangle sides
    triangle = [
        (triangle_center[0] + math.cos(angle) * 150, triangle_center[1] - math.sin(angle) * 150),
        (triangle_center[0] + math.cos(angle + 120) * 150, triangle_center[1] - math.sin(angle + 120) * 150),
        (triangle_center[0] + math.cos(angle + 240) * 150, triangle_center[1] - math.sin(angle + 240) * 150)
    ]

    if check_collision(pygame.Rect(ball_pos[0]-BALL_SIZE//2, ball_pos[1]-BALL_SIZE//2, BALL_SIZE, BALL_SIZE), triangle):
        for i in range(len(triangle)):
            if (ball_pos[0] - triangle[i][0]) * (triangle[(i + 1) % len(triangle)][0] - triangle[i][0]) < 0:
                ball_vel[0] = -ball_vel[0]
                break
            if (ball_pos[1] - triangle[i][1]) * (triangle[(i + 1) % len(triangle)][1] - triangle[i][1]) < 0:
                ball_vel[1] = -ball_vel[1]
                break

    # Clear screen and redraw
    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, tuple(ball_pos), BALL_SIZE)
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
