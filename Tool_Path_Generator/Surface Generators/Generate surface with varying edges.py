import numpy as np
from scipy.spatial import Delaunay
import open3d as o3d

def generate_irregular_polygon(num_edges, radius=2.5, perturbation=0.5):
    """
    Generate the vertices of an irregular polygon.

    Parameters:
    - num_edges (int): Number of edges of the polygon.
    - radius (float): Radius of the base circle.
    - perturbation (float): Maximum perturbation of the vertices.

    Returns:
    - vertices (numpy array): Coordinates of the polygon vertices.
    """
    angles = np.linspace(0, 2 * np.pi, num_edges, endpoint=False)
    np.random.shuffle(angles)  # Shuffle to randomize vertex positions
    vertices = np.array([(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles])
    
    # Perturb the vertices
    perturb = np.random.uniform(-perturbation, perturbation, vertices.shape)
    vertices += perturb
    
    return vertices

def interpolate_surface(vertices, func, grid_resolution=100):
    """
    Interpolate a surface over the polygon using a given function.

    Parameters:
    - vertices (numpy array): Polygon vertices.
    - func (function): Function to define surface heights.
    - grid_resolution (int): Resolution of the grid for interpolation.

    Returns:
    - X, Y, Z (numpy arrays): Coordinates of the point cloud.
    """
    # Generate a Delaunay triangulation of the vertices
    tri = Delaunay(vertices)
    
    # Create a grid of points within the bounding box of the polygon
    min_x, min_y = np.min(vertices, axis=0)
    max_x, max_y = np.max(vertices, axis=0)
    x = np.linspace(min_x, max_x, grid_resolution)
    y = np.linspace(min_y, max_y, grid_resolution)
    X, Y = np.meshgrid(x, y)
    
    # Mask out points outside the polygon
    mask = tri.find_simplex(np.c_[X.ravel(), Y.ravel()]) >= 0
    Z = np.full(X.shape, np.nan)
    Z.ravel()[mask] = func(X.ravel()[mask], Y.ravel()[mask])
    
    return X, Y, Z, mask

def surface_function(X, Y, max_z):
    """
    Define the surface function.

    Parameters:
    - X, Y (numpy arrays): Grid points.
    - max_z (float): Maximum z value for the surface.

    Returns:
    - Z (numpy array): Surface values at the grid points.
    """
    # Create a gentle curve for the z values
    Z = max_z * np.sin(np.sqrt(X**2 + Y**2) / 10)  # Adjusted for a gentler curve
    return Z

def export_point_cloud(X, Y, Z, mask, filename):
    """
    Export the point cloud surface to a text file.

    Parameters:
    - X, Y, Z (numpy arrays): Coordinates of the point cloud.
    - mask (numpy array): Mask to indicate valid points.
    - filename (str): Name of the output file.
    """
    X_masked = X.ravel()[mask]
    Y_masked = Y.ravel()[mask]
    Z_masked = Z.ravel()[mask]

    with open(filename, 'w') as file:
        for x, y, z in zip(X_masked, Y_masked, Z_masked):
            file.write(f"{x},{y},{z}\n")  # Use comma as delimiter for compatibility

def visualize_with_open3d(X, Y, Z, mask):
    """
    Visualize the point cloud using Open3D.

    Parameters:
    - X, Y, Z (numpy arrays): Coordinates of the point cloud.
    - mask (numpy array): Mask to indicate valid points.
    """
    # Create a point cloud object
    X_masked = X.ravel()[mask]
    Y_masked = Y.ravel()[mask]
    Z_masked = Z.ravel()[mask]
    points = np.vstack((X_masked, Y_masked, Z_masked)).T
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud])

if __name__ == "__main__":
    num_edges = int(input("Enter the number of edges: "))
    max_z = float(input("Enter the maximum z value: "))
    vertices = generate_irregular_polygon(num_edges)
    X, Y, Z, mask = interpolate_surface(vertices, lambda x, y: surface_function(x, y, max_z))
    export_point_cloud(X, Y, Z, mask, "chosen_edges.txt")
    print("Point cloud exported to 'chosen_edges.txt'")
    visualize_with_open3d(X, Y, Z, mask)
