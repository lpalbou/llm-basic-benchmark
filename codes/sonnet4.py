import pygame
import math
import random


class Vector2D:
    """2D Vector class for position and velocity calculations."""
    
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def dot(self, other):
        """Calculate dot product with another vector."""
        return self.x * other.x + self.y * other.y
    
    def magnitude(self):
        """Calculate the magnitude of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        """Return a normalized version of the vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def to_tuple(self):
        """Convert to tuple for pygame compatibility."""
        return (self.x, self.y)


class Triangle:
    """Triangle class that handles rotation and collision detection."""
    
    def __init__(self, center, vertices, rotation_speed=30):
        self.center = Vector2D(center[0], center[1])
        self.original_vertices = [Vector2D(v[0], v[1]) for v in vertices]
        self.rotation_angle = 0
        self.rotation_speed = rotation_speed  # degrees per second
    
    def rotate(self, dt):
        """Rotate the triangle by the specified amount."""
        self.rotation_angle += self.rotation_speed * dt
        self.rotation_angle %= 360
    
    def get_rotated_vertices(self):
        """Get the current rotated vertices of the triangle."""
        angle_rad = math.radians(self.rotation_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        rotated_vertices = []
        for vertex in self.original_vertices:
            # Translate to origin
            translated = vertex - self.center
            
            # Rotate
            rotated_x = translated.x * cos_a - translated.y * sin_a
            rotated_y = translated.x * sin_a + translated.y * cos_a
            
            # Translate back
            rotated_vertex = Vector2D(rotated_x, rotated_y) + self.center
            rotated_vertices.append(rotated_vertex)
        
        return rotated_vertices
    
    def point_inside_triangle(self, point):
        """Check if a point is inside the triangle using barycentric coordinates."""
        vertices = self.get_rotated_vertices()
        v0, v1, v2 = vertices
        
        # Calculate barycentric coordinates
        denom = (v1.y - v2.y) * (v0.x - v2.x) + (v2.x - v1.x) * (v0.y - v2.y)
        if abs(denom) < 1e-10:
            return False
        
        a = ((v1.y - v2.y) * (point.x - v2.x) + (v2.x - v1.x) * (point.y - v2.y)) / denom
        b = ((v2.y - v0.y) * (point.x - v2.x) + (v0.x - v2.x) * (point.y - v2.y)) / denom
        c = 1 - a - b
        
        return a >= 0 and b >= 0 and c >= 0
    
    def get_closest_edge_and_normal(self, point):
        """Get the closest edge and its normal vector for collision detection."""
        vertices = self.get_rotated_vertices()
        min_distance = float('inf')
        closest_normal = None
        
        for i in range(3):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % 3]
            
            # Calculate edge vector and normal
            edge = v2 - v1
            normal = Vector2D(-edge.y, edge.x).normalize()
            
            # Calculate distance from point to edge
            to_point = point - v1
            distance = abs(to_point.dot(normal))
            
            if distance < min_distance:
                min_distance = distance
                closest_normal = normal
        
        return closest_normal


class Ball:
    """Ball class that handles physics and collision detection."""
    
    def __init__(self, position, velocity, radius=10):
        self.position = Vector2D(position[0], position[1])
        self.velocity = Vector2D(velocity[0], velocity[1])
        self.radius = radius
        self.color = (255, 0, 0)  # Red color
    
    def update(self, dt, triangle):
        """Update ball position and handle collisions."""
        # Update position
        self.position = self.position + self.velocity * dt
        
        # Check collision with triangle
        self.handle_collision(triangle)
    
    def handle_collision(self, triangle):
        """Handle collision with the triangle boundaries."""
        # Check if ball center is inside triangle
        if not triangle.point_inside_triangle(self.position):
            # Ball is outside, need to reflect
            normal = triangle.get_closest_edge_and_normal(self.position)
            if normal:
                # Reflect velocity
                self.velocity = self.reflect_velocity(self.velocity, normal)
                
                # Move ball back inside (simple approach)
                # Find a position inside the triangle
                center = triangle.center
                direction_to_center = (center - self.position).normalize()
                
                # Move ball towards center until it's inside
                step = 0.5
                while not triangle.point_inside_triangle(self.position):
                    self.position = self.position + direction_to_center * step
    
    def reflect_velocity(self, velocity, normal):
        """Reflect velocity vector off a surface with given normal."""
        # v_reflected = v - 2 * (v · n) * n
        dot_product = velocity.dot(normal)
        reflection = velocity - normal * (2 * dot_product)
        return reflection


class BouncingBallSimulation:
    """Main simulation class that manages the game loop."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = None
        self.clock = None
        self.running = False
        
        # Initialize game objects
        self.triangle = self._create_triangle()
        self.ball = self._create_ball()
    
    def _create_triangle(self):
        """Create a triangle in the center of the screen."""
        center = (self.width // 2, self.height // 2)
        size = 200
        
        # Create an equilateral triangle
        vertices = [
            (center[0], center[1] - size),  # Top vertex
            (center[0] - size * 0.866, center[1] + size * 0.5),  # Bottom left
            (center[0] + size * 0.866, center[1] + size * 0.5)   # Bottom right
        ]
        
        return Triangle(center, vertices, rotation_speed=30)
    
    def _create_ball(self):
        """Create a ball with random initial position and velocity."""
        # Start ball at triangle center
        center = (self.width // 2, self.height // 2)
        
        # Random initial velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 200)
        velocity = (
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        
        return Ball(center, velocity, radius=8)
    
    def initialize(self):
        """Initialize pygame and create the display."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Reset ball position and velocity
                    self.ball = self._create_ball()
    
    def update(self, dt):
        """Update all game objects."""
        self.triangle.rotate(dt)
        self.ball.update(dt, self.triangle)
    
    def render(self):
        """Render all game objects."""
        # Clear screen
        self.screen.fill((0, 0, 0))  # Black background
        
        # Draw triangle
        vertices = self.triangle.get_rotated_vertices()
        triangle_points = [v.to_tuple() for v in vertices]
        pygame.draw.polygon(self.screen, (255, 255, 255), triangle_points, 2)
        
        # Draw ball
        ball_pos = (int(self.ball.position.x), int(self.ball.position.y))
        pygame.draw.circle(self.screen, self.ball.color, ball_pos, self.ball.radius)
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        instructions = [
            "ESC: Quit",
            "SPACE: Reset ball"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text, (10, 10 + i * 30))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        self.initialize()
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()


if __name__ == "__main__":
    simulation = BouncingBallSimulation()
    simulation.run()
