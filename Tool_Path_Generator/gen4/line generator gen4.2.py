import numpy as np
import open3d as o3d
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from math import sin, cos, sqrt, radians

# Function to get resolution values based on the selected option
def get_resolution(option, custom_value):
    if option == "Low":
        return 0.5
    elif option == "Medium":
        return 1.0
    elif option == "High":
        return 2.0
    elif option == "Custom":
        return float(custom_value) / 100.0  # Custom value as a percentage
    else:
        return 1.0  # Default to Medium if something goes wrong

# Function to get tolerance values based on the selected option
def get_tolerance(option, custom_value):
    if option == "Custom":
        return float(custom_value)
    elif option == "Low":
        return 0.25
    elif option == "Medium":
        return 0.1
    elif option == "High":
        return 0.01
    else:
        return 0.1  # Default to Medium if something goes wrong

# Function to calculate maximum grind width
def calculate_maximum_grind_width(diameter, depth, angle_degrees):
    angle_radians = radians(angle_degrees)
    chord_height = depth / sin(angle_radians)
    stone_radius = diameter / 2
    distance_from_tool_center = stone_radius - chord_height
    return 2 * sqrt(stone_radius**2 - distance_from_tool_center**2)

# Function to move points by the average normal direction, ensuring normals are in the same general direction
def move_points_by_normal(points, region_size, distance, avg_normal):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=region_size, max_nn=30))
    
    normals = np.asarray(point_cloud.normals)
    points = np.asarray(point_cloud.points)
    
    # Ensure all normals are in the same general direction
    dot_products = np.dot(normals, avg_normal)
    normals[dot_products < 0] = -normals[dot_products < 0]
    
    moved_points = points + distance * normals
    
    return moved_points

# Function to delete points too close to the edge
def delete_edge_points(points, instep):
    min_x, max_x = np.min(points[:, 0]), np.max(points[:, 0])
    min_y, max_y = np.min(points[:, 1]), np.max(points[:, 1])
    
    mask_x = (points[:, 0] > (min_x + instep)) & (points[:, 0] < (max_x - instep))
    mask_y = (points[:, 1] > (min_y + instep)) & (points[:, 1] < (max_y - instep))
    
    mask = mask_x & mask_y
    filtered_points = points[mask]
    
    return filtered_points

