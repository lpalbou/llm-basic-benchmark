import pygame
import math
from random import randint

# Initialize Pygame
pygame.init()

# Set up display window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Triangle")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.radius = 20
        # Random starting position within the triangle
        self.x = randint(self.radius, WIDTH - self.radius)
        self.y = randint(self.radius, HEIGHT - self.radius)
        # Initial velocity
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)

    def update_position(self):
        self.x += self.vx
        self.y += self.vy

    def bounce_off_edges(self):
        if self.x < self.radius:
            self.x = self.radius
            self.vx *= -1
        elif self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.vx *= -1
            
        if self.y < self.radius:
            self.y = self.radius
            self.vy *= -1
        elif self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(window, RED, (int(self.x), int(self.y)), self.radius)

class Triangle:
    def __init__(self):
        self.points = [
            (WIDTH/2 + 200, 50),
            (WIDTH/2 + 50, HEIGHT - 50),
            (WIDTH/2 - 150, HEIGHT/2)
        ]
        # Rotation angle
        self.angle = 0
        
    def rotate(self):
        # Rotate triangle by small amount each frame
        self.angle += math.radians(1)

    def get_point_angle(self, point):
        # Calculate rotation matrix for triangle points
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        
        x = point[0] * cos_a - point[1] * sin_a
        y = point[0] * sin_a + point[1] * cos_a
        
        return (x, y)

    def draw(self):
        # Draw rotated triangle
        for i in range(3):
            # Calculate new point positions after rotation
            x_new, y_new = self.get_point_angle(self.points[i])
            
            pygame.draw.line(window, WHITE, self.points[(i-1)%3], 
                            (x_new + WIDTH/2, y_new + HEIGHT/2), 2)

def main():
    ball = Ball()
    triangle = Triangle()

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update positions
        ball.update_position()
        
        # Check collision with triangle edges
        for point in triangle.points:
            dx = ball.x - point[0]
            dy = ball.y - point[1]
            
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < (ball.radius + 10):  # Collision threshold
                # Calculate collision normal vector
                nx = (point[0] - ball.x) / distance
                ny = (point[1] - ball.y) / distance
                
                # Reflect velocity
                ball.vx -= 2 * nx * dx
                ball.vy -= 2 * ny * dy

        # Update triangle rotation
        triangle.rotate()

        # Draw everything
        window.fill((0, 0, 0))
        triangle.draw()
        ball.draw()

        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
