import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Triangle")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Ball properties
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = -5

# Triangle properties
triangle_angle = 0
triangle_vertices = [
    [WIDTH // 2, HEIGHT // 3],
    [WIDTH // 4, HEIGHT * 2/3],
    [WIDTH * 3/4, HEIGHT * 2/3]
]

def rotate_triangle(angle):
    """Rotate the triangle by a given angle"""
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    rotated_vertices = []
    
    for x, y in triangle_vertices:
        # Translate to origin
        tx = x - center_x
        ty = y - center_y
        
        # Rotate
        rx = tx * math.cos(math.radians(angle)) - ty * math.sin(math.radians(angle))
        ry = tx * math.sin(math.radians(angle)) + ty * math.cos(math.radians(angle))
        
        # Translate back
        rotated_vertices.append([rx + center_x, ry + center_y])
    
    return rotated_vertices

def check_collision(ball_pos, triangle):
    """Check if the ball is colliding with any side of the triangle"""
    for i in range(3):
        x1 = triangle[i][0]
        y1 = triangle[i][1]
        x2 = triangle[(i + 1) % 3][0]
        y2 = triangle[(i + 1) % 3][1]
        
        # Calculate distance from ball center to line segment
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx**2 + dy**2)
        
        if length == 0:
            continue
            
        t = max(0, min(1, ((ball_pos[0] - x1) * dx + (ball_pos[1] - y1) * dy) / (length**2)))
        px = x1 + t * dx
        py = y1 + t * dy
        
        distance = math.sqrt((ball_pos[0] - px)**2 + (ball_pos[1] - py)**2)
        
        if distance < ball_radius:
            # Calculate reflection angle
            normal_x = dy / length
            normal_y = -dx / length
            
            dot_product = (ball_speed_x * normal_x) + (ball_speed_y * normal_y)
            
            # Reflect the ball's velocity
            ball_speed_x -= 2 * dot_product * normal_x
            ball_speed_y -= 2 * dot_product * normal_y
            
            return True
    
    return False

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update triangle rotation
    triangle_angle += 0.5
    rotated_triangle = rotate_triangle(triangle_angle)
    
    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Check for collision with triangle sides
    if check_collision([ball_x, ball_y], rotated_triangle):
        pass
    
    # Keep ball inside the screen
    ball_x = max(ball_radius, min(WIDTH - ball_radius, ball_x))
    ball_y = max(ball_radius, min(HEIGHT - ball_radius, ball_y))
    
    # Draw everything
    screen.fill(WHITE)
    
    # Draw triangle
    pygame.draw.polygon(screen, (0, 0, 255), rotated_triangle, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
