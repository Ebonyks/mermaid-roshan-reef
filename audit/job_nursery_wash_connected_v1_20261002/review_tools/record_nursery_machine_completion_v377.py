from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ci=read(F/'full_ci_v1/RECEIPT.json')
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0
assert len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert len(ci['source_checks'])==783 and all(x['match'] and sha((R/x['path']).read_bytes())==x['before_sha256'] for x in ci['source_checks'])
assert all(sha((F/'full_ci_v1'/(n+'.log')).read_bytes())==ci[n+'_sha256'] for n in ['stdout','stderr'])
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
target=F/'review_tools'/Path(__file__).name;receipt=F/'MACHINE_COMPLETION_V377.json'
imp['files']=sorted(set(imp['files'])|{target.relative_to(R).as_posix(),receipt.relative_to(R).as_posix()});write(ip,imp)
shutil.copyfile(Path(__file__),target)
sentence='Official Godot 4.7.2 unmodified full suite passes 82/82 probes, process 0; all 783 frozen source files remain unchanged. All 53 raw engine diagnostics are preserved and qualified. Local machine verification does not grant strict-zero 2D debt, visual, device, child, owner, integration or release acceptance.'
p=F/'index.html';t=p.read_text(encoding='utf-8');old='The full current trusted Godot suite is running.';assert t.count(old)==1;t=t.replace(old,sentence,1)
t=t.replace('</header>','<p><a href="full_ci_v1/RECEIPT.json">Current full-suite receipt and every source comparison</a> · <a href="full_ci_v1/stdout.log">Unfiltered stdout</a> · <a href="full_ci_v1/stderr.log">Unfiltered stderr</a></p></header>',1);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'audit/MASTER_AUDIT_2026-08-09.md';t=p.read_text(encoding='utf-8');old='Current full unmodified suite running; phone/child/owner, continuous action, comprehensive all-job completion and integration remain open.';assert t.count(old)==1;t=t.replace(old,sentence+' Phone/child/owner, continuous action and comprehensive all-job completion remain open.',1);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'design/05_DOC_LEDGER.md';t=p.read_text(encoding='utf-8');old='Current unmodified full suite running.';assert t.count(old)==1;t=t.replace(old,'Local official 4.7.2 unmodified full suite passes 82/82; all 783 source hashes unchanged, 53 raw diagnostics preserved. No strict-2D/visual/owner acceptance.',1);p.write_text(t,encoding='utf-8',newline='\n')
p=R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';t=p.read_text(encoding='utf-8');note='\n\n### Connected Nursery verification continuation — 2026-10-02\n\n`MA-VIS-006`, `MA-PLAY-004`, and `MA-OPERA-012` retain their existing lifecycle states. [Current Nursery report](../job_nursery_wash_connected_v1_20261002/index.html): the unmodified official Godot 4.7.2 suite passes all 82 probes, process 0, with all 783 frozen local source hashes unchanged; all 53 raw diagnostics remain available. This is machine evidence. Static states 4.5–4.6, meaningful washing 3.9, attention 3.8 and room 2.9 remain separate drafting opinions; device, child, owner and complete all-job acceptance are open. The [local motion A1](../../assets_src/local_motion/nursery_connected_scrub_v1_20261002/index.html) is rejected at reference action 3.6 after all 41 native frames were inspected. The [complete dated Doctor review](../job_nursery_wash_connected_v1_20261002/doctor_dated_full_review_v1/index.html) retains whole washing 2.7 and twelve individual priorities; no current Doctor acceptance or source change. Targeted Nursery eyes-to-hands generation awaits explicit source/destination upload authorization after automatic approval review rejected that transmission; no reference was uploaded.\n'
assert '### Connected Nursery verification continuation — 2026-10-02' not in t;p.write_text(t+note,encoding='utf-8',newline='\n')
p=R/'.gitattributes';t=p.read_text(encoding='utf-8');line='assets_src/imagegen/nursery_palm_attention_v1_20261002/** -text\n';assert line not in t;p.write_text(t+'\n'+line,encoding='utf-8',newline='\n')
imp=read(ip)
for v in imp['validation']:
 if v['command']=='Current source/reuse inventory and fresh baseline capture':v.update(result='PASS',evidence='audit/job_nursery_wash_connected_v1_20261002/PLAN.json; baseline_capture/PROCESS_RECEIPT.json; original fixture/boundary prose separately qualified.')
 if v['command']=='Connected wash specialist and whole-canvas source normalization':v.update(result='PASS',evidence='audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json; six mounted static states 4.5–4.6 and source provenance verified. Current complete action 3.9 remains an independent failed floor, not acceptance.')
imp['validation'].append({'command':'Current Nursery complete meaningful washing visual floor','result':'FAIL','evidence':'audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json; action 3.9, attention 3.8, room 2.9 remain priorities.'})
write(receipt,{'status':'LOCAL_MACHINE_PASS_CREATIVE_PRIORITIES_OPEN','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'suite':'full_ci_v1/RECEIPT.json','suite_sha256':sha((F/'full_ci_v1/RECEIPT.json').read_bytes()),'probes':82,'source_count':783,'all_current_source_hashes_match':True,'raw_engine_diagnostics':53,'qualification':sentence,'owner_acceptance':None,'integration':False,'release':False})
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()});write(ip,imp)
p=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B','audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v34.py'],cwd=R,capture_output=True,check=True)
print(p.stdout.decode('utf-8').strip())
print('NURSERY_MACHINE_COMPLETION|82/82|783 unchanged|53 raw diagnostics retained|creative priorities open')
