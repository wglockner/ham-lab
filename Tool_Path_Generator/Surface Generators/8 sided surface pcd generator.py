import numpy as np
import open3d as o3d
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

# Generate z-coordinates with convex curvature for points inside the polygon
center_x = sum(v[0] for v in vertices) / num_edges
center_y = sum(v[1] for v in vertices) / num_edges
z_values = np.zeros(grid_points.shape[0])
for i, (x, y) in enumerate(grid_points):
    if inside_polygon[i]:
        distance_to_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        max_distance_to_center = np.sqrt((min_x - center_x) ** 2 + (min_y - center_y) ** 2)
        z_values[i] = delta_z * (1 - (distance_to_center / max_distance_to_center) ** 2)

# Combine points and z-values
complete_surface_points = np.hstack((grid_points, z_values[:, np.newaxis]))
complete_surface_points = complete_surface_points[inside_polygon]

# Convert to Open3D point cloud
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(complete_surface_points)

# Estimate normals
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=1.0, max_nn=30))

# Invert normals
normals = np.asarray(pcd.normals)
pcd.normals = o3d.utility.Vector3dVector(-normals)

# Orient normals consistently
pcd.orient_normals_consistent_tangent_plane(k=30)

# Save to .pcd file
output_pcd_file = '8_sided_convex_surface_with_inverted_normals.pcd'
o3d.io.write_point_cloud(output_pcd_file, pcd)

print(f"Point cloud with inverted normals saved to {output_pcd_file}")
