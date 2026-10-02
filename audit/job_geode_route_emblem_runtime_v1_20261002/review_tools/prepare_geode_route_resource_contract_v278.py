from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
p=f/'resource_contract.gd';assert not p.exists();s='''extends SceneTree
## Read-only actual loader/catalog validation for the atlas reuse.
func _initialize() -> void:
\tvar errors: PackedStringArray = OperaHotspotCatalog.validate_specs()
\tassert(errors.is_empty(), str(errors))
\tvar source: Texture2D = load("res://assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png") as Texture2D
\tvar direct: AtlasTexture = load("res://assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres") as AtlasTexture
\tvar relative: AtlasTexture = load("res://assets/opera/worlds/props/../geology/coherent_geode_v1_20261002/open_geode.tres") as AtlasTexture
\tassert(source != null and direct != null and relative != null)
\tassert(direct.atlas == source and relative.atlas == source)
\tassert(direct.region == relative.region)
\tassert(source.get_size() == Vector2(2048, 1024))
\tassert(source.get_image().get_format() == Image.FORMAT_RGBA8)
\tvar spec: Dictionary = OperaHotspotCatalog.spec("geologist", "GEODE")
\tassert(String(spec.path) == source.resource_path)
\tvar size: Vector2 = spec.size as Vector2
\tvar region: Rect2 = spec.region as Rect2
\tassert(absf(size.x / size.y - region.size.x / region.size.y) < 0.001)
\tvar result: Dictionary = {"status":"PASS_UNRELAXED_CATALOG_AND_SHARED_ATLAS_CACHE", "catalog_errors":errors, "source_path":source.resource_path, "source_size":[source.get_width(),source.get_height()], "source_format":"RGBA8", "nominal_decoded_bytes":8388608, "shared_source_rid":source.get_rid().get_id(), "direct_atlas_rid":direct.atlas.get_rid().get_id(), "goal_relative_atlas_rid":relative.atlas.get_rid().get_id(), "same_cached_texture":direct.atlas == source and relative.atlas == source, "direct_and_goal_region":str(direct.region), "closed_invitation_region":str(region), "invitation_size":str(size), "qualification":"Actual Godot4.7.2 headless ResourceLoader identity and existing whole catalog alpha/dimension/aspect/role checks. Nominal RGBA8 bytes are not physical device VRAM/fps or complete mounted acceptance."}
\tvar file := FileAccess.open("res://audit/job_geode_route_emblem_runtime_v1_20261002/RESOURCE_CONTRACT.json", FileAccess.WRITE)
\tassert(file != null)
\tfile.store_string(JSON.stringify(result, "\\t") + "\\n")
\tfile.close()
\tprint("GEODE_RESOURCE_CONTRACT|PASS|shared atlas 8MiB|catalog unchanged gates")
\tquit(0)
''';p.write_text(s,encoding='utf-8',newline='\n')
p=f/'review_tools/run_geode_route_gates_v276.py';s=p.read_text();old='assert action in commands';new='commands["contract"] = [godot, "--headless", "--path", str(r), "--script", "audit/job_geode_route_emblem_runtime_v1_20261002/resource_contract.gd"]\n'+old;assert old in s;s=s.replace(old,new);p.write_text(s,encoding='utf-8',newline='\n');compile(s,str(p),'exec')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}|{(f/'RESOURCE_CONTRACT.json').relative_to(b).as_posix()});ip.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared read-only actual loader/cache and unrelaxed alpha/aspect contract; device budget remains separate.',flush=True)
