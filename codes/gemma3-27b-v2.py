import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

# Colors
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 5
ball_speed_y = 5

# Triangle properties
triangle_vertices = [
    (width // 2 - 100, height // 2 - 50),
    (width // 2 + 100, height // 2 - 50),
    (width // 2, height // 2 + 100)
]
rotation_speed = 0.005  # Adjust for slower/faster rotation
angle = 0

def rotate_point(point, angle, center):
    """Rotates a point around a center point."""
    x = point[0] - center[0]
    y = point[1] - center[1]
    rotated_x = x * math.cos(angle) - y * math.sin(angle)
    rotated_y = x * math.sin(angle) + y * math.cos(angle)
    return (int(rotated_x + center[0]), int(rotated_y + center[1]))

def is_inside_triangle(point, vertices):
    """Determines if a point is inside a triangle using barycentric coordinates."""
    x, y = point
    x1, y1 = vertices[0]
    x2, y2 = vertices[1]
    x3, y3 = vertices[2]

    denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if denominator == 0:
        return False  # Avoid division by zero if the triangle is degenerate

    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
    c = 1 - a - b

    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1


def draw_triangle(screen, vertices):
    """Draws a triangle given its vertices."""
    pygame.draw.polygon(screen, white, vertices)

def draw_ball(screen, x, y, radius):
    """Draws a ball at a given position."""
    pygame.draw.circle(screen, red, (x, y), radius)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Wall collision
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_speed_x = -ball_speed_x
    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_speed_y = -ball_speed_y

    # Update triangle rotation
    rotated_vertices = [rotate_point(v, angle, (width // 2, height // 2)) for v in triangle_vertices]
    angle += rotation_speed

    # Triangle collision
    if not is_inside_triangle((ball_x, ball_y), rotated_vertices):
        # Reflect the ball's velocity
        # Calculate the normal vector of the closest edge
        # This is a simplified reflection - a more accurate solution would involve
        # finding the closest point on the triangle and calculating the normal at that point.

        #For simplicity, just reverse the direction, this is not perfect but improves the behavior
        ball_speed_x = -ball_speed_x
        ball_speed_y = -ball_speed_y

    # Clear the screen
    screen.fill(black)

    # Draw the triangle and ball
    draw_triangle(screen, rotated_vertices)
    draw_ball(screen, ball_x, ball_y, ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
