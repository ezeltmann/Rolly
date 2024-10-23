"""This is a python script for blender (tested on blender 4.2) to find the normals of an object.
The main use of this is to find the normals of the different faces and how it works together.
Could likely be updated to something directly in blender, but that's for a later day.
This must be run in blender, under the "scripting" tag.
"""
import bpy # type: ignore

#How to use:
# Select the object you're working with and select a face in edit mode.
# Set the number to the number on the face of what you're looking at.
# Run the Script, output will go to the windows console output.
# Repeat as necessary.
# Output can go directly into Rolly as a part of the face_dict object.

#Set to the number of the face that you're trying to find the normals to
num = 6

#Sets the mode to object mode, allowing you to look at the selection
bpy.ops.object.mode_set(mode='OBJECT')

obj = bpy.context.active_object
for p in obj.data.polygons:
    if (p.select):
        print(f"{num}:Vec3({p.normal.x},{p.normal.y},{p.normal.z}),")
    
    
bpy.ops.object.mode_set(mode='EDIT')