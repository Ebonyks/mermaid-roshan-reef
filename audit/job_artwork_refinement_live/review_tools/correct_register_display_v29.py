from pathlib import Path
import datetime,json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');live=b/'audit/job_artwork_refinement_live';f=b/'audit/job_geode_coherent_runtime_v1_20261002';prefix=f.relative_to(b).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
old=read(live/'ALL_ITEMS.json');assert old['counts']['registered_items']==1721
shutil.copyfile(live/'ALL_ITEMS.json',live/'ALL_ITEMS_V28.json')
(live/'all_items_V28.html').write_text((live/'all_items.html').read_text(encoding='utf-8').replace('ALL_ITEMS.json','ALL_ITEMS_V28.json'),encoding='utf-8',newline='\n')
for x in old['items']:
 if x['id'].startswith('GEO-COHERENT-RUNTIME'):
  if x['region'] is not None:x['kind']='runtime prop region'
  x['current_object_sequence_score']=4.5
  x['current_complete_action_score']=None
  x['source_qualification']+=' The4.5 sequence score covers geode opening only; complete embodied work remains limited by contact2.7 and room2.8. No whole-job4.5 pass.'
old['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();old['scope']=old['scope'].replace('V28','V29')+' Register display correction: exact runtime region crops and assigned mounted/object sequence scores shown; complete embodied action remains unassigned here.'
old['counts'].pop('individual_runtime_prop_regions',None)
write(live/'ALL_ITEMS.json',old)
p=live/'all_items.html';s=p.read_text(encoding='utf-8')
needle=' · Mounted/action scores unassigned in this register.'
assert s.count(needle)==1
s=s.replace(needle,' · Mounted: ${q.current_mounted_score==null?\'unassigned\':esc(q.current_mounted_score)+\'/5\'} · Object sequence: ${q.current_object_sequence_score==null?\'unassigned\':esc(q.current_object_sequence_score)+\'/5\'} · Complete action: ${q.current_complete_action_score==null?\'unassigned\':esc(q.current_complete_action_score)+\'/5\'}.')
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
shutil.copyfile(__file__,live/'review_tools/correct_register_display_v29.py')
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';d=read(ip);d['scope']+=' V29 display repair: current geode runtime region kind matches existing CSS crop renderer, mounted/object-only sequence opinions shown honestly, no complete embodied action4.5 claim.';d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for folder in [f,live] for p in folder.rglob('*') if p.is_file()});write(ip,d)
p=b/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8').replace('V28 known register1721','V29 known register1721');p.write_text(s,encoding='utf-8',newline='\n')
p=b/'tmp/v2_preview_allowed.json';write(p,sorted(set(read(p))|{p.relative_to(b).as_posix() for folder in [f,live] for p in folder.rglob('*') if p.is_file()}))
print('V29: seven actual regions crop correctly, mounted4.5/object opening4.5 shown; complete embodied action remains unassigned.')
