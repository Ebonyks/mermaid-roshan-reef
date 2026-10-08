from pathlib import Path
from datetime import datetime, timezone
import ctypes, hashlib, json, shutil, subprocess, sys, time
from PIL import Image, ImageStat

setup_start = time.monotonic()
root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
engine = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
script = 'audit/astronaut_clearance_20261006/capture_birthday_native_v3.gd'
job = root/'tmp/astronaut_native_birthday_capture_v3_20261007'
log = packet/'NATIVE_BIRTHDAY_CAPTURE_V3_LOG.txt'
preflight = packet/'NATIVE_BIRTHDAY_CAPTURE_V3_PREFLIGHT.json'
receipt = packet/'NATIVE_BIRTHDAY_CAPTURE_V3_RECEIPT.json'
manifest_path = packet/'NATIVE_BIRTHDAY_CAPTURE_V3_MANIFEST.json'
TIME_CAP = 180
OUTPUT_CAP = 512*1024**2
CACHE_CAP = 64*1024**2
FLOOR = 3*1024**3

def sha(path):
 h = hashlib.sha256()
 with path.open('rb') as stream:
  for block in iter(lambda: stream.read(1024**2), b''): h.update(block)
 return h.hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def dir_bytes(path): return sum(q.stat().st_size for q in path.rglob('*') if q.is_file()) if path.exists() else 0
class MemoryStatus(ctypes.Structure):
 _fields_ = [('length',ctypes.c_uint32),('load',ctypes.c_uint32),('total_phys',ctypes.c_uint64),('avail_phys',ctypes.c_uint64),('total_page',ctypes.c_uint64),('avail_page',ctypes.c_uint64),('total_virtual',ctypes.c_uint64),('avail_virtual',ctypes.c_uint64),('avail_extended',ctypes.c_uint64)]
def resources(cache=False):
 m=MemoryStatus();m.length=ctypes.sizeof(m)
 assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
 d={'C_free_bytes':shutil.disk_usage('C:/').free,'physical_available_bytes':m.avail_phys}
 if cache: d['cache_bytes']=dir_bytes(root/'.godot')
 return d
def occupancy():
 command="@(Get-CimInstance Win32_Process -Filter \"Name='Godot_v4.7.2-stable_win64.exe'\" | Select-Object ProcessId,ExecutablePath) | ConvertTo-Json -Compress"
 q=subprocess.run(['powershell','-NoProfile','-Command',command],capture_output=True,text=True,timeout=15)
 assert q.returncode==0, 'Cannot verify exact approved engine occupancy'
 d=json.loads(q.stdout) if q.stdout.strip() else []
 return d if isinstance(d,list) else [d]
