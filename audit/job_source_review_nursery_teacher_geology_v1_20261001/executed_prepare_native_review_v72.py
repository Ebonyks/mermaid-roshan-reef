from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_source_review_nursery_teacher_geology_v1_20261001';assert not out.exists();out.mkdir()
(out/'.gdignore').write_text('')
paths=['assets/opera/worlds/nursery/refinement_v1/cradle.png','assets/opera/worlds/nursery/refinement_v1/pillows.png','assets/opera/worlds/hotspots/geologist_fossil.svg','assets/opera/worlds/hotspots/geologist_layered_rock.svg','assets/opera/worlds/hotspots/teacher_lesson_board.svg','assets/opera/worlds/props/goal_geologist.svg','assets/opera/worlds/ui/crests/opera_crest_geologist.svg']
items=[]
for p in paths:
 source=r/p;digest=hashlib.sha256(source.read_bytes()).hexdigest()
 evidence=subprocess.run(['rg','-n','-F',Path(p).name,'scripts','scenes'],cwd=r,capture_output=True,text=True,encoding='utf-8')
 items.append(dict(path=p,sha256=digest,bytes=source.stat().st_size,source_score=None,review='PENDING_CURRENT_NATIVE_PIXELS',literal_reference_evidence=evidence.stdout,reference_search_exit=evidence.returncode))
 if p.endswith('.png'):
  image=Image.open(source).convert('RGBA');alpha=image.getchannel('A');thresholds={str(t):alpha.point(lambda a:255 if a>=t else 0).getbbox() for t in [1,16,128]}
  for name,color in [('white',(255,255,255,255)),('aqua',(208,240,241,255))]:
   bg=Image.new('RGBA',image.size,color);bg.alpha_composite(image);bg.convert('RGB').save(out/(source.stem+'_review_'+name+'.png'))
  items[-1].update(dimensions=list(image.size),alpha_bbox=thresholds,transformation='Complete native source composited only over neutral review backgrounds; no source repair/crop/scale.')
script='extends SceneTree\nfunc _initialize() -> void:\n'
for p in paths[2:]:
 name=Path(p).stem
 script+=f'\tvar image_{name} := Image.new()\n\tassert(image_{name}.load_svg_from_string(FileAccess.get_file_as_string("res://{p}")) == OK)\n\tassert(image_{name}.save_png("res://{out.relative_to(r).as_posix()}/{name}_native.png") == OK)\n'
script+='\tprint("JOB_SOURCE_SVG_NATIVE|5_RENDERED|NO_RUNTIME_EDIT")\n\tquit(0)\n'
tmp=r/'tmp/render_nursery_teacher_geology_sources_v72.gd';tmp.write_text(script,encoding='utf-8',newline='\n');shutil.copyfile(tmp,out/'render_svg_native.gd');shutil.copyfile(Path(__file__),out/'executed_prepare_native_review_v72.py')
profile=dict(status='PREPARED_CURRENT_NATIVE_SOURCE_REVIEW',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline='56d66f63e375b61cf02936b426a05a2b92c14d3b',scope='Seven currently unassigned nursery/teacher/geologist source opinions. Native/current exact pixels and reference traces required before assigning source scores; vector sources remain runtime authority. Named illustration/semantic gaps determine any later reversible derivatives.',items=items,qualification='Source-only inventory/neutral technical previews; no complete current timeline/action or mounted/owner acceptance.')
(out/'PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8',newline='\n')
template=json.loads((r/'design/audit_impacts/job-shared-native-source-review-20261001.json').read_text(encoding='utf-8'))
impact=dict(id='job-nursery-teacher-geology-native-review-20261001',scope=profile['scope'],baseline=profile['baseline'],rules=template['rules'],findings=template['findings'],files=sorted(p.relative_to(r).as_posix() for p in out.rglob('*') if p.is_file()),validation=[dict(command='Current literal source/native-pixel and individual opinion review',result='PENDING',evidence=out.relative_to(r).as_posix()+'/PROFILE.json')],acceptance_gaps='All7 source opinions initially pending; actual source hashes preserved. Current mounted, semantic contact/action, complete training/story/return, device/child/owner and global acceptance remain open.')
(r/'design/audit_impacts/job-nursery-teacher-geology-native-review-20261001.json').write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8',newline='\n')
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
proc=subprocess.run([godot,'--headless','--path',str(r),'--script','res://'+tmp.relative_to(r).as_posix()],cwd=r,capture_output=True)
(out/'svg_render.stdout.log').write_bytes(proc.stdout);(out/'svg_render.stderr.log').write_bytes(proc.stderr)
receipt=dict(status='PASS_NATIVE_SVG_RENDER_ONLY' if proc.returncode==0 else 'FAIL_PRESERVED',process_exit=proc.returncode,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sources_unchanged=all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in items),qualification='Five complete256x256 vector sources mechanically rendered by official Godot4.7.2. No creative score or runtime edit follows from machine render.')
(out/'RENDER_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
impact['files']=sorted(p.relative_to(r).as_posix() for p in out.rglob('*') if p.is_file());(r/'design/audit_impacts/job-nursery-teacher-geology-native-review-20261001.json').write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt));raise SystemExit(proc.returncode)
