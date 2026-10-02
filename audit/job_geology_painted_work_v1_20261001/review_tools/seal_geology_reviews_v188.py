from pathlib import Path
import datetime, hashlib, html, json, posixpath, re, shutil

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
work=b/'audit/job_geology_painted_work_v1_20261001'
river=b/'assets_src/imagegen/geologist_river_components_v1_20261001'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ci=read(work/'full_ci_v1/RECEIPT.json')
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0 and ci['source_unchanged'] and len(ci['source_checks'])==349 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
machine='Fresh current officialGodot4.7.2 unmodified complete suite passes82/82, process0; all349 literal source hashes unchanged. All53 raw engine diagnostics retained and separately qualified. This is local machine verification, not hosted or visual/owner acceptance.'
p=work/'index.html';s=p.read_text(encoding='utf-8');s=re.sub(r'(<p id="ci-state">).*?(</p>)',lambda m:m[1]+machine+m[2],s,count=1);p.write_text(s,encoding='utf-8',newline='\n')
p=work/'REVIEW.json';d=read(p);d['machine_verification']={'receipt':'audit/job_geology_painted_work_v1_20261001/full_ci_v1/RECEIPT.json','status':ci['status'],'probes':82,'literal_source_count':349,'source_unchanged':True,'raw_engine_diagnostics':53,'qualification':machine};write(p,d)
for name,old in [('audit/MASTER_AUDIT_2026-08-09.md','Fresh current full suite pending; historical H82/82 remains its own334-source evidence.'),('audit/findings/ACTIVE_FINDINGS_2026-08-13.md','Fresh current complete suite pending; H82/82 is historical334-source evidence.')]:
 p=b/name;s=p.read_text(encoding='utf-8');assert old in s or machine in s,name;s=s.replace(old,machine,1);p.write_text(s,encoding='utf-8',newline='\n')
p=b/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8');lines=s.splitlines();marker='`audit/job_geology_painted_work_v1_20261001/index.html`';found=False
for i,line in enumerate(lines):
 if marker in line:
  line=line.replace('Fresh current full CI pending, earlier H82/82 applies only to its334 literal sources. ','')
  lines[i]=line
  if 'Fresh current full suite82/82' not in line:lines[i]=line[:-2]+' Fresh current full suite82/82,349 literal hashes unchanged,53 raw diagnostics retained; local machine result only. |'
  found=True
assert found;p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
# Add literal current native comparisons; source artwork and runtime remain separate.
p=river/'index.html';s=p.read_text(encoding='utf-8');d=read(work/'REVIEW.json');views=[x for x in d['current_views'] if x['width']==1280 and (x['state']=='river_task_open' or x['state'].startswith('river_earned'))];assert len(views)==2
pics=''.join('<figure><img class="whole" src="'+posixpath.relpath(x['path'],river.relative_to(b).as_posix())+'" alt="'+html.escape(x['state'])+'"><figcaption>'+html.escape(x['state'].replace('_',' ').title())+' · current1280×720 · '+str(x['sampled_state_score'])+'/5</figcaption></figure>' for x in views)
s=s.replace('<p><a href="../../../audit/job_geology_painted_work_v1_20261001/index.html">All46',pics+'<p><a href="../../../audit/job_geology_painted_work_v1_20261001/index.html">All46',1);p.write_text(s,encoding='utf-8',newline='\n')
qa=read(river/'LIBRARY_LINK_QA.json');qa['references']+=[{'reference':posixpath.relpath(x['path'],river.relative_to(b).as_posix()),'target':x['path'],'exists':(b/x['path']).is_file()} for x in views];qa['checked_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write(river/'LIBRARY_LINK_QA.json',qa)
publisher=work/'review_tools/executed_publish_geology_work_v183.py';s=publisher.read_text(encoding='utf-8');needle="assert len(snapshot)==349 and all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in snapshot)";assert needle in s;s=s.replace(needle,needle+"\nci=json.loads((b/'audit/job_geology_painted_work_v1_20261001/full_ci_v1/RECEIPT.json').read_text())\nassert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])",1);s=s.replace('Expand the individual register to1586 entries without counting repeated prop instances as new images.','Expand the individual register to1596 entries without counting repeated prop instances as new images. Preserve two fresh river originals/two uniform derivatives and six source component opinions: four selected4.6, two sealed-ended connectors rejected4.0. These river sources remain unbound; no network/action score inferred.');publisher.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,work/'review_tools'/Path(__file__).name)
for impact,folder in [('job-geology-painted-work-20261001.json',work),('job-geology-river-painted-source-20261001.json',river)]:
 p=b/'design/audit_impacts'/impact;d=read(p);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in folder.rglob('*') if p.is_file()});write(p,d)
print('Current82/82 machine result linked; two actual native river comparisons added; exact scoped publisher hardened.')
