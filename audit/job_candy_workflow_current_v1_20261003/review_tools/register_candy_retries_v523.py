from pathlib import Path
import copy,datetime,hashlib,html,json,re,shutil,subprocess
from PIL import Image
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
m=b/'assets_src/imagegen/candy_wrap_contact_v1_20261003';c=b/'audit/job_candy_workflow_current_v1_20261003';l=b/'audit/job_artwork_refinement_live'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
dest=m/'attempt10';assert not dest.exists();dest.mkdir()
original=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-c982b9bc-6a1d-4168-9e67-d895e1a73635.png')
shutil.copyfile(original,dest/'native.png')
(m/'PROMPT_A10.txt').write_text("Use case: precise-object-edit. Edit this transparent 2 by 2 painted game atlas. Repair ONLY the TOP-RIGHT panel's golden paper and hand contact. Keep the other three panels, all character identities, outlines, clothing, hair, face and table framing unchanged.\n\nThe top-right panel is the stage AFTER folding long edges but BEFORE twisting either end. Remove the two thick raised gold rings at the ends of the candy. Replace them with smooth LOOSE gathered paper necks, like two flat pleats flowing continuously into the broad attached fans, absolutely no ring, knot, bead or spiral. Both mittens slide inward to contact the loose pleats. Make this enclosed candy belly the SAME small oval size and center as the red sweet in top-left, with only a thin paper thickness added. It rests on the tabletop, never floats or grows.\n\nPreserve the top-right body/table position and the sheet's transparent gutters. Keep the existing painted gold material, coral mittens and rounded navy/plum contour style. No arrows, text, effects, additional hands, utensils or background. Preserve actual RGBA transparency.",encoding='utf-8')
im=Image.open(dest/'native.png')
source={'native_path':(dest/'native.png').relative_to(b).as_posix(),'sha256':sha(dest/'native.png'),'generated_original_path':str(original),'generated_original_sha256':sha(original),'dimensions':list(im.size),'mode':im.mode,'alpha_extrema':list(im.getchannel('A').getextrema()),'prompt_path':(m/'PROMPT_A10.txt').relative_to(b).as_posix(),'prompt_sha256':sha(m/'PROMPT_A10.txt'),'attempt':10,'generation_method':'builtin_image_gen_precise_edit','reference':{'path':(m/'attempt09/native.png').relative_to(b).as_posix(),'sha256':sha(m/'attempt09/native.png'),'role':'edit target; directly inspected generated native'},'modifications':'No post-generation pixel edits; exact native RGBA preserved. Generator instructed to repair only top-right paper/contact; invariance is not assumed from the instruction.','production_binding':False,'owner_acceptance':None}
assert source['sha256']==source['generated_original_sha256']
review={'status':'REJECTED_BRIDGE_CONTINUITY','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'direct_native_review':True,'opinions':[{'item':'Half edge fold','score':4.5,'evaluation':'One continuous gold sheet partly encloses the red sweet; two mittens contact the lifted edges. Static source state only.'},{'item':'Slide to untwisted necks','score':4.4,'evaluation':'Premature gold rings are removed, so the necks now read as untwisted attached pleats. Mittens still hold the broad fans outside the narrow necks; the enclosed belly remains taller than the original sweet. The missing sliding grip is not yet accepted.'},{'item':'First opposing wrist roll','score':4.3,'evaluation':'Connected arms are sound, but the early-roll state still has an oversized belly and already tight coiled necks inherited from the edit target. It remains a rejected intermediate.'},{'item':'Released settle','score':4.5,'evaluation':'Both mittens rest clear of the attached fans; the finished gold sweet remains supported on the table. Useful static endpoint, not a full-action pass.'},{'item':'Whole bridge source','score':4.2,'evaluation':'Untwisted pleats and release improve wrapper semantics. Missing slide contact, candy-size drift and an already finished half-roll still reject complete bridge continuity. Actual A5 motion remains4.1; no new binding.'}],'production_binding':False,'owner_acceptance':None,'qualification':'All four native source states directly inspected. No actual use, complete action, runtime-ready texture, device, child or owner acceptance is transferred.'}
write(dest/'SOURCE.json',source);write(dest/'DIRECT_REVIEW.json',review)
allrev=json.loads((m/'COMPLETE_SOURCE_REVIEW.json').read_text(encoding='utf-8'))
assert len(allrev['sources'])==8
for n in [9,10]:
 q=m/f'attempt{n:02d}';s=json.loads((q/'SOURCE.json').read_text(encoding='utf-8'));r=json.loads((q/'DIRECT_REVIEW.json').read_text(encoding='utf-8'))
 opinions=[{'state':v['item'],'region':[(i%2)*627,(i//2)*627,627,627],'score':v['score'],'scope':'Authored bridge state; static/source only, rejected complete sheet.'} for i,v in enumerate(r['opinions'][:4])]
 allrev['sources'].append({'attempt':n,'source':s,'whole_source_score':r['opinions'][-1]['score'],'source_review':r,'state_opinions':opinions,'production_binding':False,'owner_acceptance':None})
allrev['reviewed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();allrev['qualification']='All ten exact native sources and forty individual states directly inspected. A7 selected endpoints4.5–4.6; actual A5 complete wrapping4.1 rejected. Bridges A8/A9/A10 whole4.1/4.1/4.2 remain unbound. Static source opinions never establish full motion, runtime integration, device, child or owner acceptance.'
write(m/'COMPLETE_SOURCE_REVIEW.json',allrev)
mt=(m/'index.html').read_text(encoding='utf-8')
mt=mt.replace('Eight reversible built-in ImageGen source attempts. Every complete native source and all32 individual states directly reviewed.','Ten reversible built-in ImageGen source attempts. Every complete native source and all 40 individual states directly reviewed.').replace('A8 bridges4.1 fail chronology/size/settle and are not used.','A8/A9 bridges score 4.1; A10 scores 4.2. Loose pleats and released hands improve, while the sliding grip and conserved candy size remain below the floor.')
extras=''
for n in [9,10]:
 q=m/f'attempt{n:02d}';r=json.loads((q/'DIRECT_REVIEW.json').read_text(encoding='utf-8'));s=json.loads((q/'SOURCE.json').read_text(encoding='utf-8'))
 extras+=f'<article id="attempt{n}"><h2>Attempt {n} · complete source {r["opinions"][-1]["score"]}/5 · rejected</h2><figure><a href="attempt{n:02d}/native.png"><img loading="lazy" alt="Complete four-state wrapping bridge candidate {n}" src="attempt{n:02d}/native.png"></a><figcaption>{s["sha256"]}</figcaption></figure>'
 for v in r['opinions']:extras+=f'<p><strong>{html.escape(v["item"])} · {v["score"]}/5.</strong> {html.escape(v["evaluation"])}</p>'
 extras+=f'<p><a href="attempt{n:02d}/SOURCE.json">Exact provenance</a> · <a href="attempt{n:02d}/DIRECT_REVIEW.json">Individual evaluations</a> · <a href="PROMPT_A{n}.txt">Exact built-in prompt</a></p></article>'
assert '</main>' in mt;mt=mt.replace('</main>',extras+'</main>');(m/'index.html').write_text(mt,encoding='utf-8')
for name,backup in [('ALL_ITEMS.json','ALL_ITEMS_V43.original.json'),('all_items.html','all_items_V43.original.html'),('CURRENT_BOUNDARY_REFRESH.json','BOUNDARY_V43.original.json')]:
 assert not (l/backup).exists();shutil.copyfile(l/name,l/backup)
reg=json.loads((l/'ALL_ITEMS.json').read_text(encoding='utf-8'));assert len(reg['items'])==1924
template=next(x for x in reg['items'] if x['id']=='CANDY-M-SOURCE-08')
for n in [9,10]:
 s=json.loads((m/f'attempt{n:02d}/SOURCE.json').read_text(encoding='utf-8'));r=json.loads((m/f'attempt{n:02d}/DIRECT_REVIEW.json').read_text(encoding='utf-8'))
 for i,v in enumerate([r['opinions'][-1]]+r['opinions'][:4]):
  it=copy.deepcopy(template);it.update(id=f'CANDY-M-SOURCE-{n:02d}' if i==0 else f'CANDY-M-A{n:02d}-STATE-{i}',path=s['native_path'],label=f'Connected wrapper contact source {n}' if i==0 else f'{v["item"]} · contact source {n}',earlier_sha256=s['sha256'],current_checkout_sha256=s['sha256'],historical_source_score=v['score'],current_source_score=v['score'],source_dimensions=s['dimensions'],preview_path=s['native_path'],image_path=s['native_path'],evaluation=v['evaluation'],original_reports=[f'assets_src/imagegen/candy_wrap_contact_v1_20261003/index.html#attempt{n}'],latest_refinement={'report':f'assets_src/imagegen/candy_wrap_contact_v1_20261003/index.html#attempt{n}','note':v['evaluation']},priority=True)
  if i:
   it.update(kind='source object region',region=[((i-1)%2)*627,((i-1)//2)*627,627,627],parent_source_id=f'CANDY-M-SOURCE-{n:02d}',families=['Candy Maker','Unbound contact state regions'],individual_scope='Bridge state only; full sheet remains rejected and unbound.')
  reg['items'].append(it)
reg['counts'].update(unique_source_files=1277,individual_source_object_regions=178,registered_items=1934,inclusive_current_source_priorities=772,unique_source_file_priorities=585,new_candy_generated_sources=13,new_candy_state_regions=52)
assert len(reg['items'])==1934 and len({x['id'] for x in reg['items']})==1934
reg['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();reg['display_revision']='V44';reg['refresh_command']='python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v44.py'
new=l/'ALL_ITEMS_V44.new.json';new.write_text(json.dumps(reg,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
assert new.stat().st_size<4*1024*1024;assert json.loads(new.read_text(encoding='utf-8'))==reg;new.replace(l/'ALL_ITEMS.json')
refresh=l/'review_tools/refresh_current_job_review_v44.py';shutil.copyfile(l/'review_tools/refresh_current_job_review_v43.py',refresh)
for p in [l/'index.html',l/'all_items.html']:
 t=p.read_text(encoding='utf-8');t=t.replace('V43','V44').replace('v43.py','v44.py').replace('1924','1934').replace('762 source','772 source').replace('583 unique','585 unique').replace('all8 source','all10 source').replace('all8 contact','all10 contact').replace('all32 states','all40 states');p.write_text(t,encoding='utf-8')
for p in [b/'audit/MASTER_AUDIT_2026-08-09.md',b/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 t=p.read_text(encoding='utf-8');t=t.replace('Eight contact originals/three wrapper originals and44 state regions separately scored; missing bridgeA8 source4.1 rejected. V43 known register1924 entries/762 source-cell-region priorities/583 unique source priorities/48 current Candy priorities/377 source reviews remain.','Ten contact originals/three wrapper originals and52 state regions separately scored; bridges A8/A9/A10 score4.1/4.1/4.2 and remain rejected. V44 known register1934 entries/772 source-cell-region priorities/585 unique source priorities/48 current Candy priorities/377 source reviews remain.');p.write_text(t,encoding='utf-8')
ledger=b/'design/05_DOC_LEDGER.md';t=ledger.read_text(encoding='utf-8').replace('all8 preserved original sources/32 individual authored states reviewed. A7 static4.5;A8 bridge4.1 rejected; no production binding.','all10 preserved original sources/40 individual authored states reviewed. A7 static4.5; A8/A9/A10 bridges4.1/4.1/4.2 rejected; no production binding.')
t+='\n| `audit/job_artwork_refinement_live/ALL_ITEMS_V43.original.json` | ⚪ | `HISTORICAL_SUPPORTING`; exact1924-entry register before the two additional rejected bridge sources. Prior source/action scores and boundary remain preserved. |\n';ledger.write_text(t,encoding='utf-8')
licenses=b/'ASSET_LICENSES.md';t=licenses.read_text(encoding='utf-8')
for n in [9,10]:t+=f'\n| `assets_src/imagegen/candy_wrap_contact_v1_20261003/attempt{n:02d}/native.png` | OpenAI built-in ImageGen; owner-requested Candy wrapper contact continuity trial | Generated for this project; source refs retained in SOURCE.json | No external URL; exact prompt PROMPT_A{n}.txt and native SHA256 preserved | No post-generation pixel edits; unbound rejected bridge candidate, not runtime-ready or accepted motion |\n'
licenses.write_text(t,encoding='utf-8')
gat=b/'.gitattributes';t=gat.read_text(encoding='utf-8')
for n in ['ALL_ITEMS_V43.original.json','all_items_V43.original.html','BOUNDARY_V43.original.json']:t+=f'\naudit/job_artwork_refinement_live/{n} -text\n'
gat.write_text(t,encoding='utf-8')
shutil.copyfile(__file__,c/'review_tools/register_candy_retries_v523.py')
ip=b/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=json.loads(ip.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for folder in [m,c,l] for p in folder.rglob('*') if p.is_file()});d['acceptance_gaps']=d['acceptance_gaps'].replace('A8 bridge4.1 rejected.','A8/A9/A10 bridge sources4.1/4.1/4.2 rejected; latest loose pleats and release do not pass the sliding grip, conserved sweet size or whole actual motion.');write(ip,d)
r=subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(refresh)],cwd=b,text=True,capture_output=True);print(r.stdout);assert r.returncode==0,r.stderr
allow=b/'tmp/v2_preview_allowed.json';a=json.loads(allow.read_text(encoding='utf-8'));a=sorted(set(a)|set(d['files']));write(allow,a)
print('V44:',len(reg['items']),'items;',reg['counts']['inclusive_current_source_priorities'],'inclusive source/cell/region priorities; nativeA10',source['sha256'],'whole4.2 rejected.')

