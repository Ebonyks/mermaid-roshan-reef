from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys
r=Path(__file__).resolve().parents[3];s=Path(__file__).resolve().parent;name=sys.argv[1];assert name in ['current01','current02','current03','current04']
actual=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def actual_pins():return {p.name:sha(p) for p in actual.glob('reef_save*') if p.is_file()}
private=r/'tmp'/('boxer_capture_appdata_'+name);assert not private.exists(),'Fresh private home required; never overwrite an earlier capture.'
(private/'Roaming').mkdir(parents=True);(private/'Local').mkdir();env=os.environ.copy();env['APPDATA']=str(private/'Roaming');env['LOCALAPPDATA']=str(private/'Local')
files=[r/'scripts'/p for p in ['opera_boxing_surface.gd','nursery_painted_art.gd','painted_feedback_art.gd','opera_gesture_surface.gd','opera_nursery_catch.gd','opera_career_world_2d.gd','opera_roshan_actor.gd','opera_world_backdrop_2d.gd','opera_stage_paths.gd']]+list((r/'assets/opera/worlds/nursery_quality_20261019').glob('*.png'))+list((r/'assets/opera/worlds/nursery').glob('baby_*.png'))+[r/'assets/opera/worlds/widgets/widget_pour_nursery_mover.png',r/'project.godot',s/('capture_'+name+'.gd')]
files+=list((r/'assets/ui').glob('pearl_*.png'))+list((r/'assets/opera/worlds/boxer_quality_20261019').glob('*.png'))+list((r/'assets/opera/worlds/props').glob('fx_invite*.png'))
pins={p.relative_to(r).as_posix():sha(p) for p in files};before=actual_pins();log=s/('capture_'+name+'.log');assert not log.exists()
with log.open('wb') as output:
 try:q=subprocess.run(['C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe','--path',str(r),'--audio-driver','Dummy','--script',str(s/('capture_'+name+'.gd'))],cwd=r,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=300);code=q.returncode
 except subprocess.TimeoutExpired:code=124
text=log.read_text('utf-8',errors='replace');after=actual_pins();drift=[p for p,h in pins.items() if sha(r/p)!=h]
status='PASS' if code==0 and 'BOXER_CURRENT_CAPTURE|PASS|' in text and 'SCRIPT ERROR' not in text and 'USERDATA_ISOLATION|PASS|' in text and before==after and not drift else 'FAIL'
record={'status':status,'exit':code,'checked_utc':datetime.now(timezone.utc).isoformat(),'private_appdata':str(private),'guard':'OS.get_user_data_dir validated inside private APPDATA before main scene initialization; no unsupported CLI isolation flag.','actual_desktop_save_sha256_before':before,'actual_desktop_save_sha256_after':after,'actual_save_unchanged':before==after,'source_sha256':pins,'source_drift':drift,'log_sha256':sha(log),'limits':'Configured current Mobile GUI; canonicalQA11, whole-time motion/human/device/child/owner acceptance separate.'}
(s/('capture_'+name+'_receipt.json')).write_text(json.dumps(record,indent=2)+'\n');print(text[-3800:]);print(status,'actual save unchanged',before==after,'source drift',drift);raise SystemExit(0 if status=='PASS' else 1)
