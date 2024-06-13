import numpy as np
import random
from scipy.spatial import Delaunay

# Parameters
num_edges = 8
min_length = 1.0
max_length = 5.0
target_size = 9.0  # inches in both x and y directions
delta_z = 0.5  # curvature in inches
points_per_side = 100  # Number of points per side to define the surface resolution

# Generate random edge lengths and ensure they sum up to maintain size
edge_lengths = np.random.uniform(min_length, max_length, num_edges)
scale_factor = target_size / max(np.sum(edge_lengths[:4]), np.sum(edge_lengths[4:]))
edge_lengths *= scale_factor

# Calculate angles for the polygon
angles = np.linspace(0, 2 * np.pi, num_edges, endpoint=False)

# Generate polygon vertices
vertices = []
x, y = 0, 0
for i in range(num_edges):
    x += edge_lengths[i] * np.cos(angles[i])
    y += edge_lengths[i] * np.sin(angles[i])
    vertices.append((x, y))

# Create a fine grid of points inside the bounding box of the polygon
min_x = min(v[0] for v in vertices)
max_x = max(v[0] for v in vertices)
min_y = min(v[1] for v in vertices)
max_y = max(v[1] for v in vertices)
x_grid, y_grid = np.mgrid[min_x:max_x:complex(0, points_per_side), min_y:max_y:complex(0, points_per_side)]
grid_points = np.vstack((x_grid.ravel(), y_grid.ravel())).T

# Check which points are inside the polygon
polygon_path = np.array(vertices)
inside_polygon = Delaunay(polygon_path).find_simplex(grid_points) >= 0

# Generate z-coordinates with curvature for points inside the polygon
center_x = sum(v[0] for v in vertices) / num_edges
center_y = sum(v[1] for v in vertices) / num_edges
z_values = np.zeros(grid_points.shape[0])
for i, (x, y) in enumerate(grid_points):
    if inside_polygon[i]:
        z_values[i] = delta_z * ((x - center_x) ** 2 + (y - center_y) ** 2) / (center_x ** 2 + center_y ** 2)

# Combine points and z-values
complete_surface_points = np.hstack((grid_points, z_values[:, np.newaxis]))
complete_surface_points = complete_surface_points[inside_polygon]

# Save to text file with comma delimiter
output_file = '8_sided_curved_surface.txt'
np.savetxt(output_file, complete_surface_points, fmt='%.6f', delimiter=',')

print(f"Point cloud data saved to {output_file}")
