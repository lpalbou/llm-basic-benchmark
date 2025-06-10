import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

# Triangle vertices
triangle_vertices = [
    (WIDTH // 2, 50),  # Top vertex
    (50, HEIGHT - 25),  # Bottom-left vertex
    (WIDTH - 50, HEIGHT - 25)  # Bottom-right vertex
]

# Rotation angle (in degrees)
rotation_angle = 0
rotation_speed = 0.5

# Function to rotate a point around a center
def rotate_point(point, center, angle):
    """Rotates a point around a center point by a given angle (in degrees)."""
    x, y = point
    cx, cy = center
    angle_rad = math.radians(angle)  # Corrected: Use 'angle' not 'angle_rad'
    new_x = cx + (x - cx) * math.cos(angle_rad) - (y - cy) * math.sin(angle_rad)
    new_y = cy + (x - cx) * math.sin(angle_rad) + (y - cy) * math.cos(angle_rad)
    return (new_x, new_y)

# Function to calculate distance between a point and a line segment
def distance_point_line(point, line_start, line_end):
    """Calculates the distance between a point and a line segment."""
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)

    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx**2 + dy**2)

    if t < 0:
        return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    elif t > 1:
        return math.sqrt((x0 - x2)**2 + (y0 - y2)**2)
    else:
        x = x1 + t * dx
        y = y1 + t * dy
        return math.sqrt((x0 - x)**2 + (y0 - y)**2)



# Main game loop
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
    if ball_x + ball_radius > WIDTH or ball_x - ball_radius < 0:
        ball_speed_x = -ball_speed_x
    if ball_y + ball_radius > HEIGHT or ball_y - ball_radius < 0:
        ball_speed_y = -ball_speed_y

    # Rotate the triangle vertices
    rotated_vertices = []
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    for x, y in triangle_vertices:
        rotated_x, rotated_y = rotate_point((x, y), (center_x, center_y), rotation_angle)
        rotated_vertices.append((rotated_x, rotated_y))

    # Collision detection with triangle edges
    # Check collision with each line segment of the triangle
    for i in range(3):
        line_start = rotated_vertices[i]
        line_end = rotated_vertices[(i + 1) % 3]
        distance = distance_point_line((ball_x, ball_y), line_start, line_end)

        if distance <= ball_radius:
            # Calculate the normal vector to the line
            dx = line_end[0] - line_start[0]
            dy = line_end[1] - line_start[1]
            normal_x = dy
            normal_y = -dx

            # Normalize the normal vector
            magnitude = math.sqrt(normal_x**2 + normal_y**2)
            normal_x /= magnitude
            normal_y /= magnitude

            # Reflect the ball's velocity
            dot_product = ball_speed_x * normal_x + ball_speed_y * normal_y
            ball_speed_x -= 0.5 * dot_product * normal_x
            ball_speed_y -= 0.5 * dot_product * normal_y


    # Update rotation angle
    rotation_angle += rotation_speed

    # Clear the screen
    screen.fill(BLACK)

    # Draw the rotating triangle
    pygame.draw.polygon(screen, WHITE, rotated_vertices)

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
