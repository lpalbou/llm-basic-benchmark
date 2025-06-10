import pygame
import math
import sys


class Vector2D:
    """Represents a 2D vector with x and y components."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, other):
        """Add two vectors."""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def subtract(self, other):
        """Subtract another vector from this one."""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def multiply(self, scalar):
        """Multiply vector by a scalar."""
        return Vector2D(self.x * scalar, self.y * scalar)
    
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
    
    def rotate(self, angle, center):
        """Rotate the vector around a center point by the given angle (in radians)."""
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
    
    def to_tuple(self):
        """Convert to tuple for pygame functions."""
        return (int(self.x), int(self.y))


class Ball:
    """Represents a bouncing ball with position, velocity, and radius."""
    
    def __init__(self, position, velocity, radius=10, color=(255, 0, 0)):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color
    
    def update_position(self, dt):
        """Update ball position based on velocity and time delta."""
        self.position = self.position.add(self.velocity.multiply(dt))
    
    def bounce(self, normal):
        """Reflect velocity off a surface with given normal vector."""
        # v_new = v - 2 * (v · n) * n
        dot_product = self.velocity.dot(normal)
        reflection = normal.multiply(2 * dot_product)
        self.velocity = self.velocity.subtract(reflection)
    
    def draw(self, screen):
        """Draw the ball on the screen."""
        pygame.draw.circle(screen, self.color, self.position.to_tuple(), self.radius)


class Triangle:
    """Represents a rotating triangle defined by three vertices."""
    
    def __init__(self, vertices, rotation_speed=0.5):
        self.vertices = vertices
        self.rotation_angle = 0
        self.rotation_speed = rotation_speed  # radians per second
        self.center = self._calculate_center()
    
    def _calculate_center(self):
        """Calculate the centroid of the triangle."""
        x = sum(v.x for v in self.vertices) / 3
        y = sum(v.y for v in self.vertices) / 3
        return Vector2D(x, y)
    
    def rotate(self, dt):
        """Rotate the triangle by rotation_speed * dt."""
        angle_delta = self.rotation_speed * dt
        self.rotation_angle += angle_delta
        
        # Rotate each vertex around the center
        for i in range(len(self.vertices)):
            self.vertices[i] = self.vertices[i].rotate(angle_delta, self.center)
    
    def get_edges(self):
        """Return the three edges of the triangle as pairs of vertices."""
        edges = []
        for i in range(3):
            edges.append((self.vertices[i], self.vertices[(i + 1) % 3]))
        return edges
    
    def draw(self, screen):
        """Draw the triangle on the screen."""
        points = [v.to_tuple() for v in self.vertices]
        pygame.draw.polygon(screen, (255, 255, 255), points, 3)


class CollisionDetector:
    """Static methods for collision detection and response."""
    
    @staticmethod
    def point_to_line_distance(point, line_start, line_end):
        """Calculate the shortest distance from a point to a line segment."""
        line_vec = line_end.subtract(line_start)
        point_vec = point.subtract(line_start)
        line_length = line_vec.magnitude()
        
        if line_length == 0:
            return point_vec.magnitude()
        
        # Project point onto line
        t = max(0, min(1, point_vec.dot(line_vec) / (line_length ** 2)))
        projection = line_start.add(line_vec.multiply(t))
        
        return point.subtract(projection).magnitude()
    
    @staticmethod
    def get_line_normal(line_start, line_end):
        """Get the outward-pointing normal vector of a line."""
        line_vec = line_end.subtract(line_start)
        # Rotate 90 degrees counter-clockwise for outward normal
        normal = Vector2D(-line_vec.y, line_vec.x)
        return normal.normalize()
    
    @staticmethod
    def check_ball_triangle_collision(ball, triangle):
        """Check if ball collides with any edge of the triangle and handle collision."""
        edges = triangle.get_edges()
        
        for edge in edges:
            distance = CollisionDetector.point_to_line_distance(
                ball.position, edge[0], edge[1]
            )
            
            if distance <= ball.radius:
                # Calculate normal vector pointing away from the edge
                edge_normal = CollisionDetector.get_line_normal(edge[0], edge[1])
                
                # Check if ball is on the correct side of the edge
                # by checking if it's inside the triangle
                if CollisionDetector.is_ball_escaping_triangle(ball, triangle, edge_normal):
                    # Reflect the velocity
                    ball.bounce(edge_normal)
                    
                    # Move ball away from edge to prevent sticking
                    push_distance = ball.radius - distance + 1
                    ball.position = ball.position.add(edge_normal.multiply(push_distance))
    
    @staticmethod
    def is_ball_escaping_triangle(ball, triangle, edge_normal):
        """Check if the ball is trying to escape the triangle."""
        # If velocity is pointing in the same direction as the normal,
        # the ball is trying to escape
        return ball.velocity.dot(edge_normal) > 0
    
    @staticmethod
    def is_point_in_triangle(point, triangle):
        """Check if a point is inside the triangle using barycentric coordinates."""
        v0 = triangle.vertices[0]
        v1 = triangle.vertices[1]
        v2 = triangle.vertices[2]
        
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
        
        d1 = sign(point, v0, v1)
        d2 = sign(point, v1, v2)
        d3 = sign(point, v2, v0)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)


class Game:
    """Main game class that manages the game loop and all objects."""
    
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game objects
        self._initialize_objects()
    
    def _initialize_objects(self):
        """Initialize the ball and triangle."""
        # Create triangle vertices (equilateral triangle)
        center_x, center_y = self.width // 2, self.height // 2
        size = 200
        vertices = []
        for i in range(3):
            angle = i * 2 * math.pi / 3 - math.pi / 2
            x = center_x + size * math.cos(angle)
            y = center_y + size * math.sin(angle)
            vertices.append(Vector2D(x, y))
        
        self.triangle = Triangle(vertices, rotation_speed=0.5)
        
        # Create ball at center with initial velocity
        ball_pos = Vector2D(center_x, center_y)
        ball_vel = Vector2D(200, 150)  # pixels per second
        self.ball = Ball(ball_pos, ball_vel, radius=8)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        """Update all game objects."""
        # Update ball position
        self.ball.update_position(dt)
        
        # Rotate triangle
        self.triangle.rotate(dt)
        
        # Check for collisions
        CollisionDetector.check_ball_triangle_collision(self.ball, self.triangle)
    
    def draw(self):
        """Draw all game objects."""
        self.screen.fill((0, 0, 0))  # Clear screen with black
        
        # Draw triangle
        self.triangle.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point of the program."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
