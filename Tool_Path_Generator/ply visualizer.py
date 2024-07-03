import open3d as o3d
import tkinter as tk
from tkinter import filedialog

# Function to browse and load the PLY file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PLY files", "*.ply")])
    if file_path:
        visualize_ply(file_path)

# Function to visualize the PLY file
def visualize_ply(file_path):
    mesh = o3d.io.read_triangle_mesh(file_path)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh])

# Create the main window
root = tk.Tk()
root.title("PLY File Visualizer")

# Create and place the widgets
label_file_path = tk.Label(root, text="Select PLY file:")
label_file_path.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=1, padx=10, pady=5)

# Run the GUI main loop
root.mainloop()
