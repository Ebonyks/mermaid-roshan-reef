from pathlib import Path
import datetime, hashlib, html, json, posixpath, re, shutil, subprocess

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
prefix='assets_src/imagegen/geologist_river_components_v1_20261001'
f=b/prefix
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
tech=read(f/'TECHNICAL_DERIVATIVES.json')
tech['status']='TWO_COMPLETE_CANVAS_DERIVATIVES_DIRECTLY_REVIEWED_UNBOUND'
tech['reviewed_utc']=utc
for x in tech['derivatives']:
 x['direct_review']=True
 x['qualification']='Direct whole native1024 derivative review; first sheet4.4 contains rejected sealed channels4.0. Selected nodes/open strips4.6 source only. No runtime/network/action approval.'
write(f/'TECHNICAL_DERIVATIVES.json',tech)
attempts=[read(f/('attempt_%02d/REVIEW.json'%i)) for i in [1,2]]
components=[x for a in attempts for x in a['components']]
review={'schema':'reef.individual-river-source-review.v1','reviewed_utc':utc,'status':'FOUR_SELECTED4_6_SOURCE_COMPONENTS_UNBOUND_TWO_SEALED4_0_REJECTED','native_originals':[{k:a[k] for k in ['native_path','native_sha256','native_dimensions','source_score']} for a in attempts],'technical_derivatives':tech['derivatives'],'components':components,'selected_component_ids':[x['id'] for x in components if x['source_score']==4.6],'rejected_component_ids':[x['id'] for x in components if x['source_score']==4.0],'current_game_source_scores':{'dry_grid':3.5,'connected_water_path':3.8},'current_game_mechanics':'Nine columns by five rows. Any source-connected excavation path is valid; isolated cleared cells stay dry. Component generation has not changed these mechanics or bindings.','runtime_bound':False,'mounted_network_score':None,'complete_action_score':None,'device_child_owner_acceptance':None,'qualification':'Every2 complete native originals,2 uniformly scaled complete derivatives and6 source component regions directly inspected. CSS region windows are read-only views of whole images, not generated/cropped derivative files. Four selected components meet source4.6; joined networks, literal work contact, transitions, room, ordinary route/training/story and external acceptance remain pending.'}
write(f/'REVIEW.json',review)
rel=lambda p:posixpath.relpath(p,prefix)
esc=html.escape
cards=[]
for x in components:
 rx,ry,rw,rh=x['region'];dw,dh=x['source_dimensions'];s=340/max(rw,rh)
 style=f'width:{rw*s:.2f}px;height:{rh*s:.2f}px'
 image_style=f'width:{dw*s:.2f}px;height:{dh*s:.2f}px;left:{-rx*s:.2f}px;top:{-ry*s:.2f}px'
 cards.append(f'<article id="{x["id"]}"><h3>{esc(x["name"].replace("_"," ").title())}</h3><div class="region" style="{style}"><img src="{esc(rel(x["path"]))}" alt="{esc(x["name"])}" style="{image_style}"></div><p><strong>Source {x["source_score"]}/5</strong> · material {x["source_material_score"]}/5 · {esc(x["status"].replace("_"," ").lower())}</p><p>{esc(x["evaluation"])}</p><details><summary>Individual provenance and qualification</summary><pre>{esc(json.dumps(x,indent=2))}</pre></details></article>')
whole=[]
for i,a in enumerate(attempts,1):
 d=tech['derivatives'][i-1]
 whole.append(f'<article><h3>Attempt {i}: complete original and derivative</h3><p>Whole source {a["source_score"]}/5. '+('Two circular nodes selected4.6; both closed connectors rejected4.0.' if i==1 else 'Both open channels selected4.6; actual joins still unreviewed.')+f'</p><img class="whole" src="attempt_{i:02d}/native_generated.png" alt="Complete1254 native river attempt{i}"><p>Preserved1254×1254 native original</p><img class="whole" src="attempt_{i:02d}/whole_canvas_1024.png" alt="Complete1024 technical derivative{i}"><p>One uniform complete-canvas normalization to1024×1024; no masking or contour repair.</p><a href="attempt_{i:02d}/PROVENANCE.json">Generation provenance</a> · <a href="attempt_{i:02d}/REVIEW.json">Attempt review</a></article>')
