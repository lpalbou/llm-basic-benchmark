import pygame
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the window and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Red Ball")
clock = pygame.time.Clock()

# Triangle vertices (centered at screen center)
triangle = [(WIDTH // 2, HEIGHT // 4), (WIDTH * 3 // 4, HEIGHT * 3 // 4), (WIDTH // 4, HEIGHT * 3 // 4)]
rotation_angle = 0
rotation_speed = 1 # degrees per frame

# Ball properties
ball_radius = 20
ball_pos = list(triangle[0])
ball_velocity = [5, 7]

def rotate_point(point, origin, angle):
    """Rotate a point around another center."""
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
    qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
    return qx, qy

def check_collision():
    """Check if the ball has collided with any edge of the triangle."""
    for i in range(3):
        p1 = triangle[i]
        p2 = triangle[(i + 1) % 3]
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = ball_pos

        # Check if the point is inside the line segment
        dx, dy = x2 - x1, y2 - y1
        det = dx * (y3 - y1) - (x3 - x1) * dy
        length_sq = dx*dx + dy*dy
        param = det / length_sq if length_sq != 0 else -1

        # If the point is on the line segment, check if it's within the circle
        if 0 <= param <= 1:
            x4 = x1 + param * dx
            y4 = y1 + param * dy
            distance_sq = (x4 - x3) ** 2 + (y4 - y3) ** 2
            if distance_sq <= ball_radius ** 2:
                return True
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the triangle rotation
    rotation_angle += rotation_speed
    rotation_angle %= 360
    triangle = [rotate_point(v, (WIDTH // 2, HEIGHT // 2), rotation_angle) for v in triangle]

    # Update the ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Check for collisions
    if check_collision():
        # Reverse velocity to create bouncing effect
        ball_velocity[0] *= -1
        ball_velocity[1] *= -1

    # Keep the ball inside the screen
    ball_pos[0] = max(ball_radius, min(WIDTH - ball_radius, ball_pos[0]))
    ball_pos[1] = max(ball_radius, min(HEIGHT - ball_radius, ball_pos[1]))

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.polygon(screen, (0, 0, 255), triangle)
    pygame.draw.circle(screen, RED, ball_pos, ball_radius)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
