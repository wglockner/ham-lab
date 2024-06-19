import numpy as np

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

# Function to check if a point is inside a polygon using ray-casting algorithm
def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Check which points are inside the polygon
inside_polygon = np.array([is_point_in_polygon(point, vertices) for point in grid_points])

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

# Rotate points 90 degrees about the y-axis
rotation_matrix = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [-1, 0, 0]
])
rotated_surface_points = complete_surface_points.dot(rotation_matrix.T)

# Save to text file with comma delimiter
output_file = '8_sided_curved_surface_rotated.txt'
np.savetxt(output_file, rotated_surface_points, fmt='%.6f', delimiter=',')

print(f"Rotated point cloud data saved to {output_file}")
