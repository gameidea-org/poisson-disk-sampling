import pygame
import random
import math

# Pygame setup
pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poisson Disc Sampling using Bridson's Algorithm")
clock = pygame.time.Clock()

# Parameters for Poisson disc sampling
RADIUS = 8
K = 30 # Number of samples to choose before rejection in the algorithm
GRID_SIZE = RADIUS / math.sqrt(2)

# Create a grid to store points
cols, rows = int(WIDTH / GRID_SIZE) + 1, int(HEIGHT / GRID_SIZE) + 1

def initialize_grid():
    return [[None for _ in range(rows)] for _ in range(cols)]

grid = initialize_grid()

# List to store active points
active = []
points = []

# Helper functions
def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def generate_point_around(point):
    r = RADIUS * (random.random() + 1)
    angle = 2 * math.pi * random.random()
    new_x = point[0] + r * math.cos(angle)
    new_y = point[1] + r * math.sin(angle)
    return new_x, new_y

def in_bounds(point):
    return 0 <= point[0] < WIDTH and 0 <= point[1] < HEIGHT

def fits(point):
    col = int(point[0] / GRID_SIZE)
    row = int(point[1] / GRID_SIZE)
    for i in range(max(col - 2, 0), min(col + 3, cols)):
        for j in range(max(row - 2, 0), min(row + 3, rows)):
            neighbor = grid[i][j]
            if neighbor is not None and distance(point, neighbor) < RADIUS:
                return False
    return True

def restart_simulation(start_point):
    global grid, active, points
    grid = initialize_grid()
    points = [start_point]
    active = [start_point]
    col = int(start_point[0] / GRID_SIZE)
    row = int(start_point[1] / GRID_SIZE)
    grid[col][row] = start_point

# Initialize with a random point
initial_point = (random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
restart_simulation(initial_point)

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_simulation(mouse_pos)

    if active:
        rand_index = random.randint(0, len(active) - 1)
        point = active[rand_index]
        found = False

        for _ in range(K):
            new_point = generate_point_around(point)
            if in_bounds(new_point) and fits(new_point):
                points.append(new_point)
                active.append(new_point)
                col = int(new_point[0] / GRID_SIZE)
                row = int(new_point[1] / GRID_SIZE)
                grid[col][row] = new_point
                found = True
                break

        if not found:
            active.pop(rand_index)

    # Draw points
    for p in points:
        pygame.draw.circle(screen, (255, 255, 255), (int(p[0]), int(p[1])), 2)

    # Draw active points
    for a in active:
        pygame.draw.circle(screen, (255, 0, 0), (int(a[0]), int(a[1])), 2)

    pygame.display.flip()
    # clock.tick(1000)

pygame.quit()
