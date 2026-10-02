from pathlib import Path
import json,hashlib,datetime,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002';S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002';L=R/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
extra=['.gitattributes','design/05_DOC_LEDGER.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/job_artwork_refinement_live/ALL_ITEMS.json','audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json','audit/job_artwork_refinement_live/ALL_ITEMS_V33.original.json','audit/job_artwork_refinement_live/ALL_ITEMS_V33.original.html','audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v34.py','audit/job_review_v2_20261001/index.html','audit/job_review_v2_20261001/INDEX_BEFORE_NURSERY_V360.original.html']
imp['files']=sorted(set(imp['files'])|set(extra));imp['scope']+=' Extend the refreshable known-item register with all seven new source attempts, seven reversible runtime derivatives and thirteen separately scored current state/use/action opinions. Preserve exact V33 bytes; withhold old Geologist mounted evidence after the shared CareerWorld binding changes. Current Nursery static states4.5–4.6, action3.9 and room2.9 do not close global or owner gates.';write(ip,imp)
assert not (L/'ALL_ITEMS_V33.original.json').exists()
shutil.copyfile(L/'ALL_ITEMS.json',L/'ALL_ITEMS_V33.original.json');shutil.copyfile(L/'all_items.html',L/'ALL_ITEMS_V33.original.html')
shutil.copyfile(R/'audit/job_review_v2_20261001/index.html',R/'audit/job_review_v2_20261001/INDEX_BEFORE_NURSERY_V360.original.html')
d=read(L/'ALL_ITEMS.json');assert len(d['items'])==1729
review=read(F/'DIRECT_REVIEW_CURRENT_V3.json');report=F.relative_to(R).as_posix()+'/index.html';now=review['reviewed_utc']
template=next(x for x in d['items'] if x['kind']=='source')
for p in sorted(S.glob('*/SOURCE_REVIEW.json')):
 o=read(p);folder=p.parent.name;norm=o['runtime_normalization']
 for variant,path,dims in [('NATIVE',p.parent.relative_to(R).as_posix()+'/native.png',o['native']['size']),('RUNTIME',norm['path'],norm['size'])]:
  ident='NUR-WASH-SRC-'+folder.upper().replace('_','-')+'-'+variant
  q={k:v for k,v in template.items() if k in ['kind','native_reference_observations','protected_original']}
  q.update(id=ident,aliases=[ident],kind='source',path=path,earlier_sha256=sha(R/path),current_checkout_sha256=sha(R/path),historical_source_score=o['score'],current_source_score=o['score'],evaluation=o['note'],refinement='Static source draft only. Preserve the weak clasp unbound; refine action/attention and mounted room independently.',families=['Nursery','Connected washing',folder,variant.lower()],original_reports=[S.relative_to(R).as_posix()+'/index.html',report],source_qualification='Native individually inspected built-in imagegen source; runtime is the recorded uniform whole-canvas derivative. The selected runtime state has separate native mounted review. This source opinion is not complete action or owner acceptance.',preview_path=path,image_path=path,image_scope='Complete preserved native RGBA' if variant=='NATIVE' else 'Uniform whole-canvas1024 POT runtime derivative',current_byte_status='EXACT_REVIEWED_GENERATION_BYTES',source_dimensions=dims,priority=o['score']<=4.5,current_mounted_score=None,current_complete_action_score=None,current_reviewed_utc=o['reviewed_utc'],native_reference_observations=[],protected_original=False,owner_acceptance=None,latest_refinement={'report':S.relative_to(R).as_posix()+'/index.html','note':folder+' source '+str(o['score'])+'/5; current complete action3.9 is separate.'})
  d['items'].append(q)
