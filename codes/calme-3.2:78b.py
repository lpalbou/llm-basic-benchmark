import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in a Rotating Triangle")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_pos = [width // 2, height // 2]
ball_vel = [2, 2]

# Triangle properties
triangle_points = [(width // 2, 50), (width // 4, height - 50), (3 * width // 4, height - 50)]
angle = 0
angle_speed = 0.01

# Function to rotate the triangle
def rotate_triangle(points, angle):
    center = (width // 2, height // 2)
    rotated_points = []
    for point in points:
        x, y = point
        x -= center[0]
        y -= center[1]
        x_new = x * math.cos(angle) - y * math.sin(angle)
        y_new = x * math.sin(angle) + y * math.cos(angle)
        rotated_points.append((int(x_new + center[0]), int(y_new + center[1])))
    return rotated_points

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Rotate the triangle
    rotated_points = rotate_triangle(triangle_points, angle)
    angle += angle_speed

    # Draw the triangle
    pygame.draw.polygon(screen, (0, 0, 0), rotated_points)

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check collision with triangle
    for i in range(3):
        p1 = rotated_points[i]
        p2 = rotated_points[(i + 1) % 3]
        if (ball_pos[0] - ball_radius < p2[0] and ball_pos[0] + ball_radius > p1[0] and
            ball_pos[1] - ball_radius < p2[1] and ball_pos[1] + ball_radius > p1[1]):
            ball_vel[0] *= -1
            ball_vel[1] *= -1

    # Draw the ball
    pygame.draw.circle(screen, red, [int(ball_pos[0]), int(ball_pos[1])], ball_radius)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
