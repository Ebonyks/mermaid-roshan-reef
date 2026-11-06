from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,sys,json,hashlib,time,datetime,re
W=Path.cwd();T=Path(__file__).parent;D=T/'r146_native_capture_v2';assert not D.exists(),'Resume recorded nativecapture handle; never duplicate';D.mkdir();G=['git','-c','core.safecrlf=false'];g=lambda *a:subprocess.check_output(G+list(a),stderr=subprocess.DEVNULL);BASE='e70081ea871bd2aab2440be2168abe33d20ee328';assert g('rev-parse','HEAD').decode().strip()==BASE
sha=lambda b:hashlib.sha256(b).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip());assert sha(E.read_bytes())=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
script=W/'scripts/racer/reef_kart_race.gd';candidate=script.read_bytes();old=g('show',BASE+':scripts/racer/reef_kart_race.gd');assert candidate!=old and b'const GasButtonArt'in candidate and b'const GasButtonArt'not in old;(D/'candidate_script_backup.gd').write_bytes(candidate);fixture='assets_src/review/r146_racer_gas_20261106/capture_review.gd';fixture_hash=sha((W/fixture).read_bytes());outroot=W/'assets_src/review/r146_racer_gas_20261106/captures_v2';assert not outroot.exists();outroot.mkdir()
paths=sorted(set(p for p in g('ls-files','--cached','--others','--exclude-standard','-z','--','scripts','assets','scenes','shaders','addons','project.godot','export_presets.cfg').decode().split('\0')if p))
def hash_all():
 with ThreadPoolExecutor(max_workers=4)as pool:return dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
before=hash_all();np=json.loads((T/'NORMAL_SAVE_PIN.json').read_text(encoding='utf-8'));nb=Path(np['normal_base'])
def normals():return{s:sha(Path(str(nb)+s).read_bytes())if Path(str(nb)+s).is_file()else'absent'for s in np['hashes']}
normal_before=normals();write(D/'SOURCE_PIN.json',{'baseline_code':BASE,'candidate_raw_script_sha256':sha(candidate),'baseline_raw_script_sha256':sha(old),'runtime_hashes_before':before,'actual_runtime_inputs':len(paths),'fixture':fixture,'fixture_sha256':fixture_hash,'engine':str(E),'engine_sha256':sha(E.read_bytes()),'normal_before':normal_before,'baseline_scope':'Baseline uses actualE700 scripts; newunused candidatePNG/import remain present during baseline render and are not falsely called cleanE700 full dependency closure. Diagnostic only.'});results=[]
try:
 for variant,data in [('source',old),('candidate',candidate)]:
  script.write_bytes(data)
  for width in [1280,1600]:
   label=variant+'_'+str(width);d=D/label;d.mkdir();out=outroot/label;out.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',R146_CAPTURE_DEST=str(out),R146_CAPTURE_VARIANT=variant,R146_CAPTURE_WIDTH=str(width))
   for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
    q=d/key;q.mkdir();env[key]=str(q)
   cmd=[str(E),'--path',str(W),'--rendering-method','mobile','--display-driver','windows','--audio-driver','Dummy','--log-file',str(d/'native_engine.log'),'-s','res://'+fixture];write(T/'R146_CAPTURE_STATE.json',{'stage':'RUNNING_'+label,'source_script_sha256':sha(data),'command':cmd,'log':str(d/'console.log'),'at_utc':now()});started=time.monotonic()
   with(d/'console.log').open('wb')as log:
    proc=subprocess.Popen(cmd,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
    try:rc=proc.wait(timeout=240)
    except subprocess.TimeoutExpired:
     subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True);proc.wait(timeout=15);raise RuntimeError('Own configuredcapture timedout; inspect before any retry')
   text=(d/'console.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in text.splitlines()if re.search(r'SCRIPT ERROR|Parse Error|Assertion failed|ERROR:|R146_CAPTURE\|FAIL',l)];assert rc==0 and not bad,(label,rc,bad,text[-4000:]);records=json.loads((out/'captures.json').read_text(encoding='utf-8'));assert records['failures']==0 and len(records['records'])==5 and records['width']==width and records['source_script_sha256']==sha(data)
   for row in records['records']:assert row['size']==[width,720]and row['renderer']=='mobile'and row['sha256']==sha((out/row['file']).read_bytes())
   assert sum(r['target_visible']for r in records['records'])==3;assert sha(script.read_bytes())==sha(data)and sha((W/fixture).read_bytes())==fixture_hash;result={'label':label,'exit_code':rc,'elapsed_seconds':round(time.monotonic()-started,3),'source_script_sha256':sha(data),'records':records,'console_sha256':sha((d/'console.log').read_bytes()),'native_log_sha256':sha((d/'native_engine.log').read_bytes())};write(d/'RESULT.json',result);results.append(result);print('R146_NATIVE_PASS',label,flush=True)
finally:script.write_bytes(candidate)
after=hash_all();assert before==after,'Runtime source drift after exactcandidate restoration';assert normals()==normal_before and sha((W/fixture).read_bytes())==fixture_hash
record={'state':'PASS20_SOURCE_CANDIDATE_CONFIGURED_NATIVE_MOBILE_FRAMES_V2','baseline_code':BASE,'results':results,'actual_runtime_inputs':len(paths),'normal_save_unchanged':True,'candidate_restored_raw_sha256':sha(candidate),'runtime_drift':[],'native_events':20,'previous_failed_events':5,'previous_failed_evidence':'R146_CAPTURE_FIRST_FAILURE.json','target_visible_configured_events':12,'no_touch_target_PC_negative_events':8,'source_variant_limit':'Unreferenced candidatePNG/import present with unchangedE700 baselinecode. No cleanGit/fresh-runtime/sourcecommit/fullrouteclaim.','formal_QA11':None,'device':None,'child':None,'owner':None,'accepted_removed':0,'finished_at_utc':now()};write(D/'RESULT.json',record);write(T/'R146_CAPTURE_STATE.json',{'stage':'TERMINAL_PASS','result':str(D/'RESULT.json'),'actual_runtime_inputs':len(paths),'native_events':20});print(record['state'],flush=True)
