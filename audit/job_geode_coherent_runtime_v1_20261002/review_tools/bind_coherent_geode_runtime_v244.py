from pathlib import Path
import datetime,hashlib,json,re,shutil,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
remote=read(b/'tmp/geology_checkpoint_j_remote_v242/RESULT.json');assert remote['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
base=subprocess.run(['git','rev-parse','HEAD'],cwd=b,capture_output=True,check=True).stdout.decode().strip()
assert base==remote['revision']
f=b/'audit/job_geode_coherent_runtime_v1_20261002';assert not f.exists();(f/'review_tools').mkdir(parents=True)
(f/'.gdignore').write_text('',encoding='utf-8')
selected=read(b/'assets_src/imagegen/geologist_geode_coherent_states_v1_20261002/SELECTED_PILOT_STATES.json')
source=b/'assets_src/imagegen/geologist_geode_coherent_states_v1_20261002';assets=b/'assets/opera/worlds/geology/coherent_geode_v1_20261002';assert not assets.exists()
sp=b/'scripts/opera_geology_surface.gd';before=sp.read_text();before_sha=sha(sp)
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json'
rules=read(b/'design/audit_impacts/job-geode-coherent-opening-20261002.json')['rules']
planned=['scripts/opera_geology_surface.gd','ASSET_LICENSES.md',f.relative_to(b).as_posix()+'/.gdignore',f.relative_to(b).as_posix()+'/capture.gd',f.relative_to(b).as_posix()+'/PLAN.json',f.relative_to(b).as_posix()+'/BINDING.json',f.relative_to(b).as_posix()+'/MECHANIC_UNCHANGED.json',f.relative_to(b).as_posix()+'/review_tools/'+Path(__file__).name]
planned.extend((assets.relative_to(b).as_posix()+'/'+name+suffix) for name in ['opening_six_states.png','opening_bridge.png'] for suffix in ['','.import'])
write(ip,dict(id='job-geode-coherent-runtime-20261002',scope='Reversibly bind seven individually reviewed authored geode states, exact completePOT copies, stable center/base/aspect; update drawing and right-half hit bounds only to match displayed art. Preserve original four source files and all failed trials. Crystals stay embedded in both mineral cavities through earned completion. Actual production visual sequence and fresh fullCI remain required; ordinary2D state art, no cinematic exception.',baseline=base,rules=rules,findings=['MA-PLAY-004','MA-VIS-006'],files=planned,validation=[dict(command='Current existing art/source inventory and unbound complete pilot',result='PASS',evidence='audit/job_geode_coherent_pilot_v1_20261002/REVIEW.json: every312 frames/26 boards/8 details; provisional object opening4.5, contact2.7/clap4.0 separate. Exact newruntime source/progress/render/fullCI/device/child/owner evidence pending.')],acceptance_gaps='Actual production opening/art/state/contact/celebration; full unmodified current suite; training/story/actual production return/device/child/owner and final comprehensive all-job report. Inclusive4.5 state edge/continuity remains priority. No finding closure, integration or release.'))
write(f/'PLAN.json',dict(baseline=base,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),rules=rules,findings=['MA-PLAY-004','MA-VIS-006'],inventory=[dict(path=p.relative_to(b).as_posix(),sha256=sha(p)) for p in sorted((b/'assets/opera/worlds/geology/painted_geode_v1_20261001').glob('*.png'))],gap='Current actual continuous opening4.2 has abrupt silhouette swaps and top drop. Existing seven-state source pilot4.5 remedies that named defect; reuse these reviewed sheets instead of new generation.',validation='Exact complete source copies, unchanged mechanic/save methods, parser/inference/import/analyzer, actual312 timed frames at both widths and fresh full suite; source/visual/device/child/owner claims separated.'))
# Preserve publication verification receipt and all recovery failures separately.
rf=f/'prior_checkpoint_j_remote_verified';rf.mkdir()
for src in [b/'tmp/geology_checkpoint_j_remote_v242',b/'tmp/geology_checkpoint_j_publish_v242',b/'tmp/geology_checkpoint_j_seal_v241',b/'tmp/geology_checkpoint_j_resume_v243']:
 for p in src.glob('*'):
  if p.is_file():shutil.copyfile(p,rf/(src.name+'_'+p.name))
assets.mkdir(parents=True)
copies=[]
mapping={str((source/'attempt_08/whole_canvas_2048x1024.png').relative_to(b).as_posix()):'opening_six_states.png',str((source/'attempt_10/whole_canvas_2048x1024.png').relative_to(b).as_posix()):'opening_bridge.png'}
for src,name in mapping.items():
 dst=assets/name;shutil.copyfile(b/src,dst);assert sha(dst)==sha(b/src)
 copies.append(dict(source=src,path=dst.relative_to(b).as_posix(),sha256=sha(dst),dimensions=[2048,1024],modification='Exact completePOT whole-canvas byte copy; no crop,alpha repair,subject transformation or recompression. Native originals and prior whole-canvas normalization provenance retained.'))
