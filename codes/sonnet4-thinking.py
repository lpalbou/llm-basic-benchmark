import pygame
import math
import sys
from typing import List, Tuple, Optional


class Vector2D:
    """2D Vector class for position and velocity calculations."""
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector2D':
        return self.__mul__(scalar)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self) -> 'Vector2D':
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def dot(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y
    
    def rotate(self, angle: float) -> 'Vector2D':
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


class Ball:
    """Represents a bouncing ball with physics."""
    
    def __init__(self, position: Vector2D, velocity: Vector2D, radius: float = 10.0):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = (255, 0, 0)  # Red color
    
    def update(self) -> None:
        """Update ball position based on velocity."""
        self.position = self.position + self.velocity
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ball on the screen."""
        pygame.draw.circle(
            screen, 
            self.color, 
            (int(self.position.x), int(self.position.y)), 
            int(self.radius)
        )
    
    def bounce_off_edge(self, edge_start: Vector2D, edge_end: Vector2D) -> None:
        """Handle collision with a triangle edge."""
        # Calculate edge vector and normal
        edge_vector = edge_end - edge_start
        edge_normal = Vector2D(-edge_vector.y, edge_vector.x).normalize()
        
        # Ensure normal points inward (toward triangle center)
        # We'll handle this in the collision detection logic
        
        # Reflect velocity: v' = v - 2(v·n)n
        dot_product = self.velocity.dot(edge_normal)
        self.velocity = self.velocity - edge_normal * (2 * dot_product)
        
        # Move ball slightly away from edge to prevent getting stuck
        self.position = self.position + edge_normal * 2


class Triangle:
    """Represents a rotating triangle boundary."""
    
    def __init__(self, center: Vector2D, size: float = 200.0):
        self.center = center
        self.size = size
        self.rotation = 0.0
        self.rotation_speed = 0.01  # Radians per frame
        self.color = (255, 255, 255)  # White color
        
        # Initial vertices (equilateral triangle)
        self.base_vertices = [
            Vector2D(0, -size * 2/3),  # Top vertex
            Vector2D(-size * math.sqrt(3)/2, size/3),  # Bottom left
            Vector2D(size * math.sqrt(3)/2, size/3)   # Bottom right
        ]
        self.vertices = self.base_vertices.copy()
        self._update_vertices()
    
    def update(self) -> None:
        """Update triangle rotation and vertex positions."""
        self.rotation += self.rotation_speed
        self._update_vertices()
    
    def _update_vertices(self) -> None:
        """Update vertex positions based on current rotation."""
        self.vertices = []
        for base_vertex in self.base_vertices:
            rotated_vertex = base_vertex.rotate(self.rotation)
            world_vertex = self.center + rotated_vertex
            self.vertices.append(world_vertex)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the triangle outline."""
        if len(self.vertices) >= 3:
            points = [vertex.to_tuple() for vertex in self.vertices]
            pygame.draw.polygon(screen, self.color, points, 2)
    
    def get_edges(self) -> List[Tuple[Vector2D, Vector2D]]:
        """Return list of triangle edges as (start, end) pairs."""
        edges = []
        for i in range(len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % len(self.vertices)]
            edges.append((start, end))
        return edges
    
    def point_inside(self, point: Vector2D) -> bool:
        """Check if a point is inside the triangle using barycentric coordinates."""
        v0 = self.vertices[2] - self.vertices[0]
        v1 = self.vertices[1] - self.vertices[0]
        v2 = point - self.vertices[0]
        
        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)
        
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        return (u >= 0) and (v >= 0) and (u + v <= 1)
    
    def get_closest_edge(self, point: Vector2D) -> Tuple[Vector2D, Vector2D]:
        """Find the closest edge to a given point."""
        min_distance = float('inf')
        closest_edge = None
        
        for edge_start, edge_end in self.get_edges():
            distance = self._point_to_line_distance(point, edge_start, edge_end)
            if distance < min_distance:
                min_distance = distance
                closest_edge = (edge_start, edge_end)
        
        return closest_edge
    
    def _point_to_line_distance(self, point: Vector2D, line_start: Vector2D, line_end: Vector2D) -> float:
        """Calculate the shortest distance from a point to a line segment."""
        line_vec = line_end - line_start
        point_vec = point - line_start
        
        line_len_sq = line_vec.dot(line_vec)
        if line_len_sq == 0:
            return (point - line_start).magnitude()
        
        t = max(0, min(1, point_vec.dot(line_vec) / line_len_sq))
        projection = line_start + line_vec * t
        return (point - projection).magnitude()


class BouncingBallGame:
    """Main game class that manages the bouncing ball simulation."""
    
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game objects
        triangle_center = Vector2D(width // 2, height // 2)
        self.triangle = Triangle(triangle_center, 180)
        
        ball_position = Vector2D(width // 2, height // 2 - 50)
        ball_velocity = Vector2D(3, 2)
        self.ball = Ball(ball_position, ball_velocity, 8)
        
        self.background_color = (0, 0, 0)  # Black background
    
    def handle_events(self) -> None:
        """Process pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self) -> None:
        """Update all game objects and handle collisions."""
        # Update triangle rotation
        self.triangle.update()
        
        # Update ball position
        self.ball.update()
        
        # Check for collision with triangle
        self._handle_triangle_collision()
    
    def _handle_triangle_collision(self) -> None:
        """Handle collision between ball and triangle edges."""
        # Check if ball center is outside triangle
        if not self.triangle.point_inside(self.ball.position):
            # Find closest edge and bounce off it
            closest_edge = self.triangle.get_closest_edge(self.ball.position)
            if closest_edge:
                edge_start, edge_end = closest_edge
                
                # Calculate edge normal pointing inward
                edge_vector = edge_end - edge_start
                edge_normal = Vector2D(-edge_vector.y, edge_vector.x).normalize()
                
                # Ensure normal points toward triangle center
                to_center = self.triangle.center - self.ball.position
                if edge_normal.dot(to_center) < 0:
                    edge_normal = edge_normal * -1
                
                # Reflect velocity
                dot_product = self.ball.velocity.dot(edge_normal)
                self.ball.velocity = self.ball.velocity - edge_normal * (2 * dot_product)
                
                # Move ball back inside triangle
                self.ball.position = self.ball.position + edge_normal * 3
    
    def draw(self) -> None:
        """Render all game objects."""
        self.screen.fill(self.background_color)
        self.triangle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the bouncing ball game."""
    game = BouncingBallGame()
    game.run()


if __name__ == "__main__":
    main()
