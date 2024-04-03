import numpy as np
import matplotlib.pyplot as plt

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        if not self.boundary.contains_point(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            if self.northeast.insert(point) or self.northwest.insert(point) or \
               self.southeast.insert(point) or self.southwest.insert(point):
                return True
            else:
                return False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2
        ne_bound = Rectangle(x + w / 2, y + h / 2, w, h)
        self.northeast = QuadTree(ne_bound, self.capacity)
        nw_bound = Rectangle(x - w / 2, y + h / 2, w, h)
        self.northwest = QuadTree(nw_bound, self.capacity)
        se_bound = Rectangle(x + w / 2, y - h / 2, w, h)
        self.southeast = QuadTree(se_bound, self.capacity)
        sw_bound = Rectangle(x - w / 2, y - h / 2, w, h)
        self.southwest = QuadTree(sw_bound, self.capacity)
        self.divided = True

    def query_range(self, boundary, found_points):
        if not self.boundary.intersects_boundary(boundary):
            return
        for point in self.points:
            if boundary.contains_point(point):
                found_points.append(point)
        if self.divided:
            self.northeast.query_range(boundary, found_points)
            self.northwest.query_range(boundary, found_points)
            self.southeast.query_range(boundary, found_points)
            self.southwest.query_range(boundary, found_points)

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains_point(self, point):
        return (self.x - self.width / 2 <= point[0] < self.x + self.width / 2) and \
               (self.y - self.height / 2 <= point[1] < self.y + self.height / 2)

    def intersects_boundary(self, boundary):
        return not (boundary.x - boundary.width / 2 > self.x + self.width / 2 or
                    boundary.x + boundary.width / 2 < self.x - self.width / 2 or
                    boundary.y - boundary.height / 2 > self.y + self.height / 2 or
                    boundary.y + boundary.height / 2 < self.y - self.height / 2)

def generate_poisson_disk_samples(width=1.0, height=1.0, radius=0.025, num_samples=8):
    boundary = Rectangle(width / 2, height / 2, width, height)
    quadtree = QuadTree(boundary, 4)
    points = []
    active_points = [np.array([np.random.uniform(0, width), np.random.uniform(0, height)])]

    while active_points:
        index = np.random.randint(len(active_points))
        current_point = active_points[index]
        found_valid_point = False

        for _ in range(num_samples):
            angle = np.random.uniform(0, 2 * np.pi)
            distance = np.random.uniform(radius, 2 * radius)
            new_point = current_point + np.array([distance * np.sin(angle), distance * np.cos(angle)])

            if 0 <= new_point[0] < width and 0 <= new_point[1] < height:
                nearby_points = []
                query_boundary = Rectangle(new_point[0], new_point[1], 2 * radius, 2 * radius)
                quadtree.query_range(query_boundary, nearby_points)

                if not nearby_points:
                    points.append(new_point)
                    quadtree.insert(new_point)
                    active_points.append(new_point)
                    found_valid_point = True
                    break

        if not found_valid_point:
            active_points.pop(index)

    return np.array(points)

if __name__ == '__main__':
    plt.figure()
    plt.subplot(1, 1, 1, aspect=1)

    sampled_points = generate_poisson_disk_samples()
    X = [x for (x, y) in sampled_points]
    Y = [y for (x, y) in sampled_points]
    plt.scatter(X, Y, s=10, c='g', marker='o')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()
