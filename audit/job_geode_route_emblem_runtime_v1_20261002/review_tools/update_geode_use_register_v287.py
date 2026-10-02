from pathlib import Path
import copy, datetime, hashlib, json, shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_geode_route_emblem_runtime_v1_20261002';live=r/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(live/'ALL_ITEMS.json');assert d['counts']['registered_items']==1722
if (live/'ALL_ITEMS_V30.json').exists():
 assert sha(live/'ALL_ITEMS.json')==sha(live/'ALL_ITEMS_V30.json')
 assert sha(live/'all_items.html')==sha(live/'all_items_V30.original.html')
else:
 shutil.copyfile(live/'ALL_ITEMS.json',live/'ALL_ITEMS_V30.json')
 shutil.copyfile(live/'all_items.html',live/'all_items_V30.original.html')
 (live/'all_items_V30.html').write_text((live/'all_items.html').read_text(encoding='utf-8').replace("fetch('ALL_ITEMS.json')","fetch('ALL_ITEMS_V30.json')"),encoding='utf-8',newline='\n')
review=read(f/'REVIEW.json');plan=read(f/'PLAN.json');resource=read(f/'RESOURCE_CONTRACT.json')
path='assets/opera/worlds/geology/coherent_geode_v1_20261002/opening_six_states.png';source_sha=sha(r/path)
assert source_sha=='e47a731414210ef70c0b5fffce2828922a15611c6093c244811ee0a283534503'
regions={
 'GEO-USE-LIBRARY':[1392.270574971815,556.446448703495,617.632468996618,393.668545659527],
 'GEO-USE-INVITATION':plan['bindings']['invitation']['region'],
 'GEO-USE-CELEBRATION':[1392.270574971815,556.446448703495,617.632468996618,393.668545659527],
 'GEO-USE-DEV-MENU':[1392.270574971815,556.446448703495,617.632468996618,393.668545659527]}
bindings={'GEO-USE-LIBRARY':'scripts/castle_career_routes.gd','GEO-USE-INVITATION':'scripts/opera_hotspot_catalog.gd','GEO-USE-CELEBRATION':'scripts/opera_career_world_2d.gd','GEO-USE-DEV-MENU':'scripts/opera_job_playtest_menu.gd'}
for x in review['individual_objects'][:4]:
 q=dict(id=x['id'],aliases=[x['id']],kind='runtime prop region',path=path,region=regions[x['id']],source_dimensions=[2048,1024],earlier_sha256=source_sha,historical_source_score=x['artwork_score'],current_source_score=x['artwork_score'],evaluation=x['evaluation'],refinement=x['refinement'],families=['Geologist','Current actual '+x['name']],original_reports=[f.relative_to(r).as_posix()+'/index.html#'+x['id']],source_qualification='Individually inspected current presentation at1280/1600. Exact source region and complete captured native context preserved; material, mounting and complete embodied action remain separate. No owner/device/whole-job acceptance.',preview_path=path,native_reference_observations=[],current_checkout_sha256=source_sha,current_byte_status='EXACT_EARLIER_BYTES',priority=x['priority'],protected_original=False,current_mounted_score=x['score'],current_complete_action_score=None,image_path=path,image_scope='Exact unchanged source region shown by CSS; current mounted screenshot/evaluation linked separately',current_binding=bindings[x['id']],binding_sha256=sha(r/bindings[x['id']]),owner_acceptance=None,latest_refinement=dict(report=f.relative_to(r).as_posix()+'/index.html#'+x['id'],note=x['name']+'; source '+str(x['artwork_score'])+'/5, actual mounting '+str(x['score'])+'/5. '+x['evaluation']))
 d['items'].append(q)
