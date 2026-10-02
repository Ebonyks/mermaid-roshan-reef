from pathlib import Path
import datetime, hashlib, html, json, shutil, subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');s=b/'assets_src/imagegen/geologist_river_junctions_v1_20261001';f=b/'audit/job_river_join_study_v1_20261001';live=b/'audit/job_artwork_refinement_live'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
if not(s/'REVIEW_V1.json').exists():shutil.copyfile(s/'REVIEW.json',s/'REVIEW_V1.json');shutil.copyfile(s/'index.html',s/'index_v1.html')
base=read(s/'REVIEW_V1.json'); natives=list(base['native_originals']);derivs=list(base['technical_derivatives']);components=list(base['components'])
for name in ['wet_attempt_02','straight_attempt_02','dry_attempt_02','dry_attempt_03','dry_attempt_04','dry_attempt_05']:
 a=s/name
 if not(a/'REVIEW.json').exists():continue
 d=read(a/'REVIEW.json');n=dict(d);n.pop('components');natives.append(n);components.extend(d['components'])
 if(a/'TECHNICAL_DERIVATIVE.json').exists():derivs.append(read(a/'TECHNICAL_DERIVATIVE.json'))
for x in natives+derivs:
 assert x.get('direct_review') is True;assert sha(b/x.get('native_path',x.get('path')))==x['sha256']
latest=max([v for v in range(5,10) if(f/('REVIEW_V%d.json'%v)).exists()]);review=read(f/('REVIEW_V%d.json'%latest));total=review['direct_native_views_all_attempts']
note='All%d isolated native study stills directly reviewed. Latest V%d joined dry/wet detail4.5 provisional; painted bed4.6. A2/A3 dry whole-source red fringes4.4 rejected and preserved. No production/actor/full-room/timed-action/device/child/owner/global acceptance.'%(total,latest)
qualification='Every native original and listed derivative directly reviewed; every component individually scored and illustrated. Current source opinions retain exact hashes and rejected edge attempts. Join-study sampling does not pass whole-source edges or full game context. Originals preserved; uniform complete-canvas transforms only; no alpha or pixel repair.'
d=dict(status='DIRECT_INDIVIDUAL_SOURCE_REVIEWS_REJECTED_FRINGES_PRESERVED',reviewed_utc=now,native_originals=natives,technical_derivatives=derivs,components=components,prior_reviews=['assets_src/imagegen/geologist_river_junctions_v1_20261001/REVIEW_V1.json'],latest_refinement=dict(report='audit/job_river_join_study_v1_20261001/index_v%d.html'%latest,note=note),qualification=qualification)
write(s/'REVIEW.json',d);write(s/'REVIEW_V2.json',d)
style='body{font:17px/1.5 system-ui;background:#edf3f6;color:#28263f;max-width:1140px;margin:auto;padding:26px}article{background:#fff;padding:20px;margin:22px 0;border-radius:14px;overflow:hidden}img{display:block;max-width:100%;height:auto}figure{margin:12px auto;background:repeating-conic-gradient(#d7e3e9 0% 25%,#f6f9fc 0% 50%) 50%/24px 24px}code,a,h2{overflow-wrap:anywhere}a{color:#504092}'
cards=[]
for x in natives+derivs:
 path=x.get('native_path',x.get('path'));rel=path.split('geologist_river_junctions_v1_20261001/')[1]
 cards.append('<article><h2>%s · complete source%s/5</h2><img src="%s" alt="%s" loading="eager"><p>%s</p><code>%s</code></article>'%(html.escape(rel),x['source_score'],rel,html.escape(rel),html.escape(x.get('qualification',qualification)),x['sha256']))
for x in components:
 rect=x['region'];dims=x['source_dimensions'];scale=420/max(rect[2:]);w=rect[2]*scale;h=rect[3]*scale;path=x['path'].split('geologist_river_junctions_v1_20261001/')[1]
 cards.append('<article id="%s"><h2>%s · component source%s/5</h2><figure style="width:%spx;height:%spx;position:relative;overflow:hidden"><img src="%s" alt="%s" loading="eager" style="position:absolute;max-width:none;width:%spx;height:%spx;left:%spx;top:%spx"></figure><p>%s</p><p>%s</p><code>%s</code></article>'%(x['id'],x['id'],x['source_score'],w,h,path,x['id'],dims[0]*scale,dims[1]*scale,-rect[0]*scale,-rect[1]*scale,html.escape(x['evaluation']),html.escape(x['qualification']),x['sha256']))
