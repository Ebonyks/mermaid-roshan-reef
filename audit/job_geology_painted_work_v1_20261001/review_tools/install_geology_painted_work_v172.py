from pathlib import Path
import hashlib,json,shutil

root=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
family=root/'audit/job_geology_painted_work_v1_20261001'
runtime=root/'assets/opera/worlds/geology/painted_work_v1_20261001'
source=root/'assets_src/imagegen/geologist_painted_rebuild_v1_20261001'
impact=root/'design/audit_impacts/job-geology-painted-work-20261001.json'
assert not family.exists() and not runtime.exists() and not impact.exists()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((root/'design/audit_impacts/job-geode-painted-runtime-20261001.json').read_text())
scope='Continue owner-requested geology rebuild using six existing individually reviewed4.6 painted derivatives at separate runtime paths, preserving original bytes. Mount fossil at its authored aspect, conserved three-piece reconstruction, pan basin/grains/minerals, layered-rock invitation and painted stone work surface. Replace misleading geologist station invitations with matching isolated props using measured AtlasTexture regions; other careers retain unchanged sampling. Keep river diagram/material/soil cover/remote actor acting explicitly pending. Preserve ordinary input, one completion, save schema and all existing regression probes. Review actual four-phase desktop Mobile route at1280/1600 before any acceptance; source finish does not grant complete scene/action acceptance. Archive exact publishedH verification receipts. No release/integration/finding closure.'
write(impact,{'id':'job-geology-painted-work-20261001','baseline':'e1b431f49258eef1d293b11a732353f0a3aa12e9','scope':scope,'rules':old['rules'],'findings':old['findings'],'files':['scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_hotspot_catalog.gd','scripts/opera_world_hotspot_2d.gd','ASSET_LICENSES.md'],'validation':[{'command':'Inventory six exact previously reviewed painted sources; native current mounted review and full official4.7.2 suite','result':'PENDING','evidence':'audit/job_geology_painted_work_v1_20261001/; preserve H full-suite evidence separately'}],'acceptance_gaps':'Room native coverage, river/soil artwork, remote acting, continuous action, complete castle/story/training entry, device/child/owner and comprehensive all-job report remain open.'})
family.mkdir();(family/'.gdignore').write_text('',encoding='utf-8');runtime.mkdir(parents=True)
(family/'review_tools').mkdir();shutil.copyfile(__file__,family/'review_tools'/Path(__file__).name)
changed=['scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_hotspot_catalog.gd','scripts/opera_world_hotspot_2d.gd']
write(family/'SOURCE_BEFORE.json',{'baseline':old.get('next_baseline','e1b431f49258eef1d293b11a732353f0a3aa12e9'),'source_files':[{'path':p,'sha256':sha(root/p)} for p in changed],'prior_native_baseline':'audit/job_geode_runtime_v1_20261001/attempt_03/','qualification':'Exact H source and36 directly reviewed native states, before new bindings.'})
copies=[('fossil','fossil/attempt_02/whole_canvas_1024.png',[115,171,802,674]),('pan','washing_pan/attempt_02/whole_canvas_1024.png',[44,75,936,455]),('work_slab','work_surface/attempt_04/whole_canvas_1024.png',[68,332,889,369]),('grain','pan_grain/attempt_01/whole_canvas_1024.png',[228,120,569,439]),('mineral','crystal_reward/attempt_01/whole_canvas_1024.png',[231,130,569,767]),('layered_rock','layered_rock/attempt_01/whole_canvas_1024.png',[120,188,800,674])]
records=[]
for name,src,region in copies:
 target=runtime/(name+'.png');shutil.copyfile(source/src,target)
 assert sha(target)==sha(source/src)
 records.append({'id':name,'source_path':(source/src).relative_to(root).as_posix(),'runtime_path':target.relative_to(root).as_posix(),'sha256':sha(target),'atlas_region':region,'source_score':4.6,'mounted_score':None,'pixel_modifications':'None; exact byte copy. Atlas region is runtime sampling only.','owner_acceptance':None})
