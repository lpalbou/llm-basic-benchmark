import pygame
import math
from typing import List, Tuple, Optional


class Vector2D:
    """Represents a 2D vector for positions, velocities, and mathematical operations."""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def add(self, other: 'Vector2D') -> 'Vector2D':
        """Add two vectors."""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def subtract(self, other: 'Vector2D') -> 'Vector2D':
        """Subtract another vector from this one."""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def multiply(self, scalar: float) -> 'Vector2D':
        """Multiply vector by a scalar."""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def dot(self, other: 'Vector2D') -> float:
        """Calculate dot product with another vector."""
        return self.x * other.x + self.y * other.y
    
    def magnitude(self) -> float:
        """Calculate the magnitude of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self) -> 'Vector2D':
        """Return a normalized version of this vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def rotate(self, angle: float, center: 'Vector2D') -> 'Vector2D':
        """Rotate vector around a center point by given angle (radians)."""
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        
        # Translate to origin
        translated_x = self.x - center.x
        translated_y = self.y - center.y
        
        # Rotate
        rotated_x = translated_x * cos_angle - translated_y * sin_angle
        rotated_y = translated_x * sin_angle + translated_y * cos_angle
        
        # Translate back
        return Vector2D(rotated_x + center.x, rotated_y + center.y)
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to integer tuple for pygame."""
        return (int(self.x), int(self.y))


class Ball:
    """Represents the bouncing ball."""
    
    def __init__(self, position: Vector2D, velocity: Vector2D, radius: float = 10):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = (255, 0, 0)  # Red
        self.gravity = Vector2D(0, 0.5)  # Gravity acceleration
        self.damping = 0.99  # Energy loss factor
    
    def update(self, dt: float):
        """Update ball position based on velocity and gravity."""
        # Apply gravity
        self.velocity = self.velocity.add(self.gravity.multiply(dt))
        
        # Apply damping
        self.velocity = self.velocity.multiply(self.damping)
        
        # Update position
        self.position = self.position.add(self.velocity.multiply(dt))
    
    def draw(self, screen: pygame.Surface):
        """Draw the ball on the screen."""
        pygame.draw.circle(screen, self.color, self.position.to_tuple(), self.radius)
        pygame.draw.circle(screen, (150, 0, 0), self.position.to_tuple(), self.radius, 2)
    
    def set_velocity(self, velocity: Vector2D):
        """Set the ball's velocity."""
        self.velocity = velocity


class Triangle:
    """Represents the rotating triangle container."""
    
    def __init__(self, center: Vector2D, size: float = 200):
        self.center = center
        self.size = size
        self.rotation_angle = 0
        self.rotation_speed = 0.5  # Radians per second
        self.color = (100, 100, 255)
        
        # Initialize vertices (equilateral triangle)
        self._init_vertices()
    
    def _init_vertices(self):
        """Initialize triangle vertices."""
        angles = [0, 2 * math.pi / 3, 4 * math.pi / 3]
        self.base_vertices = []
        
        for angle in angles:
            x = self.center.x + self.size * math.cos(angle - math.pi / 2)
            y = self.center.y + self.size * math.sin(angle - math.pi / 2)
            self.base_vertices.append(Vector2D(x, y))
        
        self.vertices = self.base_vertices.copy()
    
    def rotate(self, dt: float):
        """Rotate the triangle."""
        self.rotation_angle += self.rotation_speed * dt
        
        # Update vertices based on rotation
        self.vertices = []
        for vertex in self.base_vertices:
            rotated = vertex.rotate(self.rotation_angle, self.center)
            self.vertices.append(rotated)
    
    def get_edges(self) -> List[Tuple[Vector2D, Vector2D]]:
        """Get the edges of the triangle."""
        edges = []
        for i in range(3):
            edges.append((self.vertices[i], self.vertices[(i + 1) % 3]))
        return edges
    
    def draw(self, screen: pygame.Surface):
        """Draw the triangle on the screen."""
        points = [v.to_tuple() for v in self.vertices]
        pygame.draw.polygon(screen, self.color, points, 3)