(s/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Individual painted river source library</title><style>'+style+'</style><h1>Individual painted river sources and preserved iterations</h1><p>%d native originals, %d complete derivatives, %d individual component reviews.</p><p>%s</p><p><a href="REVIEW.json">Complete written reviews and hashes</a> · <a href="index_v1.html">Original source history</a> · <a href="../../../audit/job_river_join_study_v1_20261001/index_v%d.html">Latest native join study</a></p><p>%s</p>'%(len(natives),len(derivs),len(components),html.escape(note),latest,html.escape(qualification))+''.join(cards),encoding='utf-8',newline='\n')
for name in ['ALL_ITEMS.json','all_items.html']:
 target=live/(Path(name).stem+'_V24'+Path(name).suffix)
 if not target.exists():shutil.copyfile(live/name,target)
code=(b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v24.py').read_text(encoding='utf-8')
code=code.replace('build_current_job_item_register_v24.py','build_current_job_item_register_v25.py').replace('28 source-object regions','%d source-object regions'%(20+len(components))).replace('plus28 source-object regions including six embedded geode details, six first river candidates and eight dry/wet junctions.','plus%d source-object regions, including every independently scored river source iteration and rejected fringe component.'%(20+len(components)))
code=code.replace("historical_source_score=4.6,evaluation='Complete painted junction atlas directly inspected: four dry or wet open-interior endcap/elbow/T/cross objects. Native original or uniform complete1024 derivative preserved. Source4.6 does not pass actual wet joins4.4 or flat bed3.2.'", "historical_source_score=x['source_score'],evaluation=x.get('qualification','Complete native source directly reviewed; each component separately scored. Source and mounted/full-action claims stay distinct.')")
old="q['latest_refinement']=dict(report='audit/job_river_join_study_v1_20261001/index_v5.html',note='Every106 isolated native study still directly reviewed. Source4.6, bed4.6, dry selected4.5 provisional, wet joints4.4. All349 production bytes unchanged; full actor/room/action/owner acceptance remains open.')"
assert old in code;code=code.replace(old,"q['latest_refinement']=dict(report="+repr('audit/job_river_join_study_v1_20261001/index_v%d.html'%latest)+",note="+repr(note)+")")
target=b/'audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v25.py';target.write_text(code,encoding='utf-8',newline='\n');subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(target)],cwd=b,check=True)
licenses=b/'ASSET_LICENSES.md';text=licenses.read_text(encoding='utf-8');add=[]
for file in sorted(s.rglob('*.png')):
 p=file.relative_to(b).as_posix()
 if '`'+p+'`' not in text:add.append('| `'+p+'` | Owner-commissioned built-in Codex ImageGen; exact prompt/reference/provenance preserved | Project-generated review artwork; owner acceptance pending | assets_src/imagegen/geologist_river_junctions_v1_20261001/REVIEW.json | Exact native original; optional uniform complete-canvas derivative. No alpha/pixel repair. Source-only per-item score; rejected red-fringe attempts retained; unbound. |')
for file in sorted(f.rglob('*.webp')):
 p=file.relative_to(b).as_posix()
 if '`'+p+'`' not in text:add.append('| `'+p+'` | Native Godot4.7.2 Mobile-rendered review screenshot; source provenance retained | Project review evidence | audit/job_river_join_study_v1_20261001/index_v%d.html | Native lossless WebP preserved. Isolated inherited-input study; direct-review scope in versioned records, no actor/full-room/timed-action acceptance. |'%latest)