statefiles={'ready':'ready','wet':'wet','rub_palm':'rub_palm02','rub_back':'rub_back','rinse':'rinse','clean':'clean'}
for o in review['individual_items']:
 state=next((s for s in statefiles if o['id']=='NUR-WASH-STATE-'+s.upper().replace('_','-')),None)
 stem=statefiles[state] if state else ('clean' if o['id'] in ['NUR-WASH-USE-CONSEQUENCE','NUR-WASH-USE-TRANSITION'] else 'rub_palm02')
 path='assets/opera/worlds/nursery/wash_connected_v1_20261002/'+stem+'.png'
 detail=next(x for x in review['native_details'] if x['case']=='actual_bubble_bath_1280' and x['state']==(state or ('clean' if stem=='clean' else 'rub_palm')))
 source_score=o['artwork_score'] if o['artwork_score'] is not None else (4.6 if o['id'] in ['NUR-WASH-USE-BASIN','NUR-WASH-USE-CONSEQUENCE'] else None)
 action=o['score'] if o['id'] in ['NUR-WASH-USE-ACTION','NUR-WASH-USE-ATTENTION','NUR-WASH-USE-TRANSITION'] else None
 q=dict(id=o['id'],aliases=[o['id']],kind='runtime prop region',path=path,region=[0,0,1024,1024],source_dimensions=[1024,1024],earlier_sha256=sha(R/path),current_checkout_sha256=sha(R/path),historical_source_score=source_score,current_source_score=source_score,current_mounted_score=o['score'],current_complete_action_score=action,evaluation=o['evaluation'],refinement=o['refinement'],families=['Nursery','Connected washing',o['name']],original_reports=[report+'#'+o['id']],source_qualification=review['method']+' '+review['route_qualification'],preview_path=detail['path'],image_path=detail['path'],image_scope='Full native actual Bubble Bath mounted capture; region refers to related whole-canvas runtime source, not a crop of this screenshot.',current_byte_status='EXACT_CURRENT_REVIEW_BYTES',priority=o['priority'],native_reference_observations=[],protected_original=False,current_binding='scripts/opera_nursery_surface.gd',binding_sha256=sha(R/'scripts/opera_nursery_surface.gd'),capture_family='nursery_wash_v3',current_capture_review=F.relative_to(R).as_posix()+'/DIRECT_REVIEW_CURRENT_V3.json',current_reviewed_utc=now,owner_acceptance=None,latest_refinement={'report':report+'#'+o['id'],'note':o['name']+' '+str(o['score'])+'/5. '+o['evaluation']})
 d['items'].append(q)
