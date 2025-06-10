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
        self.x = randint(100, WIDTH - 100)  # Changed to center of screen
        self.y = randint(100, HEIGHT - 100)
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
        # Rotation angle for triangle
        self.angle = 0
        
    def rotate(self):
        # Rotate triangle by small amount each frame
        self.angle += math.radians(1)
        
        # Update triangle points based on rotation
        new_points = []
        for point in self.points:
            # Calculate rotated point
            x_new, y_new = (point[0] + 200*math.cos(self.angle),
                          point[1] - 100*math.sin(self.angle))
            new_points.append((x_new, y_new))
        
        self.points = new_points

    def draw(self):
        for i in range(3):
            # Calculate new point positions after rotation
            x_new, y_new = (self.points[(i-1)%3][0] + 200*math.cos(self.angle),
                          self.points[(i-1)%3][1] - 100*math.sin(self.angle))
            
            pygame.draw.line(window, WHITE, 
                             self.points[i],
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
                ball.vx *= (-nx)
                ball.vy *= (-ny)

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
