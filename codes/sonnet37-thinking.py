import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Red Ball in Rotating Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_BLUE = (200, 220, 255)

# FPS setting
clock = pygame.time.Clock()
FPS = 60

# Ball properties
ball_radius = 20
ball_speed = 3  # Speed magnitude
ball_angle = math.radians(45)  # Initial direction angle
ball_vel = np.array([ball_speed * math.cos(ball_angle), ball_speed * math.sin(ball_angle)], dtype=float)
damping_factor = 0.995  # Slight damping to simulate energy loss

# Triangle properties
triangle_center = np.array([WIDTH // 2, HEIGHT // 2])  # Center of rotation
triangle_size = 200  # Distance from center to vertices
triangle_angle = 0  # Initial angle in degrees
triangle_rotation_speed = 0.5  # Degrees per frame

def calculate_triangle_vertices(center, size, angle):
    """Calculate the vertices of an equilateral triangle centered at 'center' with the given size and rotation angle."""
    vertices = []
    for i in range(3):
        angle_rad = math.radians(angle + i * 120)
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        vertices.append(np.array([x, y]))
    return vertices

def distance_point_to_line(point, line_start, line_end):
    """Calculate the shortest distance from a point to a line segment."""
    line_vec = line_end - line_start
    point_vec = point - line_start
    
    line_len = np.linalg.norm(line_vec)
    line_unit_vec = line_vec / line_len
    
    projection = np.dot(point_vec, line_unit_vec)
    projection = max(0, min(line_len, projection))
    
    closest_point = line_start + line_unit_vec * projection
    
    distance = np.linalg.norm(point - closest_point)
    
    # Calculate normal vector (perpendicular to the line)
    normal = np.array([-line_unit_vec[1], line_unit_vec[0]])
    
    # Check if the normal points to the inside of the triangle
    if np.dot(normal, triangle_center - closest_point) < 0:
        normal = -normal
    
    return distance, closest_point, normal

def is_point_in_triangle(point, triangle_vertices):
    """Check if a point is inside a triangle."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    v1, v2, v3 = triangle_vertices
    d1 = sign(point, v1, v2)
    d2 = sign(point, v2, v3)
    d3 = sign(point, v3, v1)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)

def handle_ball_triangle_collision(ball_pos, ball_radius, ball_vel, triangle_vertices):
    """Handle collision between the ball and the triangle sides."""
    collision_occurred = False
    
    # Check collision with each side of the triangle
    for i in range(3):
        v1 = triangle_vertices[i]
        v2 = triangle_vertices[(i + 1) % 3]
        
        distance, closest_point, normal = distance_point_to_line(ball_pos, v1, v2)
        
        # Collision detected
        if distance < ball_radius:
            # Reflect velocity
            ball_vel = ball_vel - 2 * np.dot(ball_vel, normal) * normal
            
            # Apply damping
            ball_vel = ball_vel * damping_factor
            
            # Maintain constant speed
            ball_vel = ball_vel * (ball_speed / np.linalg.norm(ball_vel))
            
            # Move ball away from the edge to prevent sticking
            overlap = ball_radius - distance
            ball_pos = ball_pos + normal * overlap * 1.01
            
            collision_occurred = True
            break
    
    return ball_pos, ball_vel, collision_occurred

def ensure_ball_inside_triangle(ball_pos, ball_radius, ball_vel, triangle_vertices, collision_occurred):
    """Ensure the ball stays inside the triangle."""
    if not is_point_in_triangle(ball_pos, triangle_vertices):
        # Find the closest edge
        min_distance = float('inf')
        closest_point = None
        closest_normal = None
        
        for i in range(3):
            v1 = triangle_vertices[i]
            v2 = triangle_vertices[(i + 1) % 3]
            
            distance, point, normal = distance_point_to_line(ball_pos, v1, v2)
            
            if distance < min_distance:
                min_distance = distance
                closest_point = point
                closest_normal = normal
        
        # Move ball inside triangle
        ball_pos = closest_point + closest_normal * (ball_radius + 1)
        
        # Reflect velocity if we weren't already in a collision
        if not collision_occurred:
            ball_vel = ball_vel - 2 * np.dot(ball_vel, closest_normal) * closest_normal
            
            # Apply damping
            ball_vel = ball_vel * damping_factor
            
            # Maintain constant speed
            ball_vel = ball_vel * (ball_speed / np.linalg.norm(ball_vel))
    
    return ball_pos, ball_vel

# Initialize triangle and ball
triangle_vertices = calculate_triangle_vertices(triangle_center, triangle_size, triangle_angle)
ball_pos = triangle_center.copy()  # Start at the center of the triangle

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill(WHITE)
    
    # Update triangle angle
    triangle_angle += triangle_rotation_speed
    # Calculate new triangle vertices
    triangle_vertices = calculate_triangle_vertices(triangle_center, triangle_size, triangle_angle)
    
    # Update ball position
    ball_pos += ball_vel
    
    # Handle ball-triangle collision
    ball_pos, ball_vel, collision_occurred = handle_ball_triangle_collision(ball_pos, ball_radius, ball_vel, triangle_vertices)
    
    # Ensure ball stays inside triangle
    ball_pos, ball_vel = ensure_ball_inside_triangle(ball_pos, ball_radius, ball_vel, triangle_vertices, collision_occurred)
    
    # Draw triangle with fill
    pygame.draw.polygon(screen, LIGHT_BLUE, [(v[0], v[1]) for v in triangle_vertices])
    # Draw triangle outline
    pygame.draw.polygon(screen, BLACK, [(v[0], v[1]) for v in triangle_vertices], 2)
    
    # Draw ball as a red circle (🔴)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
