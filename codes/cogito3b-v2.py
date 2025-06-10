import pygame
import math
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Define constants
WIDTH = 800
HEIGHT = 600
FPS = 60
BALL_RADIUS = 10

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Rotation rate (degrees per frame)
ROTATION_RATE = math.pi * 2 / FPS

def get_triangle_vertices():
    """Returns vertices of an equilateral triangle."""
    v1_x = WIDTH // 2
    v1_y = -HEIGHT // 3
    
    v2_x = WIDTH // 2 + HEIGHT//6*math.sqrt(3)/2 
    v2_y = HEIGHT//4.5 + (WIDTH/2)*0.866025403784439*math.cos(math.radians(60))
    
    v3_x = WIDTH // 2 - HEIGHT//6*math.sqrt(3)/2
    v3_y = HEIGHT//4.5 - (WIDTH/2)*0.866025403784439*math.cos(math.radians(60))
    
    return [Vector2(v1_x, v1_y), Vector2(v2_x, v2_y), Vector2(v3_x, v3_y)]

def get_triangle_center(vertices):
    """Returns center of triangle."""
    cx = sum(v.x for v in vertices)/len(vertices)
    cy = sum(v.y for v in vertices)/len(vertices)
    return (cx, cy)

def is_point_in_triangle(point, triangle_vertices):
    """Check if point lies inside or on the boundary of triangle."""
    p1, p2, p3 = triangle_vertices
    
    def cross_product(a, b):
        """Compute 2D cross product."""
        return a.x * b.y - a.y * b.x

    v1 = Vector2(p2) - Vector2(p1)
    v2 = Vector2(p3) - Vector2(p1)

    h = (cross_product(v1, v2)) / (cross_product(v1, v1))

    if 0 <= h <= 1:
        return True
    elif cross_product(v1, v2) < 0:
        p1, p2, p3 = p3, p1, p2

    h = ((cross_product(Vector2(p2), Vector2(p3)) +
           (cross_product(Vector2(p3), Vector2(p1))) -
           (cross_product(v1, v2)))) /
         (cross_product(v1, v1))

    return abs(h) < 1e-9

def get_triangle_rotation(vertices):
    """Returns vertices with triangle rotated by ROTATION_RATE."""
    center = get_triangle_center(vertices)
    new_vertices = [Vector2(x + math.cos(ROTATION_RATE)*y - math.sin(ROTATION_RATE)*x, 
                            y + math.sin(ROTATION_RATE)*y) for x,y in zip([a.x for a in vertices], 
[a.y for a in vertices])]
    
    return [new_vertices[0].add(center), new_vertices[1].add(center), new_vertices[2].add(center)]

def main():
    # Create and setup ball
    ball = pygame.Rect(400, 300, BALL_RADIUS*2, BALL_RADIUS*2)

    triangle_vertices = get_triangle_vertices()
    
    last_time = pygame.time.get_ticks()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            ball.y -= 5
        if keys[pygame.K_s]:
            ball.y += 5
        if keys[pygame.K_a]:
            ball.x -= 5
        if keys[pygame.K_d]:
            ball.x += 5

        # Update ball position within triangle boundary
        if not is_point_in_triangle(ball, triangle_vertices):
            ball = pygame.Rect(400, 300, BALL_RADIUS*2, BALL_RADIUS*2)

        # Rotate triangle slowly over time
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - last_time) / 1000.0
        last_time = current_time

        if delta_time > 0:
            triangle_vertices = get_triangle_rotation(triangle_vertices)
            triangle_center = get_triangle_center(triangle_vertices)

        # Draw everything
        screen.fill((255, 255, 255))  # Clear background to white
        
        for vertex in triangle_vertices:
            pygame.draw.line(screen, (0, 0, 0), 
                             (int(vertex.x), int(vertex.y)),
                             (int(vertex.x + 10), int(vertex.y - 10)), 2)

        ball.x = max(0, min(ball.x, WIDTH))
        ball.y = max(0, min(ball.y, HEIGHT))

        pygame.draw.rect(screen, (255, 0, 0),
                         (ball.x - BALL_RADIUS, ball.y - BALL_RADIUS,
                          BALL_RADIUS * 2, BALL_RADIUS * 2))

        pygame.display.flip()

        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
