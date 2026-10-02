from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
assert base=='d13a28287ef6916fb9c910de9c07d110ced315c2'
art='assets/opera/worlds/geology/painted_geode_v1_20261001'
audit='audit/job_geode_runtime_v1_20261001'
sources={
 'closed.png':'closed_geode/attempt_01/whole_canvas_1024.png',
 'early_crack.png':'opening_geode/early_crack/attempt_01/whole_canvas_1024.png',
 'middle_open.png':'opening_geode/middle_open/attempt_01/whole_canvas_1024.png',
 'open_embedded.png':'open_geode/attempt_02/whole_canvas_1024.png',
}
source_root='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/'
impact=r/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
planned=['scripts/opera_geology_surface.gd','ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md',
 audit+'/SOURCE_BEFORE.json',audit+'/PROVENANCE.json',audit+'/.gdignore',audit+'/index.html',audit+'/REVIEW.json',audit+'/runtime_gate/RECEIPT.json',
 'audit/job_review_v2_20261001/review_tools/install_geode_runtime_v152.py']
planned += [art+'/'+n+suffix for n in sources for suffix in ['', '.import']]
write(impact,dict(id='job-geode-painted-runtime-20261001',baseline=base,
 scope='Carry four already directly inspected painted geode source states into reversible production Canvas rendering. The named owner gap is empty rock/loose loot instead of rooted interior crystals. Preserve five seam taps,120px drag, save schema, single completion and sibling geology tasks. Preserve existing source originals/rejected drafts. Native source pixels copied byte-for-byte to four new runtime paths; alpha regions expressed only as Godot AtlasTexture. Shared base515 and state-dependent visible right-half bounds drive artwork, pointer and selection together. Ordinary complete career route, passive/cancel/repeat/save/native two-width evidence and exact full suite required. Background/remote actor remain separately open; no general acceptance.',
 rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-INT-01','DL-INT-02','DL-INT-03','DL-INT-04','DL-INT-06','DL-MED-01','DL-READ-02','DL-READ-05','DL-QA-03','DL-QA-06','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-VIS-08'],
 findings=['MA-PLAY-004','MA-VIS-006'],files=sorted(planned),
 validation=[dict(command='Source inventory / existing18-source native register and current source hashes',result='PASS',evidence='assets_src/imagegen/geologist_painted_rebuild_v1_20261001/GENERATED_NATIVE_REGISTER_V6.json; geode source4.6; open attempt01 excluded; G native312 selected static evidence, not current production.'),dict(command='Fresh official4.7.2 import/analyzer/intentional and passive ordinary career route / complete trusted suite',result='PENDING',evidence=audit+'/runtime_gate/RECEIPT.json; new current byte boundary needed before acceptance')],
 acceptance_gaps='Current source4.6 and earlier review-only sequence4.5 provisional do not establish new runtime, full timed action, actor contact, device, child, owner or final comprehensive all-job acceptance. No integration/release or finding closure.'))
(r/audit).mkdir(exist_ok=False)
(r/audit/'.gdignore').write_text('',encoding='utf-8')
tracked=subprocess.check_output(['git','ls-files','-z','scripts','tools','project.godot'],cwd=r).split(b'\0')
files=[p.decode() for p in tracked if p and (p.endswith(b'.gd') or p.endswith(b'.sh') or p==b'project.godot')]
write(r/audit/'SOURCE_BEFORE.json',{'baseline':base,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[{'path':p,'sha256':sha(r/p)} for p in sorted(files)],'qualification':'Before actual geode production edit; all changes later compared, not inherited325-source full-suite approval.'})
(r/art).mkdir(parents=True,exist_ok=False)
provenance=[]
for name,source in sources.items():
 src=r/(source_root+source);dst=r/art/name;shutil.copyfile(src,dst)
 provenance.append({'path':art+'/'+name,'sha256':sha(dst),'source_path':source_root+source,'source_sha256':sha(src),'modifications':'None; exact existing whole-canvas technical derivative bytes copied. Godot AtlasTexture display regions do not alter source pixels.','source_review_score':4.6,'runtime_score':None,'owner_acceptance':None})
