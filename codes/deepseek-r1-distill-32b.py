import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 10

class Ball:
    def __init__(self):
        self.x = random.randint(ball_radius, width - ball_radius)  # Random initial position
        self.y = random.randint(ball_radius, height - ball_radius)
        self.dx = 2
        self.dy = 2
        self.color = RED

class Triangle:
    def __init__(self):
        self.center_x = width // 2
        self.center_y = height // 2
        self.side_length = 300
        self.angle = 0  # Initial angle in radians
        self.points = self.calculate_points()

    def calculate_points(self):
        half_side = self.side_length / 2
        points = []
        for i in range(3):
            x = self.center_x + half_side * math.cos(self.angle + (i * 2 * math.pi / 3))
            y = self.center_y + half_side * math.sin(self.angle + (i * 2 * math.pi / 3))
            points.append((x, y))
        return points

    def rotate(self):
        self.angle += 0.01  # Increment angle for rotation
        self.points = self.calculate_points()

def point_on_segment(x, y, x1, y1, x2, y2):
    cross_product = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
    if abs(cross_product) > 0.00001:
        return False
    dot_product = (x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)
    if dot_product < 0:
        return False
    squared_length = (x2 - x1)**2 + (y2 - y1)**2
    if dot_product > squared_length:
        return False
    return True

def segment_intersects_ball(ball, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    len_sq = dx**2 + dy**2
    if len_sq == 0:
        return False
    t = ((ball.x - x1) * dx + (ball.y - y1) * dy) / len_sq
    t = max(0, min(1, t))
    closest_x = x1 + t*dx
    closest_y = y1 + t*dy
    distance = math.hypot(ball.x - closest_x, ball.y - closest_y)
    return distance < ball_radius

def calculate_normal(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    normal_x = -dy
    normal_y = dx
    length = math.hypot(normal_x, normal_y)
    if length == 0:
        return (0, 0)
    return (normal_x / length, normal_x / length)

def reflect_velocity(ball, nx, ny):
    dot_product = ball.dx * nx + ball.dy * ny
    ball.dx -= 2 * dot_product * nx
    ball.dy -= 2 * dot_product * ny

def main():
    running = True
    clock = pygame.time.Clock()
    
    triangle = Triangle()
    ball = Ball()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update ball position
        new_x = ball.x + ball.dx
        new_y = ball.y + ball.dy

        # Check collisions with triangle edges
        collision = False
        points = triangle.points + [triangle.points[0]]
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            if segment_intersects_ball(ball, x1, y1, x2, y2):
                collision = True
                nx, ny = calculate_normal(x1, y1, x2, y2)
                reflect_velocity(ball, nx, ny)
        
        if not collision:
            ball.x += ball.dx
            ball.y += ball.dy
        
        # Check window boundaries (though triangle should contain the ball)
        if ball.x < ball_radius or ball.x > width - ball_radius:
            ball.dx *= -1
        if ball.y < ball_radius or ball.y > height - ball_radius:
            ball.dy *= -1

        # Rotate triangle
        triangle.rotate()

        # Draw everything
        screen.fill(WHITE)
        
        # Draw triangle
        points = triangle.points + [triangle.points[0]]
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 3)
        
        # Draw ball
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), ball_radius)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
