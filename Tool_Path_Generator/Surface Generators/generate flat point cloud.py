import numpy as np
import matplotlib.pyplot as plt

# Define the flat surface function (z = constant)
def flat_surface_function(x, y):
    return np.zeros_like(x)

# Generate grid points
x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
x, y = np.meshgrid(x, y)

# Calculate z values for the flat surface
z = flat_surface_function(x, y)

# Flatten the arrays to create a list of points
points = np.column_stack((x.ravel(), y.ravel(), z.ravel()))

# Save point cloud data to a file
np.savetxt("flat_surface.txt", points, delimiter=",", comments="")

# Visualize the point cloud data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2], c=points[:,2], cmap='viridis', marker='.')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