write(family/'PROVENANCE.json',{'status':'SIX_REVIEWED_EXACT_SOURCE_COPIES_MOUNTED_REVIEW_PENDING','assets':records,'protected_originals_changed':False,'new_generations':0})
receipt=family/'geode_runtime_remote_verified_h';receipt.mkdir()
for dirname,names in [('geode_runtime_remote_v164',['RESULT.json','VERIFICATION_JOURNAL.jsonl']),('geode_runtime_publish_v164',['RECEIPT.json','COMMIT_MESSAGE.txt','push.stdout.log','push.stderr.log'])]:
 for name in names:
  p=root/'tmp'/dirname/name
  if p.is_file():shutil.copyfile(p,receipt/(dirname+'_'+name))
def edit(rel,fn):
 p=root/rel;s=p.read_text(encoding='utf-8');p.write_text(fn(s),encoding='utf-8',newline='\n')
def surface(s):
 s=s.replace('const FOSSIL_TARGET_RECT := Rect2(610.0, 205.0, 390.0, 234.0)','const FOSSIL_ART_WIDTH := 234.0 * 802.0 / 674.0\nconst FOSSIL_TARGET_RECT := Rect2(805.0 - FOSSIL_ART_WIDTH * 0.5, 205.0, FOSSIL_ART_WIDTH, 234.0)')
 s=s.replace('const FOSSIL_PIECE_SIZE := Vector2(130.0, 234.0)','const FOSSIL_PIECE_SIZE := Vector2(FOSSIL_ART_WIDTH / 3.0, 234.0)')
 s=s.replace('const FOSSIL_PATH := "res://assets/opera/worlds/hotspots/geologist_fossil.svg"','const WORK_ART := "res://assets/opera/worlds/geology/painted_work_v1_20261001/"\nconst FOSSIL_PATH := WORK_ART + "fossil.png"')
 s=s.replace('const ROCK_PATH := "res://assets/opera/worlds/hotspots/geologist_layered_rock.svg"','const ROCK_PATH := WORK_ART + "layered_rock.png"')
 s=s.replace('const PAN_PATH := ""','const PAN_PATH := WORK_ART + "pan.png"').replace('const CRYSTALS_PATH := "res://assets/opera/worlds/props/goal_geologist.svg"','const CRYSTALS_PATH := WORK_ART + "mineral.png"')
 s=s.replace('var crystals_texture: Texture2D = null','var crystals_texture: Texture2D = null\nvar _work_slab_texture: Texture2D = null\nvar _pan_grain_texture: Texture2D = null')
 s=s.replace('fossil_texture = _optional_texture(FOSSIL_PATH)','fossil_texture = _geode_atlas(FOSSIL_PATH, Rect2(115, 171, 802, 674))')
 s=s.replace('rock_texture = _optional_texture(ROCK_PATH)','rock_texture = _geode_atlas(ROCK_PATH, Rect2(120, 188, 800, 674))')
 s=s.replace('pan_texture = _optional_texture(PAN_PATH)','pan_texture = _geode_atlas(PAN_PATH, Rect2(44, 75, 936, 455))')
 s=s.replace('crystals_texture = _optional_texture(CRYSTALS_PATH)','crystals_texture = _geode_atlas(CRYSTALS_PATH, Rect2(231, 130, 569, 767))\n\t_work_slab_texture = _geode_atlas(WORK_ART + "work_slab.png", Rect2(68, 332, 889, 369))\n\t_pan_grain_texture = _geode_atlas(WORK_ART + "grain.png", Rect2(228, 120, 569, 439))')
 s=s.replace('draw_texture_rect(fossil_texture, rect, false, tint)','var scale_factor := minf(rect.size.x / fossil_texture.get_width(),\n\t\t\trect.size.y / fossil_texture.get_height())\n\t\tvar fit_size := fossil_texture.get_size() * scale_factor\n\t\tdraw_texture_rect(fossil_texture, Rect2(rect.get_center() - fit_size * 0.5,\n\t\t\tfit_size), false, tint)')
 a=s.index('func _draw_pan() -> void:');z=s.index('\n\nfunc _geode_atlas',a)
 s=s[:a]+'''func _draw_pan() -> void:
	if pan_texture == null or _pan_grain_texture == null or crystals_texture == null:
		return
	var ratio := pan_texture.get_width() / float(pan_texture.get_height())
	var fit_size := Vector2(PAN_RECT.size.x, PAN_RECT.size.x / ratio)
	var rect := Rect2(PAN_RECT.get_center() + Vector2(pan_visual_x, 0.0)
		- fit_size * 0.5, fit_size)
	draw_texture_rect(pan_texture, rect, false)
	var water_center := rect.position + fit_size * Vector2(0.50, 0.44)
	var grain_count := maxi(3, 20 - floori(pan_wash * 17.0))
	for index in range(grain_count):
		var angle := float(index) * 2.399
		var radial := sqrt((float(index) + 0.5) / float(grain_count))
		var grain_pos := water_center \\
			+ Vector2(cos(angle) * 122.0, sin(angle) * 31.0) * radial
		grain_pos.x += pan_visual_x * 0.12 \\
			+ sin(float(index) + pan_visual_x * 0.02) * 6.0
		var grain_size := Vector2(15.0 * _pan_grain_texture.get_width()
			/ float(_pan_grain_texture.get_height()), 15.0)
		draw_texture_rect(_pan_grain_texture,
			Rect2(grain_pos - grain_size * 0.5, grain_size), false)
	for index in range(pan_minerals):
		var mineral_size := Vector2(68.0 * crystals_texture.get_width()
			/ float(crystals_texture.get_height()), 68.0)
		var base := water_center + Vector2(-82.0 + float(index) * 82.0, 20.0)
		_draw_ellipse(base + Vector2(0.0, -2.0), Vector2(24.0, 6.0),
			Color(0.22, 0.60, 0.65, 0.35), Color(0.57, 0.89, 0.88, 0.72), 2.0)
		draw_texture_rect(crystals_texture,
			Rect2(base - Vector2(mineral_size.x * 0.5, mineral_size.y),
				mineral_size), false)
'''+s[z:]
 s=s.replace('func _draw_work_surface() -> void:\n','''func _draw_work_surface() -> void:
	# River excavation retains its diagram until a matching material is reviewed.
	if mode != "geology_river" and _work_slab_texture != null:
		var slab_width := 1100.0 if mode == "geology_fossil" else 860.0
		var slab_center := Vector2(760.0, 450.0) if mode == "geology_fossil" \\
			else Vector2(760.0, 400.0)
		var slab_size := Vector2(slab_width, slab_width
			* _work_slab_texture.get_height() / float(_work_slab_texture.get_width()))
		draw_texture_rect(_work_slab_texture,
			Rect2(slab_center - slab_size * 0.5, slab_size), false)
		return
''')
 s=s.replace('Missing painted geode state:', 'Missing painted geology source:')
 return s
