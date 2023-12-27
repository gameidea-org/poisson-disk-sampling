import numpy as np
import matplotlib.pyplot as plt


def generate_bridson_sampling_points(width=1.0, height=1.0, radius=0.025, num_neighbors=30):
    def calculate_squared_distance(point1, point2):
        return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2

    def generate_random_points_around(center_point, num_points=1):
        # Note: This is not uniformly distributed around the center_point, but it's acceptable for this purpose
        radii = np.random.uniform(radius, 2 * radius, num_points)
        angles = np.random.uniform(0, 2 * np.pi, num_points)
        new_points = np.empty((num_points, 2))
        new_points[:, 0] = center_point[0] + radii * np.sin(angles)
        new_points[:, 1] = center_point[1] + radii * np.cos(angles)
        return new_points

    def is_point_within_limits(point):
        return 0 <= point[0] < width and 0 <= point[1] < height

    def get_neighborhood_indices(shape, index, n=2):
        row, col = index
        row_start, row_end = max(row - n, 0), min(row + n + 1, shape[0])
        col_start, col_end = max(col - n, 0), min(col + n + 1, shape[1])
        indices = np.dstack(np.mgrid[row_start:row_end, col_start:col_end])
        indices = indices.reshape(indices.size // 2, 2).tolist()
        indices.remove([row, col])
        return indices

    def is_point_in_neighborhood(point):
        i, j = int(point[0] / cell_size), int(point[1] / cell_size)
        if grid_mask[i, j]:
            return True
        for (i, j) in neighborhood_indices[(i, j)]:
            if grid_mask[i, j] and calculate_squared_distance(point, points_grid[i, j]) < squared_radius:
                return True
        return False

    def add_point_to_grid(point):
        points_list.append(point)
        i, j = int(point[0] / cell_size), int(point[1] / cell_size)
        points_grid[i, j], grid_mask[i, j] = point, True

    # Calculate cell size based on radius and dimensions
    cell_size = radius / np.sqrt(2)
    num_rows = int(np.ceil(width / cell_size))
    num_cols = int(np.ceil(height / cell_size))

    # Calculate squared radius for squared distance comparison
    squared_radius = radius * radius

    # Initialize arrays for points and grid
    points_grid = np.zeros((num_rows, num_cols, 2), dtype=np.float32)
    grid_mask = np.zeros((num_rows, num_cols), dtype=bool)

    # Generate neighborhood indices for each grid cell
    neighborhood_indices = {}
    for i in range(num_rows):
        for j in range(num_cols):
            neighborhood_indices[(i, j)] = get_neighborhood_indices(grid_mask.shape, (i, j), 2)

    # Initialize list to store points
    points_list = []

    # Add an initial random point to the grid
    add_point_to_grid((np.random.uniform(width), np.random.uniform(height)))

    # Generate points using Bridson's algorithm
    while len(points_list):
        random_index = np.random.randint(len(points_list))
        current_point = points_list[random_index]
        del points_list[random_index]

        new_points = generate_random_points_around(current_point, num_neighbors)
        for new_point in new_points:
            if is_point_within_limits(new_point) and not is_point_in_neighborhood(new_point):
                add_point_to_grid(new_point)

    return points_grid[grid_mask]


if __name__ == '__main__':
    plt.figure()
    plt.subplot(1, 1, 1, aspect=1)

    sampled_points = generate_bridson_sampling_points()
    X = [x for (x, y) in sampled_points]
    Y = [y for (x, y) in sampled_points]
    plt.scatter(X, Y, s=10)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()
