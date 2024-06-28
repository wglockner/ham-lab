import numpy as np
import open3d as o3d

def visualize_lines(file_path):
    # Load the ordered lines from the file
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            point = list(map(float, line.strip().split(',')))
            lines.append(point)

    # Convert lines to a NumPy array
    lines = np.array(lines)

    # Create a point cloud object from the lines
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(lines)

    # Paint the point cloud
    point_cloud.paint_uniform_color([0, 0, 1])  # Blue color for the lines

    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud])

if __name__ == "__main__":
    file_path = 'ordered_lines.txt'  # Replace with the path to your generated file
    visualize_lines(file_path)
