import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_position = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ball_velocity = pygame.Vector2(4, 3)

# Triangle properties
triangle_points = [
    pygame.Vector2(WIDTH // 2, HEIGHT // 4),
    pygame.Vector2((WIDTH // 2) + 150, (HEIGHT // 4) + 200),
    pygame.Vector2((WIDTH // 2) - 150, (HEIGHT // 4) + 200)
]
triangle_rotation = 0
rotation_speed = 0.01

# Function to rotate points around the center of the triangle
def rotate_points(points, angle):
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    rotated_points = []
    for point in points:
        translated_point = point - center
        rotated_point = pygame.Vector2(
            translated_point.x * math.cos(angle) - translated_point.y * math.sin(angle),
            translated_point.x * math.sin(angle) + translated_point.y * math.cos(angle)
        )
        rotated_points.append(rotated_point + center)
    return rotated_points

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_position += ball_velocity

    # Check collision with triangle borders (simplified collision detection)
    rotated_triangle_points = rotate_points(triangle_points, triangle_rotation)

    # Simplified collision detection for this example
    if ball_position.x < 50 or ball_position.x > WIDTH - 50:
        ball_velocity.x *= -1

    if ball_position.y < 50 or ball_position.y > HEIGHT - 50:
        ball_velocity.y *= -1

    # Rotate the triangle
    triangle_rotation += rotation_speed

    # Drawing
    screen.fill(WHITE)

    # Draw rotated triangle
    pygame.draw.polygon(screen, RED, rotated_triangle_points, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_position.x), int(ball_position.y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
