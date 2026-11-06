from pathlib import Path
import os,sys,json,hashlib,subprocess,datetime,re
W=Path.cwd();T=Path(__file__).parent;lane=sys.argv[1];assert lane == 'combined'
D=W.parent/'combined_validation_80975b0051/native';assert not D.exists(), 'Resume existing recorded capture instead of duplicating it';D.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
pin=json.loads((T/'NORMAL_SAVE_PIN.json').read_text());normal=Path(pin['normal_base'])
def normal_hashes():return {s:sha(Path(str(normal)+s)) if Path(str(normal)+s).is_file() else 'absent' for s in pin['hashes']}
assert normal_hashes()==pin['hashes']
assert json.loads((W.parent/'combined_validation_80975b0051/import/RESULT.json').read_text())['exit_code']==0
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip()).with_name('godot.exe')
assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R143_CAPTURE_OUT=str(D/'output'),R143_SOURCE_SHA256=sha(W/'scripts/racer/reef_kart_race.gd'))
for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
 p=D/key;p.mkdir();env[key]=str(p)
command=[str(E),'--path',str(W),'--rendering-method','mobile','--display-driver','windows','--log-file',str(D/'native_engine.log'),'-s','res://docs/handoffs/codex_flat_vector_art_2026-10-07/r143_racer_required_painted_runtime/capture_context.gd']
with (D/'engine.log').open('wb') as log:
 proc=subprocess.Popen(command,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
 wr(D/'LAUNCH.json',{'pid':proc.pid,'command':command,'source_sha256':env['R143_SOURCE_SHA256'],'fixture_sha256':sha(W/'docs/handoffs/codex_flat_vector_art_2026-10-07/r143_racer_required_painted_runtime/capture_context.gd'),'started_at_utc':now(),'lane':lane})
 print('NATIVE_CAPTURE_PID',proc.pid,lane,flush=True);rc=proc.wait(timeout=900)
text=(D/'engine.log').read_text(encoding='utf-8',errors='replace');errors=[l for l in text.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:',l)]
assert rc==0 and not errors,(rc,errors,text[-4000:])
rows=json.loads((D/'output/captures.json').read_text());assert len(rows)==54
for row in rows:
 assert row['save_error']==0 and sha(D/'output'/row['file'])==row['sha256']
 assert row['profile']['quality']=='speedy' and row['profile']['renderer']=='mobile' and row['profile']['stretch']=='canvas_items/expand'
 assert row['source_sha256']==env['R143_SOURCE_SHA256']
assert normal_hashes()==pin['hashes']
wr(D/'RESULT.json',{'state':'PASS_CONFIGURED_NATIVE_MOBILE_SPEEDY_EXPAND_REVIEW_REQUIRED','lane':lane,'frames':len(rows),'source_sha256':env['R143_SOURCE_SHA256'],'log_sha256':sha(D/'engine.log'),'normal_before':pin['hashes'],'normal_after':normal_hashes(),'normal_unchanged':True,'formal_QA11':None,'device':None,'child':None,'owner':None,'completed_at_utc':now()})
print('NATIVE_CAPTURE_PASS',lane,len(rows),flush=True)