edit('scripts/opera_geology_surface.gd',surface)
def catalog(s):
 a=s.index('\t"geologist": {');z=s.index('\n\t},',a)+4
 specs=[]
 for phase,path,region,size,motion in [('RIVER','painted_work_v1_20261001/layered_rock.png',[120,188,800,674],[142,142*674/800],'pulse'),('FOSSIL','painted_work_v1_20261001/fossil.png',[115,171,802,674],[142,142*674/802],'rock'),('PAN','painted_work_v1_20261001/pan.png',[44,75,936,455],[180,180*455/936],'rock'),('GEODE','painted_geode_v1_20261001/closed.png',[192,213,645,602],[142,142*602/645],'pulse')]:
  specs.append('\t\t"%s": {"path": "res://assets/opera/worlds/geology/%s", "region": Rect2(%s), "motion": "%s", "size": Vector2(%s), "presentation": "overlay"},'%(phase,path,', '.join(map(str,region)),motion,', '.join(map(str,size))))
 s=s[:a]+'\t"geologist": {\n'+'\n'.join(specs)+'\n\t},'+s[z:]
 for oldpath in ['hotspots/geologist_layered_rock.svg','hotspots/geologist_fossil.svg','props/goal_geologist.svg']:
  s='\n'.join(l for l in s.split('\n') if '"res://assets/opera/worlds/'+oldpath+'":' not in l)
 i=s.index('\n}\n',s.index('const ASSET_META'))
 additions='\n'+''.join('\t"res://assets/opera/worlds/geology/%s": {"dimensions": Vector2i(%s), "role": "object"},\n'%(p,dim) for p,dim in [('painted_work_v1_20261001/layered_rock.png','1024, 1024'),('painted_work_v1_20261001/fossil.png','1024, 1024'),('painted_work_v1_20261001/pan.png','1024, 585'),('painted_geode_v1_20261001/closed.png','1024, 1024')])
 s=s[:i]+additions+s[i:]
 s=s.replace('var source_aspect := float(dimensions.x) / float(dimensions.y)','var region: Rect2 = entry.get("region", Rect2()) as Rect2\n\t\t\tif region.has_area() and (region.position.x < 0.0 or region.position.y < 0.0 \\\n\t\t\t\t\tor region.end.x > dimensions.x or region.end.y > dimensions.y):\n\t\t\t\terrors.append("%s samples outside source canvas: %s" % [label, region])\n\t\t\tvar source_size := region.size if region.has_area() else Vector2(dimensions)\n\t\t\tvar source_aspect := source_size.x / source_size.y')
 s=s.replace('or path.begins_with("res://assets/opera/worlds/nursery/baby_")','or path.begins_with("res://assets/opera/worlds/nursery/baby_") \\\n\t\tor path.begins_with("res://assets/opera/worlds/geology/painted_work_v1_20261001/") \\\n\t\tor path == "res://assets/opera/worlds/geology/painted_geode_v1_20261001/closed.png"')
 return s
