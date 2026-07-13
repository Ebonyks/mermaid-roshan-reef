import bpy, sys, os
argv=sys.argv[sys.argv.index("--")+1:]
src,dst=argv[0],argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(src))
for img in list(bpy.data.images):
    if img.size[0]==0: continue
    if max(img.size)>1024: img.scale(min(img.size[0],1024),min(img.size[1],1024))
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    nt=mat.node_tree
    b=next((n for n in nt.nodes if n.type=="BSDF_PRINCIPLED"),None)
    if b is None: continue
    for s in ("Normal","Metallic","Roughness"):
        so=b.inputs.get(s)
        if so:
            for lk in list(so.links): nt.links.remove(lk)
    b.inputs["Metallic"].default_value=0.0; b.inputs["Roughness"].default_value=0.9
    em=b.inputs.get("Emission Color")
    if em:
        for lk in list(em.links): nt.links.remove(lk)
        em.default_value=(0,0,0,1)
arm=next((o for o in bpy.data.objects if o.type=="ARMATURE"),None)
mesh=max((o for o in bpy.data.objects if o.type=="MESH"),key=lambda o:len(o.data.vertices),default=None)  # largest: skips stray env spheres
bpy.ops.object.select_all(action="DESELECT")
mesh.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active=arm
bpy.ops.export_scene.gltf(filepath=os.path.abspath(dst),export_format="GLB",use_selection=True,
    export_animation_mode="NLA_TRACKS",export_anim_single_armature=False,export_skins=True,export_yup=True,export_apply=False)
print("SHRUNK",dst,os.path.getsize(os.path.abspath(dst)))
acts=[a.name for a in bpy.data.actions]
print("ACTIONS:",acts)
