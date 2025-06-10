import pygame
import sys
import math
import numpy as np

class Triangle:
    def __init__(self, center, size):
        """
        Initialize a triangle with a center point and size
        
        Args:
            center (tuple): (x, y) coordinates of the center
            size (float): Size of the triangle
        """
        self.center = center
        self.size = size
        self.rotation_angle = 0
        self.rotation_speed = 0.5  # degrees per frame
        
        # Initial vertices - equilateral triangle
        self.base_vertices = [
            (0, -size),  # Top
            (-size * math.sqrt(3)/2, size/2),  # Bottom left
            (size * math.sqrt(3)/2, size/2)   # Bottom right
        ]
        
        # Calculate initial vertices positions
        self.vertices = self._calculate_vertices()
        
    def _calculate_vertices(self):
        """Calculate the vertices based on current rotation"""
        vertices = []
        
        for x, y in self.base_vertices:
            # Apply rotation
            x_rot = x * math.cos(math.radians(self.rotation_angle)) - y * math.sin(math.radians(self.rotation_angle))
            y_rot = x * math.sin(math.radians(self.rotation_angle)) + y * math.cos(math.radians(self.rotation_angle))
            
            # Apply translation
            vertices.append((x_rot + self.center[0], y_rot + self.center[1]))
            
        return vertices
    
    def update(self):
        """Update the triangle rotation"""
        self.rotation_angle += self.rotation_speed
        if self.rotation_angle >= 360:
            self.rotation_angle -= 360
            
        # Recalculate vertices after rotation
        self.vertices = self._calculate_vertices()
    
    def draw(self, screen):
        """
        Draw the triangle on the screen
        
        Args:
            screen: Pygame screen object
        """
        pygame.draw.polygon(screen, (255, 255, 255), self.vertices, 2)
    
    def get_lines(self):
        """
        Return the three lines of the triangle as pairs of points
        
        Returns:
            list: Three lines [(p1, p2), (p2, p3), (p3, p1)]
        """
        v = self.vertices
        return [(v[0], v[1]), (v[1], v[2]), (v[2], v[0])]
    
    def is_point_inside(self, point):
        """
        Check if a point is inside the triangle using barycentric coordinates
        
        Args:
            point (tuple): (x, y) coordinates to check
            
        Returns:
            bool: True if point is inside the triangle
        """
        # Convert to numpy arrays for vector operations
        v0 = np.array(self.vertices[0])
        v1 = np.array(self.vertices[1])
        v2 = np.array(self.vertices[2])
        p = np.array(point)
        
        # Compute vectors
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        v0p = p - v0
        
        # Compute dot products
        dot00 = np.dot(v0v1, v0v1)
        dot01 = np.dot(v0v1, v0v2)
        dot02 = np.dot(v0v1, v0p)
        dot11 = np.dot(v0v2, v0v2)
        dot12 = np.dot(v0v2, v0p)
        
        # Compute barycentric coordinates
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        # Check if point is inside triangle
        return (u >= 0) and (v >= 0) and (u + v <= 1)


class Ball:
    def __init__(self, position, radius, velocity):
        """
        Initialize a ball with position, radius and velocity
        
        Args:
            position (tuple): (x, y) coordinates
            radius (float): Radius of the ball
            velocity (tuple): (vx, vy) velocity components
        """
        self.position = list(position)
        self.radius = radius
        self.velocity = list(velocity)
        self.color = (255, 0, 0)  # Red color
    
    def update(self, triangle):
        """
        Update the ball position and handle collisions with the triangle
        
        Args:
            triangle (Triangle): Triangle object for collision detection
        """
        # Store previous position
        prev_position = self.position.copy()
        
        # Update position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Check if the new position is inside the triangle
        if not triangle.is_point_inside((self.position[0], self.position[1])):
            # Find the closest intersection with the triangle sides
            lines = triangle.get_lines()
            min_distance = float('inf')
            intersection_point = None
            normal = None
            
            for line in lines:
                p1, p2 = line
                
                # Calculate the normal to the line (perpendicular)
                line_vector = (p2[0] - p1[0], p2[1] - p1[1])
                line_normal = (-line_vector[1], line_vector[0])
                line_normal_length = math.sqrt(line_normal[0]**2 + line_normal[1]**2)
                line_normal = (line_normal[0]/line_normal_length, line_normal[1]/line_normal_length)
                
                # Get intersection point
                # Line equation: p = p1 + t*(p2-p1)
                # Ray equation: r = prev_position + s*velocity
                
                # Convert to numpy for easier calculation
                p1_np = np.array(p1)
                p2_np = np.array(p2)
                prev_np = np.array(prev_position)
                vel_np = np.array(self.velocity)
                
                # Calculate intersection
                v1 = prev_np - p1_np
                v2 = p2_np - p1_np
                v3 = np.array([-vel_np[1], vel_np[0]])
                
                # Check if lines are parallel
                dot_product = np.dot(v2, v3)
                if abs(dot_product) < 1e-6:
                    continue
                
                t1 = np.cross(v1, v3) / dot_product
                t2 = np.dot(v1, v2) / dot_product
                
                # Check if intersection is on the line segment and in the direction of velocity
                if 0 <= t1 <= 1 and t2 >= 0:
                    intersection = p1_np + t1 * v2
                    dist = np.linalg.norm(intersection - prev_np)
                    
                    if dist < min_distance:
                        min_distance = dist
                        intersection_point = intersection
                        normal = line_normal
            
            if intersection_point is not None and normal is not None:
                # Place the ball at the intersection point
                self.position = intersection_point.tolist()
                
                # Reflect velocity based on the normal
                dot_product = self.velocity[0] * normal[0] + self.velocity[1] * normal[1]
                self.velocity[0] -= 2 * dot_product * normal[0]
                self.velocity[1] -= 2 * dot_product * normal[1]
                
                # Add a small correction to avoid getting stuck
                self.position[0] += self.velocity[0] * 0.1
                self.position[1] += self.velocity[1] * 0.1
            else:
                # If no intersection found, just revert to previous position
                self.position = prev_position
                self.velocity[0] *= -1
                self.velocity[1] *= -1
    
    def draw(self, screen):
        """
        Draw the ball on the screen
        
        Args:
            screen: Pygame screen object
        """
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)


class Simulation:
    def __init__(self, width, height):
        """
        Initialize the simulation environment
        
        Args:
            width (int): Screen width
            height (int): Screen height
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Create triangle
        triangle_size = min(width, height) / 3
        self.triangle = Triangle((width // 2, height // 2), triangle_size)
        
        # Create ball inside the triangle
        ball_radius = 10
        self.ball = Ball(
            (width // 2, height // 2),  # Start at center
            ball_radius,
            (3, 4)  # Initial velocity
        )
    
    def run(self):
        """Run the main simulation loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update
            self.triangle.update()
            self.ball.update(self.triangle)
            
            # Draw
            self.screen.fill((0, 0, 0))
            self.triangle.draw(self.screen)
            self.ball.draw(self.screen)
            
            # Refresh display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    pygame.init()
    simulation = Simulation(800, 600)
    simulation.run()
