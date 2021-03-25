import bpy

def make_tube():
    obj_original = bpy.context.object
    # Separate the selected mesh elements (hopefully the user selected some edges!)
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Get the object that was created from the selected parts
    obj_tube = bpy.context.selected_objects[1]
    bpy.ops.object.select_all(action='DESELECT')
    # Set this to the active object
    obj_tube.select_set(True)
    bpy.context.view_layer.objects.active = obj_tube
    # Enter edit mode and run bevel
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bevel(offset_type='PERCENT', offset_pct=25.0, segments=4, vertex_only=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    # Convert to a curve
    bpy.ops.object.convert(target='CURVE')
    bpy.context.object.data.bevel_depth = 0.1
    bpy.context.object.data.bevel_resolution = 2
    bpy.ops.object.shade_smooth()
    bpy.ops.object.convert(target='MESH')
    # Join back to the original object
    obj_original.select_set(True)
    bpy.context.view_layer.objects.active = obj_original
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')

make_tube()
