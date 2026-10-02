from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,time
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=r/'tmp/doctor_sink_contact_v58';assert not out.exists();out.mkdir()

sources=['scripts/opera_career_world_2d.gd','scripts/opera_gesture_surface.gd','scripts/opera_roshan_actor.gd','scripts/opera_hotspot_catalog.gd','assets/flats/castle/interactions_v2/bubble_bath_sink_sheet.png','assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/attempt_06_native.png','assets_src/imagegen/day2_doctor_wash_motion_v1_20261001/motion_key01_attempt01_native.png','assets_src/imagegen/day2_doctor_wash_clean_result_v1_20261001/attempt01_native.png','assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png']
before={p:hashlib.sha256((r/p).read_bytes()).hexdigest() for p in sources}
profile={'status':'PREPARED_STATIC_CONTACT_STUDY','baseline':'56d66f63e375b61cf02936b426a05a2b92c14d3b','intention':'After actual doctor station arrival, Roshan brings connected soapy hands above the existing painted sink. Test scale/layer contact before runtime binding.','lane':'Gameplay static composition study; not motion or cinematic delivery','source_before':before,'reuse':'First256x256 cell of existing painted sink, unchanged. Complete outward-reaching doctor source unchanged; preceding keys also checked unchanged.','variants':'One complete outward-reaching doctor key, uniform figure fits250/300px, reused sink extents140/160px, offsets0/20px,1280/1600 desktop widths;18 static views including2 current originals. Original first sink cell behind character, identical original front-rim/cabinet region0,116,256,140 in front. No source-pixel editing or new sink generation.','missing_evidence':'No new gameplay binding, causal water/foam/clean result, temporal loop/exit or device/child/owner acceptance.'}
(out/'PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8')

env=dict(os.environ)
for key,sub in [('APPDATA','Roaming'),('LOCALAPPDATA','Local')]:folder=out/sub;folder.mkdir();env[key]=str(folder)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';script='tmp/capture_doctor_sink_contact_v58.gd'
commands=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',script]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',script]),('analyzer',[godot,'--headless','--path',str(r),'--check-only','--script','res://'+script]),('native',[godot,'--path',str(r),'--windowed','--resolution','1280x720','--script','res://'+script,'--','--touch','--classic-touch-test'])]
rows=[]
for name,command in commands:
 start=time.monotonic()
 with (out/(name+'.stdout.log')).open('wb') as stdout,(out/(name+'.stderr.log')).open('wb') as stderr:
  try:p=subprocess.run(command,cwd=r,env=env,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW,timeout=300);code=p.returncode;timeout=False
  except subprocess.TimeoutExpired:code=None;timeout=True
 rows.append({'name':name,'command':command,'process_exit':code,'timed_out_owned_child':timeout,'seconds':time.monotonic()-start});print(name,code,flush=True)
 if code!=0:break
after={p:hashlib.sha256((r/p).read_bytes()).hexdigest() for p in before};passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and before==after
(out/'PROCESS_RECEIPT.json').write_text(json.dumps({'status':'PASS_STATIC_CAPTURE_ONLY' if passed else 'FAIL_PRESERVED','processes':rows,'source_before':before,'source_after':after,'source_unchanged':before==after,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':profile['missing_evidence']},indent=2)+'\n',encoding='utf-8');raise SystemExit(0 if passed else 1)