assert len(d['items'])==1726
assert not set(regions)&{x['id'] for x in d['items'][:-4]}
assert len({x['id'] for x in d['items'][-4:]})==4
c=d['counts'];c['registered_items']=1726;c['additional_runtime_prop_regions']=49;c['exact_earlier_bytes']+=4
assert c['unique_source_files']==1245 and c['inclusive_current_source_priorities']==676 and c['unreviewed_current_source']==385
d['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['scope']='V31 known source union:1245 unique source files,328 pose cells,49 runtime prop/use regions and104 source-object regions =1726 entries. Four added current Geologist uses are separate presentations of the same existing atlas, not four new sources. V30 exact JSON/HTML bytes preserved; source priorities676 and unassigned385 unchanged. Current celebration material4.6 does not pass unsupported mounting4.2. This is not exhaustive actual use or all-job/owner acceptance.'
d['qualification']='Literal source-byte continuity retains qualified source opinions. Current mounted/opening opinions are assigned only where exact reports state them; complete embodied action stays separate. The same source can pass material while failing mounting. Inclusive<=4.5 priorities include the named weak current representations;676 counts source opinions only. Protected originals and historical opinions remain preserved; broad all-job/device/child/owner acceptance is open.'
write(live/'ALL_ITEMS.json',d)
status=dict(status='CURRENT_REGISTER_V31_QUALIFIED_SOURCE_AND_USE_OPINIONS',baseline=review['baseline'],created_utc=d['created_utc'],counts=c,new_presentation_ids=list(regions),source_priorities_unchanged=True,owner_acceptance=None,qualification=d['qualification'])
write(live/'CURRENT_REGISTER_V31.json',status)
p=live/'all_items.html';s=p.read_text(encoding='utf-8')
needle='Current source: ${q.current_source_score===null?'
assert s.count(needle)==1;s=s.replace(needle,'Current source/cell artwork: ${q.current_source_score===null?')
s=s.replace("${q.priority?' · priority':''}","${q.priority?' · source or mounted priority':''}")
p.write_text(s,encoding='utf-8',newline='\n')
for rel in ['audit/job_artwork_refinement_live/index.html','audit/job_review_v2_20261001/index.html']:
 p=r/rel;s=p.read_text(encoding='utf-8');pos=s.index('</h1>')+len('</h1>')
 link='../job_geode_route_emblem_runtime_v1_20261002/index.html'
 s=s[:pos]+f'<p><a href="{link}">Current geode: four actual uses and every58 stills/316 frames</a> — Library/invitation4.5 provisional; developer icon4.6; celebration painting4.6 but mounting4.2/composition3.3. V31 known register1726 entries; source676 priorities/385 unassigned remain. FullCI pending372 sources; broad acceptance open.</p>'+s[pos:]
 p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ledger=r/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8')
lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith('| `audit/job_artwork_refinement_live/all_items.html`'):
  lines[i]='| `audit/job_artwork_refinement_live/all_items.html` | 🟣 | `CANDIDATE`; V31 searchable known union1726 entries/1245 unique source files/328 pose cells/49 runtime prop-use regions/104 source-object regions. Four current geode presentations of the same unchanged atlas carry separate material and mounted opinions; goal material4.6 fails placement4.2. Literal source priorities676/unassigned385 unchanged. V30 exact JSON/HTML bytes preserved; current source/use opinions do not grant exhaustive actual use, full actions, device/child/owner or all-job acceptance. |'
ledger.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';impact=read(ip)
impact['files']=sorted(set(impact['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{p.relative_to(r).as_posix() for p in [live/'ALL_ITEMS.json',live/'ALL_ITEMS_V30.json',live/'all_items.html',live/'all_items_V30.html',live/'all_items_V30.original.html',live/'CURRENT_REGISTER_V31.json',live/'index.html',r/'audit/job_review_v2_20261001/index.html']})
impact['scope']+=' V31 adds four distinct actual-use regions without changing unique-source or source-priority counts; oldV30 exact bytes preserved, celebration material/mounting separated.'
write(ip,impact)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(impact['files'])))
print('V31:1726 entries;1245 sources,49 runtime regions;676 source priorities/385 unassigned unchanged. Four actual geode uses recorded.')
