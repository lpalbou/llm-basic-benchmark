import math
import pygame

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ball Bouncing in Rotating Triangle")
clock = pygame.time.Clock()
running = True

# Triangle Parameters
center_x, center_y = 400, 300
triangle_radius = 150
rotation_angle = 0.0
rotation_speed = 0.01  # radians per frame

# Ball Parameters
bx, by = 400.0, 300.0  # Ball position
vx, vy = 200.0, 150.0  # Ball velocity
r = 20.0  # Ball radius

def get_triangle_vertices(rotation_angle):
    """Return the triangle's vertices based on current rotation."""
    vertices = []
    for i in range(3):
        angle = rotation_angle + 2 * math.pi * i / 3
        x = center_x + triangle_radius * math.cos(angle)
        y = center_y + triangle_radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def line_from_points(p1, p2):
    """Return coefficients (a, b, c) for the line through p1 and p2."""
    a = p2[1] - p1[1]
    b = p1[0] - p2[0]
    c = p2[0] * p1[1] - p1[0] * p2[1]
    return a, b, c

def signed_distance_to_line(a, b, c, x, y):
    """Return signed distance from point (x, y) to the line ax + by + c = 0."""
    norm = math.hypot(a, b)
    return (a * x + b * y + c) / norm

def reflect_velocity(vx, vy, nx, ny):
    """Reflect velocity vector (vx, vy) over unit normal (nx, ny)."""
    dot = vx * nx + vy * ny
    vx_new = vx - 2 * dot * nx
    vy_new = vy - 2 * dot * ny
    return vx_new, vy_new

# Main Loop
while running:
    dt = clock.tick(60) / 1000  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    bx += vx * dt
    by += vy * dt

    # Get triangle vertices
    triangle = get_triangle_vertices(rotation_angle)
    rotation_angle += rotation_speed

    # Check collision with each triangle edge
    for i in range(3):
        p1 = triangle[i]
        p2 = triangle[(i + 1) % 3]
        a, b, c = line_from_points(p1, p2)

        # Compute signed distance
        dist = signed_distance_to_line(a, b, c, bx, by)

        if dist < 0 and math.hypot(bx - center_x, by - center_y) < triangle_radius + r:
            # Collision detected
            nx = a / math.hypot(a, b)
            ny = b / math.hypot(a, b)

            # Move ball outside
            push = -dist - 0.1  # Add a small buffer to avoid sticking
            bx += nx * push
            by += ny * push

            # Reflect velocity
            vx, vy = reflect_velocity(vx, vy, nx, ny)

    # Draw everything
    screen.fill((30, 30, 30))
    pygame.draw.polygon(screen, (255, 255, 255), triangle, 2)
    pygame.draw.circle(screen, (255, 0, 0), (int(bx), int(by)), int(r))
    pygame.display.flip()

pygame.quit()
