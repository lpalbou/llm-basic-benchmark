import pygame
import numpy as np
import math

# Initialization
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Ball
ball_radius = 10
ball_pos = np.array([0.0, -100.0])
ball_vel = np.array([2.0, 1.5])

# Triangle (equilateral, centered at origin)
def create_triangle():
    angle = 2 * np.pi / 3
    return np.array([
        [math.cos(i * angle), math.sin(i * angle)]
        for i in range(3)
    ]) * 300  # scale to size

triangle = create_triangle()
rotation_angle = 0.0

def rotate(points, angle):
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s], [s, c]])
    return points @ R.T

def reflect(velocity, edge_normal):
    return velocity - 2 * np.dot(velocity, edge_normal) * edge_normal

def point_in_triangle(p, tri):
    A, B, C = tri
    v0 = C - A
    v1 = B - A
    v2 = p - A

    d00 = np.dot(v0, v0)
    d01 = np.dot(v0, v1)
    d11 = np.dot(v1, v1)
    d20 = np.dot(v2, v0)
    d21 = np.dot(v2, v1)

    denom = d00 * d11 - d01 * d01
    if denom == 0:
        return False

    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w

    return (u >= 0) and (v >= 0) and (w >= 0)

def get_normal(edge):
    v = edge[1] - edge[0]
    n = np.array([-v[1], v[0]])
    return n / np.linalg.norm(n)

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(BLACK)

    # Rotate triangle
    rotation_angle += 0.2 * dt
    rot_tri = rotate(triangle, rotation_angle)
    tri_center = np.array([WIDTH // 2, HEIGHT // 2])
    screen_tri = rot_tri + tri_center

    # Ball update in triangle frame
    ball_pos += ball_vel

    # Collision detection in rotated frame
    world_ball_pos = ball_pos.copy()
    if not point_in_triangle(world_ball_pos, rot_tri):
        for i in range(3):
            a, b = rot_tri[i], rot_tri[(i+1)%3]
            edge = np.array([a, b])
            edge_vec = b - a
            edge_normal = get_normal(edge)
            to_edge = ball_pos - a
            if np.dot(to_edge, edge_normal) > 0:
                ball_vel = reflect(ball_vel, edge_normal)
                ball_pos += ball_vel
                break

    # Draw triangle
    pygame.draw.polygon(screen, WHITE, screen_tri, 2)

    # Draw ball
    screen_ball = tri_center + rotate(ball_pos, rotation_angle)
    pygame.draw.circle(screen, RED, screen_ball.astype(int), ball_radius)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

