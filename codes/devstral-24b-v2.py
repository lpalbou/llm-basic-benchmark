import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_position = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ball_velocity = pygame.Vector2(4, 3)

# Triangle properties
triangle_points = [
    pygame.Vector2(WIDTH // 2, HEIGHT // 4),
    pygame.Vector2((WIDTH // 2) + 150, (HEIGHT // 4) + 200),
    pygame.Vector2((WIDTH // 2) - 150, (HEIGHT // 4) + 200)
]
triangle_rotation = 0
rotation_speed = 0.01

# Function to rotate points around the center of the triangle
def rotate_points(points, angle):
    center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    rotated_points = []
    for point in points:
        translated_point = point - center
        rotated_point = pygame.Vector2(
            translated_point.x * math.cos(angle) - translated_point.y * math.sin(angle),
            translated_point.x * math.sin(angle) + translated_point.y * math.cos(angle)
        )
        rotated_points.append(rotated_point + center)
    return rotated_points

# Function to check collision with triangle
def is_collision_with_triangle(point, points):
    # Check if point is outside the bounding box of the triangle first for optimization
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)

    if not (min_x <= point.x <= max_x and min_y <= point.y <= max_y):
        return False

    # Check if the point is inside the triangle using ray-casting algorithm
    def is_point_in_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False

        px, py = polygon[0]
        for i in range(n + 1):
            sx, sy = polygon[i % n]
            if (y > min(py, sy)) and (y <= max(py, sy)) and (x <= max(px, sx)):
                if py != sy:
                    xinters = (y - py) * (sx - px) / (sy - py) + px
                else:
                    xinters = px

                if x < xinters:
                    inside = not inside

            px, py = sx, sy

        return inside

    # Check for collision with triangle sides using a simple distance approach
    def check_collision_with_sides(point, points):
        for i in range(3):
            p1 = points[i]
            p2 = points[(i + 1) % 3]

            if is_point_in_polygon((point.x, point.y), [p1, p2, (WIDTH//2, HEIGHT//4)]):
                return True

        return False

    # Check both bounding box and sides
    return check_collision_with_sides(point, points)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    new_position = ball_position + ball_velocity

    # Check collision with triangle borders (proper collision detection)
    rotated_triangle_points = rotate_points(triangle_points, triangle_rotation)

    # If the new position would result in a collision, reverse direction and stay at the edge
    if is_collision_with_triangle(new_position, rotated_triangle_points):
        ball_velocity *= -1

    # Update actual ball position after checking for collision
    ball_position = new_position

    # Rotate the triangle
    triangle_rotation += rotation_speed

    # Drawing
    screen.fill(WHITE)

    # Draw rotated triangle
    pygame.draw.polygon(screen, RED, rotated_triangle_points, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_position.x), int(ball_position.y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
