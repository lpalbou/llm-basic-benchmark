import pygame
import math
import sys

# Window size
WIDTH, HEIGHT = 800, 600

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 10
        self.vx = 3
        self.vy = 3

    def update(self):
        self.x += self.vx
        self.y += self.vy

class Triangle:
    def __init__(self):
        self.angle = 0
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.size = 200

    def get_points(self):
        points = []
        for i in range(3):
            angle = self.angle + i * math.pi * 2 / 3
            px = self.center_x + self.size * math.cos(angle)
            py = self.center_y + self.size * math.sin(angle)
            points.append((px, py))
        return points

def check_collision(ball, triangle):
    points = triangle.get_points()
    # Check if ball is outside the triangle
    if not is_point_inside_triangle(ball.x, ball.y, points[0][0], points[0][1], points[1][0], 
                                    points[1][1], points[2][0], points[2][1]):
        # Find closest point on the edge of the triangle
        closest_distance = float('inf')
        closest_point = None
        for i in range(3):
            p1 = points[i]
            p2 = points[(i + 1) % 3]
            distance, point = distance_to_line(ball.x, ball.y, p1[0], p1[1], p2[0], p2[1])
            if distance < closest_distance:
                closest_distance = distance
                closest_point = point

        # Move the ball to the closest point on the edge of the triangle
        ball.x = closest_point[0]
        ball.y = closest_point[1]

        # Reflect the velocity around the normal of the line segment
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.hypot(dx, dy)
        
        if length > 0:
            normal_x = dy / length
            normal_y = -dx / length
            dot_product = ball.vx * normal_x + ball.vy * normal_y
            ball.vx -= 2 * dot_product * normal_x
            ball.vy -= 2 * dot_product * normal_y

def is_point_inside_triangle(x, y, x1, y1, x2, y2, x3, y3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign((x, y), (x1, y1), (x2, y2)) < 0.0
    b2 = sign((x, y), (x2, y2), (x3, y3)) < 0.0
    b3 = sign((x, y), (x3, y3), (x1, y1)) < 0.0

    return ((b1 == b2) and (b2 == b3))

def distance_to_line(x, y, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length_squared = dx * dx + dy * dy
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / length_squared))
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    distance = math.hypot(x - closest_x, y - closest_y)
    return distance, (closest_x, closest_y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    triangle = Triangle()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        triangle.angle += 0.01
        points = triangle.get_points()
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)

        ball.update()
        check_collision(ball, triangle)
        
        # Boundary checking to prevent the ball from going out of screen
        if ball.x - ball.radius < 0:
            ball.vx *= -1
            ball.x = ball.radius
        elif ball.x + ball.radius > WIDTH:
            ball.vx *= -1
            ball.x = WIDTH - ball.radius

        if ball.y - ball.radius < 0:
            ball.vy *= -1
            ball.y = ball.radius
        elif ball.y + ball.radius > HEIGHT:
            ball.vy *= -1
            ball.y = HEIGHT - ball.radius
        
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), ball.radius)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
