import numpy as np
import open3d as o3d
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from math import sin, cos, sqrt, radians, acos, pi
from sklearn.linear_model import LinearRegression
import os

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

# Function to move points by the normal direction
def move_points_by_normal(points, distance, normals):
    if points.shape[0] == 0:
        return points
    moved_points = points + distance * normals
    return moved_points

# Function to delete points too close to the edge
def delete_edge_points(points, instep):
    if points.shape[0] == 0:
        return points
    min_x, max_x = np.min(points[:, 0]), np.max(points[:, 0])
    min_y, max_y = np.min(points[:, 1]), np.max(points[:, 1])
    
    mask_x = (points[:, 0] > (min_x + instep)) & (points[:, 0] < (max_x - instep))
    mask_y = (points[:, 1] > (min_y + instep)) & (points[:, 1] < (max_y - instep))
    
    mask = mask_x & mask_y
    filtered_points = points[mask]
    
    return filtered_points

# Function to create arrow geometries for normals
def create_normal_arrows(points, normals, length=0.05, radius=0.001, colors=None):
    arrows = []
    color_index = 0
    if colors is None:
        colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0]]  # Default to red, green, blue, yellow
    for i in range(points.shape[0]):
        arrow = o3d.geometry.TriangleMesh.create_arrow(cylinder_radius=radius, cone_radius=2*radius, cylinder_height=length, cone_height=4*radius)
        arrow.rotate(get_rotation_matrix(normals[i]), center=(0, 0, 0))
        arrow.translate(points[i])
        arrow.paint_uniform_color(colors[color_index % len(colors)])  # Cycle through colors
        color_index += 1
        arrows.append(arrow)
    return arrows

# Function to create an arrow for the global normal
def create_global_normal_arrow(global_normal, length=0.1, radius=0.002):
    arrow = o3d.geometry.TriangleMesh.create_arrow(cylinder_radius=radius, cone_radius=2*radius, cylinder_height=length, cone_height=4*radius)
    arrow.rotate(get_rotation_matrix(global_normal), center=(0, 0, 0))
    arrow.paint_uniform_color([1, 0, 1])  # Magenta color for the global normal arrow
    return arrow

# Function to get rotation matrix aligning z-axis with given normal
def get_rotation_matrix(normal):
    normal = normal / np.linalg.norm(normal)
    axis = np.cross([0, 0, 1], normal)
    axis_len = np.linalg.norm(axis)
    if axis_len == 0:
        return np.eye(3)
    axis = axis / axis_len
    angle = acos(np.dot([0, 0, 1], normal))
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    R = np.eye(3) + sin(angle) * K + (1 - cos(angle)) * np.dot(K, K)
    return R

# Function to downsample points and normals for visualization
def downsample(points, normals, factor=0.1):
    indices = np.random.choice(points.shape[0], int(points.shape[0] * factor), replace=False)
    return points[indices], normals[indices]

