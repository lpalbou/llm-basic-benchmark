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

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

class Triangle:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 200
        self.angle = 0
        self.points = self.calculate_points()

    def calculate_points(self):
        points = []
        for i in range(3):
            angle = math.radians(self.angle + i * 120)
            px = self.x + self.size * math.cos(angle)
            py = self.y + self.size * math.sin(angle)
            points.append((px, py))
        return points

    def update(self):
        self.angle += 0.5
        self.points = self.calculate_points()

    def draw(self, screen):
        pygame.draw.polygon(screen, WHITE, self.points)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def collide_edge(ball, edge_start, edge_end):
    dx = edge_end[0] - edge_start[0]
    dy = edge_end[1] - edge_start[1]

    normal_x = dy
    normal_y = -dx

    length = math.sqrt(normal_x ** 2 + normal_y ** 2)
    normal_x /= length
    normal_y /= length

    tangent_x = -normal_y
    tangent_y = normal_x

    v_normal = ball.velocity_x * normal_x + ball.velocity_y * normal_y
    v_tangent = ball.velocity_x * tangent_x + ball.velocity_y * tangent_y

    v_normal = -v_normal

    ball.velocity_x = v_normal * normal_x + v_tangent * tangent_x
    ball.velocity_y = v_normal * normal_y + v_tangent * tangent_y

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

        ball.update()

        for i in range(3):
            p1 = triangle.points[i]
            p2 = triangle.points[(i + 1) % 3]

            distance_to_edge = abs((p2[0] - p1[0]) * (p1[1] - ball.y) - (p1[0] - ball.x) * (p2[1] - 
p1[1])) / math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[0]) ** 2)

            if distance_to_edge < ball.radius:
                collide_edge(ball, p1, p2)

        ball.x = max(0, min(ball.x, WIDTH))
        ball.y = max(0, min(ball.y, HEIGHT))

        triangle.draw(screen)
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), ball.radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

