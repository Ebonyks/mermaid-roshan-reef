from pathlib import Path
import os,subprocess,json,hashlib,time
from datetime import datetime,timezone
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';v=s/'verification';v.mkdir(exist_ok=True);exe=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(exe)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
actual=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light';pins=lambda:{p.name:sha(p) for p in actual.glob('reef_save*') if p.is_file()};before=pins();records=[]
sources=list((r/'scripts').glob('*.gd'))+list((r/'assets/opera/worlds/support_quality_20261019').glob('*.png'));sourcepins={p.relative_to(r).as_posix():sha(p) for p in sources}
jobs=[('trace_diagnostic01',['--headless','--script','assets_src/imagegen/job_art_support_careers_20261019/probe_trace_diagnostic01.gd'],480)]
for name,args,timeout in jobs:
 home=r/'tmp'/('p6_native_'+name);assert not home.exists();(home/'Roaming').mkdir(parents=True);(home/'Local').mkdir();env=os.environ.copy();env['APPDATA']=str(home/'Roaming');env['LOCALAPPDATA']=str(home/'Local');env['PYTHONDONTWRITEBYTECODE']='1'
 guard=home/'guard.gd';expected=str(home/'Roaming').replace('\\','/');guard.write_text('extends SceneTree\nfunc _initialize() -> void:\n\tif not OS.get_user_data_dir().replace("\\\\", "/").begins_with('+json.dumps(expected)+' + "/"):\n\t\tquit(2)\n\t\treturn\n\tprint("USERDATA_ISOLATION|PASS|", OS.get_user_data_dir())\n\tquit(0)\n',encoding='utf-8');q=subprocess.run([str(exe),'--headless','--path',str(r),'--script',str(guard)],env=env,cwd=r,capture_output=True,timeout=60);assert q.returncode==0 and b'USERDATA_ISOLATION|PASS|' in q.stdout,(q.returncode,q.stdout,q.stderr)
 log=v/(name+'.log');assert not log.exists();started=time.monotonic()
 with log.open('wb') as f:
  try:q=subprocess.run([str(exe),'--path',str(r),*args],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout);code=q.returncode
  except subprocess.TimeoutExpired:code=124
 text=log.read_text('utf-8',errors='replace');bad=any(x in text for x in ['SCRIPT ERROR:','Parse Error:','Compile Error:','FAIL']);row={'name':name,'raw_exit':code,'elapsed_seconds':round(time.monotonic()-started,3),'sha256':sha(log),'private_home':str(home),'userdata_guard':'PASS before production main/probe','status':'PASS' if code==0 and not bad else 'FAIL'};records.append(row);print(row,flush=True);print(text[-2400:],flush=True)
 drift=[n for n,h in sourcepins.items() if sha(r/n)!=h];record={'checked_utc':datetime.now(timezone.utc).isoformat(),'records':records,'actual_desktop_save_sha256_before':before,'actual_desktop_save_sha256_after':pins(),'actual_save_unchanged':before==pins(),'source_drift':drift,'source_sha256_raw_checkout':sourcepins,'status':'PASS' if all(x['status']=='PASS' for x in records) and before==pins() and not drift else 'FAIL'};(v/'trace_diagnostic01.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
 if row['status']!='PASS' or record['status']!='PASS':raise SystemExit(1)
print('All current native checks PASS',flush=True)
