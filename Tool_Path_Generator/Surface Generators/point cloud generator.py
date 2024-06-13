import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the function to generate the curved surface
def surface_function(x, y):
    return -(x**2 + y**2)/200

# Generate grid points
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
x, y = np.meshgrid(x, y)

# Calculate z values based on the surface function
z = surface_function(x, y)

# Flatten the arrays to create a list of points
points = np.column_stack((x.ravel(), y.ravel(), z.ravel()))

# Save point cloud data to a file
np.savetxt("point_cloud.txt", points, delimiter=",", comments="")

# Visualize the point cloud data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2], c=points[:,2], cmap='viridis', marker='.')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
