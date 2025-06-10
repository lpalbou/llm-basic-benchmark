import sys
import math
import pygame

# ---------- Simple 2D vector helper functions ----------
def dot(a, b):
    return a.x * b.x + a.y * b.y

def cross(a, b):
    return a.x * b.y - a.y * b.x

# ---------- Main Program ----------
def main():
    # Initialize pygame
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ball Bouncing off Rotating Triangle")
    
    clock = pygame.time.Clock()
    FPS = 60

    # Colors (R,G,B)
    BLACK = (0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)

    # ---------- Setup initial positions ----------
    # Ball properties
    ball_pos = pygame.math.Vector2(100, 300)
    # The ball moves at a constant velocity.
    # You can change these values to alter its speed/direction.
    ball_vel = pygame.math.Vector2(0.5, 1.2)
    
    # Triangle vertices (using Vector2 objects)
    A = pygame.math.Vector2(400, 200)
    B = pygame.math.Vector2(500, 200)
    C = pygame.math.Vector2(450, 250)
    triangle_vertices = [A, B, C]
    
    # Compute the center of the triangle (average of vertices)
    center = (A + B + C) / 3
    
    # Rotation speed for the triangle in degrees per second.
    rotation_speed = 30.0  # degrees/sec

    # ---------- Main loop ----------
    running = True
    while running:
        dt_sec = clock.tick(FPS) / 1000.0  # time delta in seconds
        
        # --- Event processing ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Update triangle rotation ---
        # Increase the angle by (rotation_speed * dt_sec)
        current_angle = math.radians(rotation_speed * dt_sec)  # convert to radians
        # For each vertex, compute its rotated position about the center.
        for i in range(len(triangle_vertices)):
            # Vector from center to vertex:
            rel_pos = triangle_vertices[i] - center
            # Rotate by the current_angle (counterclockwise)
            new_x = rel_pos.x * math.cos(current_angle) - rel_pos.y * math.sin(current_angle)
            new_y = rel_pos.x * math.sin(current_angle) + rel_pos.y * math.cos(current_angle)
            triangle_vertices[i] = center + pygame.math.Vector2(new_x, new_y)

        # --- Collision detection and response ---
        # For each edge of the triangle (in CCW order), check if the ball is outside.
        # In a CCW triangle the point should satisfy:
        #    cross(edge, (ball_pos - vertex)) >= 0
        for i in range(3):
            v_current = triangle_vertices[i]
            v_next = triangle_vertices[(i+1) % 3]
            
            edge = v_next - v_current
            
            # For a CCW oriented edge, the inward normal is given by:
            #   n_inward = (-edge.y, edge.x)
            n_inward = pygame.math.Vector2(-edge.y, edge.x).normalize()
            
            # Compute the cross product between the edge and (ball_pos - v_current).
            if cross(edge, ball_pos - v_current) < 0:
                # The ball is outside this edge; reflect its velocity about n_inward.
                normal_component = dot(ball_vel, n_inward)
                tangent = ball_vel - normal_component * n_inward
                ball_vel = tangent - normal_component * n_inward
        
        # --- Update ball position ---
        ball_pos += ball_vel * dt_sec

        # Optional: if you want the ball to “wrap around” or stop at screen edges,
        # add code here. For now we simply let it bounce off only the triangle.

        # --- Drawing everything ---
        screen.fill(BLACK)
        
        # Draw the triangle (corrected: vertices as number pairs)
        pygame.draw.polygon(screen, WHITE, [(v.x, v.y) for v in triangle_vertices], 2)
        
        # Draw the ball
        pygame.draw.circle(screen, RED, (int(ball_pos.x), int(ball_pos.y)), 10)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
