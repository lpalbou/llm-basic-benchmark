import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
ROTATION_SPEED = 0.005  # radians per frame
BALL_RADIUS = 15
BALL_SPEED = 3

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Triangle base points (before rotation)
triangle_points = [
    (0, -100),
    (-100, 100),
    (100, 100)
]

# Initialize Pygame
screen = pygame.display(screen=(WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Red Ball in Rotating Triangle")
clock = pygame.time.Clock()

# Triangle rotation
angle = 0  # current rotation angle

# Ball position and velocity
ball_pos = [0, 0]
ball_velocity = [0, 0]

# Functions
def rotate_point(x, y, angle):
    """Rotate point (x, y) around origin by angle radians."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a

def rotate_triangle(triangle, angle):
    """Rotate all triangle points around origin by angle radians."""
    return [rotate_point(px, py, angle) for (px, py) in triangle]

def point_in_triangle(p, a, b, c):
    """Check if point p is inside triangle defined by points a, b, c."""
    def area(p1, p2, p3):
        return abs((p1[0] * (p2[1] - p3[1]) + p1[1] * (p3[0] - p2[0]) + p2[0] * p3[1] - p3[0] * p2[1]) / 2)
    area_total = area(a, b, c)
    area1 = area(p, b, c)
    area2 = area(a, p, c)
    area3 = area(a, b, p)
    return abs(area1 + area2 + area3 - area_total) < 0.01

def reflect_velocity(ball_pos, triangle_points, velocity):
    """Reflect ball velocity when it hits triangle edge."""
    # Find closest edge
    min_dist = float('inf')
    closest_edge = None
    for i in range(len(triangle_points)):
        a = triangle_points[i]
        b = triangle_points[(i + 1) % len(triangle_points)]
        # Reflect ball position
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        # Find normal vector
        normal = (-dy, dx)
        # Normalize
        length = math.sqrt(normal[0]**2 + normal[1]**2)
        normal = (normal[0]/length, normal[1]/length)
        # Compute distance from ball to edge
        dot = normal[0]*(ball_pos[0] - a[0]) + normal[1]*(ball_pos[1] - a[1])
        if dot < 0:
            dot = -dot
        if dot < min_dist:
            min_dist = dot
            closest_edge = (a, b, normal)

    # Reflect velocity
    a, b, normal = closest_edge
    dot = normal[0] * velocity[0] + normal[1] * velocity[1]
    # Reflect velocity
    velocity[0] -= 2 * dot * normal[0]
    velocity[1] -= 2 * dot * normal[1]

# Main Loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Time step

    # Clear screen
    screen.fill(BLACK)

    # Update triangle rotation
    angle += ROTATION_SPEED
    rotated_triangle = rotate_triangle(triangle_points, angle)

    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Check if ball is inside triangle
    ball_inside = point_in_triangle(ball_pos, *rotated_triangle)

    # If ball is outside, reflect it
    if not ball_inside:
        reflect_velocity(ball_pos, rotated_triangle, ball_velocity)

    # Draw triangle
    draw_points = [(int(x + WIDTH/2), int(y + HEIGHT/2)) for (x, y) in rotated_triangle]
    pygame.draw.polygon(screen, WHITE, draw_points, width=3)

    # Draw ball
    ball_draw_pos = (int(ball_pos[0] + WIDTH/2), int(ball_pos[1] + HEIGHT/2))
    pygame.draw.circle(screen, RED, ball_draw_pos, BALL_RADIUS)

    # Event handling
    for event in pygame.event():
        if event.type == pygame.QUIT:
            running = False

    # Update display
    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
