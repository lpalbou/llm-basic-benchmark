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
        
        # Create initial triangle vertic
