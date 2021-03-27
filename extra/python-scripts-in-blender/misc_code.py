# This is here so you can run everything
# from the text editor if you prefer
import bpy

# ----------------------------------------------------------

# Playing Around in the Console
# -----------------------------

# Objects can be accessed directly by name
# and referenced by local variables
obj = bpy.data.objects['Cube']

# Select and deselect objects using select_set
obj.select_set(True)
# The selection state can be accessed with select_get
obj.select_get()
# > True

# All selected objects are stored in a list
bpy.context.selected_objects
# > [bpy.data.objects['Cube']]
# The active object can be accessed directly
bpy.context.object
# > bpy.data.objects['Cube']
# Because bpy.context.object is read-only, setting
# it requires setting a different variable.
bpy.context.view_layer.objects.active = obj


# ----------------------------------------------------------

# Now let's get some properties of this object.
obj.name
# > 'Cube'
# The object type tells us what is stored in obj.data.
# In this case, obj.data is a mesh.
obj.type
# > 'MESH'
obj.location
# > Vector((0, 0, 0))
# We can set the position of the cube easily by modifying its location.
# Watch it move in the 3d view when you enter the commands.
obj.location.z = 3
obj.location.z = 0


# ----------------------------------------------------------

# This little snippet will create four copies
# of the cube (assuming it is still selected).
for i in range(1,5):
    bpy.ops.object.duplicate()
    bpy.ops.transform.translate(value=(0, 2, 0))


# ----------------------------------------------------------

# First Script
# ------------

# Although it's already loaded in the Python console,
# Blender's bpy module must be imported manually in a script.
import bpy

# We can use a generator to get all selected mesh objects
selected_objects = [o for o in bpy.context.selected_objects if o.type == 'MESH']
# Alternatively, we can get all mesh objects in the scene
all_objects = [o for o in bpy.context.scene.objects if  o.type == 'MESH']

for i, obj in enumerate(all_objects):
    obj.name = 'Box_' + str(i+1)
    obj.location.z = i