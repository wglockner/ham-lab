import numpy as np
import matplotlib.pyplot as plt

# Define the radius of the cylinder
radius = 2  # Radius of the cylinder in inches
length = 8  # Half-length of the cylinder in inches (to extend from -8 to 8 inches)

# Define the cylindrical surface function for a cylinder aligned along the x-axis
def cylindrical_surface(theta, x):
    y = radius * np.cos(theta)
    z = radius * np.sin(theta)
    return x, y, z

# Generate points for the cylindrical surface
theta = np.linspace(0, np.pi, 200)  # Half-circle for the cylindrical surface
x = np.linspace(-length, length, 200)  # Extends from -8 to 8 inches
theta, x = np.meshgrid(theta, x)

# Calculate x, y, z values for the cylindrical surface
x, y, z = cylindrical_surface(theta, x)

# Flatten the arrays to create a list of points
points = np.column_stack((x.ravel(), y.ravel(), z.ravel()))

# Save point cloud data to a file
np.savetxt("half_cylindrical_surface_4x1.txt", points, delimiter=",", comments="")

# Visualize the point cloud data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:,0], points[:,1], points[:,2], c=points[:,2], cmap='viridis', marker='.')
ax.set_xlabel('X (inches)')
ax.set_ylabel('Y (inches)')
ax.set_zlabel('Z (inches)')
plt.show()