# Create GUI for selecting file and grind parameters
def browse_file():
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def start_processing():
    file_path = entry_file_path.get()
    
    surface_resolution_option = surface_res_option.get()
    surface_resolution_custom_value = spin_surface_res.get()
    tolerance_resolution_option = tolerance_res_option.get()
    tolerance_custom_value = spin_tolerance_res.get()
    cross_cut_enabled = cross_cut_var.get()
    show_original = show_original_var.get()
    show_surface_lines = show_surface_lines_var.get()

    grind_depth = float(spin_grind_depth.get())
    stone_diameter = float(spin_stone_diameter.get())
    grind_angle = float(spin_grind_angle.get())
    initial_stepover_factor = float(spin_initial_stepover_factor.get()) / 100.0
    region_size = float(spin_region_size.get())
    anomaly_height = float(spin_anomaly_height.get())
    
    # Calculate the maximum grind width
    max_grind_width = calculate_maximum_grind_width(stone_diameter, grind_depth, grind_angle)
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

    # Set tolerance based on tolerance resolution
    if tolerance_resolution_option == "Custom":
        tolerance = float(tolerance_custom_value)
    else:
        tolerance = get_tolerance(tolerance_resolution_option, tolerance_custom_value)

    # Display calculated stepover and tolerance
    label_stepover_value.config(text=f"{stepover:.2f} (in)")
    label_tolerance_value.config(text=f"{tolerance:.2f} (in)")
    
    # Calculate z_offset
    stone_radius = stone_diameter / 2
    z_offset = stone_radius * sin(radians(grind_angle))
    
    # Calculate instep
    instep = stone_radius * cos(radians(grind_angle))
    label_instep_value.config(text=f"{instep:.2f} (in)")
    
    # Load point cloud data, skip the first row (header)
    points = np.loadtxt(file_path, delimiter=',', skiprows=1)
    
    # Delete points too close to the edge
    points = delete_edge_points(points, instep)
    
    # Calculate average normal for the surface
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=region_size, max_nn=30))
    avg_normal = np.mean(np.asarray(point_cloud.normals), axis=0)
    avg_normal /= np.linalg.norm(avg_normal)  # Normalize the average normal
    
    # Extract and average lines on the surface parallel to the y-axis (stepover x)
    surface_stepover_lines, surface_initial_stepover_lines = extract_lines(points, stepover, tolerance, axis='x', initial_stepover=initial_stepover)
    averaged_surface_stepover_lines = average_lines(surface_stepover_lines, axis='x')
    averaged_surface_initial_stepover_lines = average_lines(surface_initial_stepover_lines, axis='x')

    cross_cut_points = []
    initial_cross_cut_points = []
    if cross_cut_enabled:
        # Extract and average lines parallel to the x-axis (stepover y)
        cross_cut_lines, initial_cross_cut_lines = extract_lines(points, stepover, tolerance, axis='y', initial_stepover=initial_stepover)
        averaged_cross_cut_lines = average_lines(cross_cut_lines, axis='y')
        averaged_initial_cross_cut_lines = average_lines(initial_cross_cut_lines, axis='y')
        cross_cut_points.extend(averaged_cross_cut_lines)
        initial_cross_cut_points.extend(averaged_initial_cross_cut_lines)
    
    # Create Open3D PointCloud objects for visualization
    geometries = []

    if show_original:
        original_point_cloud = o3d.geometry.PointCloud()
        original_point_cloud.points = o3d.utility.Vector3dVector(points)
        original_point_cloud.paint_uniform_color([0.5, 0.5, 0.5])  # Set all points to gray
        geometries.append(original_point_cloud)

    if show_surface_lines:
        surface_stepover_cloud = o3d.geometry.PointCloud()
        surface_stepover_cloud.points = o3d.utility.Vector3dVector(averaged_surface_stepover_lines)
        surface_stepover_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
        geometries.append(surface_stepover_cloud)

        initial_surface_stepover_cloud = o3d.geometry.PointCloud()
        initial_surface_stepover_cloud.points = o3d.utility.Vector3dVector(averaged_surface_initial_stepover_lines)
        initial_surface_stepover_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
        geometries.append(initial_surface_stepover_cloud)

        if cross_cut_enabled:
            initial_cross_cut_cloud = o3d.geometry.PointCloud()
            initial_cross_cut_cloud.points = o3d.utility.Vector3dVector(initial_cross_cut_points)
            initial_cross_cut_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
            geometries.append(initial_cross_cut_cloud)

            cross_cut_cloud = o3d.geometry.PointCloud()
            cross_cut_cloud.points = o3d.utility.Vector3dVector(cross_cut_points)
            cross_cut_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
            geometries.append(cross_cut_cloud)

    # Move points by z_offset increments and add them to the geometries
    z_height_count = 0
    line_counter = 0
    while z_height_count < anomaly_height:
        move_distance = (line_counter + 1) * z_offset
        moved_points = move_points_by_normal(points, region_size, move_distance, avg_normal)
        z_height_count += z_offset

        stepover_lines, initial_stepover_lines = extract_lines(moved_points, stepover, tolerance, axis='x', initial_stepover=initial_stepover)
        averaged_stepover_lines = average_lines(stepover_lines, axis='x')
        averaged_initial_stepover_lines = average_lines(initial_stepover_lines, axis='x')

        initial_stepover_cloud = o3d.geometry.PointCloud()
        initial_stepover_cloud.points = o3d.utility.Vector3dVector(averaged_initial_stepover_lines)
        initial_stepover_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
        geometries.append(initial_stepover_cloud)

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(averaged_stepover_lines)
        point_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
        geometries.append(point_cloud)

        if cross_cut_enabled:
            cross_cut_lines, initial_cross_cut_lines = extract_lines(moved_points, stepover, tolerance, axis='y', initial_stepover=initial_stepover)
            averaged_cross_cut_lines = average_lines(cross_cut_lines, axis='y')
            averaged_initial_cross_cut_lines = average_lines(initial_cross_cut_lines, axis='y')

            initial_cross_cut_cloud = o3d.geometry.PointCloud()
            initial_cross_cut_cloud.points = o3d.utility.Vector3dVector(averaged_initial_cross_cut_lines)
            initial_cross_cut_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
            geometries.append(initial_cross_cut_cloud)

            cross_cut_cloud = o3d.geometry.PointCloud()
            cross_cut_cloud.points = o3d.utility.Vector3dVector(averaged_cross_cut_lines)
            cross_cut_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
            geometries.append(cross_cut_cloud)

        line_counter += 1

    print(f"Line Counter: {line_counter}")

    # Visualize the points
    o3d.visualization.draw_geometries(geometries)

