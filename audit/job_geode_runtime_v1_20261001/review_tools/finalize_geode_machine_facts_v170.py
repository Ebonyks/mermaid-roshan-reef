from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import datetime,hashlib,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'audit/job_geode_runtime_v1_20261001'
full=json.loads((out/'full_ci_v2/RECEIPT.json').read_text());assert full['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE'
assert len(full['source_checks'])==334 and len(full['probe_results'])==82 and full['source_unchanged']
diagnostics=full['raw_diagnostic_count']
machine='Fresh officialGodot4.7.2 unmodified full suite passes82/82;334 literal source hashes unchanged. '+str(diagnostics)+' raw engine diagnostics retained and separately qualified; strict2D and creative acceptance remain open.'
for name in ['audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 p=b/name;s=p.read_text(encoding='utf-8')
 for old in ['Fresh334-source whole suite pending; prior325 source result no longer validates changed runtime.','new334-source entire suite pending.','Fresh334-source full suite pending; prior325-source suite cannot validate changed runtime.']:
  s=s.replace(old,machine)
 if name.endswith('MASTER_AUDIT_2026-08-09.md'):
  lines=s.splitlines();lines=[x.replace('No closure/integration/release.','Known register1573 entries/1196 source files/328 pose cells/38 prop regions/11 source-object regions, including the six embedded geode details;579 inclusive source priorities/388 source-unassigned remain. No closure/integration/release.') if x.startswith('Painted geode production review (2026-10-01):') else x for x in lines];s='\n'.join(lines)+'\n'
 p.write_text(s,encoding='utf-8',newline='\n')
for name in ['assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html','audit/job_review_v2_20261001/index.html','audit/job_artwork_refinement_live/index.html']:
 p=b/name;s=p.read_text(encoding='utf-8');s=s.replace('New source boundary requires its own334-source fresh complete suite.',machine+' The current register includes all six individually reviewed embedded details.');p.write_text(s,encoding='utf-8',newline='\n')
report=out/'index.html';s=report.read_text(encoding='utf-8');s=s.replace('Fresh full suite result pending; source scores do not establish a green run.',machine);report.write_text(s,encoding='utf-8',newline='\n')
q=out/'LIBRARY_QA.json';shutil.copyfile(q,out/'LIBRARY_QA_V1.json');qa=json.loads(q.read_text());qa['checked_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();qa['report_sha256']=hashlib.sha256(report.read_bytes()).hexdigest();qa['checks'].append({'check':'six annotated original-raster cavity cards rendered with six component-specific written evaluations; DOM card/annotation count6, content width1265 equals viewport1265','result':'PASS'});qa['qualification']='Observed browser usability and source-preserving component display; no artwork/device/child/owner acceptance. Earlier pre-expansion report receipt preserved as LIBRARY_QA_V1.json.';q.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v:self.links.append(v)
x=Links();x.feed(report.read_text(encoding='utf-8'));rows=[]
for link in sorted(set(x.links)):
 u=urlparse(link)
 if u.scheme or u.netloc or not u.path:continue
 p=(out/unquote(u.path)).resolve();rows.append({'link':link,'path':p.relative_to(b).as_posix(),'exists':p.is_file(),'inside_workspace':p.is_relative_to(b)})
assert all(x['exists'] and x['inside_workspace'] for x in rows)
(out/'LIBRARY_LINK_CHECK.json').write_text(json.dumps({'status':'PASS_ALL_LITERAL_LOCAL_LIBRARY_LINKS','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'links':rows,'qualification':'Every literal report href/src resolves; frame slider points to separately archived real native screenshots.'},indent=2)+'\n',encoding='utf-8',newline='\n')
dest=out/'review_tools/finalize_geode_machine_facts_v170.py';shutil.copyfile(__file__,dest)
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in out.rglob('*') if p.is_file()});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
allow=b/'tmp/v2_preview_allowed.json';paths=set(json.loads(allow.read_text()));paths.update(d['files']);allow.write_text(json.dumps(sorted(paths),indent=2)+'\n',encoding='utf-8',newline='\n')
print(machine,flush=True);print('Current report references',len(rows),'distinct local files; all exist.',flush=True)