assert len(d['items'])==1756 and len({x['id'] for x in d['items']})==1756
d['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
d['scope']='V34 known union:1261 unique source files,328 pose cells,63 runtime state/prop-use records,104 source-object regions =1756 entries. Fourteen new Nursery source/derivative files and thirteen current individual state/use/action opinions. Fresh Nursery direct review covers1631 consecutive captured frames on36 ordered boards and36 native state details. Six selected stills4.5–4.6; complete action3.9, attention3.8, room2.9. Old Geologist mounted evidence is withheld after shared CareerWorld change until a fresh rerender. Exact V33 JSON/HTML and old opinions remain available. Other opinions retain their own dates. This known union is not exhaustive live-use or all-job acceptance.'
d['counts'].update(unique_source_files=1261,additional_runtime_prop_regions=63,registered_items=1756,inclusive_current_source_priorities=690,current_nursery_mounted_priorities=10,current_geode_mounted_priorities=0,new_named_generated_sources=7,new_runtime_derivatives=7)
d['refresh_command']='python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v34.py';write(L/'ALL_ITEMS.json',d)
src=(L/'review_tools/refresh_current_job_review_v33.py').read_text()
needle="(live/'CURRENT_BOUNDARY_REFRESH.json').write_text"
insert="""nursery=root/'audit/job_nursery_wash_connected_v1_20261002'
nsnapshot=json.loads((nursery/'SOURCE_CURRENT_MACHINE_V3.json').read_text())
nboundary=[dict(path=x['path'],recorded_sha256=x['sha256'],observed_sha256=sha(root/x['path'])) for x in nsnapshot['source_files']]
nchanged=[x for x in nboundary if x['recorded_sha256']!=x['observed_sha256']]
stamp.update(nursery_capture_boundary_match=not nchanged,nursery_capture_source_count=len(nboundary),nursery_changed_sources=nchanged,nursery_review='audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json')
stamp['status']='CURRENT_NURSERY_BOUNDARY_MATCH_GEODE_REVIEW_STALE' if not nchanged and changed else ('CURRENT_CAPTURE_BOUNDARIES_MATCH' if not nchanged and not changed else 'NURSERY_CURRENT_CAPTURE_REVIEW_STALE')
stamp['qualification']+=' Current Nursery v3 room/caller captures are separately source-bound; old Doctor/birthday/full-career/device evidence is not promoted by a hash refresh.'
"""
assert needle in src;src=src.replace(needle,insert+needle);(L/'review_tools/refresh_current_job_review_v34.py').write_text(src,encoding='utf-8',newline='\n')
p=L/'all_items.html';s=p.read_text().replace('refresh_current_job_review_v33.py','refresh_current_job_review_v34.py')
old="(q.id.startsWith('GEO-USE-')&&!stamp.geode_capture_boundary_match)"
assert old in s;s=s.replace(old,"(q.id.startsWith('GEO-USE-')&&!stamp.geode_capture_boundary_match)||(q.capture_family==='nursery_wash_v3'&&!stamp.nursery_capture_boundary_match)")
s=s.replace("!q.id.startsWith('GEO-USE-')&&q.current_source_score", "!q.id.startsWith('GEO-USE-')&&q.capture_family!=='nursery_wash_v3'&&q.current_source_score")
needle="d.counts.unreviewed_current_source=";assert needle in s;s=s.replace(needle,"d.counts.current_nursery_mounted_priorities=d.items.filter(q=>q.capture_family==='nursery_wash_v3'&&q.current_mounted_score!=null&&q.current_mounted_score<=4.5).length;"+needle)
s=s.replace('${c.current_geode_mounted_priorities} additional current geode mounted priorities;', '${c.current_geode_mounted_priorities} current geode mounted priorities; ${c.current_nursery_mounted_priorities} additional current Nursery state/use/action priorities;')
s=s.replace('<h1>', '<p><a href="../job_nursery_wash_connected_v1_20261002/index.html">Current Nursery washing: every state and complete action</a></p><h1>',1);p.write_text(s,encoding='utf-8',newline='\n')
p=R/'.gitattributes';s=p.read_text();s+='\naudit/job_artwork_refinement_live/ALL_ITEMS_V33.original.* -text\naudit/job_review_v2_20261001/INDEX_BEFORE_NURSERY_V360.original.html -text\n';p.write_text(s,encoding='utf-8',newline='\n')
p=R/'ASSET_LICENSES.md';s=p.read_text();lines=s.splitlines()
for i,l in enumerate(lines):
 if l.startswith('| `assets/opera/worlds/nursery/wash_connected_v1_20261002/'):
  lines[i]=l.replace('1280 to1024','1254 to1024').replace('1280to1024','1254to1024')
lines.append('| `audit/job_nursery_wash_connected_v1_20261002/**` | Authorized native game captures, ordered QA contact sheets and documentary browser proof | Project-authored review evidence | Corresponding source-bound PLAN/capture/direct-review receipts | All frames/failed attempts preserved. Read-only sheets are display evidence, never generation or runtime pixels. Static, complete-action, machine, device and owner lanes remain separate. |')
p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
p=R/'audit/job_review_v2_20261001/index.html';s=p.read_text();new='<section id="current-nursery"><h2>Current Nursery washing review</h2><p>The empty work subject is repaired with connected painted wet, palm, back, rinse and earned-clean states. All1631 current consecutive frames and36 native details directly reviewed at1280/1600 in training/catalog fixtures and actual Bubble Bath caller routes. Selected stills4.5–4.6; full washing action3.9, attention3.8 and room2.9 remain priorities. Weak clasp4.4 and earlier puff overlap preserved. Current full suite running; no device, child, owner or all-job acceptance.</p><p><a href="../job_nursery_wash_connected_v1_20261002/index.html">Illustrated report and complete native frame viewer</a> · <a href="../../assets_src/imagegen/nursery_wash_connected_v1_20261002/index.html">Every source attempt</a> · <a href="../job_artwork_refinement_live/all_items.html">V34 individual library</a></p><p>Earlier Geologist capture opinions retain their recorded source and dates. The shared CareerWorld change requires a fresh Geologist rerender before mounted claims apply to this candidate; the V34 refresh withholds them.</p></section>'
s=s.replace('<main>','<main>'+new,1) if '<main>' in s else s.replace('<body>','<body>'+new,1);p.write_text(s,encoding='utf-8',newline='\n')
p=R/'design/05_DOC_LEDGER.md';s=p.read_text();lines=s.splitlines()
for i,l in enumerate(lines):
 if l.startswith('| `audit/job_artwork_refinement_live/all_items.html`'):
  lines[i]='| `audit/job_artwork_refinement_live/all_items.html` | 🟣 | `CANDIDATE`; V34 known union1756 entries/1261 source files/328 pose cells/63 runtime state-use records/104 source-object regions. New Nursery seven native plus seven derivative files and thirteen source-bound state/use/action opinions;690 inclusive source/cell/region priorities plus10 current Nursery mounted/action priorities,385 unassigned source reviews. Current shared CareerWorld changes withhold prior Geologist mounted claims until rerender. Exact V33 bytes and earlier opinions preserved; refreshV34 grants no fresh visual/owner approval. Not exhaustive live-use or all-job acceptance. |'
s='\n'.join(lines)+'\n'
s+='\n| `audit/job_nursery_wash_connected_v1_20261002/index.html` | 🟣 | `CANDIDATE`; connected Nursery washv3,1631 native frames/36 ordered boards/36 full native details directly reviewed. Six selected static states4.5–4.6; action3.9, attention3.8, room2.9 remain weak. Four training/catalog fixtures and two actual Bubble Bath partial-career caller routes at1280/1600; no ordinary birthday/full-career reward/device/child/owner acceptance. Current unmodified full suite running. |\n| `assets_src/imagegen/nursery_wash_connected_v1_20261002/index.html` | 🟣 | `CANDIDATE_SOURCE`; seven preserved built-in imagegen RGBA1254 originals, exact prompts/references/provenance, whole-canvas1024 POT derivatives. Weak clasp4.4 unbound; six selected static states meet provisional4.5 floor. Complete motion/room and owner lanes separate. |\n| `audit/job_artwork_refinement_live/ALL_ITEMS_V33.original.json` | ⚪ | `HISTORICAL_SUPPORTING`; exact precedingV33 register, source opinions and dated Geologist mounted evidence preserved; no current-context promotion. |\n| `audit/job_review_v2_20261001/INDEX_BEFORE_NURSERY_V360.original.html` | ⚪ | `HISTORICAL_SUPPORTING`; exact pre-Nursery landing and its scoped checkpoint status. |\n'
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text();paragraph='\nConnected Nursery washing continuation (2026-10-02): [current illustrated report](job_nursery_wash_connected_v1_20261002/index.html) preserves seven generated attempts, weak clasp4.4 and earlier generic puff-overlap. All1631 current consecutive frames on36 ordered boards plus36 full native state details directly reviewed. Connected selected static states4.5–4.6; whole meaningful wash3.9, attention3.8 and room2.9 remain priorities. Four training/authored catalog fixtures and two actual Bubble Bath partial-career caller routes at1280/1600; Nursery is absent from live birthday roster. V34 library1756 entries adds14 source/derivative files and13 separate current state/use/action opinions, retains V33 bytes and withholds old Geologist mounted claims after shared CareerWorld change. Current full unmodified suite running; phone/child/owner, continuous action, comprehensive all-job completion and integration remain open. [Impact](../design/audit_impacts/job-nursery-wash-connected-20261002.json). No finding closure.\n'
s=s.replace('## 0. Planning entry\n','## 0. Planning entry\n'+paragraph,1)
heading='## Development task index\n';assert heading in s;s=s.replace(heading,heading+paragraph,1);p.write_text(s,encoding='utf-8',newline='\n')
p=R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';s=p.read_text();note=' 2026-10-02 connected Nursery washv3 review: audit/job_nursery_wash_connected_v1_20261002/index.html records1631 consecutive native frames/36 boards/36 full native details, selected static4.5–4.6 but meaningful action3.9/attention3.8/room2.9. Actual Bubble Bath partial-career routes and direct training/catalog fixtures are qualified; no ordinary birthday/full-career/device/child/owner/global acceptance. V34 retains weak clasp/puff history and withholds old Geologist mounted context after shared source change. Current full-suite verification still running; lifecycle unchanged.'
for ident in ['MA-VIS-006','MA-PLAY-004','MA-OPERA-012']:
 start=s.index('## '+ident+'\n');next_heading=s.find('\n## ',start+4);end=next_heading if next_heading>=0 else len(s);chunk=s[start:end];assert '**History:**' in chunk
 lines=chunk.splitlines();found=False
 for i,l in enumerate(lines):
  if l.startswith('**History:**'):lines[i]=l+note;found=True;break
 assert found;s=s[:start]+'\n'.join(lines)+'\n'+s[end:]
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,S] for p in base.rglob('*') if p.is_file()});write(ip,imp)
a=R/'tmp/v2_preview_allowed.json';allow=set(read(a));allow.update(imp['files']);write(a,sorted(allow))
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(L/'review_tools/refresh_current_job_review_v34.py')],cwd=R,check=True)
print('V34:1756 entries,1261 sources,13 separately scored Nursery uses; priorV33 bytes preserved. Current action/room weak, Geologist mount stale. Lifecycle unchanged.')
