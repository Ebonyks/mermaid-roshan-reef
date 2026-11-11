"""Verify that the corrected native rig only changes anatomy influences."""
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
import json, math
from rebind_arm import world_rest

here=Path(__file__).resolve().parent
source=here.parent/"revision_08"/"roshan_original.rigby"
output=here/"roshan_arm_rebound.rigby"
def hash_file(path): return sha256(path.read_bytes()).hexdigest()
def project(path):
    with ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==len(set(names))
        return (json.loads(z.read("project.json")),
                {name:sha256(z.read(name)).hexdigest() for name in names if name!="project.json"})
old, source_art=project(source)
new, rebound_art=project(output)
assert source_art==rebound_art
edits=[]
rest=world_rest(old["bones"])
def bind_point(rows):
    points=[]
    for w in rows:
        bx,by,a=rest[w["bone"]]
        c,s=math.cos(a),math.sin(a)
        x,y=w["x"],w["y"]
        points.append(((bx+c*x-s*y)*w["weight"],(by+s*x+c*y)*w["weight"]))
    return tuple(math.fsum(p[i] for p in points) for i in (0,1))
def compare(a,b,path=()):
    assert type(a)==type(b),path
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for key in a:
            if key=="weights" and a.get("type")=="mesh" and a.get("name")=="anatomy":
                assert len(a[key])==len(b[key]),path
                changed=[i for i,(old,new) in enumerate(zip(a[key],b[key])) if old!=new]
                for i in changed:
                    row=b[key][i]
                    assert row and len({v["bone"] for v in row})==len(row),(path,i)
                    assert all(0<=v["bone"]<17 and v["weight"]>0 and
                               all(math.isfinite(v[k]) for k in ("weight","x","y")) for v in row),(path,i)
                    assert abs(sum(v["weight"] for v in row)-1)<1e-8,(path,i)
                if changed:
                    rest_delta=max(math.dist(bind_point(a[key][i]),bind_point(b[key][i])) for i in changed)
                    assert rest_delta<1e-8,(path,rest_delta)
                    edits.append({"attachment":list(path),"vertex_count":len(changed),"bind_position_delta":rest_delta})
            else: compare(a[key],b[key],(*path,key))
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)): compare(x,y,(*path,i))
    else: assert a==b,path
compare(old,new)
assert edits
receipt={"source_sha256":hash_file(source),"derived_sha256":hash_file(output),
         "edited_anatomy_influences":edits,"unchanged_source_art":source_art,
         "same_skeleton_slots_skins_keys_uvs_triangles":True}
(here/"binding_verification.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt))
