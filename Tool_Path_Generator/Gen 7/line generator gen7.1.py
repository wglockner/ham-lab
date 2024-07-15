import numpy as np
import open3d as o3d
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from math import sin, cos, sqrt, radians, acos, pi
import csv
from sklearn.linear_model import LinearRegression
################################################################################################
# Initialize a global mesh for the surface
global_surface_mesh = None

################################################################################################
# Define Utility Functions 
# Function to read surface file
# Read the different file types into an Open3D pcd
def read_surface_file(file_path):
    if file_path.endswith('.ply'):
        pcd = o3d.io.read_surface_file(file_path)
    elif file_path.endswith('.pcd'):
        pcd = o3d.io.read_surface_file(file_path)
    elif file_path.endswith('.csv') or file_path.endswith('.txt'):
        points = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                points.append([float(coord) for coord in row])
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
    else:
        raise ValueError("Unsupported File Type")
    return pcd

# Function to convert surface to mesh
def convert_to_mesh(pcd):
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist
    bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivovting(pcd, o3d.utility.DoubleVector([radius, radius * 2]))
    return bpa_mesh

# Function to display the mesh surface
def display_mesh(mesh):
    o3d.visualization.draw_geometries([mesh])




#################################################################################################
# Define GUI Functions
# Function to browse files; currently supporting .ply, .pcd, and .csv
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Point Cloud Files", "*.ply *.pcd *.csv *.txt")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

# Function to load the surface mesh file
def load_surface_mesh():
    global global_surface_mesh
    file_path = entry_file_path.get()
    if file_path.endwith('.ply'):
        global_surface_mesh = o3d.io.read_triangle_mesh(file_path)
    else:
        pcd = read_surface_file(file_path)
        global_surface_mesh = convert_to_mesh(pcd)

# Function to process and display the mesh. Mesh gets 
def process_and_display():
    global global_surface_mesh
    try:
        display_mesh(global_surface_mesh)
    except Exception as e:
        print(f"Error: {e}")







#################################################################################################
# Create the GUI
# Create Main Window
root = tk.Tk()
root.title("Grind Path Generator")

# Place File Browser Widget
label_file_path =tk.Label(root, text="Select Surface File:")
label_file_path.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=5)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=5)

# Place Stone Diameter Widget
label_initial_stone_diameter = tk.Label(root, text="Stone Diameter (in):")
label_initial_stone_diameter.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

spin_initial_stone_diameter = tk.Spinbox(root, from_=0.0, to=12, increment=.25)
spin_initial_stone_diameter.grid(row=1, column=1, padx=10, pady=5)

# Place Grind Depth Widget
label_grind_depth = tk.Label(root, text="Grind Depth (in):")
label_grind_depth.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

spin_grind_depth = tk.Spinbox(root, from_=0.0, to=10.0, increment=0.1)
spin_grind_depth.grid(row=2, column=1, padx=10, pady=5)








# Place button to process and display the mesh
button_process_and_display = tk.Button(root, text="Generate", command=process_and_display)
button_process_and_display.grid(row=10, column=2, padx=10, pady=5)




######################################################################################################
# Run the GUI Loop
root.mainloop()