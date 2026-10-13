"""Aggregate unchanged CI pre-gates and all trusted probes with exact same-command retries."""
from pathlib import Path
import json,re,hashlib,subprocess,datetime
P=Path(__file__).resolve().parent;R=P.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
ci=(R/'scripts/ci.sh').read_text(encoding='utf-8',newline='\n');expected=re.search(r'^for p in (.*); do$',ci,re.M).group(1).split();raw=(P/'publication_diagnostics/full_local_ci.log').read_bytes();text=raw.decode('utf-8','replace');started=re.findall(r'^=== (probe_[^ ]+) ===$',text,re.M);exits=re.findall(r'^PROBE (probe_[^ ]+) process exit: (\d+)$',text,re.M)
assert len(expected)==len(set(expected)) and started==expected and [p for p,c in exits]==expected,'full required probe census'
original=json.loads((P/'publication_diagnostics/full_local_ci_record.json').read_text(encoding='utf-8'));assert original['exit_code'] in [0,1],'unexpected fullgate termination'
retries=json.loads((P/'LOCAL_CI_TARGET_RETRIES.json').read_text(encoding='utf-8'))['results'];retry={x['probe']:x for x in retries};resolved=subprocess.check_output(['python','-B','tools/resolve_godot.py'],cwd=R,text=True).strip();rows=[]
assert not re.findall(r'^PROBE .* (?:reported a failure|reported a resource|hit a script compile|produced no output)',text,re.M),'hard content/resource failures require repair'
for p,rc in exits:
 if rc=='0':rows.append({'probe':p,'result':'PASS','evidence':'publication_diagnostics/full_local_ci.log','initial_process_exit':0});continue
 x=retry[p];assert x['native_windows_returncode']==0 and not x['timed_out'] and not x['failure_lines'],'unresolved failedprobe '+p
 flag='--hybrid-touch-test' if p in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test'
 assert x['command']==[resolved,'--headless','--path',str(R),'-s','scripts/'+p+'.gd','--','--touch',flag],'retry command/engine drift'
 b=(P/x['log']).read_bytes();assert sha(b)==x['log_sha256'] and b.strip(),'retry exactbytes/floor';rows.append({'probe':p,'result':'PASS_AFTER_SAME_SOURCE_NATIVE_RETRY','initial_process_exit':int(rc),'evidence':x['log'],'log_sha256':x['log_sha256']})
assert not subprocess.check_output(['git','diff','e2b3c73789707aa49a91b4f42e2a9dd4b68225df','--','scripts','scenes','assets','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE),'runtime source drift'
record={'schema':'reef.full_validation/1','recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_PROBE_BY_PROBE_WITH_RECORDED_RETRIES','approved_engine':resolved,'engine_version':'4.7.2.stable.official.ed1daf0bf','source_baseline':'e2b3c73789707aa49a91b4f42e2a9dd4b68225df','runtime_diff':[],'pre_probe_static_import_and_2d_gates':'PASS: unchangedci exits before probe loop on anypregate failure;fulltranscriptreachesallrequiredtrustedprobes. Finaldoc/2Dgatesseparatelyrecorded aftermetadatachanges.','original_full_ci_exit':original['exit_code'],'original_full_ci_log_sha256':sha(raw),'trusted_required':len(expected),'trusted_passed':len(rows),'same_source_native_retries':sum(x['result']!='PASS' for x in rows),'rows':rows,'limit':'Original Bash CI failure remains recorded;native sameengine/args/profile retries satisfy permitted probe-by-probe lane,not an unmodifiedCI green claim. Prematurecode127causeunestablished. No probe/gate changes. No creative/device/child/owner acceptance.'}
(P/'FULL_VALIDATION.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('FULL_VALIDATION|ALL OK|',len(rows),'trustedprobes with',record['same_source_native_retries'],'recorded same-source native retries;originalCIexit',original['exit_code'])
