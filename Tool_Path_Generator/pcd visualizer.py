import open3d as o3d
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Function to create a coordinate frame for the axes
def create_axis_lines(length):
    points = [[0, 0, 0], [length, 0, 0], [0, 0, 0], [0, length, 0], [0, 0, 0], [0, 0, length]]
    lines = [[0, 1], [2, 3], [4, 5]]
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set

# Visualization function
def visualize_with_axes(point_cloud, coordinate_frame, axis_lines):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(point_cloud)
    vis.add_geometry(coordinate_frame)
    vis.add_geometry(axis_lines)

    # Adjust render options
    opt = vis.get_render_option()
    opt.point_size = 2.0

    vis.run()
    vis.destroy_window()

# Main function to run the visualization with file selection
def main():
    # Open file dialog to select the PCD file
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Point Cloud Files", "*.pcd")])
    
    if file_path:
        # Load the selected point cloud
        pcd = o3d.io.read_point_cloud(file_path)

        # Create coordinate frame and axis lines
        axis_length = 10.0
        coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=axis_length)
        axis_lines = create_axis_lines(axis_length)

        # Visualize the point cloud with axes
        visualize_with_axes(pcd, coordinate_frame, axis_lines)
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
