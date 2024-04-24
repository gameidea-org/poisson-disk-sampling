import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_squared_distance(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    dz = point1[2] - point2[2]
    return dx * dx + dy * dy + dz * dz

def generate_random_points_around(center_point, radius, num_points=1):
    new_points = []
    for _ in range(num_points):
        r = random.uniform(radius, 2 * radius)
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        x = center_point[0] + r * math.sin(phi) * math.cos(theta)
        y = center_point[1] + r * math.sin(phi) * math.sin(theta)
        z = center_point[2] + r * math.cos(phi)
        new_points.append((x, y, z))
    return new_points

def is_point_within_limits(point, width, height, depth):
    if 0 <= point[0] < width and 0 <= point[1] < height and 0 <= point[2] < depth:
        return True
    else:
        return False

def get_neighborhood_indices(grid_size, index, n=2):
    row, col, depth = index
    row_start = max(row - n, 0)
    row_end = min(row + n + 1, grid_size[0])
    col_start = max(col - n, 0)
    col_end = min(col + n + 1, grid_size[1])
    depth_start = max(depth - n, 0)
    depth_end = min(depth + n + 1, grid_size[2])
    indices = []
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            for d in range(depth_start, depth_end):
                if (r, c, d) != (row, col, depth):
                    indices.append((r, c, d))
    return indices

def is_point_in_neighborhood(point, points_grid, neighborhood_indices, cell_size, squared_radius):
    i = int(point[0] / cell_size)
    j = int(point[1] / cell_size)
    k = int(point[2] / cell_size)
    if points_grid[i][j][k] != (0, 0, 0):
        return True
    for (r, c, d) in neighborhood_indices[(i, j, k)]:
        if points_grid[r][c][d] != (0, 0, 0) and calculate_squared_distance(point, points_grid[r][c][d]) < squared_radius:
            return True
    return False

def add_point_to_grid(point, points_list, points_grid, cell_size):
    points_list.append(point)
    i = int(point[0] / cell_size)
    j = int(point[1] / cell_size)
    k = int(point[2] / cell_size)
    points_grid[i][j][k] = point

def generate_bridson_sampling_points(width=1.0, height=1.0, depth=1.0, radius=0.075, num_neighbors=30):
    cell_size = radius / math.sqrt(3)
    num_rows = int(math.ceil(width / cell_size))
    num_cols = int(math.ceil(height / cell_size))
    num_depths = int(math.ceil(depth / cell_size))
    squared_radius = radius * radius
    points_grid = []
    for _ in range(num_rows):
        row = [[(0, 0, 0)] * num_depths for _ in range(num_cols)]
        points_grid.append(row)
    neighborhood_indices = {}
    for i in range(num_rows):
        for j in range(num_cols):
            for k in range(num_depths):
                neighborhood_indices[(i, j, k)] = get_neighborhood_indices((num_rows, num_cols, num_depths), (i, j, k), 2)
    points_list = []
    initial_point = (random.uniform(0, width), random.uniform(0, height), random.uniform(0, depth))
    add_point_to_grid(initial_point, points_list, points_grid, cell_size)
    while points_list:
        random_index = random.randint(0, len(points_list) - 1)
        current_point = points_list[random_index]
        del points_list[random_index]
        new_points = generate_random_points_around(current_point, radius, num_neighbors)
        for new_point in new_points:
            if is_point_within_limits(new_point, width, height, depth) and not is_point_in_neighborhood(new_point, points_grid, neighborhood_indices, cell_size, squared_radius):
                add_point_to_grid(new_point, points_list, points_grid, cell_size)
    sampled_points = []
    for row in points_grid:
        for col in row:
            for point in col:
                if point != (0, 0, 0):
                    sampled_points.append(point)
    return sampled_points

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sampled_points = generate_bridson_sampling_points()
    X, Y, Z = zip(*sampled_points)
    ax.scatter(X, Y, Z, s=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    plt.show()