report='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Geologist river — individual painted source drafts</title><style>body{margin:0;background:#eef4f8;color:#26304b;font:17px/1.55 system-ui}main{max-width:1260px;margin:auto;padding:24px}header,article,section{padding:22px;background:white;border-radius:16px;margin-bottom:18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:18px}.grid article{min-width:0;margin:0}.region{position:relative;overflow:hidden;margin:auto;background:repeating-conic-gradient(#dce5ed 0%25%,#f8fbff 0%50%)50%/24px 24px}.region img{position:absolute;max-width:none;max-height:none}.whole{display:block;width:100%;height:auto;background:#e0e8ee}a{color:#504096;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}h1,h2,h3{line-height:1.25}img{max-width:100%}@media(max-width:700px){main{padding:12px}.grid{grid-template-columns:1fr}.region{max-width:100%}}</style><main>'''
report+='<header><a href="'+rel('audit/job_artwork_refinement_live/index.html')+'">All-job review entry</a><h1>Geologist river: painted source drafts</h1><p>The four selected dry/wet nodes and open channels score4.6/5 as individual sources. The first sealed-ended connectors score4.0 and remain rejected. These drafts are unbound; the current flat game graphics still score3.5 dry/3.8 connected water.</p><p>Existing gameplay permits any connected path through a9×5 grid. Painted sources must preserve readable arbitrary junctions and isolated dry excavation; source quality does not establish a network or action pass.</p><p><a href="REVIEW.json">Complete written evaluations</a> · <a href="REUSE_INVENTORY.json">Reuse inventory</a> · <a href="TECHNICAL_DERIVATIVES.json">Technical derivative provenance</a></p></header><h2>Every individual component</h2><div class="grid">'+''.join(cards)+'</div><h2>Every complete source attempt</h2><div class="grid">'+''.join(whole)+'</div><section><h2>Current actual-game comparison</h2><p>Flat excavation grid3.5; source-connected rectilinear water path3.8. Nine columns/five rows, not a prescribed four-connection route. Current room2.8 and detached actor contact2.7 remain separate priorities.</p>'
current=read(b/'audit/job_geology_painted_work_v1_20261001/REVIEW.json')
# Use explicit current captures selected by their durable phase/state records.
for p in sorted((b/'audit/job_geology_painted_work_v1_20261001').rglob('*.png')):
 if 'attempt_04' in p.as_posix() and '1280' in p.as_posix() and ('river_task_open' in p.name or 'river_earned' in p.name):
  report+=f'<figure><img class="whole" src="{rel(p.relative_to(b).as_posix())}" alt="{esc(p.stem)}"><figcaption>{esc(p.stem)}</figcaption></figure>'
