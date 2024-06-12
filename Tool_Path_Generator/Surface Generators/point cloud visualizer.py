import numpy as np
import open3d as o3d
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

#######################################
# Create GUI for selecting file and grind parameters
def browse_file():
    file_path = filedialog.askopenfilename()
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def start_processing():
    file_path = entry_file_path.get()
    
    # Load point cloud data
    points = np.loadtxt(file_path, delimiter=',')
    
    # Convert points to Open3D point cloud format
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points[:, :3])
    
    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud])

# Create main window
root = tk.Tk()
root.title("Tool Path Generator")

# Frame for file selection
frame_file = ttk.Frame(root, padding="10")
frame_file.grid(row=0, column=0, sticky="ew")

label_file = ttk.Label(frame_file, text="Select Scan Data:")
label_file.grid(row=0, column=0, padx=(0, 5))

entry_file_path = ttk.Entry(frame_file, width=40)
entry_file_path.grid(row=0, column=1)

button_browse = ttk.Button(frame_file, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2)

# Start Processing Button
button_process = ttk.Button(root, text="Process", command=start_processing)
button_process.grid(row=2, column=0, pady=10)

root.mainloop()
