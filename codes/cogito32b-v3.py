import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

# Triangle properties
TRIANGLE_SIZE = 200
ROTATION_SPEED = 0.005

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
    def bounce(self, edges):
        # Check collision with triangle edges
        for i in range(len(edges)):
            (x1, y1) = edges[i][0]  # Unpack first point
            (x2, y2) = edges[i][1]  # Unpack second point
            
            # Line equation: ax + by + c = 0
            a = y2 - y1
            b = x1 - x2
            c = (x2 * y1) - (x1 * y2)
            
            # Distance from point to line
            distance = abs(a * self.x + b * self.y + c) / math.sqrt(a*a + b*b)
            
            if distance <= BALL_RADIUS:
                # Reflect the ball's velocity
                normal_x = a / math.sqrt(a*a + b*b)
                normal_y = b / math.sqrt(a*a + b*b)
                
                # Calculate reflection vector
                dot_product = (self.speed_x * normal_x) + (self.speed_y * normal_y)
                self.speed_x -= 2 * dot_product * normal_x
                self.speed_y -= 2 * dot_product * normal_y
                
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), BALL_RADIUS)

def get_triangle_points(rotation_angle):
    # Center of the triangle
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    
    # Calculate vertices of the equilateral triangle
    points = []
    for i in range(3):
        angle = rotation_angle + (math.pi * 2 * i / 3)
        x = center_x + TRIANGLE_SIZE * math.cos(angle)
        y = center_y + TRIANGLE_SIZE * math.sin(angle)
        points.append((x, y))
    
    return points

def main():
    running = True
    ball = Ball()
    rotation_angle = 0
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        screen.fill(WHITE)
        
        # Update triangle angle and get vertices
        rotation_angle += ROTATION_SPEED
        triangle_points = get_triangle_points(rotation_angle)
        
        # Draw rotating triangle
        pygame.draw.polygon(screen, BLACK, triangle_points)  # Changed color to BLACK
        
        # Move ball
        ball.move()
        
        # Get edges of the triangle as lines for collision detection
        edges = []
        for i in range(len(triangle_points)):
            edge_start = triangle_points[i]
            edge_end = triangle_points[(i + 1) % len(triangle_points)]
            edges.append((edge_start, edge_end))
            
        # Check collisions with triangle edges
        ball.bounce(edges)
        
        # Draw ball
        ball.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
