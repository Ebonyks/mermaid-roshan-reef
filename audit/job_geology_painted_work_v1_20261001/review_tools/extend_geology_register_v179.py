from pathlib import Path
import json, shutil, sys
root=Path(sys.argv[1]);family=root/'audit/job_geology_painted_work_v1_20261001'
old=root/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v20.py'
new=old.with_name('build_current_job_item_register_v21.py')
assert not new.exists()
s=old.read_text(encoding='utf-8').replace("geo_prefix+'/REVIEW_V7.json'","geo_prefix+'/REVIEW_V8.json'")
s=s.replace('18 generated originals,34 neutral displays and13 technical derivatives','20 generated originals,34 existing neutral displays and14 technical derivatives')
s=s.replace("'Unbound ImageGen source/technical review'","'ImageGen source/technical review with exact binding status'")
s=s.replace('11 source-object regions','14 source-object regions').replace('plus11 source-object regions','plus14 source-object regions')
insert="""
# Seven painted-work exact runtime copies and conserved fossil thirds. Repeated instances are not additional sources.
work=read('audit/job_geology_painted_work_v1_20261001/ARTWORK_ITEMS.json')
for x in work['source_items']:
 p=x['path']; actual=hashlib.sha256((r/p).read_bytes()).hexdigest();assert actual==x['sha256']
 items[p]=dict(id=x['id'],aliases=[],kind='source',path=p,source_dimensions=x['source_dimensions'],earlier_sha256=actual,historical_source_score=x['source_finish'],latest_source_score=x['source_finish'],latest_source_sha256=actual,evaluation=x['evaluation'],refinement='Painted material4.6 does not pass room2.8/contact2.7/clearing3.9, articulated pan3.8 or provisional fossil/geode progression4.5.',families=['Geologist painted production candidate'],original_reports=['audit/job_geology_painted_work_v1_20261001/index.html'],source_qualification=x['qualification'],preview_path=p,native_reference_observations=[],runtime_binding_state='BOUND_TOPIC_RUNTIME_CANDIDATE',latest_refinement=dict(report='audit/job_geology_painted_work_v1_20261001/index.html',note='All46 current ordinary-input native stills directly inspected; static material and complete action scores remain separate.',evidence=x))
for x in work['fossil_source_regions']:
 items[x['id']]=dict(id=x['id'],aliases=[],kind='source object region',path=x['path'],region=x['region'],source_dimensions=x['source_dimensions'],earlier_sha256=x['sha256'],historical_source_score=x['source_finish'],evaluation=x['evaluation'],refinement='Three conserved source thirds rejoin exactly; straight partition/support4.5 provisional remains an inclusive priority.',families=['Geologist fossil assembly'],original_reports=['audit/job_geology_painted_work_v1_20261001/index.html'],source_qualification=x['qualification'],preview_path=x['path'],native_reference_observations=[],runtime_binding_state='BOUND_TOPIC_RUNTIME_REGION',latest_refinement=dict(report='audit/job_geology_painted_work_v1_20261001/index.html',note='Current sampled painting4.6, partition/support4.5 provisional; no separate regenerated source image or complete action approval.',evidence=x))
"""
anchor='for key,q in items.items():'
if anchor not in s:
 anchor='for q in items.values():\n p=q'
