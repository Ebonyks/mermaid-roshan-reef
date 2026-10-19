"""Native GUI capture with verified APPDATA isolation and real-save hash guard."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,sys
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
actual=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def actual_pins():
    return {p.name:sha(p) for p in actual.glob('reef_save*') if p.is_file()}
name=sys.argv[1]
assert name in ['current_04','current_05','current_06','chapter2_01','chapter2_02','chapter2_03','chapter2_04','chapter2_05']
private=root/'tmp'/('chef_capture_appdata_'+name)
private.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['APPDATA']=str(private)
before=actual_pins()
sources=[root/'scripts'/p for p in ['chef_painted_art.gd','opera_gesture_surface.gd','opera_chef_surface.gd','opera_career_world_2d.gd','opera_world_backdrop_2d.gd']]
sources+=list((root/'assets/opera/worlds/chef_quality_20261019').glob('*.png'))
sources+=[root/'assets/opera/worlds/widgets'/p for p in ['widget_target_chef_piece_2.png','widget_pour_chef_mover.png','widget_crank_chef_mover.png']]
source_pins={p.relative_to(root).as_posix():sha(p) for p in sources}
log=src/('capture_'+name+'.log')
with log.open('wb') as handle:
    run=subprocess.run(['C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe',
        '--path',str(root),'--audio-driver','Dummy','--script',str(src/('capture_chef_'+name+'.gd'))],
        cwd=root,env=env,stdout=handle,stderr=subprocess.STDOUT,timeout=300)
after=actual_pins()
drift=[p for p,h in source_pins.items() if sha(root/p)!=h]
transcript=log.read_text('utf-8',errors='replace')
assert before==after,'Actual desktop save changed during isolated capture'
assert 'USERDATA_ISOLATION|PASS|' in transcript,'Capture did not prove isolated path before game initialization'
status='PASS' if run.returncode==0 and 'CAPTURE|PASS|' in transcript and 'SCRIPT ERROR' not in transcript and not drift else 'FAIL'
(src/('capture_'+name+'_receipt.json')).write_text(json.dumps({'status':status,'exit':run.returncode,
    'checked_utc':datetime.now(timezone.utc).isoformat(),'private_appdata':str(private),
    'actual_desktop_save_sha256_before':before,'actual_desktop_save_sha256_after':after,
    'actual_save_unchanged':before==after,'source_sha256':source_pins,'source_drift':drift,
    'log_sha256':sha(log),'limits':'Configured GUI fixture; no device, child or owner acceptance.'},indent=2)+'\n')
print(transcript[-2600:]);raise SystemExit(0 if status=='PASS' else 1)
