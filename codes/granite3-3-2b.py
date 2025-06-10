import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices

    def rotate(self, angle):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                   [np.sin(angle),  np.cos(angle)]])
        self.vertices = np.dot(rotation_matrix, self.vertices)

class Ball:
    def __init__(self, color, position, radius):
        self.color = color
        self.position = position
        self.radius = radius

    def move(self, velocity):
        new_position = self.position + velocity
        if np.linalg.norm(new_position - self.position) <= self.radius:
            # Bounce off the triangle's edge
            self.position = new_position
        else:
            self.position += velocity

# Initialize triangle vertices
vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2)])
triangle = Triangle(vertices)

# Ball initial conditions
ball_color = 'red'
ball_position = np.array([0.5, 0])
ball_radius = 0.1
velocity = np.array([0, -0.1])

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 2)

line, = ax.plot(vertices[:, 0], vertices[:, 1], 'k-')

def update(frame):
    # Update triangle rotation
    angle += 0.05  # Rotate every frame
    triangle.rotate(angle)

    # Update ball movement
    ball.move(velocity)

    # Check for collision with triangle
    if np.linalg.norm(ball.position - triangle.vertices[0]) <= ball.radius:
        velocity = -velocity * 2  # Reverse direction upon collision

    line.set_data(triangle.vertices[:, 0], triangle.vertices[:, 1])
    ax.clear()
    ax.plot(triangle.vertices[:, 0], triangle.vertices[:, 1], 'k-')
    ball_points = plt.Circle((ball.position[0], ball.position[1]), ball.radius, color=ball_color)
    ax.add_artist(ball_points)

    return line,

# Initial setup
angle = 0

ani = FuncAnimation(fig, update, interval=20, blit=True)
plt.show()
