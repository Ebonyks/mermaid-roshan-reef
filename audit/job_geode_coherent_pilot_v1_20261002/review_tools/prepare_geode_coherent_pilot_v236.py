from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef'); f=b/'assets_src/imagegen/geologist_geode_coherent_states_v1_20261002'; prefix=f.relative_to(b).as_posix(); a=f/'attempt_10'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-8c7c1bd8-c54d-4d41-b9ee-18396bc2fc13.png'); shutil.copyfile(source,a/'native.png'); assert sha(source)==sha(a/'native.png')
im=Image.open(a/'native.png'); w,h=im.size; cells=[]
for n in range(2):
 rect=[round(n*w/2),0,round((n+1)*w/2),h]; reg=im.crop(rect); box=reg.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(); assert box
 cells.append(dict(id='GEO-COHERENT-A10-STATE-'+str(n),state_index=n,source_rect=rect,source_bbox=[rect[0]+box[0],box[1],box[2]-box[0],box[3]-box[1]],source_aspect=(box[2]-box[0])/(box[3]-box[1]),score=4.5,material_score=4.6,bridge_geometry_score=3.9 if n==0 else 4.5,direct_review=True,evaluation='Painted rock and occluded crystals retain the established identity; residual fringe keeps source4.5 provisional. '+('First requested bridge is narrower than the quarter endpoint and is excluded from the sequence; geometry3.9.' if n==0 else 'Second bridge falls between quarter and half silhouettes; selected for non-runtime mounted pilot.'),priority=True,owner_acceptance=None))
write(a/'REVIEW.json',dict(status='TWO_SOURCES_REVIEWED_ONE_BRIDGE_SELECTED',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native_path=prefix+'/attempt_10/native.png',sha256=sha(a/'native.png'),dimensions=[w,h],mode=im.mode,sheet_score=4.5,cells=cells,qualification='Both directly inspected. First bridge target geometry3.9 excluded; second geometry/source4.5 provisional. No mounted action or production/owner acceptance.'))
write(a/'GENERATION.json',dict(method='built-in image_gen',attempt=10,prompt_path=prefix+'/attempt_10/PROMPT.txt',prompt_sha256=sha(a/'PROMPT.txt'),native_source_path=str(source),native_sha256=sha(source),native_preserved_bytes=True,transparent_background_requested=True,references=read(a/'PLAN.json')['references'],acceptance='ONE_BRIDGE_SELECTED_FOR_NON_RUNTIME_PILOT'))
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'; normalized=[]
for num in [8,10]:
 p=f/('attempt_%02d'%num); args=[ffmpeg,'-hide_banner','-loglevel','error','-i',str(p/'native.png'),'-vf','scale=2048:1024:flags=lanczos','-frames:v','1',str(p/'whole_canvas_2048x1024.png')]; q=subprocess.run(args,cwd=b,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW); (p/'normalization.stderr.log').write_bytes(q.stderr)
 normalized.append(dict(path=(p/'whole_canvas_2048x1024.png').relative_to(b).as_posix(),sha256=sha(p/'whole_canvas_2048x1024.png'),source_path=(p/'native.png').relative_to(b).as_posix(),source_sha256=sha(p/'native.png'),source_dimensions=list(Image.open(p/'native.png').size),dimensions=[2048,1024],method='Uniform complete-canvas ffmpeg Lanczos scale;2:1 aspect/generated alpha retained. No alpha cleanup or component pixel edits. Non-runtime POT atlas.',command=args))
write(f/'NORMALIZATION.json',dict(atlases=normalized))
prior=read(f/'attempt_08/REVIEW.json')['cells']; selected=prior[:3]+[cells[1]]+prior[3:]; regions=[]
for n,x in enumerate(selected):
 num=10 if n==3 else 8; regions.append(dict(index=n,source_id=x['id'],source_score=x['score'],path=prefix+('/attempt_%02d/whole_canvas_2048x1024.png'%num),region=[v*2048/1774 for v in x['source_bbox']],source_aspect=x['source_aspect']))