write(r/audit/'PROVENANCE.json',{'status':'COPIED_ALREADY_REVIEWED_GEODE_STATES_RUNTIME_REVIEW_PENDING','items':provenance,'generation_method':'Prior built-in ImageGen; no new generation or pixel repair for this placement/binding change.','native_sources_preserved':True,'excluded':'open_geode/attempt_01 and crystal_reward are not geode reveal pixels.','regions':{'closed':[192,213,645,602],'early_crack':[77,85,870,741],'middle_open':[99,70,845,569],'open_left':[53,91,448,501],'open_right':[524,91,448,500]},'acceptance':'No owner/runtime acceptance carried from source scores.'})
p=r/'scripts/opera_geology_surface.gd';s=p.read_text(encoding='utf-8')
s=s.replace('## Approved vectors remain runtime authority until the new raster candidates\n## pass alpha/native-resolution review. Never load rejected checkerboard art.','## Painted geode states reuse reviewed transparent source art. Other geology\n## surfaces retain their independently tracked artwork and contact priorities.')
s=s.replace('const GEODE_PATH := ""',f'const GEODE_ART := "res://{art}/"\nconst GEODE_PATH := GEODE_ART + "closed.png"')
s=s.replace('var geode_texture: Texture2D = null','var geode_texture: Texture2D = null\nvar _geode_crack_texture: Texture2D = null\nvar _geode_middle_texture: Texture2D = null\nvar _geode_open_left_texture: Texture2D = null\nvar _geode_open_right_texture: Texture2D = null')
a=s.index('func geode_half_center() -> Vector2:');b=s.index('\n\n',a)
s=s[:a]+'func geode_half_center() -> Vector2:\n\treturn _geode_right_rect().get_center()'+s[b:]
s=s.replace('\tgeode_texture = _optional_texture(GEODE_PATH)','\tgeode_texture = _geode_atlas(GEODE_PATH, Rect2(192, 213, 645, 602))\n\t_geode_crack_texture = _geode_atlas(GEODE_ART + "early_crack.png",\n\t\tRect2(77, 85, 870, 741))\n\t_geode_middle_texture = _geode_atlas(GEODE_ART + "middle_open.png",\n\t\tRect2(99, 70, 845, 569))\n\t_geode_open_left_texture = _geode_atlas(GEODE_ART + "open_embedded.png",\n\t\tRect2(53, 91, 448, 501))\n\t_geode_open_right_texture = _geode_atlas(GEODE_ART + "open_embedded.png",\n\t\tRect2(524, 91, 448, 500))')
a=s.index('func _geode_right_rect() -> Rect2:');b=s.index('\n\n',a)
s=s[:a]+'''func _geode_right_rect() -> Rect2:
\tif geode_pull >= 90.0 and _geode_open_right_texture != null:
\t\tvar width := 320.0 * _geode_open_right_texture.get_width() \\
\t\t\t/ float(_geode_open_right_texture.get_height())
\t\treturn Rect2(Vector2(GEODE_RECT.get_center().x + geode_pull, 195.0),
\t\t\tVector2(width, 320.0))
\tif geode_pull > 0.0:
\t\tvar texture := _geode_crack_texture if geode_pull < 40.0 else _geode_middle_texture
\t\tif texture != null:
\t\t\tvar pair := _geode_pair_rect(texture, 350.0)
\t\t\treturn Rect2(Vector2(pair.get_center().x, pair.position.y),
\t\t\t\tVector2(pair.size.x * 0.5, pair.size.y))
\treturn Rect2(Vector2(GEODE_RECT.get_center().x + geode_pull,
\t\tGEODE_RECT.position.y), Vector2(GEODE_RECT.size.x * 0.5, GEODE_RECT.size.y))'''+s[b:]
a=s.index('func _draw_geode() -> void:');b=s.index('\n\nfunc _draw_work_surface()',a)
s=s[:a]+'''func _geode_atlas(path: String, region: Rect2) -> Texture2D:
\tvar texture := _optional_texture(path)
\tif texture == null:
\t\tpush_error("Missing painted geode state: " + path)
\t\treturn null
\tvar atlas := AtlasTexture.new()
\tatlas.atlas = texture
\tatlas.region = region
\treturn atlas


func _geode_pair_rect(texture: Texture2D, height: float) -> Rect2:
\tvar size := Vector2(height * texture.get_width() / float(texture.get_height()), height)
\tvar center := Vector2(GEODE_RECT.get_center().x + geode_pull * 0.5,
\t\tGEODE_RECT.end.y - height * 0.5)
\treturn Rect2(center - size * 0.5, size)


func _draw_geode() -> void:
\tif geode_texture == null:
\t\treturn
\tif geode_pull <= 0.0:
\t\tdraw_texture_rect(geode_texture, _geode_pair_rect(geode_texture, 350.0), false)
\t\tfor index: int in range(GEODE_SEAM_SPOTS.size()):
\t\t\tvar done := geode_seams[index]
\t\t\tdraw_circle(GEODE_SEAM_SPOTS[index], 15.0,
\t\t\t\tColor("#8ce6dd") if done else Color("#ffe69a"))
\t\t\tif not done:
\t\t\t\tdraw_arc(GEODE_SEAM_SPOTS[index], 25.0, 0.0, TAU, 24,
\t\t\t\t\tColor(1.0, 0.89, 0.42, 0.56), 4.0, true)
\t\treturn
\tif geode_pull < 90.0:
\t\tvar texture := _geode_crack_texture if geode_pull < 40.0 else _geode_middle_texture
\t\tif texture != null:
\t\t\tdraw_texture_rect(texture, _geode_pair_rect(texture, 350.0), false)
\t\treturn
\t# Each exposed crystal is painted into its own cavity. No loose reward layer.
\tif _geode_open_left_texture == null or _geode_open_right_texture == null:
\t\treturn
\tvar left_width := 320.0 * _geode_open_left_texture.get_width() \\
\t\t/ float(_geode_open_left_texture.get_height())
\tdraw_texture_rect(_geode_open_left_texture,
\t\tRect2(Vector2(GEODE_RECT.get_center().x - left_width, 195.0),
\t\t\tVector2(left_width, 320.0)), false)
\tdraw_texture_rect(_geode_open_right_texture, _geode_right_rect(), false)'''+s[b:]
p.write_text(s,encoding='utf-8',newline='\n')
with (r/'ASSET_LICENSES.md').open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n<!-- Geode actual runtime binding;2026-10-01; four reviewed derivatives copied intact. -->\n')
 for x in provenance:f.write('| `'+x['path']+'` | Built-in ImageGen, owner-commissioned painted geode; OpenAI generated artwork | `'+x['source_path']+'` | Exact source derivative bytes; no new pixel editing; runtime/context acceptance pending. SHA-256 `'+x['sha256']+'`. |\n')
dst=r/'audit/job_review_v2_20261001/review_tools/install_geode_runtime_v152.py';shutil.copyfile(Path(__file__),dst)
print('Prepared four exact runtime files and production geode drawing; impact recorded first. No acceptance carried.')
