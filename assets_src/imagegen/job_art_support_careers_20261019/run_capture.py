from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,sys,time
r=Path(__file__).resolve().parents[3];s=Path(__file__).resolve().parent;name=sys.argv[1];assert name in ['current01','current02','current03','current04','current05','current06','current07','current08','current09','current10','current11','current12']
exe='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();actual=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light'
def actual_pins():return {p.name:sha(p) for p in actual.glob('reef_save*') if p.is_file()}
private=r/'tmp'/('support_capture_appdata_'+name);assert not private.exists();(private/'Roaming').mkdir(parents=True);(private/'Local').mkdir();env=os.environ.copy();env['APPDATA']=str(private/'Roaming');env['LOCALAPPDATA']=str(private/'Local')
files=list((r/'scripts').rglob('*.gd'))+list((r/'scenes').rglob('*.tscn'))+[r/'project.godot',s/('capture_'+name+'.gd')]+list((r/'assets/opera/worlds/support_quality_20261019').glob('*.png'))
pins={p.relative_to(r).as_posix():sha(p) for p in files};before=actual_pins();started=time.monotonic();log=s/('capture_'+name+'.log');assert not log.exists()
check=s/('capture_'+name+'_check.log')
with check.open('wb') as output:q=subprocess.run([exe,'--headless','--path',str(r),'--check-only','--script',str(s/('capture_'+name+'.gd'))],cwd=r,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=60)
text=check.read_text('utf-8',errors='replace');print('Capture analyzer',q.returncode,text[-2000:],flush=True)
assert q.returncode==0 and 'SCRIPT ERROR' not in text
with log.open('wb') as output:
 try:q=subprocess.run([exe,'--path',str(r),'--audio-driver','Dummy','--script',str(s/('capture_'+name+'.gd'))],cwd=r,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=600);code=q.returncode
 except subprocess.TimeoutExpired:code=124
text=log.read_text('utf-8',errors='replace');after=actual_pins();drift=[p for p,h in pins.items() if sha(r/p)!=h]
status='PASS' if code==0 and 'SUPPORT_CURRENT_CAPTURE|PASS|' in text and 'SCRIPT ERROR' not in text and 'USERDATA_ISOLATION|PASS|' in text and before==after and not drift else 'FAIL'
record={'status':status,'exit':code,'elapsed_seconds':round(time.monotonic()-started,3),'checked_utc':datetime.now(timezone.utc).isoformat(),'private_appdata':str(private),'guard':'OS.get_user_data_dir checked inside exact privateAPPDATA before production main scene initialization; both APPDATA/LOCALAPPDATA redirected.','actual_desktop_save_sha256_before':before,'actual_desktop_save_sha256_after':after,'actual_save_unchanged':before==after,'source_sha256':pins,'source_drift':drift,'log_sha256':sha(log),'limits':'Configured current Mobile GUI, actual input earning; canonicalQA11/natural-route, whole-time motion/human/device/child/owner separate.'};(s/('capture_'+name+'_receipt.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(text[-4000:],flush=True);print(status,'saveunchanged',before==after,'drift',drift,flush=True);raise SystemExit(0 if status=='PASS' else 1)
