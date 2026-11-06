from pathlib import Path
import os,sys,json,subprocess,hashlib,datetime,re
W=Path.cwd();T=Path(__file__).parent;lane=sys.argv[1];assert lane in ['baseline','candidate']
D=T/lane;assert not D.exists(),'Existing operation must be resumed, not duplicated';D.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
wr=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
pin=json.loads((T/'NORMAL_SAVE_PIN.json').read_text());normal=Path(pin['normal_base'])
def nh():return {s:sha(Path(str(normal)+s)) if Path(str(normal)+s).is_file() else 'absent' for s in pin['hashes']}
assert nh()==pin['hashes']
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip()).with_name('godot.exe')
assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
F='docs/handoffs/codex_flat_vector_art_2026-10-07/r144_shared_painted_shell/capture_context.gd'
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R144_CAPTURE_OUT=str(D/'output'),R144_SOURCE_SHA256=sha(W/'scripts/shell_ornament.gd'))
for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
 p=D/key;p.mkdir();env[key]=str(p)
command=[str(E),'--path',str(W),'--rendering-method','mobile','--display-driver','windows','--audio-driver','Dummy','--log-file',str(D/'native_engine.log'),'-s','res://'+F]
with (D/'engine.log').open('wb') as log:
 proc=subprocess.Popen(command,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
 wr(D/'LAUNCH.json',{'pid':proc.pid,'command':command,'source_sha256':env['R144_SOURCE_SHA256'],'fixture_sha256':sha(W/F),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lane':lane})
 print('R144_NATIVE_PID',proc.pid,lane,flush=True)
 try: rc=proc.wait(timeout=420)
 except subprocess.TimeoutExpired:
  proc.terminate();rc=proc.wait();wr(D/'TIMEOUT.json',{'exit_code':rc});raise
text=(D/'engine.log').read_text(encoding='utf-8',errors='replace');errors=[l for l in text.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',l)]
wr(D/'PROCESS_RESULT.json',{'exit_code':rc,'errors':errors,'log_sha256':sha(D/'engine.log'),'normal_unchanged':nh()==pin['hashes']})
assert rc==0 and not errors,(rc,errors,text[-3500:])
rows=json.loads((D/'output/captures.json').read_text())
for row in rows:
 if row.get('capture') is False:continue
 assert sha(D/'output'/row['file'])==row['sha256']
 assert row['profile']['quality']=='speedy' and row['profile']['renderer']=='mobile'
 assert row['source_sha256']==env['R144_SOURCE_SHA256']
assert nh()==pin['hashes']
wr(D/'RESULT.json',{'state':'PASS_CONFIGURED_NATIVE_CAPTURE_REVIEW_PENDING','lane':lane,'frames':len([r for r in rows if r.get('file')]),'source_sha256':env['R144_SOURCE_SHA256'],'normal_unchanged':True,'formal_QA11':None,'device':None,'child':None,'owner':None})
print('R144_NATIVE_PASS',lane,len(rows),flush=True)
