import math
import bpy

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_cube_add(location=(0,0,1.5),scale=(1.5,0.08,1.5))
bpy.context.object.name="Window"

for i in range(24):
    z=0.25+i*0.105
    bpy.ops.mesh.primitive_cube_add(location=(0,0,z),scale=(1.35,0.025,0.018))
    slat=bpy.context.object
    slat.name=f"Slat_{i:02d}"
    slat.rotation_euler[0]=math.radians(45)

bpy.ops.mesh.primitive_plane_add(size=8,location=(0,0,0))
bpy.ops.object.light_add(type="SUN",location=(3,-4,5))
sun=bpy.context.object
sun.name="ExperimentSun"
sun.rotation_euler=(math.radians(35),math.radians(-20),math.radians(25))
sun.data.energy=3.0
bpy.ops.object.camera_add(location=(4,-5,3.2),rotation=(math.radians(68),0,math.radians(38)))
bpy.context.scene.camera=bpy.context.object
scene=bpy.context.scene
scene.render.resolution_x=900
scene.render.resolution_y=600
scene.render.resolution_percentage=100
scene.render.filepath="//blindlab_v01.png"
bpy.ops.wm.save_as_mainfile(filepath="//blindlab_v01.blend")
print("BlindLab v0.1 scene created.")