new=before.replace('const GEODE_ART := "res://assets/opera/worlds/geology/painted_geode_v1_20261001/"\nconst GEODE_PATH := GEODE_ART + "closed.png"','const GEODE_ART := "res://assets/opera/worlds/geology/coherent_geode_v1_20261002/"\nconst GEODE_STATE_PATHS: Array[String] = [\n'+''.join('\tGEODE_ART + "'+mapping[x['path']]+'",\n' for x in selected['states'])+']\nconst GEODE_STATE_REGIONS: Array[Rect2] = [\n'+''.join('\tRect2('+', '.join(f'{v:.12f}' for v in x['region'])+'),\n' for x in selected['states'])+']')
assert new!=before
new=re.sub(r'var _geode_crack_texture: Texture2D = null\nvar _geode_middle_texture: Texture2D = null\nvar _geode_open_left_texture: Texture2D = null\nvar _geode_open_right_texture: Texture2D = null','var _geode_states: Array[Texture2D] = []',new,count=1)
start=new.index('\tgeode_texture = _geode_atlas(');end=new.index('\trock_texture = ',start)
new=new[:start]+'''\t_geode_states.clear()
\tgeode_texture = null
\tif mode == "geology_geode":
\t\tfor index: int in range(GEODE_STATE_PATHS.size()):
\t\t\t_geode_states.append(_geode_atlas(GEODE_STATE_PATHS[index],
\t\t\t\tGEODE_STATE_REGIONS[index]))
\t\tgeode_texture = _geode_states[0]
'''+new[end:]
def replace_func(text,name,body):
 a=text.index('func '+name+'(');z=text.find('\nfunc ',a+5)
 assert z>0
 return text[:a]+body.rstrip()+'\n\n'+text[z+1:]
new=replace_func(new,'_geode_right_rect','''func _geode_state_index() -> int:
\tif geode_pull <= 0.0:
\t\treturn 0
\treturn mini(6, 1 + int(geode_pull / 20.0))


func _geode_right_rect() -> Rect2:
\tif not _geode_states.is_empty():
\t\tvar pair := _geode_pair_rect(_geode_states[_geode_state_index()], 350.0)
\t\treturn Rect2(Vector2(pair.get_center().x, pair.position.y),
\t\t\tVector2(pair.size.x * 0.5, pair.size.y))
\treturn Rect2(Vector2(GEODE_RECT.get_center().x, GEODE_RECT.position.y),
\t\tVector2(GEODE_RECT.size.x * 0.5, GEODE_RECT.size.y))
''')
new=replace_func(new,'_draw_geode','''func _draw_geode() -> void:
\tif _geode_states.is_empty():
\t\treturn
\tvar texture := _geode_states[_geode_state_index()]
\t# Every state includes both mineral cavities and their rooted crystals.
\tdraw_texture_rect(texture, _geode_pair_rect(texture, 350.0), false)
\tif geode_pull <= 0.0:
\t\tfor index: int in range(GEODE_SEAM_SPOTS.size()):
\t\t\tdraw_circle(GEODE_SEAM_SPOTS[index], 15.0,
\t\t\t\tColor("#8ce6dd") if geode_seams[index] else Color("#ffe69a"))
''')
def funcs(text):
 return {m.group(1):m.group(0).rstrip() for m in re.finditer(r'^func (\w+)\(.*?(?=^func |\Z)',text,re.M|re.S)}
oldf=funcs(before);newf=funcs(new);unchanged=[]
for name,text in oldf.items():
 if name not in ['_load_textures','_geode_right_rect','_draw_geode']:
  assert text==newf[name],name
  unchanged.append(dict(method=name,sha256=hashlib.sha256(text.encode()).hexdigest()))
sp.write_text(new,encoding='utf-8',newline='\n')
write(f/'MECHANIC_UNCHANGED.json',dict(status='PASS_ALL_EXISTING_METHODS_EXCEPT3_RENDER_ART_BOUNDARY_METHODS_LITERAL_UNCHANGED',baseline=base,script_before_sha256=before_sha,script_after_sha256=sha(sp),unchanged_methods=unchanged,changed_existing_methods=['_load_textures','_geode_right_rect','_draw_geode'],new_method='_geode_state_index',qualification='Input/progress/path/pan/fossil/geode/save/completion functions unchanged. Right-half input target follows newly displayed authored pair. Parser, actual input capture/save restore and fresh fullsuite still required.'))
write(f/'BINDING.json',dict(status='BOUND_REVERSIBLE_TOPIC_CANDIDATE_REVIEW_PENDING',baseline=base,copies=copies,selected_states=selected['states'],production_script=dict(path=sp.relative_to(b).as_posix(),sha256=sha(sp)),pivot=selected['pivot'],qualification='Unbound pilot does not establish actual production acceptance. Original four runtime/source paintings and failed trials preserved. Exactly two completePOT textures16MB decoded; prior four geode sheets are no longer loaded by this surface. No new3D/cinematic or protected-content changes.'))
s=(b/'audit/job_geology_river_runtime_v1_20261002/capture_geode_timed_sequence.gd').read_text()
s=s.replace('audit/job_geology_river_runtime_v1_20261002/timed_attempt_01','audit/job_geode_coherent_runtime_v1_20261002/attempt_01')
# Actual production renderer only; no override surface, pixel injection, freeze or explicit restore.
(f/'capture.gd').write_text(s,encoding='utf-8',newline='\n')
bt=chr(96);lp=b/'ASSET_LICENSES.md';s=lp.read_text()+'\n### Coherent geode exact runtime source copies (2026-10-02)\n\n'
for x in copies:s+='| '+bt+x['path']+bt+' | Built-in Codex ImageGen, native and reference hashes in coherent geode source library | OpenAI generated project art | '+bt+x['source']+bt+' | '+x['modification']+' SHA256 '+x['sha256']+' |\n'
lp.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});d['validation'].append(dict(command='Literal old/new method comparison',result='PASS',evidence=f.relative_to(b).as_posix()+'/MECHANIC_UNCHANGED.json; actual behavior still gated.'));write(ip,d)
print('Bound seven authored states with exact2POT copies; all'+str(len(unchanged))+' other methods unchanged. Actual render/input/fullCI review pending.')
