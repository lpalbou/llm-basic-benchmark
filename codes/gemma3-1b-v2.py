import pygame
import math
import numpy as np

# Define colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Triangle parameters
base_radius = 1
height_radius = 0.5
triangle_size = 2.5

# Ball parameters
ball_radius = 0.5
ball_x = 0
ball_y = 0
ball_speed = 2

# Ball class
class Ball:
    def __init__(self, x, y, ball_radius, ball_speed):
        self.x = x
        self.y = y
        self.ball_radius = ball_radius
        self.ball_speed = ball_speed

    def update(self, time):
        # Simple movement - update position based on time
        self.x += self.ball_speed * time

    def rotate(self, angle):
        # Rotate the ball around the Y axis
        self.y += angle

# Function to create the triangle
def create_triangle(size):
    """Creates a triangle of specified size."""
    vertices = np.array([
        [0, 0, 0],
        [size, 0, 0],
        [size, size, 0]
    ])
    return vertices


# Function to draw the triangle
def draw_triangle(screen, vertices):
    """Draws the triangle on the screen."""
    pygame.draw.polygon(screen, WHITE, vertices)

# Function to rotate the triangle
def rotate_triangle(screen, triangle, angle):
    """Rotates the triangle based on the given angle."""
    rotated_triangle = np.array(triangle)
    rotated_triangle = np.rot90(rotated_triangle, k=angle)
    
    # Set the triangle's position
    rotated_triangle = np.array(rotated_triangle)
    
    pygame.draw.polygon(screen, RED, rotated_triangle)


# Function to update the screen
def update_screen(screen, ball, triangle, time):
    """Updates the screen with the current state of the ball and triangle."""
    
    # Clear the screen
    screen.fill(BLACK)

    # Draw the triangle
    draw_triangle(screen, triangle)

    # Update the ball's position
    ball.update(time)

    # Rotate the triangle
    rotate_triangle(screen, triangle, time)  #Call the rotation function

    # Draw a red line to show the ball moving
    pygame.draw.line(screen, RED, (ball.x, ball.y), (ball.x, ball.y), 1)

    # Display the time
    text_x = 10
    text_y = 10
    text_color = (0, 0, 0)
    font = pygame.font.Font(None, 36)
    text = text_color + "Time: " + str(time) + "\n"
    font_size = 20
    text_rect = (text_x, text_y, text_size, font_size)
    screen.blit(text, text_rect)


# --- Main execution ---
if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((600, 400))
    running = True
    clock = pygame.time.Clock()

    # Create the triangle
    triangle = create_triangle(100)  # Size of the triangle

    # Initialize the ball
    ball = Ball(0, 0, ball_radius, ball_speed)

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_screen(screen, ball, triangle, 1/60)  # Update every 60 frames (adjust this)

        clock.tick(60)  # Limit frame rate to 60 frames per second

    pygame.quit()