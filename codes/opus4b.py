import pygame
import math
import sys

class Vector2D:
    """2D Vector class for position and velocity calculations"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2D(self.x / mag, self.y / mag)
        return Vector2D(0, 0)
    
    def rotate(self, angle):
        """Rotate vector by angle (in radians)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def to_tuple(self):
        return (int(self.x), int(self.y))


class Ball:
    """Ball class with physics properties"""
    
    def __init__(self, position, velocity, radius=10):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = (255, 0, 0)  # Red
        self.gravity = Vector2D(0, 0.3)
        self.damping = 0.98
    
    def update(self):
        """Update ball position and apply physics"""
        self.velocity = self.velocity + self.gravity
        self.velocity = self.velocity * self.damping
        self.position = self.position + self.velocity
    
    def draw(self, screen):
        """Draw the ball on the screen"""
        pygame.draw.circle(screen, self.color, self.position.to_tuple(), self.radius)
        pygame.draw.circle(screen, (139, 0, 0), self.position.to_tuple(), self.radius, 2)


class Triangle:
    """Triangle class with rotation and collision detection"""
    
    def __init__(self, center, size=200):
        self.center = center
        self.size = size
        self.rotation = 0
        self.rotation_speed = 0.01
        self.color = (255, 255, 255)
        
        # Create equilateral triangle vertices
        self.base_vertices = []
        for i in range(3):
            angle = i * 2 * math.pi / 3 - math.pi / 2
            vertex = Vector2D(
                size * math.cos(angle),
                size * math.sin(angle)
            )
            self.base_vertices.append(vertex)
    
    def get_vertices(self):
        """Get current rotated vertices"""
        vertices = []
        for vertex in self.base_vertices:
            rotated = vertex.rotate(self.rotation)
            vertices.append(self.center + rotated)
        return vertices
    
    def rotate_triangle(self):
        """Apply rotation to the triangle"""
        self.rotation += self.rotation_speed
    
    def get_edges(self):
        """Get triangle edges as pairs of vertices"""
        vertices = self.get_vertices()
        edges = []
        for i in range(3):
            edges.append((vertices[i], vertices[(i + 1) % 3]))
        return edges
    
    def point_to_line_distance(self, point, line_start, line_end):
        """Calculate distance from point to line segment"""
        line_vec = line_end - line_start
        point_vec = point - line_start
        line_len = line_vec.magnitude()
        
        if line_len == 0:
            return point_vec.magnitude()
        
        line_unitvec = line_vec.normalize()
        proj_length = point_vec.dot(line_unitvec)
        
        if proj_length < 0:
            return point_vec.magnitude()
        elif proj_length > line_len:
            return (point - line_end).magnitude()
        else:
            proj_point = line_start + line_unitvec * proj_length
            return (point - proj_point).magnitude()
    
    def get_edge_normal(self, edge_start, edge_end):
        """Get normal vector for an edge"""
        edge_vec = edge_end - edge_start
        # Perpendicular vector (rotate 90 degrees)
        normal = Vector2D(-edge_vec.y, edge_vec.x)
        return normal.normalize()
    
    def check_collision(self, ball):
        """Check if ball collides with triangle edges"""
        edges = self.get_edges()
        
        for edge_start, edge_end in edges:
            distance = self.point_to_line_distance(ball.position, edge_start, edge_end)
            
            if distance <= ball.radius:
                # Get edge normal pointing inward
                normal = self.get_edge_normal(edge_start, edge_end)
                
                # Check if normal points toward center (inward)
                to_center = self.center - edge_start
                if normal.dot(to_center) < 0:
                    normal = normal * -1
                
                return True, normal
        
        return False, None
    
    def reflect_velocity(self, velocity, normal):
        """Reflect velocity vector based on normal"""
        # v' = v - 2(v·n)n
        dot_product = velocity.dot(normal)
        reflected = velocity - normal * (2 * dot_product)
        return reflected * 0.8  # Energy loss on collision
    
    def is_point_inside(self, point):
        """Check if point is inside triangle using barycentric coordinates"""
        vertices = self.get_vertices()
        v0 = vertices[2] - vertices[0]
        v1 = vertices[1] - vertices[0]
        v2 = point - vertices[0]
        
        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)
        
        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        
        return (u >= 0) and (v >= 0) and (u + v <= 1)
    
    def constrain_ball(self, ball):
        """Keep ball inside triangle after rotation"""
        if not self.is_point_inside(ball.position):
            # Find closest edge and push ball inside
            edges = self.get_edges()
            min_distance = float('inf')
            closest_edge = None
            
            for edge in edges:
                distance = self.point_to_line_distance(ball.position, edge[0], edge[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_edge = edge
            
            if closest_edge:
                normal = self.get_edge_normal(closest_edge[0], closest_edge[1])
                to_center = self.center - closest_edge[0]
                if normal.dot(to_center) < 0:
                    normal = normal * -1
                
                # Push ball inside
                push_distance = ball.radius - min_distance + 5
                ball.position = ball.position + normal * push_distance
    
    def draw(self, screen):
        """Draw the triangle"""
        vertices = self.get_vertices()
        points = [v.to_tuple() for v in vertices]
        pygame.draw.polygon(screen, self.color, points, 3)


class BouncingBallSimulation:
    """Main simulation class"""
    
    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bouncing Ball in Rotating Triangle")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create triangle and ball
        triangle_center = Vector2D(width // 2, height // 2)
        self.triangle = Triangle(triangle_center)
        
        # Start ball in center with random velocity
        ball_pos = Vector2D(width // 2, height // 2 - 50)
        ball_vel = Vector2D(3, -2)
        self.ball = Ball(ball_pos, ball_vel)
        
        # Background color
        self.bg_color = (30, 30, 30)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Reset ball position and velocity
                    self.ball.position = Vector2D(self.width // 2, self.height // 2 - 50)
                    self.ball.velocity = Vector2D(3, -2)
    
    def update(self):
        """Update simulation state"""
        # Rotate triangle
        self.triangle.rotate_triangle()
        
        # Update ball physics
        self.ball.update()
        
        # Check collision with triangle edges
        collision, normal = self.triangle.check_collision(self.ball)
        if collision:
            # Reflect velocity
            self.ball.velocity = self.triangle.reflect_velocity(self.ball.velocity, normal)
            
            # Push ball out of collision
            self.ball.position = self.ball.position + normal * 2
        
        # Ensure ball stays inside triangle after rotation
        self.triangle.constrain_ball(self.ball)
    
    def draw(self):
        """Draw everything on screen"""
        self.screen.fill(self.bg_color)
        
        # Draw triangle
        self.triangle.draw(self.screen)
        
        # Draw ball
        self.ball.draw(self.screen)
        
        # Draw instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to reset, ESC to quit", True, (200, 200, 200))
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    simulation = BouncingBallSimulation()
    simulation.run()
