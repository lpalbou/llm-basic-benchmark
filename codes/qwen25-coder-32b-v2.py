import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Rotating Triangle")

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Ball properties
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [3, 4]

# Triangle properties
triangle_side_length = 200
triangle_center = (WIDTH // 2, HEIGHT // 2)
rotation_angle = 0

# Clock to control the frame rate
clock = pygame.time.Clock()

def rotate_point(point, center, angle):
    """Rotate a point around another center by a given angle."""
    ox, oy = center
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def get_triangle_vertices(center, side_length, angle):
    """Get the vertices of an equilateral triangle."""
    x, y = center
    half_side = side_length / 2
    height = math.sqrt(3) * half_side
    
    # Vertices of the triangle before rotation
    v1 = (x - half_side, y + height / 3)
    v2 = (x + half_side, y + height / 3)
    v3 = (x, y - 2 * height / 3)

    # Rotate vertices around the center
    r_v1 = rotate_point(v1, center, angle)
    r_v2 = rotate_point(v2, center, angle)
    r_v3 = rotate_point(v3, center, angle)

    return [r_v1, r_v2, r_v3]

def is_inside_triangle(point, vertices):
    """Check if a point is inside a triangle using barycentric coordinates."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(point, vertices[0], vertices[1])
    d2 = sign(point, vertices[1], vertices[2])
    d3 = sign(point, vertices[2], vertices[0])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def reflect_vector(normal, incident):
    """Reflect an incident vector off a normal."""
    dot_product = sum(n * i for n, i in zip(normal, incident))
    reflection = [2 * dot_product * n - i for n, i in zip(normal, incident)]
    return reflection

def normalize(vector):
    """Normalize a vector."""
    length = math.sqrt(sum(c ** 2 for c in vector))
    if length == 0:
        return vector
    return [c / length for c in vector]

def main():
    global ball_vel, rotation_angle
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update triangle vertices with rotation
        triangle_vertices = get_triangle_vertices(triangle_center, triangle_side_length, 
rotation_angle)

        # Move the ball
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Check if the ball is outside the triangle and calculate reflection
        if not is_inside_triangle(ball_pos, triangle_vertices):
            # Find the closest edge and reflect the velocity vector
            for i in range(3):
                v1 = triangle_vertices[i]
                v2 = triangle_vertices[(i + 1) % 3]

                # Calculate normal of the edge
                edge_vector = (v2[0] - v1[0], v2[1] - v1[1])
                normal = (-edge_vector[1], edge_vector[0])
                normal = normalize(normal)

                # Reflect velocity vector off the normal
                ball_vel = reflect_vector(normal, ball_vel)
                break

        # Clear screen
        screen.fill(WHITE)

        # Draw triangle
        pygame.draw.polygon(screen, RED, triangle_vertices)

        # Draw ball
        pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

        # Update the display
        pygame.display.flip()

        # Rotate triangle slowly
        rotation_angle += 0.02

        # Cap the frame rate at 60 FPS
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
