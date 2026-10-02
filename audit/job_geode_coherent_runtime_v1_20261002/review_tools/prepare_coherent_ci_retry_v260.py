from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geode_coherent_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ci=read(f/'full_ci_v2/RECEIPT.json')
assert ci['status']=='FAIL_PRESERVED_CURRENT_FULL_SUITE' and ci['source_unchanged']
assert [(x['probe'],x['process_exit']) for x in ci['probe_results'] if x['process_exit']] == [('probe_passive',127)]
assert len(ci['source_checks'])==368
assert all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
old=(f/'review_tools/run_coherent_geode_full_ci_v247.py').read_text(encoding='utf-8')
assert "folder=family/'full_ci_v2'" in old
old=old.replace("folder=family/'full_ci_v2'","folder=family/'full_ci_v3'").replace('/full_ci_v2/','/full_ci_v3/').replace('full suite2 scripts/ci.sh','full suite3 scripts/ci.sh')
runner=f/'review_tools/run_coherent_geode_full_ci_v261.py';assert not runner.exists();runner.write_text(old,encoding='utf-8',newline='\n')
write(f/'FULL_CI_RETRY_REASON.json',dict(status='FAILED_SUITE_PRESERVED_NEW_RUN_REQUIRED',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),failed_receipt='full_ci_v2/RECEIPT.json',failed_probe='probe_passive',process_exit=127,completed_probe_count=82,successful_probes=81,source_count=368,source_unchanged=True,observation='Godot booted and reported two completed 60-second passive legs, then exited 127 before its final verdict. No error or native crash cause is established in the retained streams or bounded Windows Application log query. Exit 127 is a failure, never a pass.',new_run='full_ci_v3/RECEIPT.json',method='Repeat the unchanged official full suite on identical frozen sources. No simultaneous display capture or independent Godot test is scheduled during this retry. No probe, engine, save contract, timeout or production behavior is changed.',qualification='A successful retry will remain separate from the failed run; no suppressed failure or invented root cause. Creative, device, child and owner acceptance remain outstanding.'))
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});d['validation'].append(dict(command='Preserved full-suite2 failure and unchanged-source retry preparation',result='PENDING',evidence=f.relative_to(b).as_posix()+'/FULL_CI_RETRY_REASON.json; suite2 passive127,81 other probes0; suite3 not yet complete.'));write(ip,d)
subprocess.run([sys.executable,'-X','utf8','-B',str(runner),'--prepare'],cwd=b,check=True)
print('Retry prepared. Frozen368 unchanged; prior failed suite retained.',flush=True)
