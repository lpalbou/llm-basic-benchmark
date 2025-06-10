"""Bouncing red ball confined within a rotating triangle simulation."""

import pygame
import math
from typing import List, Tuple, Optional


class Vector2D:
    """Represents a 2D vector with x and y components."""
    
    def __init__(self, x: float, y: float):
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
    
    def dot(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y
    
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self) -> 'Vector2D':
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def rotate(self, angle: float) -> 'Vector2D':
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        new_x = self.x * cos_angle - self.y * sin_angle
        new_y = self.x * sin_angle + self.y * cos_angle
        return Vector2D(new_x, new_y)
    
    def perpendicular(self) -> 'Vector2D':
        return Vector2D(-self.y, self.x)
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def to_int_tuple(self) -> Tuple[int, int]:
        return (int(self.x), int(self.y))


class Ball:
    """Represents the bouncing ball."""
    
    def __init__(self, position: Vector2D, velocity: Vector2D, radius: float = 10):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = (255, 0, 0)  # Red
        self.damping = 0.999  # Slight energy loss
        self.gravity = Vector2D(0, 500)  # Gravity acceleration
    
    def update(self, dt: float):
        """Update ball position and apply physics."""
        # Apply gravity
        self.velocity = self.velocity + self.gravity * dt
        
        # Apply damping
        self.velocity = self.velocity * self.damping
        
        # Update position
        self.position = self.position + self.velocity * dt
    
    def draw(self, screen):
        """Draw the ball on the screen."""
        pygame.draw.circle(screen, self.color, self.position.to_int_tuple(), self.radius)
    
    def bounce(self, normal: Vector2D):
        """Bounce off a surface with given normal."""
        # Reflection formula: v' = v - 2(v·n)n
        normal = normal.normalize()
        dot_product = self.velocity.dot(normal)
        if dot_product < 0:  # Only bounce if moving towards the surface
            self.velocity = self.velocity - normal * (2 * dot_product)
            # Add some energy loss on bounce
            self.velocity = self.velocity * 0.9


class Triangle:
    """Represents the rotating triangle container."""
    
    def __init__(self, center: Vector2D, size: float):
        self.center = center
        self.size = size
        self.rotation_angle = 0.0
        self.rotation_speed = 0.5  # Radians per second
        
        # Create initial triangle vertices (equilateral triangle)
        self.base_vertices = []
        for i in range(3):
            angle = (2 * math.pi * i / 3) - math.pi / 2  # Start with point at top
            vertex = Vector2D(
                size * math.cos(angle),
                size * math.sin(angle)
            )
            self.base_vertices.append(vertex)
    
    def update(self, dt: float):
        """Update triangle rotation."""
        self.rotation_angle += self.rotation_speed * dt
    
    def get_vertices(self) -> List[Vector2D]:
        """Get current rotated vertices."""
        vertices = []
        for base_vertex in self.base_vertices:
            rotated = base_vertex.rotate(self.rotation_angle)
            vertices.append(self.center + rotated)
        return vertices
    
    def get_edges(self) -> List[Tuple[Vector2D, Vector2D]]:
        """Get the edges of the triangle."""
        vertices = self.get_vertices()
        edges = []
        for i in range(3):
            start = vertices[i]
            end = vertices[(i + 1) % 3]
            edges.append((start, end))
        return edges
    
    def draw(self, screen):
        """Draw the triangle on the screen."""
        vertices = self.get_vertices()
        points = [v.to_int_tuple() for v in vertices]
        pygame.draw.polygon(screen, (255, 255, 255), points, 3)  # White outline


class CollisionDetector:
    """Handles collision detection between ball and triangle."""
    
    @staticmethod
    def point_to_line_distance(point: Vector2D, line_start: Vector2D, line_end: Vector2D) -> Tuple[float, Vector2D]:
        """Calculate distance from point to line segment and closest point."""
        line_vec = line_end - line_start
        point_vec = point - line_start
        line_length_sq = line_vec.dot(line_vec)
        
        if line_length_sq == 0:
            # Line start and end are the same
            return point.distance_to(line_start), line_start
        
        # Project point onto line
        t = max(0, min(1, point_vec.dot(line_vec) / line_length_sq))
        closest_point = line_start + line_vec * t
        distance = point.distance_to(closest_point)
        
        return distance, closest_point
    
    @staticmethod
    def check_ball_triangle_collision(ball: Ball, triangle: Triangle) -> Optional[Vector2D]:
        """Check and handle collision between ball and triangle edges."""
        edges = triangle.get_edges()
        
        for start, end in edges:
            distance, closest_point = CollisionDetector.point_to_line_distance(
                ball.position, start, end
            )
            
            if distance < ball.radius:
                # Collision detected, calculate normal
                normal = (ball.position - closest_point).normalize()
                
                # Move ball outside of edge
                penetration = ball.radius - distance
                ball.position = ball.position + normal * penetration
                
                return normal
        
        return None


class Game:
    """Main game class managing the simulation."""
    
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create triangle at center of screen
        center = Vector2D(width / 2, height / 2)
        self.triangle = Triangle(center, 200)
        
        # Create ball at center with random initial velocity
        self.ball = Ball(
            position=Vector2D(width / 2, height / 2),
            velocity=Vector2D(200, -150)
        )
        
        self.collision_detector = CollisionDetector()
        
        # Background color
        self.bg_color = (0, 0, 0)  # Black
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Reset ball position and give random velocity
                    self.ball.position = Vector2D(self.width / 2, self.height / 2)
                    import random
                    self.ball.velocity = Vector2D(
                        random.uniform(-300, 300),
                        random.uniform(-300, 300)
                    )
    
    def update(self, dt: float):
        """Update game state."""
        # Update triangle rotation
        self.triangle.update(dt)
        
        # Update ball physics
        self.ball.update(dt)
        
        # Check collisions
        normal = self.collision_detector.check_ball_triangle_collision(
            self.ball, self.triangle
        )
        if normal:
            self.ball.bounce(normal)
    
    def render(self):
        """Render the game."""
        self.screen.fill(self.bg_color)
        
        # Draw triangle
        self.triangle.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to reset ball", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()


def main():
    """Entry point of the program."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
