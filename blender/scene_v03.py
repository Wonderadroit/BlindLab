"""BlindLab v0.3: presentation-grade, physically-inspired room render.

This is a visual validation layer, not calibrated photometry. The mathematical
optimizer remains the source of the requested blind angle; Blender renders the
same configuration so the visual result can be inspected and compared.
Usage:
  blender -b --python blender/scene_v03.py -- --angle 45 --output artifacts/render.png
"""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector

def arg(name, default):
    argv=sys.argv
    if "--" not in argv:
        return default
    tail=argv[argv.index("--")+1:]
    for i,a in enumerate(tail):
        if a == name and i+1 < len(tail):
            return tail[i+1]
    return default

ANGLE=float(arg("--angle","45"))
OUTPUT=arg("--output","artifacts/blindlab_v03.png")
Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

scene=bpy.context.scene
# Blender 4.0 uses BLENDER_EEVEE; newer Blender releases may use
# BLENDER_EEVEE_NEXT. Prefer the legacy enum when available, with a
# conservative fallback for newer releases.
try:
    scene.render.engine = "BLENDER_EEVEE"
except TypeError:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x=960
scene.render.resolution_y=640
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.world.color=(0.035,0.035,0.035)

def mat(name, base, roughness=0.5, metallic=0.0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*base,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*base,1)
    bs.inputs["Roughness"].default_value=roughness
    bs.inputs["Metallic"].default_value=metallic
    return m

wall=mat("Warm plaster",(0.72,0.68,0.60),0.82)
floor=mat("Oak floor",(0.30,0.16,0.07),0.58)
frame=mat("Dark window frame",(0.035,0.045,0.05),0.28,0.35)
slatmat=mat("Soft white slats",(0.86,0.87,0.84),0.34)
sofa_mat=mat("Sofa fabric",(0.18,0.19,0.20),0.92)
glass=bpy.data.materials.new("Window glass")
glass.use_nodes=True
pbs=glass.node_tree.nodes.get("Principled BSDF")
pbs.inputs["Base Color"].default_value=(0.55,0.65,0.72,1)
pbs.inputs["Roughness"].default_value=0.08
pbs.inputs["Transmission Weight"].default_value=0.55
pbs.inputs["IOR"].default_value=1.45

def cube(name, loc, scale, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new("Soft edges","BEVEL"); mod.width=bevel; mod.segments=3
    o.data.materials.append(material)
    return o

cube("BackWall",(0,1.9,1.6),(3.6,0.10,1.6),wall)
cube("LeftWall",(-3.5,0,1.6),(0.10,2.0,1.6),wall)
cube("Floor",(0,0,0),(3.6,2.0,0.08),floor)

cube("WindowFrameTop",(0,1.73,3.0),(1.65,0.10,0.07),frame,0.025)
cube("WindowFrameBottom",(0,1.73,0.35),(1.65,0.10,0.07),frame,0.025)
cube("WindowFrameLeft",(-1.58,1.73,1.68),(0.07,0.10,1.4),frame,0.025)
cube("WindowFrameRight",(1.58,1.73,1.68),(0.07,0.10,1.4),frame,0.025)
cube("Glass",(0,1.82,1.68),(1.50,0.025,1.25),glass)

count=24
width=2.70
z0=0.48
spacing=2.40/(count-1)
for i in range(count):
    z=z0+i*spacing
    slat=cube(f"Slat_{i:02d}",(0,1.64,z),(width/2,0.055,0.018),slatmat,0.012)
    slat.rotation_euler[0]=math.radians(ANGLE)

cube("SofaBase",(0,-0.35,0.48),(1.35,0.48,0.35),sofa_mat,0.18)
cube("SofaBack",(0,0.05,1.05),(1.35,0.18,0.48),sofa_mat,0.15)
cube("CoffeeTable",(0,-1.05,0.38),(0.85,0.45,0.08),floor,0.04)
for x in (-0.72,0.72):
    cube("TableLeg",(x,-1.05,0.18),(0.06,0.06,0.18),floor,0.02)

bpy.ops.object.light_add(type="AREA",location=(-2.0,-1.0,4.5))
fill=bpy.context.object; fill.name="SoftFill"; fill.data.energy=450; fill.data.shape="DISK"; fill.data.size=4.0
fill.rotation_euler=(math.radians(20),0,math.radians(-25))

bpy.ops.object.light_add(type="SUN",location=(-3,-4,5))
sun=bpy.context.object; sun.name="ExperimentSun"; sun.data.energy=2.8; sun.data.angle=math.radians(1.5)
sun.rotation_euler=(math.radians(28),math.radians(-22),math.radians(-28))

bpy.ops.object.camera_add(location=(4.4,-6.2,2.35))
cam=bpy.context.object
scene.camera=cam
def point_at(obj, target):
    obj.rotation_euler=(Vector(target)-obj.location).to_track_quat("-Z","Y").to_euler()
point_at(cam,(0,0.55,1.45))
cam.data.lens=32

scene.render.filepath=str(Path(OUTPUT).resolve())
scene.view_settings.look="AgX - Medium High Contrast"
bpy.ops.render.render(write_still=True)
Path(str(Path(OUTPUT).with_suffix(".json"))).write_text(
    '{\n  "schema": "blindlab.render.v0.3",\n'
    f'  "angle_deg": {ANGLE},\n  "engine": "BLENDER_EEVEE",\n'
    '  "calibrated_photometry": false\n}\n',
    encoding="utf-8",
)
print(f"BlindLab v0.3 rendered angle={ANGLE} output={OUTPUT}")