assert anchor in s, 'Find exact pre-hash item-loop anchor; no guessed replacement.'
s=s.replace(anchor,insert+'\n'+anchor,1)
s=s.replace('design/audit_impacts/job-geode-painted-runtime-20261001.json','design/audit_impacts/job-geology-painted-work-20261001.json')
new.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),family/'review_tools'/Path(__file__).name)
# Add current ledger navigation without rewriting historical report opinions.
p=root/'design/05_DOC_LEDGER.md';text=p.read_text(encoding='utf-8')
source_row='| `assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html` | 🟣 | `CANDIDATE`; REVIEW_V8 preserves20 native ImageGen originals/34 existing neutral displays/14 whole-canvas derivatives, each directly inspected. Seven painted-work derivatives and four geode derivatives now have separate topic-runtime paths; soil attempt1 rejected4.5/source4.0geometry and attempt2 material4.6 preserved. All46 current production stills directly inspected,174 archive views83direct/91unreviewed. Material4.6, room2.8/contact2.7/clearing3.9 and provisional fossil/geode progression4.5 remain separate. Training/story/device/child/owner/full action/final all-job report open. Earlier dated review evidence unchanged. |'
text='\n'.join(source_row if '`assets_src/imagegen/geologist_painted_rebuild_v1_20261001/index.html`' in row else row for row in text.split('\n'))
row='| `audit/job_geology_painted_work_v1_20261001/index.html` | 🟣 | `CANDIDATE`; seven exact painted runtime sources at new reversible paths, three conserved fossil regions and23 repeated pan instances. All46 current actual-game stills directly reviewed across four ordinary-input phases at1280/1600;174 archived views83direct/91notdirect. Painted material4.6 and rooted geode interior4.6; room2.8/contact2.7/clearing3.9/pan action3.8 and provisional assembly/opening4.5 remain priorities. Fresh current full CI pending, earlier H82/82 applies only to its334 literal sources. No lifecycle closure or training/story/device/child/owner/integration/release/final report approval. |'
if '`audit/job_geology_painted_work_v1_20261001/index.html`' not in text:text+='\n'+row+'\n'
p.write_text(text,encoding='utf-8',newline='\n')
p=root/'audit/MASTER_AUDIT_2026-08-09.md';text=p.read_text(encoding='utf-8')
entry='Painted-work continuation (2026-10-01): [seven individual painted runtime sources and all46 current actual-game stills](job_geology_painted_work_v1_20261001/index.html) directly reviewed at1280/1600 across ordinary four-phase input/arrival/earned completion. New exact runtime copies preserve authored fossil aspect/three conserved thirds, pan grain/mineral containment, stone support and measured invitations. New deep soil source2/material4.6 replaces the flat cover; source1/cover4.0 rejected and preserved. Every174 archive view retained:83direct/91unreviewed, no inherited visual scores. Material4.6 remains separate from room2.8/contact2.7/clearing3.9/pan action3.8 and provisional fossil/geode progression4.5 priorities. Fresh current full suite pending; historical H82/82 remains its own334-source evidence. Training/story/timed action/device/child/owner/final all-job report remain open; no closure/integration/release. [Impact](../design/audit_impacts/job-geology-painted-work-20261001.json).\n\n'
assert '## 0. Planning entry\n' in text
text=text.replace('## 0. Planning entry\n','## 0. Planning entry\n\n'+entry,1);p.write_text(text,encoding='utf-8',newline='\n')
p=root/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=p.read_text(encoding='utf-8');start=text.index('## MA-PLAY-004\n');end=text.index('\n## ',start+4);section=text[start:end]
oldhist=next(x for x in section.splitlines() if x.startswith('| history |'))
history=' 2026-10-01 painted-work continuation: [seven exact painted runtime copies and every46 current actual-game native stills](../job_geology_painted_work_v1_20261001/index.html) directly reviewed. Material4.6 improves fossil/pan/grain/mineral/soil/slab/invitations while room2.8 and detached actor contact2.7 remain explicit. New soil concealment4.6 does not pass grid clearing3.9; fossil assembly and sampled geode opening4.5 provisional remain priorities. Every174 archive view retained83direct/91unreviewed. Fresh current complete suite pending; H82/82 is historical334-source evidence. Full timed work/route/training/story/device/child/owner/global acceptance and this finding lifecycle remain open.'
newhist=oldhist[:-2]+history+' |';section=section.replace(oldhist,newhist);text=text[:start]+section+text[end:];p.write_text(text,encoding='utf-8',newline='\n')
p=root/'design/audit_impacts/job-geology-painted-work-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{x.relative_to(root).as_posix() for x in [new,root/'design/05_DOC_LEDGER.md',root/'audit/MASTER_AUDIT_2026-08-09.md',root/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md',family/'review_tools'/Path(__file__).name]});p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('REGISTER179|prepared V21 and current authority facts; previous V20/V7/V6/impacts unchanged')
