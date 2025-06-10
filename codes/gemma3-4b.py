import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball properties
ball_radius = 20
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = 0
ball_speed_y = 0

# Triangle properties
triangle_size = 100
triangle_x = screen_width // 2
triangle_y = screen_height // 2
triangle_rotation_speed = 2

# Time variables
clock = pygame.time.Clock()
running = True

# Initialize Triangle vertices
triangle_vertices = [
    (triangle_x + triangle_size * math.cos(0), triangle_y + triangle_size * math.sin(0)),
    (triangle_x + triangle_size * math.cos(math.pi / 3), triangle_y + triangle_size * math.sin(math.pi / 3)),
    (triangle_x + triangle_size * math.cos(2 * math.pi / 3), triangle_y + triangle_size * math.sin(2 * math.pi / 3))
]


def draw_triangle(screen, vertices):
    """Draws a triangle on the screen."""
    pygame.draw.polygon(screen, WHITE, vertices, 3)


def collision_detection(ball_x, ball_y, triangle_vertices):
    """Checks if the ball is inside the triangle."""
    # Calculate the barycentric coordinates of the ball's position
    # within the triangle.  This is a simplified approach, and may require
    # adjustment depending on the exact implementation of the triangle
    # and more robust calculation of the triangle's area and vertices.

    # For a simpler approach, we can check if the ball's center is within
    # the triangle's bounding box and calculate the distance from the ball
    # center to each vertex of the triangle.  If the distance is less than
    # the radius, we consider it a collision.

    for vertex in triangle_vertices:
        distance = math.sqrt((vertex[0] - ball_x)**2 + (vertex[1] - ball_y)**2)
        if distance <= ball_radius:
            return True
    return False



def main():
    """Main game loop."""
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Bouncing Ball in Rotating Triangle")

    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update ball position
        ball_speed_x += 0.01
        ball_speed_y += 0.01
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bounce off the walls
        if ball_x + ball_radius > screen_width or ball_x - ball_radius < 0:
            ball_speed_x = -ball_speed_x
        if ball_y + ball_radius > screen_height or ball_y - ball_radius < 0:
            ball_speed_y = -ball_speed_y

        # Update triangle rotation
        triangle_rotation_speed += 0.02

        # Draw everything
        screen.fill(BLACK)
        draw_triangle(screen, triangle_vertices)
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
