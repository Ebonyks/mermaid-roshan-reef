import bpy, sys, math
from mathutils import Vector
glb=sys.argv[sys.argv.index("--")+1]; out=sys.argv[sys.argv.index("--")+2]; ang=float(sys.argv[sys.argv.index("--")+3])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
# bounds first (for outline thickness)
mins=Vector((1e9,)*3); maxs=Vector((-1e9,)*3)
meshes=[o for o in bpy.data.objects if o.type=='MESH']
for o in meshes:
    for c in o.bound_box:
        w=o.matrix_world@Vector(c)
        for i in range(3): mins[i]=min(mins[i],w[i]); maxs[i]=max(maxs[i],w[i])
ctr=(mins+maxs)/2; size=maxs-mins; maxdim=max(size); r=max(size.x,size.z); h=size.y
# black outline material (emission so it ignores light)
ink=bpy.data.materials.new("ink"); ink.use_nodes=True
nt=ink.node_tree; [nt.nodes.remove(n) for n in list(nt.nodes)]
em=nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value=(0,0,0,1)
tr=nt.nodes.new("ShaderNodeBsdfTransparent")
geo=nt.nodes.new("ShaderNodeNewGeometry")
mix=nt.nodes.new("ShaderNodeMixShader")
nt.links.new(geo.outputs["Backfacing"],mix.inputs[0])
nt.links.new(tr.outputs[0],mix.inputs[1])   # front faces -> transparent
nt.links.new(em.outputs[0],mix.inputs[2])   # back faces  -> black ink
mo=nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(mix.outputs[0],mo.inputs[0])
# toon-ify + inverted-hull outline per mesh
for o in meshes:
    for mat in [m for m in o.data.materials if m and m.use_nodes]:
        nt2=mat.node_tree; bsdf=nt2.nodes.get("Principled BSDF")
        outn=next((n for n in nt2.nodes if n.type=='OUTPUT_MATERIAL'),None)
        if not outn: continue
        src=None
        if bsdf:
            l=next((l for l in nt2.links if l.to_node==bsdf and l.to_socket.name=="Base Color"),None)
            if l: src=l.from_socket
        tn=nt2.nodes.new("ShaderNodeBsdfToon"); tn.component='DIFFUSE'
        tn.inputs["Size"].default_value=0.8; tn.inputs["Smooth"].default_value=0.02
        if src: nt2.links.new(src,tn.inputs["Color"])
        elif bsdf: tn.inputs["Color"].default_value=bsdf.inputs["Base Color"].default_value
        nt2.links.new(tn.outputs[0],outn.inputs["Surface"])
    o.data.materials.append(ink)
    blk=len(o.data.materials)-1
    sol=o.modifiers.new("outline","SOLIDIFY")
    sol.thickness=(0.012*maxdim); sol.offset=1.0; sol.use_flip_normals=False
    sol.material_offset=blk; sol.use_rim=False
# camera
rad=math.radians(ang)
cd=bpy.data.cameras.new("c"); cam=bpy.data.objects.new("c",cd); bpy.context.scene.collection.objects.link(cam)
cam.location=ctr+Vector((math.sin(rad)*max(h,r)*2.2,-math.cos(rad)*max(h,r)*2.2,h*0.12))
cam.rotation_euler=(ctr-cam.location).normalized().to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera=cam
for e,rz in [(4.5,30),(2.2,210)]:
    L=bpy.data.lights.new("s",'SUN'); L.energy=e; ob=bpy.data.objects.new("s",L); bpy.context.scene.collection.objects.link(ob); ob.rotation_euler=(math.radians(55),0,math.radians(rz))
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=20
sc.render.resolution_x=560; sc.render.resolution_y=820
sc.world=bpy.data.worlds.new("w"); sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.10,0.32,0.45,1)
sc.render.filepath=out; bpy.ops.render.render(write_still=True); print("RENDERED",out)
