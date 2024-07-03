import numpy as np
import open3d as o3d
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from math import sin, cos, sqrt, radians

# Function to calculate maximum grind width
def calculate_maximum_grind_width(diameter, depth, angle_degrees):
    if angle_degrees == 0:
        raise ValueError("Grind angle cannot be zero.")
    angle_radians = radians(angle_degrees)
    chord_height = depth / sin(angle_radians)
    stone_radius = diameter / 2
    distance_from_tool_center = stone_radius - chord_height
    
    if stone_radius**2 < distance_from_tool_center**2:
        raise ValueError("Invalid parameters resulting in negative value under sqrt")
    
    return 2 * sqrt(stone_radius**2 - distance_from_tool_center**2)

# Function to move points by the normal direction
def move_points_by_normal(points, distance, normal):
    if points.shape[0] == 0:
        return points
    moved_points = points + distance * normal
    return moved_points

# Function to ensure all normals face the same direction
def orient_normals_consistently(points, normals):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.normals = o3d.utility.Vector3dVector(normals)
    pcd.orient_normals_towards_camera_location()
    return np.asarray(pcd.normals)

# Function to calculate the global normal
def calculate_global_normal(normals):
    return np.mean(normals, axis=0) / np.linalg.norm(np.mean(normals, axis=0))

# Function to fit lines across the surface
def fit_lines(points, axis, step):
    lines = []
    if axis == 'x':
        min_val, max_val = np.min(points[:, 0]), np.max(points[:, 0])
        for val in np.arange(min_val, max_val, step):
            mask = (points[:, 0] >= val) & (points[:, 0] < val + step)
            line_points = points[mask]
            if line_points.shape[0] > 0:
                lines.append(np.mean(line_points, axis=0))
    return lines

# Create GUI for selecting file and grind parameters
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PLY files", "*.ply")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def start_processing():
    file_path = entry_file_path.get()
    
    grind_depth = float(spin_grind_depth.get())
    stone_diameter = float(spin_stone_diameter.get())
    grind_angle = float(spin_grind_angle.get())
    initial_stepover_factor = float(spin_initial_stepover_factor.get()) / 100.0
    anomaly_height = float(spin_anomaly_height.get())
    surface_resolution_option = surface_res_option.get()
    surface_resolution_custom_value = spin_surface_res.get()
    
    # Calculate the maximum grind width
    try:
        max_grind_width = calculate_maximum_grind_width(stone_diameter, grind_depth, grind_angle)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    
    label_max_grind_width_value.config(text=f"{max_grind_width:.2f} (in)")

    # Set stepover based on surface resolution
    if surface_resolution_option == "Custom":
        stepover = float(surface_resolution_custom_value) / 100.0 * max_grind_width
    elif surface_resolution_option == "Low":
        stepover = 0.9 * max_grind_width
    elif surface_resolution_option == "Medium":
        stepover = 0.6 * max_grind_width
    elif surface_resolution_option == "High":
        stepover = 0.25 * max_grind_width

    # Calculate initial stepover
    initial_stepover = initial_stepover_factor * stepover
    
    # Load point cloud data
    try:
        pcd = o3d.io.read_point_cloud(file_path)
        points = np.asarray(pcd.points)
        if not pcd.has_normals():
            messagebox.showwarning("Warning", "Point cloud does not have normals. Normals will be estimated.")
            pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
        normals = np.asarray(pcd.normals)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load point cloud: {e}")
        return
    
    # Ensure all normals face the same direction
    normals = orient_normals_consistently(points, normals)
    
    # Calculate global normal
    global_normal = calculate_global_normal(normals)
    
    # Fit lines across the surface along the x-axis
    lines_x = fit_lines(points, axis='x', step=stepover)
    
    # Raise lines in the direction of the global normal
    lines_x_raised = move_points_by_normal(np.array(lines_x), anomaly_height, global_normal)

    # Create Open3D PointCloud objects for visualization
    geometries = []

    original_point_cloud = o3d.geometry.PointCloud()
    original_point_cloud.points = o3d.utility.Vector3dVector(points)
    original_point_cloud.paint_uniform_color([0.5, 0.5, 0.5])  # Set all points to gray
    geometries.append(original_point_cloud)

    if len(lines_x_raised) > 0:
        lines_x_raised_cloud = o3d.geometry.PointCloud()
        lines_x_raised_cloud.points = o3d.utility.Vector3dVector(lines_x_raised)
        lines_x_raised_cloud.paint_uniform_color([1, 0, 0])  # Set all points to red
        geometries.append(lines_x_raised_cloud)

    # Visualize the points
    o3d.visualization.draw_geometries(geometries)

# Create the main window
root = tk.Tk()
root.title("Point Cloud Processor")

# Create and place the widgets
label_file_path = tk.Label(root, text="Select point cloud file:")
label_file_path.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=5)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=5)

# Grind Depth
label_grind_depth = tk.Label(root, text="Grind Depth (in):")
label_grind_depth.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

spin_grind_depth = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1)
spin_grind_depth.grid(row=1, column=1, padx=10, pady=5)

# Stone Diameter
label_stone_diameter = tk.Label(root, text="Stone Diameter (in):")
label_stone_diameter.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

spin_stone_diameter = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1)
spin_stone_diameter.grid(row=2, column=1, padx=10, pady=5)

# Grind Angle
label_grind_angle = tk.Label(root, text="Grind Angle (degrees):")
label_grind_angle.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

spin_grind_angle = tk.Spinbox(root, from_=0.0, to=90.0, increment=0.1)
spin_grind_angle.grid(row=3, column=1, padx=10, pady=5)

# Initial Stepover Factor
label_initial_stepover_factor = tk.Label(root, text="Initial Stepover Factor (%):")
label_initial_stepover_factor.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

spin_initial_stepover_factor = tk.Spinbox(root, from_=0.0, to=100.0, increment=1.0)
spin_initial_stepover_factor.grid(row=4, column=1, padx=10, pady=5)

# Anomaly Height
label_anomaly_height = tk.Label(root, text="Anomaly Height (in):")
label_anomaly_height.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

spin_anomaly_height = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1)
spin_anomaly_height.grid(row=5, column=1, padx=10, pady=5)

# Surface Resolution Options
label_surface_res = tk.Label(root, text="Surface Resolution:")
label_surface_res.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

surface_res_option = tk.StringVar(value="Medium")
surface_res_menu = ttk.OptionMenu(root, surface_res_option, "Medium", "Low", "Medium", "High", "Custom")
surface_res_menu.grid(row=6, column=1, padx=10, pady=5)

spin_surface_res = tk.Spinbox(root, from_=0.0, to=100.0, increment=1.0, state="disabled")
spin_surface_res.grid(row=6, column=2, padx=10, pady=5)
label_surface_res_percent = tk.Label(root, text="% of chord length")
label_surface_res_percent.grid(row=6, column=3, padx=10, pady=5, sticky=tk.W)

def surface_res_option_changed(*args):
    if surface_res_option.get() == "Custom":
        spin_surface_res.config(state="normal")
    else:
        spin_surface_res.config(state="disabled")

surface_res_option.trace("w", surface_res_option_changed)

# Maximum Grind Width Display
label_max_grind_width = tk.Label(root, text="Maximum Grind Width (in):")
label_max_grind_width.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

label_max_grind_width_value = tk.Label(root, text="0.00")
label_max_grind_width_value.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

button_start = tk.Button(root, text="Start", command=start_processing)
button_start.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()
