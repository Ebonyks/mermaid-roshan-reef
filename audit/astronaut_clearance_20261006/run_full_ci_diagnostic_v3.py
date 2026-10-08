from pathlib import Path
import json, hashlib, time, datetime, subprocess, os, re, ctypes
from ctypes import wintypes
ROOT=Path(__file__).resolve().parents[2]
AD=Path(__file__).resolve().parent
PLAN=json.loads((AD/'FULL_CI_DIAGNOSTIC_V3_PLAN.json').read_text())
BINDINGS=json.loads((AD/PLAN['source_bindings']).read_text())
GODOT=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
started=time.monotonic()
receipt={'result':'PENDING','source_binding_changes':[],'engine_started':False,'plan':'FULL_CI_DIAGNOSTIC_V3_PLAN.json','scope':PLAN['scope']}
def save(result):
 receipt.update(result=result,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=round(time.monotonic()-started,3))
 (AD/'FULL_CI_DIAGNOSTIC_V3_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
class Memory(ctypes.Structure):
 _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage','PrivateUsage']]
psapi=ctypes.WinDLL('psapi',use_last_error=True)
kernel=ctypes.WinDLL('kernel32',use_last_error=True)
psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Memory),wintypes.DWORD]
psapi.GetProcessMemoryInfo.restype=wintypes.BOOL
kernel.GetProcessHandleCount.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
kernel.GetProcessHandleCount.restype=wintypes.BOOL
kernel.GetProcessTimes.argtypes=[wintypes.HANDLE]+[ctypes.POINTER(wintypes.FILETIME)]*4
kernel.GetProcessTimes.restype=wintypes.BOOL
def counters(proc):
 h=wintypes.HANDLE(int(proc._handle));m=Memory();m.cb=ctypes.sizeof(m)
 hc=wintypes.DWORD();ft=[wintypes.FILETIME() for _ in range(4)]
 assert psapi.GetProcessMemoryInfo(h,ctypes.byref(m),m.cb),ctypes.get_last_error()
 assert kernel.GetProcessHandleCount(h,ctypes.byref(hc)),ctypes.get_last_error()
 assert kernel.GetProcessTimes(h,*[ctypes.byref(f) for f in ft]),ctypes.get_last_error()
 sec=lambda f:((f.dwHighDateTime<<32)+f.dwLowDateTime)/1e7
 return {'elapsed_seconds':round(time.monotonic()-started,3),'pid':proc.pid,'rss_bytes':m.WorkingSetSize,'peak_rss_bytes':m.PeakWorkingSetSize,'private_bytes':m.PrivateUsage,'kernel_cpu_seconds':sec(ft[2]),'user_cpu_seconds':sec(ft[3]),'handles':hc.value}
assert hashlib.sha256(GODOT.read_bytes()).hexdigest()=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
for n,h in BINDINGS.items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
inventory=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^Godot.*\\.exe$' -and $_.Name -notmatch '^godot-ai'}) | Select-Object ProcessId,Name,CreationDate | ConvertTo-Json -Compress"],capture_output=True,text=True,timeout=10,creationflags=subprocess.CREATE_NO_WINDOW)
assert inventory.returncode==0,inventory.stderr
receipt['entry_engine_inventory']=inventory.stdout.strip() or 'EMPTY'
if inventory.stdout.strip():save('FAIL_PREFLIGHT_OTHER_ENGINE');print('ABORT_OTHER_ENGINE',flush=True);raise SystemExit(1)
temp=Path(PLAN['temporary_root']);assert temp.parent.resolve()==Path(os.environ['LOCALAPPDATA'],'Temp').resolve();assert not temp.exists();temp.mkdir()
for n in ['appdata','localappdata','data','config']:(temp/n).mkdir()
env=os.environ.copy();env.update(APPDATA=str(temp/'appdata'),LOCALAPPDATA=str(temp/'localappdata'),XDG_DATA_HOME=str(temp/'data'),XDG_CONFIG_HOME=str(temp/'config'),PYTHONIOENCODING='utf-8',PYTHONUTF8='1')
log=AD/'FULL_CI_DIAGNOSTIC_V3_LOG.txt';res=AD/'FULL_CI_DIAGNOSTIC_V3_RESOURCES.jsonl'
argv=[str(GODOT),'--headless','--verbose','--path',str(ROOT),'-s','scripts/probe_opera_2d.gd','--','--touch','--classic-touch-test']
proc=None;termination=None
try:
 with log.open('wb') as out,res.open('w',encoding='utf-8') as samples:
  proc=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
  engine_start=time.monotonic();receipt.update(engine_started=True,pid=proc.pid,argv=argv,start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save('RUNNING');print('START Opera diagnostic PID'+str(proc.pid),flush=True)
  while proc.poll() is None:
   if time.monotonic()-engine_start>=PLAN['owned_probe_timeout_seconds'] or time.monotonic()-started>=PLAN['diagnostic_seconds_ceiling']:termination='OWNED_TIME_CAP';break
   if log.stat().st_size>32*1024**2:termination='OWNED_LOG_CAP';break
   row=counters(proc);samples.write(json.dumps(row)+'\n');samples.flush()
   if row['rss_bytes']>6*1024**3:termination='OWNED_RSS_CAP';break
   time.sleep(2)
  if termination:proc.kill()
  rc=proc.wait(timeout=10);receipt.update(exit_code=rc,engine_elapsed_seconds=round(time.monotonic()-engine_start,3),owned_termination_reason=termination)
except BaseException as exc:
 receipt['runner_error']=repr(exc)
 if proc is not None and proc.poll() is None:proc.kill();receipt['owned_termination_reason']='RUNNER_EXCEPTION_CLEANUP';receipt['exit_code']=proc.wait(timeout=10)
 save('FAIL_RUNNER');raise
text=log.read_text(encoding='utf-8',errors='replace');lines=text.splitlines()
fail=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error')
receipt.update(final_result_seen='OPERA2D|result: ALL OK' in text,failure_lines=[l for l in lines if fail.search(l)],pass_lines=sum(l.startswith('OPERA2D|OK|') for l in lines),last_lines=lines[-24:],log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),resource_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),resource_sample_count=len(res.read_text().splitlines()),source_binding_changes=[n for n,h in BINDINGS.items() if hashlib.sha256((ROOT/n).read_bytes()).hexdigest()!=h])
okay=rc==0 and receipt['final_result_seen'] and not receipt['failure_lines'] and not receipt['source_binding_changes'] and termination is None
save('PASS' if okay else 'FAIL');print(json.dumps({k:receipt[k] for k in ['result','exit_code','elapsed_seconds','engine_elapsed_seconds','final_result_seen','resource_sample_count','owned_termination_reason']}),flush=True)
raise SystemExit(0 if okay else 1)
