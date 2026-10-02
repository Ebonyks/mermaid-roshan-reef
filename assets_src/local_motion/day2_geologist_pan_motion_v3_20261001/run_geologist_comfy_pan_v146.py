from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
from urllib.request import urlopen
import msvcrt
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
packet=r/'assets_src/local_motion/day2_geologist_pan_motion_v3_20261001'
state_dir=r/'build/geologist_local_pan_study_v3_20261001'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def validate():
 m=json.loads((packet/'MANIFEST.json').read_text(encoding='utf-8'));j=m['job'];renderer=m['renderer']
 assert m['acceptance']=='LOCAL_MOTION_REFERENCE_ONLY' and m['owner_approval'] is None and m['runtime_integration'] is False
 assert renderer['settings']=={'width':896,'height':512,'frames':41,'steps':24,'weight_dtype':'GGUF_Q4_K_S'}
 for b in renderer['bindings']:
  assert sha(packet/b['packet_path'])==b['sha256']
  if b.get('check_installed_bytes',True):assert sha(Path(b['installed_path']))==b['sha256']
 for p,key in [(r/j['source_path'],'source_sha256'),(packet/j['input_path'],'input_sha256'),(packet/j['prompt_path'],'prompt_sha256')]:assert sha(p)==j[key]
 assert sha(Path(__file__))==m['worker_sha256']
 assert (packet/j['prompt_path']).read_text(encoding='utf-8').rstrip().endswith('Sound: silence.')
 return m
def matching_benchmark(local,settings):
 for pattern in ['d2m_b1q_*/RENDER_RECEIPT.json','sky_*/RENDER_RECEIPT.json']:
  for p in sorted((local/'jobs').glob(pattern),reverse=True):
   try:
    rec=json.loads(p.read_text(encoding='utf-8'));g=json.loads(p.with_name('workflow.api.json').read_text(encoding='utf-8'))
    if rec.get('status')=='PASS' and rec.get('settings')==settings and g['1']['class_type']=='UnetLoaderGGUFAdvanced' and g['1']['inputs']['unet_name']=='Wan2.2-TI2V-5B-Q4_K_S.gguf' and g['2']['inputs']['clip_name']=='umt5-xxl-encoder-Q4_K_S.gguf':return str(p)
   except (OSError,ValueError,KeyError):pass
 return None

state_dir.mkdir(parents=True,exist_ok=True)
with (state_dir/'worker.lock').open('a+b') as lock:
 lock.seek(0)
 if lock.read(1)==b'':lock.write(b'0');lock.flush()
 lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
 m=validate();j=m['job'];renderer=m['renderer'];local=Path(renderer['root']);name=j['queue_name']
 assert not list((local/'jobs').glob(name+'_*/RENDER_RECEIPT.json')),'Previous submission exists; no duplicate started'
 assert not (state_dir/'STATE.json').exists(),'Prior worker state exists; inspect before any resubmission'
 state={'status':'ADMISSION_PENDING','manifest_sha256':sha(packet/'MANIFEST.json'),'worker_sha256':sha(Path(__file__)),'created_utc':now(),'pid':os.getpid(),'acceptance':m['acceptance'],'runtime_integration':False,'owner_approval':None,'job_name':name}
 def save(status,**extra):
  state.update(status=status,checked_utc=now(),**extra);write(state_dir/'STATE.json',state);print(status,flush=True)
 benchmark=matching_benchmark(local,renderer['settings'])
 if not benchmark:save('BLOCKED_NO_MATCHING_QUANTIZED_BENCHMARK');raise SystemExit(2)
 save('WAITING_FOR90_SECOND_QUIET_NATIVE_QUEUE',benchmark_receipt=benchmark)
 idle_since=None;deadline=time.monotonic()+1800;last_status=None
 while True:
  if time.monotonic()>deadline:save('ADMISSION_TIMEOUT_NO_SUBMISSION');raise SystemExit(2)
  with urlopen(renderer['server']+'/queue',timeout=10) as resp:q=json.load(resp)
  other=[x[1] for x in q.get('queue_running',[])+q.get('queue_pending',[])]
  if other:
   idle_since=None
   if last_status!='busy':save('WAITING_FOR_EXISTING_COMFY_JOBS',existing_prompt_ids=other);last_status='busy'
  elif idle_since is None:idle_since=time.monotonic();save('QUIET_NATIVE_QUEUE_OBSERVED',existing_prompt_ids=[]);last_status='idle'
  elif time.monotonic()-idle_since>=90:break
  time.sleep(10)
 validate()
 assert not list((local/'jobs').glob(name+'_*/RENDER_RECEIPT.json'))
 command=[renderer['python'],'-s','-B',str(packet/renderer['entrypoint']),'--preset','quick','--image',str(packet/j['input_path']),'--prompt-file',str(packet/j['prompt_path']),'--name',name,'--seed',str(j['seed'])]
 with (state_dir/'CLI.stdout_stderr.log').open('wb',buffering=0) as log:
  p=subprocess.Popen(command,cwd=r,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
  save('DEVELOPED_CLI_RUNNING',command=command,owned_child_pid=p.pid)
  last_prompt=None;last_report=time.monotonic()
  while p.poll() is None:
   receipts=sorted((local/'jobs').glob(name+'_*/RENDER_RECEIPT.json'))
   if receipts:
    try:
     rec=json.loads(receipts[-1].read_text(encoding='utf-8'));prompt=rec.get('prompt_id')
     if prompt and prompt!=last_prompt:save('NATIVE_PROMPT_SUBMITTED',native_prompt_id=prompt,receipt_path=str(receipts[-1]));last_prompt=prompt
    except ValueError:pass
   if time.monotonic()-last_report>=60:print('REFERENCE_STUDY_RENDERING; identity/action scores unassigned',flush=True);last_report=time.monotonic()
   time.sleep(10)
 receipts=sorted((local/'jobs').glob(name+'_*/RENDER_RECEIPT.json'))
 if p.returncode!=0 or len(receipts)!=1:save('CLI_FAILURE_PRESERVED_NO_RESUBMISSION',process_exit=p.returncode,receipts=[str(x) for x in receipts]);raise SystemExit(2)
 receipt=json.loads(receipts[0].read_text(encoding='utf-8'));graph=json.loads(receipts[0].with_name('workflow.api.json').read_text(encoding='utf-8'))
 assert receipt['status']=='PASS' and receipt['source_sha256']==j['input_sha256'] and receipt['settings']==renderer['settings']
 assert receipt['prompt_sha256']==hashlib.sha256((packet/j['prompt_path']).read_text(encoding='utf-8').encode()).hexdigest()
 assert graph['1']['inputs']['unet_name']=='Wan2.2-TI2V-5B-Q4_K_S.gguf' and graph['2']['inputs']['clip_name']=='umt5-xxl-encoder-Q4_K_S.gguf'
 validate();save('MACHINE_RENDER_PASS_VISUAL_AUDIT_PENDING',process_exit=p.returncode,receipt_path=str(receipts[0]),native_prompt_id=receipt['prompt_id'],outputs=receipt['outputs'],completed_utc=now())