licenses.write_text(text+'\n'+'\n'.join(add)+'\n',encoding='utf-8',newline='\n')
counts=read(live/'ALL_ITEMS.json')['counts'];paragraph='River source and join continuation (2026-10-02): [all%d native isolated studies](job_river_join_study_v1_20261001/index_v%d.html) directly reviewed; latest dry/wet joined detail4.5 provisional and painted bed4.6. [Every%d source component](../assets_src/imagegen/geologist_river_junctions_v1_20261001/index.html) individually illustrated, preserving failed red-fringe A2/A3 sources4.4 and initial opinions. Current known registerV25 has%d entries/%d source files/%d source regions/%d inclusive priorities/%d source-unassigned; not exhaustive actual-use proof. Actual inherited input/arbitrary paths/JSON restore/single completion pass at both widths; no new production binding, actor/room/timed-action/training/story/device/child/owner/all-job acceptance or lifecycle closure. [Impact](../design/audit_impacts/job-geology-river-junction-source-20261001.json).'%(total,latest,len(components),counts['registered_items'],counts['unique_source_files'],counts['individual_source_object_regions'],counts['inclusive_current_source_priorities'],counts['unreviewed_current_source'])
p=b/'audit/MASTER_AUDIT_2026-08-09.md';text=p.read_text(encoding='utf-8');marker='River source and join continuation (2026-10-02):'
if marker in text:text='\n'.join(paragraph if line.startswith(marker) else line for line in text.split('\n'))
else:head,tail=text.split('\n',1);text=head+'\n\n'+paragraph+'\n'+tail
p.write_text(text,encoding='utf-8',newline='\n')
p=b/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=p.read_text(encoding='utf-8');start=text.index('## MA-PLAY-004');end=text.find('\n## ',start+1);line='River calm-floor continuation (2026-10-02): [all%d isolated native views](../job_river_join_study_v1_20261001/index_v%d.html) directly inspected. Latest joined dry/wet detail4.5 provisional, bed4.6; A2/A3 complete-source red fringes4.4 remain rejected and preserved. Inherited input/save/single completion pass; production, actor/room/timed action, training/story/device/child/owner acceptance and finding closure remain open.'%(total,latest)
marker='River calm-floor continuation (2026-10-02):'
if marker in text:text='\n'.join(line if row.startswith(marker) else row for row in text.split('\n'))
else:text=text[:end]+'\n'+line+'\n'+text[end:]
p.write_text(text,encoding='utf-8',newline='\n')
p=b/'design/05_DOC_LEDGER.md';text=p.read_text(encoding='utf-8');source_row='| `assets_src/imagegen/geologist_river_junctions_v1_20261001/index.html` | 🟣 | `CANDIDATE`; every%d native/%d complete derivative/%d individual components directly reviewed with qualified source scores. Failed red-fringe A2/A3 complete sources4.4 retained. Latest joined study4.5 provisional is separate; no production/full-action/owner acceptance. |'%(len(natives),len(derivs),len(components));text='\n'.join(source_row if '`assets_src/imagegen/geologist_river_junctions_v1_20261001/index.html`' in line else line for line in text.split('\n'))
for version in [6,7,8]:
 path='audit/job_river_join_study_v1_20261001/index_v%d.html'%version
 if(b/path).exists() and '`'+path+'`' not in text:text+='\n| `'+path+'` | 🟣 | `CANDIDATE`; exact28 native states directly reviewed at1280/1600; versioned per-state/material/join/source qualifications and prior failures retained. Actual inherited input/save/single completion separately verified. No production, actor/full-room/timed-action/device/child/owner/global acceptance. |\n'
p.write_text(text,encoding='utf-8',newline='\n')
p=live/'index.html';text=p.read_text(encoding='utf-8').replace('../job_river_join_study_v1_20261001/index_v5.html','../job_river_join_study_v1_20261001/index_v%d.html'%latest).replace('All106 individually scored native study states','All%d individually scored native study states'%total);text=text.replace('wet joined network4.4 remains a priority; the complete earth field now scores4.6 in both isolated viewport studies.','latest dry/wet joined detail reaches4.5 provisional and the earth bed4.6. Rejected A2/A3 red-fringe source scores4.4 remain explicit.');p.write_text(text,encoding='utf-8',newline='\n')
snapshot=read(b/'audit/job_geology_painted_work_v1_20261001/full_ci_v1/SOURCE_BEFORE.json')['source_files'];checked=[dict(path=x['path'],baseline_sha256=x['sha256'],current_sha256=sha(b/x['path'])) for x in snapshot];assert len(checked)==349 and all(x['baseline_sha256']==x['current_sha256'] for x in checked);write(f/('PRODUCTION_UNCHANGED_V%d.json'%latest),dict(baseline=review['baseline'],checked_utc=now,status='ALL349_LITERAL_PRODUCTION_FILES_EXACT_I_BYTES',source_files=checked,qualification='Exact bytes match I unmodified82/82 suite; no newly repeated full-suite or hosted/visual/owner acceptance.'))
shutil.copyfile(__file__,f/Path(__file__).name)
shared={'ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','audit/job_review_v2_20261001/review_tools/build_current_job_item_register_v25.py'}
for name,folder in [('job-geology-river-join-study-20261001',f),('job-geology-river-junction-source-20261001',s),('job-geology-river-bed-source-20261002',b/'assets_src/imagegen/geologist_river_bed_v1_20261002')]:
 ip=b/('design/audit_impacts/'+name+'.json');d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in folder.rglob('*') if p.is_file()}|shared|{p.relative_to(b).as_posix() for p in live.rglob('*') if p.is_file()});d['acceptance_gaps']=note;write(ip,d)
allow=b/'tmp/v2_preview_allowed.json';d=read(allow);assert isinstance(d,list);write(allow,sorted(set(d)|shared|{p.relative_to(b).as_posix() for folder in [f,s,live] for p in folder.rglob('*') if p.is_file()}))
print('Current source library',len(natives),'native',len(derivs),'derivatives',len(components),'components;',json.dumps(counts))
