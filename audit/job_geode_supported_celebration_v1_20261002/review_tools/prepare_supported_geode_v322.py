from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_geode_supported_celebration_v1_20261002'
assert not f.exists()
f.mkdir();(f/'review_tools').mkdir();(f/'baseline').mkdir()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
assert base=='bc2d14160a3f532895ed95c5db646e8cf0b451ad'
rules=['DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-MED-01','DL-INT-01','DL-INT-02','DL-INT-03','DL-INT-04','DL-INT-06','DL-INT-12','DL-SAVE-01','DL-SAVE-02','DL-QA-01','DL-QA-02','DL-QA-03','DL-QA-06','DL-LAY-07']
scope='Reversible geologist-only celebration support and room-prop reuse. Remove the shared prop bounce only for Geologist; seat the unchanged open-geode painting on the accepted painted stone slab through one geometry owner. Replace the room fossil rectangle/spiral, three empty outlined trays and polygon crystal cluster with the existing painted slab/fossil, one painted panning dish matching the actual PAN task, and mineral cluster. Preserve native PNGs, atlas opening states, input/navigation/mechanics/saves/rewards and every other career. Room background native coverage and actor-work contact remain open; source material scores do not approve mounted relationships.'
paths=['scripts/opera_career_world_2d.gd','scripts/opera_world_backdrop_2d.gd','scripts/opera_geology_surface.gd','assets/opera/worlds/geology/painted_work_v1_20261001/work_slab.png','assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png','assets/opera/worlds/geology/painted_work_v1_20261001/pan.png','assets/opera/worlds/geology/painted_work_v1_20261001/mineral.png','assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png']
inventory=[{'path':p,'sha256':sha(r/p),'bytes':(r/p).stat().st_size,'usage':'unchanged reusable source' if p.endswith('.png') else 'baseline source'} for p in paths]
gaps='Whole room background2.8/failed2048-per-screen native coverage, work contact2.7, clearing3.9, panning3.8, caption4.0, all-job/training/story/physical device/child/owner/final comprehensive acceptance and strict zero-3D remain outstanding. No finding lifecycle closure, integration or release.'
required=['Parser/inference and official Godot4.7.2 import/analyzer','Existing Opera and diegetic navigation probes unchanged','Actual normal Library card, all four intentional phases, earned supported celebration, earned Library return and separate elevator replay/back at1280/1600; every selected still and captured opening/celebration/return frame reviewed individually','Source/crop/cache and stable celebration contact evidence in engine','Fresh unmodified full scripts/ci.sh, exact literal boundary frozen throughout; preserve raw diagnostics','Document authority/development/2D gates; immutable scoped topic publication and anonymous file hash verification']
write(f/'PLAN.json',{'status':'IMPLEMENTATION_AND_FRESH_REVIEW_PENDING','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':base,'scope':scope,'rules':rules,'findings':['MA-PLAY-004','MA-VIS-006','MA-OPERA-012'],'inventory':inventory,'required_evidence':required,'acceptance_gaps':gaps})
impact=r/'design/audit_impacts/job-geode-supported-celebration-20261002.json'
write(impact,{'id':impact.stem,'scope':scope,'baseline':base,'rules':rules,'findings':['MA-PLAY-004','MA-VIS-006','MA-OPERA-012'],'files':['scripts/opera_career_world_2d.gd','scripts/opera_world_backdrop_2d.gd'],'validation':[{'command':x,'result':'PENDING','evidence':f.relative_to(r).as_posix()+'/PLAN.json'} for x in required],'acceptance_gaps':gaps})
(f/'.gdignore').write_text('',encoding='utf-8')
for p in paths[:3]:shutil.copyfile(r/p,f/'baseline'/Path(p).name)
shutil.copyfile(r/'tmp/geology_checkpoint_l_remote_v316/RESULT.json',f/'CHECKPOINT_L_REMOTE_VERIFIED.json')
# One owner supplies the support surface and the vertically centered TextureRect.
p=r/'scripts/opera_world_backdrop_2d.gd';s=p.read_text(encoding='utf-8')
s=s.replace('const SKY_LAGOON_ROOT :=', '''const GEOLOGY_WORK_ART := "res://assets/opera/worlds/geology/painted_work_v1_20261001/"
const GEOLOGY_CELEBRATION_SLAB := Rect2(475.0, 438.0, 330.0, 330.0 * 369.0 / 889.0)
const GEOLOGY_CELEBRATION_CONTACT := Vector2(640.0, 490.0)

const SKY_LAGOON_ROOT :=''')
s=s.replace('var room_variant_tiles: Array[Texture2D] = []','var room_variant_tiles: Array[Texture2D] = []\nvar geology_props: Dictionary = {}')
s=s.replace('\tscene_variant = variant\n', '\tscene_variant = variant\n\tgeology_props.clear()\n\tif career_id == "geologist":\n\t\t_load_geology_props()\n',1)
start=s.index('func _draw_geologist(')
end=s.find('\n\nfunc ',start+5)
assert end==-1, 'This scoped replacement expects _draw_geologist to be the last method.'
s=s[:start]+'''static func geology_celebration_goal_rect(texture: Texture2D) -> Rect2:
\tvar side := 220.0
\tvar painted_height := side * texture.get_height() / float(texture.get_width())
\treturn Rect2(GEOLOGY_CELEBRATION_CONTACT - Vector2(side * 0.5,
\t\t(side + painted_height) * 0.5), Vector2(side, side))


func _load_geology_props() -> void:
\tvar regions := {
\t\t"slab": ["work_slab.png", Rect2(68, 332, 889, 369)],
\t\t"fossil": ["fossil.png", Rect2(115, 171, 802, 674)],
\t\t"pan": ["pan.png", Rect2(44, 75, 936, 455)],
\t\t"mineral": ["mineral.png", Rect2(231, 130, 569, 767)],
\t}
\tfor key: String in regions:
\t\tvar entry: Array = regions[key]
\t\tvar atlas := AtlasTexture.new()
\t\tatlas.atlas = load(GEOLOGY_WORK_ART + String(entry[0])) as Texture2D
\t\tatlas.region = entry[1] as Rect2
\t\tatlas.filter_clip = true
\t\tgeology_props[key] = atlas


func _draw_geology_prop(key: String, destination: Rect2) -> void:
\tvar texture: Texture2D = geology_props.get(key) as Texture2D
\tif texture != null:
\t\tdraw_texture_rect(texture, destination, false)


func _draw_geologist(mid: Color, _accent: Color) -> void:
\t# The broad fallback cave walls remain measured native-background debt.
\t# Painted props reuse the exact specialist source regions and proportions.
\tfor band in range(5):
\t\tvar y := 150.0 + float(band) * 74.0
\t\tvar color := mid.lightened(0.18 - float(band) * 0.055)
\t\tdraw_polyline(PackedVector2Array([
\t\t\tVector2(0, y + 24), Vector2(220, y - 12),
\t\t\tVector2(470, y + 18), Vector2(760, y - 18),
\t\t\tVector2(1040, y + 12), Vector2(1280, y - 10),
\t\t]), color, 34.0)
\tif stage_mode:
\t\t# The opened specimen stays seated throughout the earned curtain call.
\t\t_draw_geology_prop("slab", GEOLOGY_CELEBRATION_SLAB)
\t\treturn
\tif bool(get_meta("geology_work_open", false)):
\t\treturn
\t_draw_geology_prop("slab", Rect2(250.0, 430.0, 250.0, 250.0 * 369.0 / 889.0))
\t_draw_geology_prop("fossil", Rect2(305.0, 402.0, 150.0, 150.0 * 674.0 / 802.0))
\t# One panning dish matches the live PAN gesture; the old empty trays did not.
\t_draw_geology_prop("pan", Rect2(650.0, 427.0, 240.0, 240.0 * 455.0 / 936.0))
\t_draw_geology_prop("mineral", Rect2(1006.0, 320.0, 148.0, 148.0 * 767.0 / 569.0))
'''
p.write_text(s,encoding='utf-8',newline='\n')
p=r/'scripts/opera_career_world_2d.gd';s=p.read_text(encoding='utf-8')
old='\tif curtain_call:\n\t\t# The completed work'
new='''\tif curtain_call:
\t\tif career_id == "geologist" and prop_rect.texture != null:
\t\t\tvar supported := OperaWorldBackdrop2D.geology_celebration_goal_rect(prop_rect.texture)
\t\t\tprop_rect.position = supported.position
\t\t\tprop_rect.size = supported.size
\t\t\tprop_rect.set_meta("anchor_station", "painted_geology_display_slab")
\t\t\tprop_rect.set_meta("support_contact", OperaWorldBackdrop2D.GEOLOGY_CELEBRATION_CONTACT)
\t\t\treturn
\t\t# The completed work'''
assert old in s;s=s.replace(old,new,1)
old='\t\t_bounce_actor(prop_rect, 26.0, 0.48)';assert s.count(old)==1
s=s.replace(old,'\t\tif career_id != "geologist":\n\t\t\t_bounce_actor(prop_rect, 26.0, 0.48)',1)
p.write_text(s,encoding='utf-8',newline='\n')
# Preserve the existing actual-input fixture and expose state-local support data.
capture=(r/'audit/job_geode_route_emblem_runtime_v1_20261002/capture.gd').read_text(encoding='utf-8')
capture=capture.replace('audit/job_geode_route_emblem_runtime_v1_20261002/attempt_02/','audit/job_geode_supported_celebration_v1_20261002/attempt_01/')
capture=capture.replace('"direct_review":false,"scores":{},"owner_acceptance":null}', '"direct_review":false,"scores":{},"owner_acceptance":null,\n\t\t"celebration_stage":is_instance_valid(motion_world) and motion_world.backdrop_node.stage_mode,\n\t\t"goal_position":motion_world.prop_rect.position if is_instance_valid(motion_world) else Vector2.ZERO,\n\t\t"goal_size":motion_world.prop_rect.size if is_instance_valid(motion_world) else Vector2.ZERO,\n\t\t"goal_anchor":motion_world.prop_rect.get_meta("anchor_station", "") if is_instance_valid(motion_world) else ""}')
(f/'capture.gd').write_text(capture,encoding='utf-8',newline='\n')
contract='''extends SceneTree

func _initialize() -> void:
\tvar backdrop := OperaWorldBackdrop2D.new()
\tbackdrop.setup("geologist")
\tassert(backdrop.geology_props.size() == 4)
\tvar goal := load("res://assets/opera/worlds/geology/coherent_geode_v1_20261002/open_geode.tres") as AtlasTexture
\tvar destination := OperaWorldBackdrop2D.geology_celebration_goal_rect(goal)
\tvar height := destination.size.x * goal.get_height() / float(goal.get_width())
\tvar bottom := destination.position.y + (destination.size.y + height) * 0.5
\tassert(is_equal_approx(bottom, OperaWorldBackdrop2D.GEOLOGY_CELEBRATION_CONTACT.y))
\tfor key: String in backdrop.geology_props:
\t\tvar texture: AtlasTexture = backdrop.geology_props[key] as AtlasTexture
\t\tassert(texture.filter_clip)
\t\tassert(texture.atlas == load(texture.atlas.resource_path))
\tbackdrop.free()
\tprint("SUPPORTED_GEODE_RESOURCE_CONTRACT|PASS|4_SHARED_PAINTED_CROPS_AND_GEODE_BASE_CONTACT")
\tquit(0)
'''
(f/'resource_contract.gd').write_text(contract,encoding='utf-8',newline='\n')
# Copy runners to the new family; no older receipt or source is overwritten.
old=(r/'audit/job_geode_route_emblem_runtime_v1_20261002/review_tools/run_geode_route_gates_v276.py').read_text(encoding='utf-8')
old=old.replace('job_geode_route_emblem_runtime_v1_20261002','job_geode_supported_celebration_v1_20261002').replace('job-geode-route-emblem-runtime-20261002','job-geode-supported-celebration-20261002').replace('run_geode_route_gates_v276.py','run_supported_geode_gates_v322.py')
old=old.replace("'scripts/castle_career_routes.gd', 'scripts/opera_career_world_2d.gd', 'scripts/opera_hotspot_catalog.gd'", "'scripts/opera_career_world_2d.gd', 'scripts/opera_world_backdrop_2d.gd'")
old=old.replace("'GEODE_RESOURCE_CONTRACT|PASS|'", "'SUPPORTED_GEODE_RESOURCE_CONTRACT|PASS|'").replace(" timeout=360", " timeout=600")
(f/'review_tools/run_supported_geode_gates_v322.py').write_text(old,encoding='utf-8',newline='\n')
ci=(r/'audit/job_geode_route_emblem_runtime_v1_20261002/review_tools/run_geode_route_full_ci_v305.py').read_text(encoding='utf-8')
ci=ci.replace('job_geode_route_emblem_runtime_v1_20261002','job_geode_supported_celebration_v1_20261002').replace('job-geode-route-emblem-runtime-20261002','job-geode-supported-celebration-20261002').replace('full_ci_v2','full_ci_v1').replace('==373','==375').replace('373-file','375-file').replace('same current','same current').replace('full suite2','supported celebration full suite1')
(f/'review_tools/run_supported_geode_full_ci_v322.py').write_text(ci,encoding='utf-8',newline='\n')
snapshot=json.loads((r/'audit/job_geode_route_emblem_runtime_v1_20261002/SOURCE_CURRENT_BEFORE_CAPTURES.json').read_text(encoding='utf-8'))
source_paths=[x['path'] for x in snapshot['source_files']]+[f.relative_to(r).as_posix()+'/'+x for x in ['capture.gd','resource_contract.gd']]
assert len(set(source_paths))==375
snapshot.update(status='CURRENT_LITERAL_SOURCE_SNAPSHOT',baseline=base,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_files=[{'path':p,'sha256':sha(r/p),'bytes':(r/p).stat().st_size} for p in sorted(source_paths)])
write(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json',snapshot)
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
p=r/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8')
old='`SUPPORTING_CURRENT` reversible same authored geode crest/invitation/normal celebration binding at exact published checkpoint `c8f88df058434f1fd1b6d7fade712677003c641a`; source4.5/4.6 does not grant actual route acceptance, fresh gates/full CI pending.'
assert old in s;s=s.replace(old,'`SUPPORTING_HISTORICAL` task baseline `c8f88df058434f1fd1b6d7fade712677003c641a`, published review checkpoint `bc2d14160a3f532895ed95c5db646e8cf0b451ad`; its unmodified full CI2 passes82/82 on373 unchanged literal sources. This dated machine evidence does not transfer to later source changes or grant visual acceptance.')
s+='\n| `audit/job_geode_supported_celebration_v1_20261002/PLAN.json` | 🔵 | `SUPPORTING_CURRENT` reversible painted celebration support and four room-prop reuse at task baseline `bc2d14160a3f532895ed95c5db646e8cf0b451ad`. Fresh source-bound runtime review and full suite pending; source material opinions do not establish supported contact, room/native-coverage or all-job acceptance. |\n'
p.write_text(s,encoding='utf-8',newline='\n')
p=r/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8');s+='\n2026-10-02 scoped reuse: `OperaWorldBackdrop2D` uses the unchanged licensed `painted_work_v1_20261001` work_slab, fossil, pan and mineral PNGs through the same measured AtlasTexture regions already used by the specialist surface. No source pixel, alpha, license or provenance change; normal Geologist celebration reuses the slab and unchanged open-geode atlas. Evidence: `audit/job_geode_supported_celebration_v1_20261002/PLAN.json`.\n';p.write_text(s,encoding='utf-8',newline='\n')
p=r/'.gitattributes';s=p.read_text(encoding='utf-8');s+='\n# Supported-geode review receipts and raw evidence retain literal bytes.\naudit/job_geode_supported_celebration_v1_20261002/** -text\n';p.write_text(s,encoding='utf-8',newline='\n')
# Fail closed on mounted opinions bound to the previous source revision.
res=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B','audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v31.py'],cwd=r,capture_output=True,text=True)
write(f/'BOUNDARY_REFRESH_PRE_REVIEW.json',{'process_exit':res.returncode,'stdout':res.stdout,'stderr':res.stderr,'qualification':'Previous mounted opinions are withheld when their binding boundary changes; new context requires new direct review.'})
assert res.returncode==0
files={p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{'scripts/opera_career_world_2d.gd','scripts/opera_world_backdrop_2d.gd','design/05_DOC_LEDGER.md','ASSET_LICENSES.md','.gitattributes','audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json'}
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(files);write(impact,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(json.loads(allow.read_text(encoding='utf-8')))|files))
print(json.dumps({'status':'REVERSIBLE_SUPPORTED_GEODE_CANDIDATE_PREPARED','baseline':base,'frozen_sources':375,'fresh_review_pending':True,'files':len(files)}))