report+='<p><a href="'+rel('audit/job_geology_painted_work_v1_20261001/index.html')+'">All46 current native game views and individual context evaluations</a></p></section><section><h2>Acceptance still required</h2><p>Joined straight/corner/branch networks, dry-to-wet changes, target/source meaning, brush contact and continuous action have no new score. Current full-suite regression validates the unchanged painted-work runtime boundary; it does not validate these unbound source drafts. Ordinary training/story routes, target device, child and owner review remain open.</p></section></main></html>'
(f/'index.html').write_text(report,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/Path(__file__).name)
builder=b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v22.py'
assert not builder.exists(),'Do not overwrite an earlier register builder.'
s=(builder.with_name('build_current_job_item_register_v21.py')).read_text(encoding='utf-8')
insertion='''# Six directly reviewed river source regions and four preserved whole source files; no runtime binding.
river_prefix='assets_src/imagegen/geologist_river_components_v1_20261001'
river=read(river_prefix+'/REVIEW.json')
for num,x in enumerate(river['native_originals']+river['technical_derivatives'],1):
 p=x.get('native_path',x.get('path'));actual=hashlib.sha256((r/p).read_bytes()).hexdigest();score=x['source_score']
 items[p]=dict(id='GEO-RIVER-WHOLE-%02d'%num,aliases=[],kind='source',path=p,earlier_sha256=actual,historical_source_score=score,evaluation='Complete painted river sheet directly reviewed. First sheet4.4 contains two source4.6 nodes and two rejected closed connectors4.0; second sheet4.6 has two open channels. Complete canvas retained; no network/runtime acceptance.',refinement='Mount and inspect arbitrary straight/corner/branch joins and actual dry/wet consequences before accepting the river game.',families=['Geologist river','Unbound painted source study'],original_reports=[river_prefix+'/index.html'],source_qualification=river['qualification'],preview_path=p,native_reference_observations=[],runtime_binding_state='UNBOUND_SOURCE_STUDY',latest_refinement=dict(report=river_prefix+'/index.html',note='Every native original and complete derivative directly reviewed; four selected components4.6, two sealed-ended channels rejected4.0.'))
for x in river['components']:
 items[x['id']]=dict(id=x['id'],aliases=[],kind='source object region',path=x['path'],region=x['region'],source_dimensions=x['source_dimensions'],earlier_sha256=x['sha256'],historical_source_score=x['source_score'],evaluation=x['evaluation'],refinement='Rejected closed connector geometry4.0 is preserved. Selected source4.6 does not pass actual joined network, working contact or complete action.',families=['Geologist river','Individual unbound painted component'],original_reports=[river_prefix+'/index.html#'+x['id']],source_qualification=x['qualification'],preview_path=x['path'],native_reference_observations=[],runtime_binding_state=x['status'],latest_refinement=dict(report=river_prefix+'/index.html#'+x['id'],note='Source/material/open-port opinions separate from pending mount/action/network.',evidence=x))

'''
s=s.replace('for q in items.values():\n p=q[\'path\']',insertion+'for q in items.values():\n p=q[\'path\']',1)
s=s.replace('38 runtime prop regions and 14 source-object regions','38 runtime prop regions and 20 source-object regions').replace('build_current_job_item_register_v20.py','build_current_job_item_register_v22.py').replace('plus14 source-object regions including six embedded geode details','plus20 source-object regions including six embedded geode details and six river candidates').replace("p=r/'design/audit_impacts/job-geology-painted-work-20261001.json'","p=r/'design/audit_impacts/job-geology-river-painted-source-20261001.json'")
builder.write_text(s,encoding='utf-8',newline='\n')
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(builder)],cwd=b,check=True)
counts=read(b/'audit/job_artwork_refinement_live/ALL_ITEMS.json')['counts']
assert counts['registered_items']==1596 and counts['inclusive_current_source_priorities']==584,counts
p=b/'audit/job_artwork_refinement_live/index.html';s=p.read_text(encoding='utf-8');note='<section id="river-source-latest"><h2>Current river source continuation</h2><p>Known1596 entries/1210 source files/328 pose cells/38 runtime prop regions/20 source-object regions;584 inclusive source priorities/388 unassigned. <a href="../../'+prefix+'/index.html">Every2 fresh river originals,2 complete derivatives and6 individual components</a>: four selected sources4.6, two sealed-ended connectors rejected4.0. Unbound source study; current river3.5/3.8, room2.8/contact2.7 remain priorities. Earlier dated counts retain their snapshot boundaries.</p></section>'
assert 'river-source-latest' not in s;s=s.replace('<main>','<main>'+note,1);p.write_text(s,encoding='utf-8',newline='\n')
p=b/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8');assert '`'+prefix+'/index.html`' not in s;s+='\n| `'+prefix+'/index.html` | 🟣 | `CANDIDATE`; two native ImageGen originals/two complete1024 derivatives and six individual components directly reviewed. Nodes and open channels4.6 source-only; first sealed channels4.0 rejected, whole first sheet4.4. All preserved/unbound; current9×5 river graphics3.5/3.8, joins/transitions/contact/action/routes/device/child/owner remain open. |\n';p.write_text(s,encoding='utf-8',newline='\n')
p=b/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text(encoding='utf-8');s=s.replace('## 0. Planning entry\n','## 0. Planning entry\n\nRiver painted-source continuation (2026-10-01): [two native originals/two whole-canvas derivatives and six individual components](../'+prefix+'/index.html) directly inspected. Four selected source components4.6; both sealed-ended channels rejected4.0, whole first sheet4.4. Actual9×5 arbitrary connected excavation remains unchanged and3.5/3.8. Sources unbound; network/contact/action/training/story/device/child/owner and comprehensive report remain open. Register1596 entries/1210 source files/20 source-object regions/584 inclusive priorities/388 unassigned. [Impact](../design/audit_impacts/job-geology-river-painted-source-20261001.json). No lifecycle closure.\n',1);p.write_text(s,encoding='utf-8',newline='\n')
p=b/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';s=p.read_text(encoding='utf-8');start=s.index('### MA-PLAY-004') if '### MA-PLAY-004' in s else s.index('## MA-PLAY-004');end=s.find('\n## ',start+5);end=len(s) if end<0 else end;section=s[start:end];assert '| history |' in section;section=re.sub(r'(\| history \|[^\n]*)( \|)',r'\1 2026-10-01 river source continuation: four painted dry/wet components4.6 source-only, two closed connectors rejected4.0, two complete native sheets/two uniform derivatives and all six individual opinions preserved in [illustrated unbound source study](../../'+prefix+r'/index.html). Actual9×5 connected excavation, network/action/contact/device/child/owner and lifecycle remain open.\2',section,count=1);s=s[:start]+section+s[end:];p.write_text(s,encoding='utf-8',newline='\n')
p=b/'design/audit_impacts/job-geology-river-painted-source-20261001.json';d=read(p);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}|{'design/05_DOC_LEDGER.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md',builder.relative_to(b).as_posix()});d['validation']=[v for v in d['validation'] if v['command']!='Native ImageGen source and each of four components'];d['acceptance_gaps']='Four selected components4.6 source-only. Actual mounting/network/junctions/dry-wet transition/contact/timeline, ordinary route/training/story/device/child/owner remain open. Current frozen349-source full suite does not validate these unbound source drafts.';write(p,d)
# Explicit local HTML reference integrity, without pretending lazy/browser images loaded.
from html.parser import HTMLParser
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,t,a):
  for k,v in a:
   if k in ['src','href'] and v:self.refs.append(v)
parser=Links();parser.feed(report);rows=[]
for ref in parser.refs:
 target=(f/ref.split('#')[0]).resolve();assert target.is_file(),ref;rows.append({'reference':ref,'target':target.relative_to(b).as_posix(),'exists':True})
write(f/'LIBRARY_LINK_QA.json',{'status':'PASS_ALL_EXPLICIT_LOCAL_REFERENCES','checked_utc':utc,'references':rows,'qualification':'Exact local file existence; browser pixels/region fit checked separately.'})
d=read(p);d['files']=sorted(set(d['files'])|{(f/'LIBRARY_LINK_QA.json').relative_to(b).as_posix()});write(p,d)
print(json.dumps({'status':'SOURCE_LIBRARY_AND_V22_REGISTER_READY','counts':counts,'references':len(rows)}))