# Function to calculate regional normals
def calculate_regional_normals(points, normals, region_size, global_normal):
    regions = {}
    rotation_matrix = get_rotation_matrix(global_normal)
    rotated_points = (rotation_matrix @ points.T).T

    for point, normal in zip(rotated_points, normals):
        region_key = (int(point[0] // region_size), int(point[1] // region_size))
        if region_key not in regions:
            regions[region_key] = []
        regions[region_key].append(normal)
    
    regional_normals = {}
    for region_key, region_normals in regions.items():
        average_normal = np.mean(region_normals, axis=0)
        average_normal /= np.linalg.norm(average_normal)
        regional_normals[region_key] = average_normal

    return regional_normals, rotation_matrix

# Function to rotate points and normals to the global normal
def rotate_to_global_normal(points, normals, global_normal):
    rotation_matrix = get_rotation_matrix(global_normal)
    rotated_points = (rotation_matrix @ points.T).T
    rotated_normals = (rotation_matrix @ normals.T).T
    return rotated_points, rotated_normals, rotation_matrix

# Create GUI for selecting file and grind parameters
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PLY files", "*.ply")])
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
    instep_option = instep_option_var.get()
    instep_custom_value = float(spin_instep_custom.get()) / 100.0
    invert_normals_enabled = invert_normals_var.get()
    normal_selection = normal_selection_var.get()
    resolution_type = resolution_type_var.get()

    grind_depth = float(spin_grind_depth.get())
    stone_diameter = float(spin_stone_diameter.get())
    grind_angle = float(spin_grind_angle.get())
    initial_stepover_factor = float(spin_initial_stepover_factor.get()) / 100.0
    region_size = float(spin_region_size.get())
    anomaly_height = float(spin_anomaly_height.get())
    line_count = int(spin_line_count.get())
    
    # Calculate the maximum grind width
    max_grind_width = calculate_maximum_grind_width(stone_diameter, grind_depth, grind_angle)
    label_max_grind_width_value.config(text=f"{max_grind_width:.2f} (in)")

    # Calculate initial stepover
    initial_stepover = initial_stepover_factor * max_grind_width

    # Set stepover based on resolution type
    if resolution_type == "By Scallop":
        if surface_resolution_option == "Custom":
            stepover = float(surface_resolution_custom_value) / 100.0 * max_grind_width
        elif surface_resolution_option == "Low":
            stepover = 0.9 * max_grind_width
        elif surface_resolution_option == "Medium":
            stepover = 0.6 * max_grind_width
        elif surface_resolution_option == "High":
            stepover = 0.25 * max_grind_width
    elif resolution_type == "Line Count":
        if line_count > 1:
            stepover = (max_grind_width - 2 * initial_stepover) / (line_count - 1)
        else:
            stepover = max_grind_width  # If line count is 1, just use the max grind width

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
    
    # Load point cloud data
    mesh = o3d.io.read_triangle_mesh(file_path)
    mesh.compute_vertex_normals()
    points = np.asarray(mesh.vertices)
    normals = np.asarray(mesh.vertex_normals)
    
    # Invert normals if the option is enabled
    if invert_normals_enabled:
        normals = -normals

    # Calculate the global normal
    global_normal = np.mean(normals, axis=0)
    global_normal /= np.linalg.norm(global_normal)  # Normalize the global normal
    print(f"Global Normal: {global_normal}")

    if normal_selection == "Regional":
        regional_normals, rotation_matrix = calculate_regional_normals(points, normals, region_size, global_normal)
    
    # Rotate points and normals to align with global normal
    rotated_points, rotated_normals, rotation_matrix = rotate_to_global_normal(points, normals, global_normal)

    # Adjust instep based on the selected option
    if instep_option == "Custom":
        adjusted_instep = instep * instep_custom_value
        rotated_points = delete_edge_points(rotated_points, adjusted_instep)
    elif instep_option == "No Instep":
        adjusted_instep = instep
    else:
        adjusted_instep = instep

    # Downsample points and normals for visualization
    downsampled_points, downsampled_normals = downsample(rotated_points, rotated_normals)
    normal_arrows = create_normal_arrows(downsampled_points, downsampled_normals)
    
    # Create an arrow for the global normal
    global_normal_arrow = create_global_normal_arrow(global_normal)

    # Extract and average lines on the surface parallel to the y-axis (stepover x)
    surface_initial_stepover_lines, surface_stepover_lines = extract_lines(rotated_points, initial_stepover, stepover, tolerance, axis='x')
    averaged_surface_initial_stepover_lines = fit_lines(surface_initial_stepover_lines, axis='x')
    
    if resolution_type == "Line Count":
        surface_stepover_lines = []
        for initial_line in surface_initial_stepover_lines:
            min_x = min(point[0] for point in initial_line)
            max_x = max(point[0] for point in initial_line)
            if line_count > 1:
                stepover_x = np.linspace(min_x, max_x, line_count + 1)[1:-1]  # Calculate evenly spaced lines between the initial lines
            else:
                stepover_x = [min_x + (max_x - min_x) / 2]  # Single line in the middle
            for x_val in stepover_x:
                mask = np.abs(rotated_points[:, 0] - x_val) < tolerance
                line = rotated_points[mask]
                if line.shape[0] > 0:
                    surface_stepover_lines.append(line)

    averaged_surface_stepover_lines = fit_lines(surface_stepover_lines, axis='x')

    cross_cut_points = []
    initial_cross_cut_points = []
    if cross_cut_enabled:
        # Extract and average lines parallel to the x-axis (stepover y)
        cross_initial_stepover_lines, cross_stepover_lines = extract_lines(rotated_points, initial_stepover, stepover, tolerance, axis='y')
        averaged_initial_cross_cut_lines = fit_lines(cross_initial_stepover_lines, axis='y')
        averaged_cross_cut_lines = fit_lines(cross_stepover_lines, axis='y')
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
        if len(averaged_surface_stepover_lines) > 0:
            surface_stepover_cloud = o3d.geometry.PointCloud()
            surface_stepover_cloud.points = o3d.utility.Vector3dVector(averaged_surface_stepover_lines)
            surface_stepover_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
            geometries.append(surface_stepover_cloud)

        if len(averaged_surface_initial_stepover_lines) > 0:
            initial_surface_stepover_cloud = o3d.geometry.PointCloud()
            initial_surface_stepover_cloud.points = o3d.utility.Vector3dVector(averaged_surface_initial_stepover_lines)
            initial_surface_stepover_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
            geometries.append(initial_surface_stepover_cloud)

        if cross_cut_enabled:
            if len(initial_cross_cut_points) > 0:
                initial_cross_cut_cloud = o3d.geometry.PointCloud()
                initial_cross_cut_cloud.points = o3d.utility.Vector3dVector(initial_cross_cut_points)
                initial_cross_cut_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
                geometries.append(initial_cross_cut_cloud)

            if len(cross_cut_points) > 0:
                cross_cut_cloud = o3d.geometry.PointCloud()
                cross_cut_cloud.points = o3d.utility.Vector3dVector(cross_cut_points)
                cross_cut_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
                geometries.append(cross_cut_cloud)

    # Add normal arrows and the global normal arrow to geometries
    geometries.extend(normal_arrows)
    geometries.append(global_normal_arrow)

    # Move points by z_offset increments and add them to the geometries
    z_height_count = 0
    line_counter = 0
    
    all_lines = []

    while z_height_count < anomaly_height:
        move_distance = (line_counter + 1) * z_offset

        if normal_selection == "Global":
            moved_points = move_points_by_normal(rotated_points, move_distance, global_normal)
        elif normal_selection == "Regional":
            moved_points = np.zeros_like(rotated_points)
            for i, point in enumerate(rotated_points):
                region_key = (int(point[0] // region_size), int(point[1] // region_size))
                if region_key in regional_normals:
                    moved_points[i] = rotated_points[i] + move_distance * regional_normals[region_key]

        z_height_count += z_offset

        if moved_points.shape[0] > 0:
            if resolution_type == "Line Count":
                initial_stepover_lines, _ = extract_lines(moved_points, initial_stepover, 0, tolerance, axis='x')
                averaged_initial_stepover_lines = fit_lines(initial_stepover_lines, axis='x')
                surface_stepover_lines = []
                for initial_line in initial_stepover_lines:
                    min_x = min(point[0] for point in initial_line)
                    max_x = max(point[0] for point in initial_line)
                    if line_count > 1:
                        stepover_x = np.linspace(min_x, max_x, line_count + 1)[1:-1]  # Calculate evenly spaced lines between the initial lines
                    else:
                        stepover_x = [min_x + (max_x - min_x) / 2]  # Single line in the middle
                    for x_val in stepover_x:
                        mask = np.abs(moved_points[:, 0] - x_val) < tolerance
                        line = moved_points[mask]
                        if line.shape[0] > 0:
                            surface_stepover_lines.append(line)
                averaged_stepover_lines = fit_lines(surface_stepover_lines, axis='x')
            else:
                initial_stepover_lines, stepover_lines = extract_lines(moved_points, initial_stepover, stepover, tolerance, axis='x')
                averaged_initial_stepover_lines = fit_lines(initial_stepover_lines, axis='x')
                averaged_stepover_lines = fit_lines(stepover_lines, axis='x')

            all_lines.extend(averaged_initial_stepover_lines)
            all_lines.extend(averaged_stepover_lines)

            if len(averaged_initial_stepover_lines) > 0:
                initial_stepover_cloud = o3d.geometry.PointCloud()
                initial_stepover_cloud.points = o3d.utility.Vector3dVector(averaged_initial_stepover_lines)
                initial_stepover_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
                geometries.append(initial_stepover_cloud)

            if len(averaged_stepover_lines) > 0:
                point_cloud = o3d.geometry.PointCloud()
                point_cloud.points = o3d.utility.Vector3dVector(averaged_stepover_lines)
                point_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
                geometries.append(point_cloud)

            if cross_cut_enabled:
                cross_initial_stepover_lines, cross_stepover_lines = extract_lines(moved_points, initial_stepover, stepover, tolerance, axis='y')
                averaged_initial_cross_cut_lines = fit_lines(cross_initial_stepover_lines, axis='y')
                averaged_cross_cut_lines = fit_lines(cross_stepover_lines, axis='y')

                all_lines.extend(averaged_initial_cross_cut_lines)
                all_lines.extend(averaged_cross_cut_lines)

                if len(averaged_initial_cross_cut_lines) > 0:
                    initial_cross_cut_cloud = o3d.geometry.PointCloud()
                    initial_cross_cut_cloud.points = o3d.utility.Vector3dVector(averaged_initial_cross_cut_lines)
                    initial_cross_cut_cloud.paint_uniform_color([0, 1, 0])  # Set all points to green
                    geometries.append(initial_cross_cut_cloud)

                if len(averaged_cross_cut_lines) > 0:
                    cross_cut_cloud = o3d.geometry.PointCloud()
                    cross_cut_cloud.points = o3d.utility.Vector3dVector(averaged_cross_cut_lines)
                    cross_cut_cloud.paint_uniform_color([0, 0, 1])  # Set all points to blue
                    geometries.append(cross_cut_cloud)

        line_counter += 1

    print(f"Line Counter: {line_counter}")

    # Save the ordered lines to a file
    with open('ordered_lines.txt', 'w') as f:
        for line in all_lines:
            line_str = ','.join(map(str, line))
            f.write(line_str + '\n')

    # Visualize the points
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    for geometry in geometries:
        vis.add_geometry(geometry)
    
    # Set fixed camera view if the file exists
    camera_view_file = "camera_view.json"
    if os.path.exists(camera_view_file):
        try:
            ctr = vis.get_view_control()
            parameters = o3d.io.read_pinhole_camera_parameters(camera_view_file)
            ctr.convert_from_pinhole_camera_parameters(parameters)
        except Exception as e:
            print(f"Failed to set camera parameters: {e}")
    
    vis.run()
    vis.destroy_window()

def extract_lines(points, initial_stepover, stepover, tolerance, axis='x'):
    if points.shape[0] == 0:
        return [], []
    
    initial_lines = []
    lines = []

    if axis == 'x':
        min_val, max_val = np.min(points[:, 0]), np.max(points[:, 0])
        initial_stepover_values = [min_val + initial_stepover, max_val - initial_stepover]
        if stepover > 0:
            stepover_values = np.arange(min_val + initial_stepover + stepover, max_val - stepover, stepover)
        else:
            stepover_values = []

        for val in initial_stepover_values:
            mask = np.abs(points[:, 0] - val) < tolerance
            line = points[mask]
            if line.shape[0] > 0:
                initial_lines.append(line)

        for val in stepover_values:
            mask = np.abs(points[:, 0] - val) < tolerance
            line = points[mask]
            if line.shape[0] > 0:
                lines.append(line)
                
    elif axis == 'y':
        min_val, max_val = np.min(points[:, 1]), np.max(points[:, 1])
        initial_stepover_values = [min_val + initial_stepover, max_val - initial_stepover]
        if stepover > 0:
            stepover_values = np.arange(min_val + initial_stepover + stepover, max_val - stepover, stepover)
        else:
            stepover_values = []

        for val in initial_stepover_values:
            mask = np.abs(points[:, 1] - val) < tolerance
            line = points[mask]
            if line.shape[0] > 0:
                initial_lines.append(line)

        for val in stepover_values:
            mask = np.abs(points[:, 1] - val) < tolerance
            line = points[mask]
            if line.shape[0] > 0:
                lines.append(line)
    
    return initial_lines, lines

def fit_lines(lines, axis='x'):
    fitted_points = []
    for line in lines:
        if line.shape[0] > 0:
            if axis == 'x':
                y = line[:, 1].reshape(-1, 1)
                z = line[:, 2]
                reg = LinearRegression().fit(y, z)
                y_min, y_max = np.min(y), np.max(y)
                y_fit = np.linspace(y_min, y_max, num=100).reshape(-1, 1)
                z_fit = reg.predict(y_fit)
                for y_val, z_val in zip(y_fit, z_fit):
                    fitted_points.append([line[0, 0], y_val[0], z_val])
            elif axis == 'y':
                x = line[:, 0].reshape(-1, 1)
                z = line[:, 2]
                reg = LinearRegression().fit(x, z)
                x_min, x_max = np.min(x), np.max(x)
                x_fit = np.linspace(x_min, x_max, num=100).reshape(-1, 1)
                z_fit = reg.predict(x_fit)
                for x_val, z_val in zip(x_fit, z_fit):
                    fitted_points.append([x_val[0], line[0, 1], z_val])
    return fitted_points

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

# Instep Options
label_instep_option = tk.Label(root, text="Instep Option:")
label_instep_option.grid(row=12, column=0, padx=10, pady=5, sticky=tk.W)

instep_option_var = tk.StringVar(value="No Instep")
instep_option_menu = ttk.OptionMenu(root, instep_option_var, "No Instep", "No Instep", "Custom")
instep_option_menu.grid(row=12, column=1, padx=10, pady=5)

spin_instep_custom = tk.Spinbox(root, from_=0.0, to=100.0, increment=1.0, state="disabled")
spin_instep_custom.grid(row=12, column=2, padx=10, pady=5)
label_instep_custom_percent = tk.Label(root, text="% of instep")
label_instep_custom_percent.grid(row=12, column=3, padx=10, pady=5, sticky=tk.W)

def instep_option_changed(*args):
    if instep_option_var.get() == "Custom":
        spin_instep_custom.config(state="normal")
    else:
        spin_instep_custom.config(state="disabled")

instep_option_var.trace("w", instep_option_changed)

# Maximum Grind Width Display
label_max_grind_width = tk.Label(root, text="Maximum Grind Width (in):")
label_max_grind_width.grid(row=13, column=0, padx=10, pady=5, sticky=tk.W)

label_max_grind_width_value = tk.Label(root, text="0.00")
label_max_grind_width_value.grid(row=13, column=1, padx=10, pady=5, sticky=tk.W)

# Instep Display
label_instep = tk.Label(root, text="Instep (in):")
label_instep.grid(row=14, column=0, padx=10, pady=5, sticky=tk.W)

label_instep_value = tk.Label(root, text="0.00")
label_instep_value.grid(row=14, column=1, padx=10, pady=5, sticky=tk.W)

# Stepover Display
label_stepover = tk.Label(root, text="Stepover (in):")
label_stepover.grid(row=15, column=0, padx=10, pady=5, sticky=tk.W)

label_stepover_value = tk.Label(root, text="0.00")
label_stepover_value.grid(row=15, column=1, padx=10, pady=5, sticky=tk.W)

# Tolerance Display
label_tolerance = tk.Label(root, text="Tolerance (in):")
label_tolerance.grid(row=16, column=0, padx=10, pady=5, sticky=tk.W)

label_tolerance_value = tk.Label(root, text="0.00")
label_tolerance_value.grid(row=16, column=1, padx=10, pady=5, sticky=tk.W)

# Invert Normals Toggle
invert_normals_var = tk.IntVar()
invert_normals_checkbox = tk.Checkbutton(root, text="Invert Normals", variable=invert_normals_var)
invert_normals_checkbox.grid(row=17, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

# Normal Selection Options
label_normal_selection = tk.Label(root, text="Normal Selection:")
label_normal_selection.grid(row=18, column=0, padx=10, pady=5, sticky=tk.W)

normal_selection_var = tk.StringVar(value="Global")
normal_selection_menu = ttk.OptionMenu(root, normal_selection_var, "Global", "Global", "Regional")
normal_selection_menu.grid(row=18, column=1, padx=10, pady=5)

# Resolution Type Options
label_resolution_type = tk.Label(root, text="Resolution Type:")
label_resolution_type.grid(row=19, column=0, padx=10, pady=5, sticky=tk.W)

resolution_type_var = tk.StringVar(value="By Scallop")
resolution_type_menu = ttk.OptionMenu(root, resolution_type_var, "By Scallop", "By Scallop", "Line Count")
resolution_type_menu.grid(row=19, column=1, padx=10, pady=5)

# Line Count
label_line_count = tk.Label(root, text="Line Count:")
label_line_count.grid(row=20, column=0, padx=10, pady=5, sticky=tk.W)

spin_line_count = tk.Spinbox(root, from_=1, to=1000, increment=1)
spin_line_count.grid(row=20, column=1, padx=10, pady=5)

button_start = tk.Button(root, text="Start", command=start_processing)
button_start.grid(row=21, column=0, columnspan=3, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()
