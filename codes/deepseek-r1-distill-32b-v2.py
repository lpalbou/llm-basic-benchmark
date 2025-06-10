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
        while True:
            self.x = random.randint(ball_radius, width - ball_radius)
            self.y = random.randint(ball_radius, height - ball_radius)
            # Ensure the ball starts inside the triangle
            if self.is_inside_triangle():
                break
        self.dx = 2
        self.dy = 2
        self.color = RED

    def is_inside_triangle(self):
        points = Triangle.points
        ax, ay = points[0]
        bx, by = points[1]
        cx, cy = points[2]
        
        # Calculate barycentric coordinates
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        b1 = sign((self.x, self.y), ax, ay) < 0
        b2 = sign((self.x, self.y), bx, by) < 0
        b3 = sign((self.x, self.y), cx, cy) < 0

        return ((b1 == b2) and (b2 == b3)) or (abs(sign((self.x, self.y), ax, ay)) <= 0.0001 or 
                abs(sign((self.x, self.y), bx, by)) <= 0.0001 or 
                abs(sign((self.x, self.y), cx, cy)) <= 0.0001)

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

def calculate_normal(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length_sq = dx**2 + dy**2
    if length_sq == 0:
        return (0.0, 0.0)
    inv_length = 1.0 / math.sqrt(length_sq)
    return (-dy * inv_length, dx * inv_length)

def reflect_velocity(ball, nx, ny):
    dot_product = ball.dx * nx + ball.dy * ny
    if abs(dot_product) < 0.0001:
        return
    
    reflection_factor = 2.0 * dot_product
    ball.dx -= reflection_factor * nx
    ball.dy -= reflection_factor * ny

def main():
    running = True
    clock = pygame.time.Clock()
    
    triangle = Triangle()
    ball = Ball()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Ensure the ball stays inside the triangle
        if not ball.is_inside_triangle():
            ball.x, ball.y = random.randint(ball_radius, width - ball_radius), random.randint(ball_radius, height - ball_radius)
            while not ball.is_inside_triangle():
                ball.x = random.randint(ball_radius, width - ball_radius)
                ball.y = random.randint(ball_radius, height - ball_radius)

        # Update ball position
        new_x = ball.x + ball.dx
        new_y = ball.y + ball.dy

        collision = False
        
        # Check collisions with triangle edges using SAT
        points = triangle.points + [triangle.points[0]]
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]

            # Edge as a line segment from (x1,y1) to (x2,y2)
            edge_x = x2 - x1
            edge_y = y2 - y1

            # Translate ball position relative to the start of the edge
            trans_x = new_x - x1
            trans_y = new_y - y1

            # Project onto edge perpendicular
            dot_product = (trans_x * -edge_y) + (trans_y * edge_x)
            if abs(dot_product) > ball_radius:
                continue  # Ball is outside the projection, no collision
            
            # Project along the edge axis
            dot_edge = trans_x * edge_x + trans_y * edge_y
            if dot_edge < 0:
                continue  # Projection behind start point
            length_sq = edge_x**2 + edge_y**2
            if dot_edge > length_sq:
                continue  # Projection beyond end point
            
            # Collision detected
            collision = True
            nx, ny = calculate_normal(x1, y1, x2, y2)
            reflect_velocity(ball, nx, ny)

        if not collision:
            ball.x += ball.dx
            ball.y += ball.dy

        # Keep the ball within screen bounds (as a fallback)
        buffer = 5 * ball_radius
        if ball.x < buffer or ball.x > width - buffer:
            ball.dx *= -1
        if ball.y < buffer or ball.y > height - buffer:
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