def source_inventory():
 files={root/'project.godot',root/'tools/godot_baseline.json',Path(__file__),root/script,packet/'NATIVE_BIRTHDAY_CAPTURE_V3_PLAN.json',packet/'verify_birthday_save_v5.gd',root/'tmp/astronaut_partial_save_repair_20261006/reef_save.json'}
 for tree in ['assets','scenes','scripts','shaders']:
  path=root/tree
  if path.exists(): files.update(q for q in path.rglob('*') if q.is_file())
 return [{'path':q.relative_to(root).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted(files)]
def signature(items): return hashlib.sha256(json.dumps(items,sort_keys=True,separators=(',',':')).encode()).hexdigest()

assert not any(q.exists() for q in [log,preflight,receipt,manifest_path]), 'Preserve prior evidence; no automatic retry'
assert not job.exists() or not any(job.iterdir()), 'Preserve prior isolated output'
job.mkdir(parents=True,exist_ok=True);(job/'frames').mkdir()
version=subprocess.check_output([str(engine),'--version'],text=True).strip()
assert version=='4.7.2.stable.official.ed1daf0bf'
engine_sha=sha(engine)
assert engine_sha=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
resource_before=resources(True); occupied=occupancy()
assert resource_before['C_free_bytes']>=FLOOR and resource_before['physical_available_bytes']>=FLOOR
assert not occupied,'Approved Godot executable already running; no competing capture launched'
sources=source_inventory();source_signature=signature(sources)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
original=(packet/'verify_birthday_save_v5.gd').read_text();candidate=(root/script).read_text()
# Every original assertion label/expression remains literally present in the cloned fixture.
original_checks=[line.strip() for line in original.splitlines() if '_check(' in line and not line.startswith('func _check')]
assert all(line in candidate for line in original_checks)
assert 'StartMenuContinueButton' in candidate
assert 'res://tmp/astronaut_native_birthday_capture_v3_20261007/reef_save.json' in candidate
assert 'res://tmp/astronaut_native_birthday_capture_v3_20261007/frames' in candidate
assert 'NATIVE_BIRTHDAY_CAPTURE_V3_MANIFEST.json' in candidate
assert script.endswith('capture_birthday_native_v3.gd')
assert 'capture_birthday_native_v1.gd' not in script
assert candidate.count('_check(')==original.count('_check(')+4
analyzer=[str(engine),'--headless','--path',str(root),'--script','res://'+script,'--check-only']
native=[str(engine),'--windowed','--resolution','1280x720','--position','64,64','--rendering-method','mobile','--rendering-driver','vulkan','--audio-driver','Dummy','--path',str(root),'--script','res://'+script]
started=utc();start=time.monotonic()
preflight.write_text(json.dumps({'started_utc':started,'baseline':head,'branch':branch,'source_state':'owned dirty local candidate; not origin/dev or strict clean-runtime acceptance','engine_version':version,'engine_sha256':engine_sha,'sources':sources,'source_signature':source_signature,'source_inventory_scope':'all files under assets/scenes/scripts/shaders plus project/baseline/driver/runner/plan and isolated prior-proof save fixture; not independently proven active-dependency closure','commands':[analyzer,native],'combined_cap_seconds':TIME_CAP,'output_cap_bytes':OUTPUT_CAP,'cache_growth_cap_bytes':CACHE_CAP,'resource_before':resource_before,'approved_executable_occupancy':occupied,'setup_seconds':round(start-setup_start,3),'fixture':'Explicit prior six birthday jobs and Day One completed fixture; isolated own save; actual picture/object touches, no phase/progress injections','original_assertion_lines_preserved':len(original_checks),'original_assertion_expected_count':103,'no_automatic_retry':True,'audio':'Dummy driver for bounded visual test; no audio acceptance','prior_native_seconds_spent':45.573,'corrective_scope':'Actual visible Continue touch fixes native-only fixture setup after preserved V1 failure; no production source change or automatic rerun'},indent=2)+'\n',encoding='utf-8')
steps=[];resource_abort=None
with log.open('xb') as output:
 for label,command in [('Godot analyzer',analyzer),('Native Mobile birthday viewport capture',native)]:
  output.write(('\nSTEP '+label+'\n').encode());output.flush()
  if label.startswith('Native'): assert not occupancy(), 'Another approved engine started before native launch'
  process=subprocess.Popen(command,cwd=root,stdout=output,stderr=subprocess.STDOUT)
  print(json.dumps({'step':label,'owned_pid':process.pid,'native':label.startswith('Native'),'cap_seconds':TIME_CAP}),flush=True)
  aborted=False;last_resource=0.0
  while process.poll() is None:
   elapsed=time.monotonic()-start
   if elapsed>TIME_CAP:
    resource_abort='combined time cap';aborted=True;break
   if dir_bytes(job)+log.stat().st_size>OUTPUT_CAP:
    resource_abort='artifact cap';aborted=True;break
   if elapsed-last_resource>=10:
    current=resources();last_resource=elapsed
    if current['C_free_bytes']<FLOOR or current['physical_available_bytes']<FLOOR:
     resource_abort='actual free disk/memory floor';aborted=True;break
   time.sleep(0.5)
  if aborted:
   process.terminate()
   try: process.wait(timeout=10)
   except subprocess.TimeoutExpired: process.kill();process.wait(timeout=10)
  steps.append({'label':label,'command':command,'owned_pid':process.pid,'exit_code':process.returncode,'aborted':aborted})
  if process.returncode!=0 or aborted: break
run_seconds=time.monotonic()-start
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
errors=[line for line in lines if any(s in line for s in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]
records=[json.loads(line.split('|',1)[1]) for line in lines if line.startswith('ASTRO_BIRTHDAY_RESULT|')]
manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
frames=manifest.get('frames',[]);pixel_checks=[]
for row in frames:
 path=root/row['path'];ok=path.is_file() and sha(path)==row['sha256'] and path.stat().st_size==row['bytes']
 with Image.open(path) as image:
  dims=list(image.size);stats=ImageStat.Stat(image.convert('RGB'));nonblank=max(stats.stddev)>1.0
 ok=ok and dims==row['dimensions']==[1280,720] and nonblank
 pixel_checks.append({'path':row['path'],'sha256':row['sha256'],'dimensions':dims,'nonblank':nonblank,'pass':ok})
labels={row['label'] for row in frames}
required={f'phase{i}_open' for i in range(4)}|{'phase0_pipe_approach','phase0_pipe_anticipation','phase0_pipe_contact_a','phase0_pipe_contact_b','phase0_pipe_release','phase0_pipe_return','room_return'}
missing=sorted(required-labels)
resources_after=resources(True);resources_after['artifact_bytes']=dir_bytes(job)+log.stat().st_size+preflight.stat().st_size+(manifest_path.stat().st_size if manifest_path.exists() else 0)
resources_after['cache_growth_bytes']=max(0,resources_after['cache_bytes']-resource_before['cache_bytes'])
resource_ok=resources_after['C_free_bytes']>=FLOOR and resources_after['artifact_bytes']<=OUTPUT_CAP and resources_after['cache_growth_bytes']<=CACHE_CAP and resource_abort is None
sources_after=source_inventory();match=sources_after==sources
backend_ok=manifest.get('display_server')!='headless' and manifest.get('rendering_method')=='mobile' and manifest.get('rendering_driver')=='vulkan'
passed=len(steps)==2 and all(s['exit_code']==0 and not s['aborted'] for s in steps) and not errors and len(records)==1 and records[0]['checks']==107 and records[0]['failures']==0 and len(records[0].get('contact_requests',[]))==10 and bool(frames) and all(x['pass'] for x in pixel_checks) and not missing and not manifest.get('errors') and backend_ok and match and resource_ok
result={'started_utc':started,'finished_utc':utc(),'baseline':head,'branch':branch,'engine_version':version,'engine_sha256':engine_sha,'steps':steps,'native_analyzer_seconds':round(run_seconds,3),'combined_cap_seconds':TIME_CAP,'setup_seconds':round(start-setup_start,3),'total_observed_seconds':round(time.monotonic()-setup_start,3),'resource_before':resource_before,'resource_after':resources_after,'resource_abort':resource_abort,'resource_limits_pass':resource_ok,'errors':errors,'result':'PASS' if passed else 'FAIL','evidence':records,'sources':sources,'source_signature':source_signature,'source_bindings_still_match':match,'source_changes':[item['path'] for item in sources_after if item not in sources],'native_backend_pass':backend_ok,'frames':len(frames),'pixel_checks':pixel_checks,'missing_required_views':missing,'manifest_path':manifest_path.relative_to(root).as_posix() if manifest_path.exists() else None,'manifest_sha256':sha(manifest_path) if manifest_path.exists() else None,'preflight_sha256':sha(preflight),'log_sha256':sha(log),'meaning':'Native diagnostic of explicit-prerequisite birthday four-mechanic touches/save/return. Raw untouched viewport pixels and state observations. No strict clean/fresh-runtime, action score, independent/device/child/owner/full-suite/integration acceptance. Local ignored output is staging, not external handoff.'}
receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'result':result['result'],'steps':steps,'frames':len(frames),'checks':records[0]['checks'] if records else 0,'failed_checks':[x for x in records[0]['rows'] if not x['pass']] if records else [],'errors':errors[:12],'missing_required_views':missing,'native_analyzer_seconds':result['native_analyzer_seconds'],'source_match':match,'resource_limits_pass':resource_ok,'receipt_sha256':sha(receipt)}),flush=True)
sys.exit(0 if passed else 1)