edit('scripts/opera_hotspot_catalog.gd',catalog)
def hotspot(s):
 s=s.replace('var object_texture: Texture2D = null','var object_texture: Texture2D = null\nvar source_region := Rect2()')
 s=s.replace('func configure_object(texture_path: String, animation_kind: String,\n\t\tvisual_size: Vector2, presentation_kind := "overlay",\n\t\tdisplay_offset := Vector2.ZERO) -> void:','func configure_object(texture_path: String, animation_kind: String,\n\t\tvisual_size: Vector2, presentation_kind := "overlay",\n\t\tdisplay_offset := Vector2.ZERO, authored_region := Rect2()) -> void:')
 a=s.index('func configure_object');z=s.index('\n\nfunc _reframe_to_stage',a)
 sec=s[a:z].replace('\t_reframe_to_stage()','\tsource_region = authored_region\n\tif object_texture != null and source_region.has_area():\n\t\tvar atlas := AtlasTexture.new()\n\t\tatlas.atlas = object_texture\n\t\tatlas.region = source_region\n\t\tobject_texture = atlas\n\tset_meta("source_region", source_region)\n\t_reframe_to_stage()')
 s=s[:a]+sec+s[z:]
 s=s.replace('"source_path": source_path,','"source_path": source_path,\n\t\t"source_region": source_region,')
 return s
edit('scripts/opera_world_hotspot_2d.gd',hotspot)
edit('scripts/opera_career_world_2d.gd',lambda s:s.replace('presentation_name, visual_offset)','presentation_name, visual_offset, spec.get("region", Rect2()) as Rect2)'))
# New capture path preserves H's immutable native views and capture script.
capture=(root/'tools/capture_geode_runtime_route.gd').read_text(encoding='utf-8')
capture=capture.replace('res://audit/job_geode_runtime_v1_20261001/attempt_03/','res://audit/job_geology_painted_work_v1_20261001/attempt_01/')
assert 'const OUT := "res://audit/job_geology_painted_work_v1_20261001/attempt_01/"' in capture
(family/'capture_geology_painted_work.gd').write_text(capture,encoding='utf-8')
(family/'attempt_01').mkdir()
license=root/'ASSET_LICENSES.md'
with license.open('a',encoding='utf-8') as f:
 f.write('\n### Painted geology task bindings — 2026-10-01\n\n| Asset | Source | License / provenance | Modifications |\n|---|---|---|---|\n')
 for r in records:f.write('| `'+r['runtime_path']+'` | `'+r['source_path']+'`; SHA256 '+r['sha256']+' | Owner-commissioned OpenAI ImageGen source; source-family generation provenance retained. No third-party URL. | Exact byte copy; alpha region mounted with AtlasTexture, originals preserved. |\n')
d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()}|{p.relative_to(root).as_posix() for p in runtime.rglob('*') if p.is_file()});write(impact,d)
print('Installed six exact painted source copies and four matching invitation regions; mounted/native review pending.')
