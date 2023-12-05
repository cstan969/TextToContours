
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# JSON data representing the scene
scene_json = '''
{
  "Scene_info": {
    "Scene_name": "Kittens on a Table",
    "Scene_x_size": 5,
    "Scene_y_size": 3,
    "Scene_z_size": 5
  },
  "Scene_objects_list": [
    {
      "object_name": "Table",
      "object_description": "A standard wooden table",
      "X": 2.25,
      "dX": 1.5,
      "Y": 0,
      "dY": 0.75,
      "Z": 2.25,
      "dZ": 1.5
    },
    {
      "object_name": "Kitten 1",
      "object_description": "A small, playful kitten",
      "X": 2.5,
      "dX": 0.2,
      "Y": 0.75,
      "dY": 0.2,
      "Z": 2.5,
      "dZ": 0.2
    },
    {
      "object_name": "Kitten 2",
      "object_description": "Another small, playful kitten",
      "X": 2.25,
      "dX": 0.2,
      "Y": 0.75,
      "dY": 0.2,
      "Z": 2.75,
      "dZ": 0.2
    },
    {
      "object_name": "Kitten 3",
      "object_description": "A curious little kitten",
      "X": 3,
      "dX": 0.2,
      "Y": 0.75,
      "dY": 0.2,
      "Z": 3,
      "dZ": 0.2
    }
  ]
}
'''

# Parse the JSON data
scene_data = json.loads(scene_json)

# Create a 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Iterate through each object in the scene and plot them
for obj in scene_data["Scene_objects_list"]:
    # Extracting object properties
    x, dx = obj["X"], obj["dX"]
    y, dy = obj["Y"], obj["dY"]
    z, dz = obj["Z"], obj["dZ"]
    
    # Plotting each object as a cube
    # Create a meshgrid for the cube
    xx, yy = np.meshgrid([x, x+dx], [y, y+dy])
    ax.plot_surface(xx, yy, np.full_like(xx, z), alpha=0.5)
    ax.plot_surface(xx, yy, np.full_like(xx, z+dz), alpha=0.5)

    # Plotting the sides
    ax.plot_surface(np.full_like(xx, x), xx, yy, alpha=0.5)
    ax.plot_surface(np.full_like(xx, x+dx), xx, yy, alpha=0.5)

    ax.plot_surface(xx, np.full_like(xx, y), yy, alpha=0.5)
    ax.plot_surface(xx, np.full_like(xx, y+dy), yy, alpha=0.5)

# Setting the axes limits
ax.set_xlim(0, scene_data["Scene_info"]["Scene_x_size"])
ax.set_ylim(0, scene_data["Scene_info"]["Scene_y_size"])
ax.set_zlim(0, scene_data["Scene_info"]["Scene_z_size"])

# Labeling axes
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

# Show the plot
plt.show()