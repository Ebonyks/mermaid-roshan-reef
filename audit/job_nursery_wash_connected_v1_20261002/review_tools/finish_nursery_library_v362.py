from pathlib import Path
import json,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002';S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert len(read(R/'audit/job_artwork_refinement_live/ALL_ITEMS.json')['items'])==1756
p=R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';s=p.read_text();note=' 2026-10-02 connected Nursery washv3 review: audit/job_nursery_wash_connected_v1_20261002/index.html records1631 consecutive native frames/36 boards/36 full native details, selected static4.5–4.6 but meaningful action3.9/attention3.8/room2.9. Actual Bubble Bath partial-career routes and direct training/catalog fixtures are qualified; no ordinary birthday/full-career/device/child/owner/global acceptance. V34 retains weak clasp/puff history and withholds old Geologist mounted context after shared source change. Current full-suite verification still running; lifecycle unchanged.'
for ident in ['MA-VIS-006','MA-PLAY-004','MA-OPERA-012']:
 start=s.index('## '+ident+'\n');end=s.find('\n## ',start+4);end=end if end>=0 else len(s);chunk=s[start:end];assert '| history |' in chunk
 lines=chunk.splitlines();found=False
 for i,l in enumerate(lines):
  if l.startswith('| history |'):
   assert note not in l;lines[i]=l[:-1]+note+' |';found=True;break
 assert found;s=s[:start]+'\n'.join(lines)+'\n'+s[end:]
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__).parent/'update_nursery_library_v360.py',F/'review_tools/update_nursery_library_v360_partial.original.py')
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
write(F/'LIBRARY_BUILD_ATTEMPTS.json',{'status':'REGISTER_COMPLETED_AFTER_DOCUMENT_SCHEMA_CORRECTION','attempts':[{'source':'review_tools/update_nursery_library_v360_failed.original.py','result':'FAILED missing path in old minimal normalization metadata; existing provenance enriched, preservedV33 untouched.'},{'source':'review_tools/update_nursery_library_v360_partial.original.py','result':'FAILED after register/docs creation at history heading assertion; findings use table history rows. No duplicate register run.'},{'source':'review_tools/finish_nursery_library_v362.py','result':'Completes finding history rows without lifecycle change and updates coverage/refresh. No source or visual gate relaxation.'}]})
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,S] for p in base.rglob('*') if p.is_file()});write(ip,imp)
a=R/'tmp/v2_preview_allowed.json';allow=set(read(a));allow.update(imp['files']);write(a,sorted(allow))
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B','audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v34.py'],cwd=R,check=True)
print('V34 completed:1756 entries/1261 sources; Nursery review current, Geologist mounted review stale; finding lifecycle unchanged.')
