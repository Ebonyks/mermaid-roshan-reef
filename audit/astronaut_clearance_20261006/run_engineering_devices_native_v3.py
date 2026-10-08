from pathlib import Path
import hashlib,json,subprocess,os,time,datetime,re,sys
ROOT=Path(__file__).resolve().parents[2]
AD=Path(__file__).resolve().parent
GODOT=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
assert hashlib.sha256(GODOT.read_bytes()).hexdigest()=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
width=int(sys.argv[1])
assert width in [1280,1600]
paths=['scripts/opera_astronaut_surface.gd','scripts/opera_astronaut_devices.gd','scripts/opera_astronaut_pipe_work.gd','scripts/opera_career_world_2d.gd','scripts/chapter_two_career_scene_adapter.gd','scripts/save_state.gd','assets/opera/worlds/widgets/astronaut_radioactive_fluid_v1.png','assets/opera/worlds/widgets/astronaut_gear_v1.png','audit/astronaut_clearance_20261006/capture_engineering_devices_v3.gd']
bind={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
run=ROOT/'tmp/astronaut_engineering_devices_v3_20261007'/f'{width}x720'
assert not run.exists(),'Never overwrite an earlier run'
(run/'frames').mkdir(parents=True)
for p in ['appdata','localappdata','data','config']:(run/p).mkdir()
env=os.environ.copy();env.update(ASTRO_NATIVE_WIDTH=str(width),APPDATA=str(run/'appdata'),LOCALAPPDATA=str(run/'localappdata'),XDG_DATA_HOME=str(run/'data'),XDG_CONFIG_HOME=str(run/'config'),VK_LOADER_LAYERS_DISABLE='~implicit~')
log=AD/f'ENGINEERING_DEVICES_NATIVE_V3_{width}_LOG.txt';receipt=AD/f'ENGINEERING_DEVICES_NATIVE_V3_{width}_RECEIPT.json'
argv=[str(GODOT),'--verbose','--path',str(ROOT),'--audio-driver','Dummy','--rendering-method','mobile','--rendering-driver','vulkan','--resolution',f'{width}x720','--max-fps','30','-s','audit/astronaut_clearance_20261006/capture_engineering_devices_v3.gd']
started=time.monotonic();print('START native',width,flush=True)
with log.open('xb') as out:
 proc=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
 try:rc=proc.wait(timeout=180)
 except subprocess.TimeoutExpired:proc.kill();rc=proc.wait(timeout=10)
text=log.read_text(encoding='utf-8',errors='replace');report=None
for line in text.splitlines():
 if line.startswith('ASTRO_BIRTHDAY_RESULT|'):report=json.loads(line.split('|',1)[1])
fail=[l for l in text.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:|ASTRO_BIRTHDAY\|FAIL',l)]
changed=[p for p,h in bind.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
result='PASS' if rc==0 and report and report['failures']==0 and not fail and not changed else 'FAIL'
data={'result':result,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-started,'exit_code':rc,'checks':report.get('checks') if report else None,'source_bindings':bind,'source_changes':changed,'failure_lines':fail,'report':report,'argv':argv,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'limits':'Native diagnostic, prior story seeded; no full-speed/device/independent/child/owner acceptance.'}
receipt.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:data[k] for k in ['result','elapsed_seconds','exit_code','checks','failure_lines']}),flush=True)
raise SystemExit(0 if result=='PASS' else 1)
