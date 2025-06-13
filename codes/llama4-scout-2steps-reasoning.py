import pygame
import math
import sys

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Ball properties
BALL_RADIUS = 10
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_vx, ball_vy = 3, 3

# Triangle properties
triangle_points = [
    (WIDTH // 2, 50),
    (50, HEIGHT - 50),
    (WIDTH - 50, HEIGHT - 50)
]

# Rotation angle
angle = 0

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def rotate_point(point, center, angle):
    x, y = point
    cx, cy = center
    new_x = cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle)
    new_y = cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle)
    return new_x, new_y

def check_collision(ball_x, ball_y, triangle_points):
    # Simple collision detection using triangle's bounding box
    for point in triangle_points:
        if (point[0] - BALL_RADIUS < ball_x < point[0] + BALL_RADIUS and
            point[1] - BALL_RADIUS < ball_y < point[1] + BALL_RADIUS):
            return True
    return False

def check_edge_collision(ball_x, ball_y, triangle_points):
    # Check collision with each edge of the triangle
    for i in range(3):
        x1, y1 = triangle_points[i]
        x2, y2 = triangle_points[(i + 1) % 3]
        if ((ball_x - x1) * (y2 - y1) - (ball_y - y1) * (x2 - x1)) * ((ball_x - x1) * (y2 - y1) - (ball_y - y1) * (x2 - x1)) < 0:
            return True
    return False

def main():
    global ball_x, ball_y, ball_vx, ball_y, angle
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move ball
        ball_x += ball_vx
        ball_y += ball_vy

        # Bounce off edges
        if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
            ball_vx *= -1
        if ball_y - BALL_RADIUS < 0 or ball_y + BALL_RADIUS > HEIGHT:
            ball_vy *= -1

        # Rotate triangle
        angle += 0.01

        # Check collision with triangle
        rotated_triangle_points = []
        for point in triangle_points:
            new_x = point[0] - WIDTH // 2
            new_y = point[1] - HEIGHT // 2
            rotated_x = new_x * math.cos(angle) - new_y * math.sin(angle) + WIDTH // 2
            rotated_y = new_x * math.sin(angle) + new_y * math.cos(angle) + HEIGHT // 2
            rotated_triangle_points.append((rotated_x, rotated_y))

        # Collision detection
        if check_edge_collision(ball_x, ball_y, rotated_triangle_points):
            ball_vx *= -1
            ball_vy *= -1

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.polygon(screen, RED, rotated_triangle_points)
        pygame.draw.circle(screen, (0, 0, 255), (int(ball_x), int(ball_y)), BALL_RADIUS)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
