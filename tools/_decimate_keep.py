import bpy, sys, os
argv=sys.argv[sys.argv.index("--")+1:]
src,dst,target=argv[0],argv[1],int(argv[2])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.abspath(src))
ms=[o for o in bpy.data.objects if o.type=="MESH"]
tot=sum(len(o.data.polygons) for o in ms)
if tot>target:
    r=target/tot
    for o in ms:
        md=o.modifiers.new("d","DECIMATE"); md.ratio=r
        dg=bpy.context.evaluated_depsgraph_get()
        nm=bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        o.modifiers.remove(o.modifiers["d"]); old=o.data; o.data=nm; bpy.data.meshes.remove(old)
print("DECIMATED",tot,"->",sum(len(o.data.polygons) for o in ms))
bpy.ops.export_scene.gltf(filepath=os.path.abspath(dst),export_format="GLB",export_yup=True)
print("WROTE",dst,os.path.getsize(os.path.abspath(dst)))