def extract_lines(points, stepover, tolerance, axis='x', initial_stepover=0):
    lines = []
    initial_lines = []
    if axis == 'x':
        min_val, max_val = np.min(points[:, 0]), np.max(points[:, 0])
        initial_stepover_values = [min_val + initial_stepover, max_val - initial_stepover]
        stepover_values = np.arange(min_val + 2*initial_stepover, max_val - 2*initial_stepover, stepover)

        for val in stepover_values:
            mask = np.abs(points[:, 0] - val) < tolerance
            line = points[mask]
            lines.append(line)

        for val in initial_stepover_values:
            mask = np.abs(points[:, 0] - val) < tolerance
            line = points[mask]
            initial_lines.append(line)

    elif axis == 'y':
        min_val, max_val = np.min(points[:, 1]), np.max(points[:, 1])
        initial_stepover_values = [min_val + initial_stepover, max_val - initial_stepover]
        stepover_values = np.arange(min_val + 2*initial_stepover, max_val - 2*initial_stepover, stepover)

        for val in stepover_values:
            mask = np.abs(points[:, 1] - val) < tolerance
            line = points[mask]
            lines.append(line)

        for val in initial_stepover_values:
            mask = np.abs(points[:, 1] - val) < tolerance
            line = points[mask]
            initial_lines.append(line)
    
    return lines, initial_lines

def average_lines(lines, axis='x'):
    averaged_points = []
    for line in lines:
        if len(line) > 0:
            if axis == 'x':
                avg_x = np.mean(line[:, 0])
                unique_y_values = np.unique(line[:, 1])
                for y in unique_y_values:
                    z_values = np.asarray([z for (x, y_val, z) in line if y_val == y])
                    avg_z = np.mean(z_values)
                    averaged_points.append([avg_x, y, avg_z])
            elif axis == 'y':
                avg_y = np.mean(line[:, 1])
                unique_x_values = np.unique(line[:, 0])
                for x in unique_x_values:
                    z_values = np.asarray([z for (x_val, y, z) in line if x_val == x])
                    avg_z = np.mean(z_values)
                    averaged_points.append([x, avg_y, avg_z])
    return averaged_points

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

# Region Size
label_region_size = tk.Label(root, text="Region Size (in):")
label_region_size.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

spin_region_size = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1)
spin_region_size.grid(row=5, column=1, padx=10, pady=5)

# Anomaly Height
label_anomaly_height = tk.Label(root, text="Anomaly Height (in):")
label_anomaly_height.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

spin_anomaly_height = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1)
spin_anomaly_height.grid(row=6, column=1, padx=10, pady=5)

# Surface Resolution Options
label_surface_res = tk.Label(root, text="Surface Resolution:")
label_surface_res.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

