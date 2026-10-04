import bpy, json, math, sys
from pathlib import Path

# Usage: blender -b --python blender/scene_v02.py -- --angle 45 --output /tmp/blindlab_v02.blend
argv=sys.argv
angle=45.0
output="//blindlab_v02.blend"
if "--" in argv:
    tail=argv[argv.index("--")+1:]
    for i,a in enumerate(tail):
        if a=="--angle" and i+1<len(tail): angle=float(tail[i+1])
        if a=="--output" and i+1<len(tail): output=tail[i+1]

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_cube_add(location=(0,0,1.5),scale=(1.5,0.08,1.5))
bpy.context.object.name="WindowFrame"
for i in range(24):
    z=0.05+i*0.06
    bpy.ops.mesh.primitive_cube_add(location=(0,0,z),scale=(1.35,0.025,0.018))
    s=bpy.context.object; s.name=f"Slat_{i:02d}"; s.rotation_euler[0]=math.radians(angle)
bpy.ops.mesh.primitive_plane_add(size=8,location=(0,0,0))
bpy.ops.object.light_add(type="SUN",location=(3,-4,5))
sun=bpy.context.object; sun.name="ExperimentSun"; sun.data.energy=3.0
sun.rotation_euler=(math.radians(35),math.radians(-20),math.radians(25))
bpy.ops.object.camera_add(location=(4,-5,3.2),rotation=(math.radians(68),0,math.radians(38)))
bpy.context.scene.camera=bpy.context.object
bpy.context.scene.render.resolution_x=900; bpy.context.scene.render.resolution_y=600
bpy.context.scene.render.resolution_percentage=100
bpy.context.scene.render.filepath="//blindlab_v02.png"
bpy.ops.wm.save_as_mainfile(filepath=output)
print(f"BlindLab v0.2 scene created angle={angle} output={output}")
