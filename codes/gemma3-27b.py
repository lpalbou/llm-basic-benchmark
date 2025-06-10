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

    # Collision detection with walls
    if ball_x - ball_radius < 0 or ball_x + ball_radius > width:
        ball_speed_x = -ball_speed_x
    if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
        ball_speed_y = -ball_speed_y

    # Update triangle rotation
    rotated_vertices = [rotate_point(v, angle, (width // 2, height // 2)) for v in triangle_vertices]
    angle += rotation_speed

    # Collision detection with triangle
    if not is_inside_triangle((ball_x, ball_y), rotated_vertices):
        # Simple "pushback" collision response
        # Find closest point on triangle and move ball away
        # This is a very basic response and can be improved with more sophisticated methods
        closest_x, closest_y = rotated_vertices[0]  # Default to first vertex
        min_dist = math.sqrt((ball_x - closest_x)**2 + (ball_y - closest_y)**2)
        
        for vertex in rotated_vertices:
            dist = math.sqrt((ball_x - vertex[0])**2 + (ball_y - vertex[1])**2)
            if dist < min_dist:
                min_dist = dist
                closest_x, closest_y = vertex

        # Move ball slightly away from closest point
        dx = ball_x - closest_x
        dy = ball_y - closest_y
        length = math.sqrt(dx**2 + dy**2)
        if length > 0:  # Avoid division by zero
            dx /= length
            dy /= length
            ball_x += dx * 5  # Adjust 5 for "pushback" strength
            ball_y += dy * 5


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