surface_res_option = tk.StringVar(value="Medium")
surface_res_menu = ttk.OptionMenu(root, surface_res_option, "Medium", "Low", "Medium", "High", "Custom")
surface_res_menu.grid(row=7, column=1, padx=10, pady=5)

spin_surface_res = tk.Spinbox(root, from_=0.0, to=100.0, increment=1.0, state="disabled")
spin_surface_res.grid(row=7, column=2, padx=10, pady=5)
label_surface_res_percent = tk.Label(root, text="% of chord length")
label_surface_res_percent.grid(row=7, column=3, padx=10, pady=5, sticky=tk.W)

def surface_res_option_changed(*args):
    if surface_res_option.get() == "Custom":
        spin_surface_res.config(state="normal")
    else:
        spin_surface_res.config(state="disabled")

surface_res_option.trace("w", surface_res_option_changed)

# Tolerance Options
label_tolerance_res = tk.Label(root, text="Tolerance:")
label_tolerance_res.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)

tolerance_res_option = tk.StringVar(value="Medium")
tolerance_res_menu = ttk.OptionMenu(root, tolerance_res_option, "Medium", "Low", "Medium", "High", "Custom")
tolerance_res_menu.grid(row=8, column=1, padx=10, pady=5)

spin_tolerance_res = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1, state="disabled")
spin_tolerance_res.grid(row=8, column=2, padx=10, pady=5)
label_tolerance_in = tk.Label(root, text="(in)")
label_tolerance_in.grid(row=8, column=3, padx=10, pady=5, sticky=tk.W)

def tolerance_res_option_changed(*args):
    if tolerance_res_option.get() == "Custom":
        spin_tolerance_res.config(state="normal")
    else:
        spin_tolerance_res.config(state="disabled")

tolerance_res_option.trace("w", tolerance_res_option_changed)

# Cross Cut Toggle
cross_cut_var = tk.IntVar()
cross_cut_checkbox = tk.Checkbutton(root, text="Cross Cut", variable=cross_cut_var)
cross_cut_checkbox.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Display Options
show_original_var = tk.IntVar()
show_original_checkbox = tk.Checkbutton(root, text="Show Original Point Cloud", variable=show_original_var)
show_original_checkbox.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

show_surface_lines_var = tk.IntVar()
show_surface_lines_checkbox = tk.Checkbutton(root, text="Show Surface Lines Only", variable=show_surface_lines_var)
show_surface_lines_checkbox.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Maximum Grind Width Display
label_max_grind_width = tk.Label(root, text="Maximum Grind Width (in):")
label_max_grind_width.grid(row=12, column=0, padx=10, pady=5, sticky=tk.W)

label_max_grind_width_value = tk.Label(root, text="0.00")
label_max_grind_width_value.grid(row=12, column=1, padx=10, pady=5, sticky=tk.W)

# Instep Display
label_instep = tk.Label(root, text="Instep (in):")
label_instep.grid(row=13, column=0, padx=10, pady=5, sticky=tk.W)

label_instep_value = tk.Label(root, text="0.00")
label_instep_value.grid(row=13, column=1, padx=10, pady=5, sticky=tk.W)

# Stepover Display
label_stepover = tk.Label(root, text="Stepover (in):")
label_stepover.grid(row=14, column=0, padx=10, pady=5, sticky=tk.W)

label_stepover_value = tk.Label(root, text="0.00")
label_stepover_value.grid(row=14, column=1, padx=10, pady=5, sticky=tk.W)

# Tolerance Display
label_tolerance = tk.Label(root, text="Tolerance (in):")
label_tolerance.grid(row=15, column=0, padx=10, pady=5, sticky=tk.W)

label_tolerance_value = tk.Label(root, text="0.00")
label_tolerance_value.grid(row=15, column=1, padx=10, pady=5, sticky=tk.W)

button_start = tk.Button(root, text="Start", command=start_processing)
button_start.grid(row=16, column=0, columnspan=3, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()
