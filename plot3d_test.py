# class NlpSceneFiller:

#     def __init__(self):
#         pass



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

# Function to create a list of vertices for a cube
def create_cube_vertices(x, y, z, dx, dy, dz):
    return [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz]
    ]

# Function to create cube faces from vertices
def create_cube_faces(vertices):
    return [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]], 
        [vertices[0], vertices[3], vertices[7], vertices[4]], 
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]]
    ]

# Parse the JSON data
scene_data = json.loads(scene_json)

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Iterate through each object in the scene and plot them
for obj in scene_data["Scene_objects_list"]:
    x, dx = obj["X"], obj["dX"]
    y, dy = obj["Y"], obj["dY"]
    z, dz = obj["Z"], obj["dZ"]

    vertices = create_cube_vertices(x, y, z, dx, dy, dz)
    faces = create_cube_faces(vertices)

    # Create a 3D polygon collection
    poly3d = Poly3DCollection(faces, alpha=0.5, edgecolors='k')
    ax.add_collection3d(poly3d)

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