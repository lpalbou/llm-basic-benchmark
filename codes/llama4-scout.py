import pygame
import math
import sys

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 20
        self.velocity_x = 5
        self.velocity_y = 5

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.velocity_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.velocity_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

class Triangle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 200
        self.angle = 0

    def update(self):
        self.angle += 0.5

    def draw(self, screen):
        points = []
        for i in range(3):
            angle = math.radians(self.angle + i * 120)
            px = self.x + self.size * math.cos(angle)
            py = self.y + self.size * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, WHITE, points)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    triangle = Triangle()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        triangle.update()
        triangle.draw(screen)

        ball.update()

        # Collision detection with triangle
        points = []
        for i in range(3):
            angle = math.radians(triangle.angle + i * 120)
            px = triangle.x + triangle.size * math.cos(angle)
            py = triangle.y + triangle.size * math.sin(angle)
            points.append((px, py))

        inside = False
        n = len(points)
        p1x, p1y = points[0]
        for i in range(n + 1):
            p2x, p2y = points[i % n]
            if ball.y > min(p1y, p2y):
                if ball.y <= max(p1y, p2y):
                    if ball.x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (ball.y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or ball.x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        if not inside:
            # Bounce off triangle
            normal_x = ball.x - triangle.x
            normal_y = ball.y - triangle.y
            length = math.sqrt(normal_x ** 2 + normal_y ** 2)
            normal_x /= length
            normal_y /= length
            dot_product = ball.velocity_x * normal_x + ball.velocity_y * normal_y
            ball.velocity_x -= 2 * dot_product * normal_x
            ball.velocity_y -= 2 * dot_product * normal_y

        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