class CollisionHandler:
    """Handles collision detection and response between ball and triangle edges."""
    
    def __init__(self):
        self.min_distance = 0.1  # Minimum distance to consider for collision
    
    def check_ball_triangle_collision(self, ball: Ball, triangle: Triangle) -> bool:
        """Check and handle collision between ball and triangle edges."""
        collision_occurred = False
        
        # Check if ball is inside triangle
        if not self.point_in_triangle(ball.position, triangle.vertices):
            # Move ball back inside
            center = triangle.center
            direction = ball.position.subtract(center).normalize()
            ball.position = center.add(direction.multiply(triangle.size * 0.5))
            ball.velocity = ball.velocity.multiply(-0.5)
            return True
        
        # Check collision with each edge
        edges = triangle.get_edges()
        for edge_start, edge_end in edges:
            if self._check_ball_edge_collision(ball, edge_start, edge_end):
                collision_occurred = True
        
        return collision_occurred
    
    def _check_ball_edge_collision(self, ball: Ball, edge_start: Vector2D, edge_end: Vector2D) -> bool:
        """Check collision between ball and a single edge."""
        # Vector from edge start to end
        edge_vector = edge_end.subtract(edge_start)
        edge_length = edge_vector.magnitude()
        
        if edge_length == 0:
            return False
        
        edge_normal = edge_vector.normalize()
        
        # Vector from edge start to ball center
        to_ball = ball.position.subtract(edge_start)
        
        # Project to_ball onto edge
        projection_length = to_ball.dot(edge_normal)
        projection_length = max(0, min(edge_length, projection_length))
        
        # Find closest point on edge
        closest_point = edge_start.add(edge_normal.multiply(projection_length))
        
        # Check distance
        distance_vector = ball.position.subtract(closest_point)
        distance = distance_vector.magnitude()
        
        if distance < ball.radius + self.min_distance:
            # Collision detected
            self._resolve_collision(ball, distance_vector, distance)
            return True
        
        return False
    
    def _resolve_collision(self, ball: Ball, collision_normal: Vector2D, distance: float):
        """Resolve collision by reflecting velocity and adjusting position."""
        if distance == 0:
            return
        
        # Normalize collision normal
        normal = collision_normal.normalize()
        
        # Reflect velocity
        velocity_dot_normal = ball.velocity.dot(normal)
        
        if velocity_dot_normal < 0:  # Ball moving towards the edge
            # Reflect velocity
            reflected_velocity = ball.velocity.subtract(normal.multiply(2 * velocity_dot_normal))
            ball.set_velocity(reflected_velocity)
            
            # Move ball out of collision
            penetration = ball.radius - distance
            if penetration > 0:
                ball.position = ball.position.add(normal.multiply(penetration + self.min_distance))
    
    def point_in_triangle(self, point: Vector2D, vertices: List[Vector2D]) -> bool:
        """Check if a point is inside a triangle using barycentric coordinates."""
        v0 = vertices[2].subtract(vertices[0])
        v1 = vertices[1].subtract(vertices[0])
        v2 = point.subtract(vertices[0])
        
        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)
        
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        return (u >= 0) and (v >= 0) and (u + v <= 1)


class Game:
    """Main game loop and window management."""
    
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Initialize game objects
        self._init_game_objects()
    
    def _init_game_objects(self):
        """Initialize all game objects."""
        # Create triangle at center of screen
        center = Vector2D(self.width / 2, self.height / 2)
        self.triangle = Triangle(center, size=200)
        
        # Create ball at center with initial velocity
        ball_pos = Vector2D(self.width / 2, self.height / 2 - 50)
        ball_vel = Vector2D(3, 0)
        self.ball = Ball(ball_pos, ball_vel)
        
        # Create collision handler
        self.collision_handler = CollisionHandler()
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Reset ball position
                    self.ball.position = Vector2D(self.width / 2, self.height / 2 - 50)
                    self.ball.velocity = Vector2D(3, 0)
    
    def update(self, dt: float):
        """Update game state."""
        # Update triangle rotation
        self.triangle.rotate(dt)
        
        # Update ball physics
        self.ball.update(dt)
        
        # Check collisions
        self.collision_handler.check_ball_triangle_collision(self.ball, self.triangle)
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill((20, 20, 20))
        
        # Draw triangle
        self.triangle.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to reset, ESC to quit", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        # Update display
        pygame.display.flip()


def main():
    """Entry point of the application."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