write(f/'SELECTED_PILOT_STATES.json',dict(status='SEVEN_STATE_MOUNT_REVIEW_PENDING',states=regions,source_height=350,pivot='Constant GEODE_RECT centerX/baseY; exact authored atlas regions mounted uniformly at350px height with preserved aspect.',qualification='Non-runtime ordinary2D state art; no pixel blending, alpha cleanup, production binding or actor/action/owner acceptance.'))
study=b/'audit/job_geode_coherent_pilot_v1_20261002'; study.mkdir(exist_ok=False); (study/'review_tools').mkdir(); (study/'.gdignore').write_text('',encoding='utf-8'); sp=study.relative_to(b).as_posix()
atlas='''extends OperaGeologySurface
## Non-runtime visual pilot. All touch/progress/save behavior inherited.
var coherent_textures: Array[Texture2D] = []

func _load_textures() -> void:
\tsuper._load_textures()
\tif not coherent_textures.is_empty():
\t\treturn
\tvar file := FileAccess.open("res://SOURCE/SELECTED_PILOT_STATES.json",FileAccess.READ)
\tvar parsed: Dictionary = JSON.parse_string(file.get_as_text()) as Dictionary
\tfile.close()
\tvar source_cache: Dictionary = {}
\tfor raw: Dictionary in parsed["states"]:
\t\tvar path: String = "res://" + String(raw["path"])
\t\tif not source_cache.has(path):
\t\t\tvar native_image := Image.load_from_file(path)
\t\t\tassert(native_image != null and not native_image.is_empty())
\t\t\tsource_cache[path] = ImageTexture.create_from_image(native_image)
\t\tvar bounds: Array = raw["region"] as Array
\t\tvar texture := AtlasTexture.new()
\t\ttexture.atlas = source_cache[path] as Texture2D
\t\ttexture.region = Rect2(float(bounds[0]),float(bounds[1]),float(bounds[2]),float(bounds[3]))
\t\tcoherent_textures.append(texture)

func authored_state_index() -> int:
\tif geode_pull <= 0.0:
\t\treturn 0
\treturn mini(6,1 + int(geode_pull / 20.0))

func _coherent_rect() -> Rect2:
\tvar texture := coherent_textures[authored_state_index()]
\tvar fit := Vector2(350.0 * texture.get_width() / float(texture.get_height()),350.0)
\treturn Rect2(Vector2(GEODE_RECT.get_center().x - fit.x * 0.5,GEODE_RECT.end.y - fit.y),fit)

func _geode_right_rect() -> Rect2:
\tif coherent_textures.is_empty():
\t\treturn super._geode_right_rect()
\tvar pair := _coherent_rect()
\treturn Rect2(Vector2(pair.get_center().x,pair.position.y),Vector2(pair.size.x * 0.5,pair.size.y))

func _draw_geode() -> void:
\tif coherent_textures.is_empty():
\t\treturn
\tdraw_texture_rect(coherent_textures[authored_state_index()],_coherent_rect(),false)
\tif geode_pull <= 0.0:
\t\tfor index: int in range(GEODE_SEAM_SPOTS.size()):
\t\t\tdraw_circle(GEODE_SEAM_SPOTS[index],15.0,Color("#8ce6dd") if geode_seams[index] else Color("#ffe69a"))
'''.replace('SOURCE',prefix)
(study/'study_surface.gd').write_text(atlas,encoding='utf-8',newline='\n')
code=(b/'audit/job_geology_river_runtime_v1_20261002/capture_geode_timed_sequence.gd').read_text(encoding='utf-8').replace('audit/job_geology_river_runtime_v1_20261002/timed_attempt_01/',sp+'/attempt_01/')
code=code.replace('var main: ReefMain','const StudySurface := preload("res://'+sp+'/study_surface.gd")\nvar main: ReefMain',1)
needle='world.setup(main,config,competition,Callable())'; assert code.count(needle)==1
injection='''
\tvar old_surface := world.surface
\tvar study := StudySurface.new()
\tstudy.name = "CoherentGeodeNonRuntimePilot"
\tstudy.position = old_surface.position
\tstudy.size = old_surface.size
\tstudy.mouse_filter = old_surface.mouse_filter
\tstudy.bop_texture = old_surface.bop_texture
\tstudy.bop_captain_texture = old_surface.bop_captain_texture
\tstudy.gesture.connect(Callable(world,"_on_gesture"))
\tstudy.progress_changed.connect(Callable(world,"_on_geology_progress_changed"))
\tvar child_index := old_surface.get_index()
\tworld.action_panel.remove_child(old_surface)
\told_surface.queue_free()
\tworld.action_panel.add_child(study)
\tworld.action_panel.move_child(study,child_index)
\tworld.surface = study
\tworld._arm_phase()
'''
code=code.replace(needle,needle+injection).replace('"phase_index":motion_world.phase_index,"direct_review":false','"phase_index":motion_world.phase_index,"authored_state":(surface as StudySurface).authored_state_index(),"direct_review":false')
code=code.replace('no capture freezes, source injection, phase forcing or restore interruption','no capture freezes or restore interruption; non-runtime inherited surface subclass and initial phase0 rebind supply seven source paintings')
code=code.replace('## Actual production surface and all four ordinary career phases. Only entry\n## fixture and isolated test save home are supplied; no phase forcing, source\n## injection, replacement surface, background overlay or completion callback patch.','## Non-runtime inherited seven-state visual pilot; ordinary four-phase touch work.\n## Surface replacement and initial phase0 rebind are explicit fixtures.\n## No later phase forcing, background overlay or completion callback patch.')
(study/'capture.gd').write_text(code,encoding='utf-8',newline='\n')
code=(b/'audit/job_geology_river_runtime_v1_20261002/review_tools/run_geology_river_gates_v222.py').read_text(encoding='utf-8'); start=code.index('commands={'); end=code.index('assert action in commands',start)
commands={'parser':['py','-X','utf8','-B','-m','gdtoolkit.parser',sp+'/study_surface.gd',sp+'/capture.gd'],'inference':['py','-X','utf8','-B','tools/lint_inference.py',sp+'/study_surface.gd',sp+'/capture.gd'],'analyzer':['godot','--headless','--path','ROOT','--check-only','--script',sp+'/capture.gd']}
for width in [1280,1600]:commands['capture'+str(width)]=['godot','--path','ROOT','-s',sp+'/capture.gd','--','--width='+str(width),'--touch','--classic-touch-test']
literal=repr(commands).replace("'py'","py").replace("'godot'","godot").replace("'ROOT'","str(r)")
code=code[:start]+'commands='+literal+'\n'+code[end:]
code=code.replace('audit/job_geology_river_runtime_v1_20261002',sp).replace('job-geology-river-painted-runtime-20261002.json','job-geode-coherent-opening-20261002.json').replace('run_geology_river_gates_v222.py','run_coherent_pilot_gates_v236.py').replace("'geology_river_'+arg+'_v216'","'geode_coherent_pilot_'+arg+'_v236'")
(study/'review_tools/run_coherent_pilot_gates_v236.py').write_text(code,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,study/'review_tools'/Path(__file__).name)
p=b/'ASSET_LICENSES.md'; s=p.read_text(encoding='utf-8')+'\n| '+chr(96)+prefix+'/attempt_10/native.png'+chr(96)+' | Built-in OpenAI ImageGen mineral bridge states | OpenAI generated project source; A8 references retained | '+prefix+'/attempt_10/GENERATION.json | Native exact bytes; two source4.5, first bridge geometry3.9 excluded; selected second4.5 provisional, unbound; SHA256 '+sha(a/'native.png')+' |\n'
for x in normalized:s+='| '+chr(96)+x['path']+chr(96)+' | Complete ImageGen source atlas uniform whole-canvas derivative | Underlying generated source | '+prefix+'/NORMALIZATION.json |2048x1024 POT scale only, native preserved, no alpha cleanup; non-runtime pilot; SHA256 '+x['sha256']+' |\n'
p.write_text(s,encoding='utf-8',newline='\n')
ip=b/'design/audit_impacts/job-geode-coherent-opening-20261002.json'; d=read(ip); d['rules']=sorted(set(d['rules'])|{'DL-SAVE-01','DL-SAVE-02','DL-INT-06'}); d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for folder in [f,study] for p in folder.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'}); d['scope']+=' Non-runtime seven-state pilot replaces fixture surface, inherits production input/progress/save, rebinds initial phase0 then uses ordinary touch/earned advancement. Exact authored atlas regions mounted with preserved aspect and stable base/center; no blending or pixel cleanup.'; write(ip,d)
print(json.dumps(dict(selected_states=len(regions),aspects=[round(x['source_aspect'],3) for x in regions],study=sp)))
