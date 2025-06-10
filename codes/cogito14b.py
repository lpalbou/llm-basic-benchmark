import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Triangle with Ball")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.speed_x = 3
        self.speed_y = 2
        
    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        
    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

class Triangle:
    def __init__(self):
        self.width = WIDTH // 2
        self.height = HEIGHT - 100
        self.angle = 0
        
    def draw(self, screen):
        # Convert to radians for rotation
        angle_rad = math.radians(self.angle)
        
        # Calculate triangle points
        top_x = WIDTH // 2
        top_y = 50
        left_x = top_x - (self.width / 2) * math.cos(angle_rad)
        left_y = top_y + (self.height / 2) * math.sin(angle_rad)
        right_x = top_x + (self.width / 2) * math.cos(angle_rad)
        right_y = top_y + (self.height / 2) * math.sin(angle_rad)
        
        pygame.draw.polygon(screen, WHITE, [(left_x, left_y), 
                                          (right_x, right_y),
                                          (top_x, top_y)])
        
    def is_point_inside(self, point):
        x, y = point
        
        # Calculate vectors
        v0x = -self.width / 2 * math.cos(math.radians(self.angle))
        v0y = -(HEIGHT-50) / 2 * math.sin(math.radians(self.angle))
        v1x = self.width / 2 * math.cos(math.radians(self.angle))
        v1y = (HEIGHT-50) / 2 * math.sin(math.radians(self.angle))
        
        # Vector from vertex to point
        vpx = x - WIDTH // 2
        vpy = y - 50
        
        # Calculate dot products
        dp1 = vpx * v0x + vpy * v0y
        dp2 = vpx * v1x + vpy * v1y
        dp3 = (v0x * v1x + v0y * v1y) - ((WIDTH // 4)**2)
        
        # Check if point is inside triangle
        return (dp1 >= 0 and dp2 >= 0 and dp3 >= dp1 + dp2)

def main():
    clock = pygame.time.Clock()
    
    ball = Ball()
    triangle = Triangle()
    angle_speed = 0.5
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Update and draw triangle
        triangle.angle += angle_speed
        if triangle.angle >= 360:
            triangle.angle -= 360
            
        # Draw the rotating triangle
        triangle.draw(screen)
        
        # Move ball
        ball.move()
        
        # Check collisions with triangle
        point = (ball.x, ball.y)
        if not triangle.is_point_inside(point):
            # Implement reflection based on normal vector
            angle_rad = math.radians(triangle.angle)
            nx = -math.sin(angle_rad)  # Normal x component
            ny = math.cos(angle_rad)   # Normal y component
            
            # Calculate dot product of velocity and normal
            dp = ball.speed_x * nx + ball.speed_y * ny
            
            if dp > 0:
                # Reflect the velocity vector
                ball.speed_x -= 2 * dp * nx
                ball.speed_y -= 2 * dp * ny
                
        # Keep ball within screen bounds
        if ball.x < ball.radius:
            ball.x = ball.radius
            ball.speed_x *= -1
        elif ball.x > WIDTH - ball.radius:
            ball.x = WIDTH - ball.radius
            ball.speed_x *= -1
            
        if ball.y < ball.radius:
            ball.y = ball.radius
            ball.speed_y *= -1
        elif ball.y > HEIGHT - ball.radius:
            ball.y = HEIGHT - ball.radius
            ball.speed_y *= -1
            
        # Draw the ball
        ball.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
