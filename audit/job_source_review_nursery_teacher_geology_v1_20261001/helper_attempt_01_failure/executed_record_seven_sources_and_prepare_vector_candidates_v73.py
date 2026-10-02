from pathlib import Path
import datetime,hashlib,html,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
report=r/'audit/job_source_review_nursery_teacher_geology_v1_20261001'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
profile=read(report/'PROFILE.json');assert read(report/'RENDER_RECEIPT.json')['sources_unchanged']
opinions=[
 (4.6,'The current fresh description-only catching arms are strongly stylized: rounded lavender cuffs, warm peach palms, deep plum contours and two calm painted value bands. The cupped palms form a broad open cradle rather than lifelike fingers or a framed scene. Full native, white and aqua views show attached contours without a visible matte plate. This preserves the already documented attempt06 source-only4.6 opinion; connection to the complete caregiver, contact at catch and settling remain separate action priorities.'),
 (4.6,'All five rounded cushions use the same soft toy volume, plum outline, grouped broad lavender/periwinkle shading and restrained seam marks. Their horizontal row is coherent and calm. The current exact source agrees with the earlier selected attempt03 source-only4.6 opinion. The runtime crop6,115,1014,117 selects the strip; alignment, landing/deformation and the complete safe-return sequence remain separate.'),
 (4.2,'The fossil is immediately recognizable as a spiral in a warm stone, and its palette belongs to the project. Its polygonal slab, very heavy uniform contour and single flat fill read as a rough symbol beside the painted job props. At the declared132px hotspot the12px source contour is about6.2 screen pixels, above the usual2–4 contour range. Add broad quiet stone value bands and a gentler contour while preserving the one spiral and slab identity; excavation/brush contact remains unreviewed.'),
 (4.0,'The colored strata and two mineral dots are easy to distinguish, but the solid dark slab, straight parallel stripes and heavy boundary read as a diagram. The two yellow dots are isolated accents rather than natural grouped mineral detail. The declared128px object makes the12px boundary about6px wide. Preserve the three colored educational layers and two dots while giving the stone a rounded mass and calm painted values. Its reuse as a PAN overlay is also a semantic action priority; prettier stone cannot prove actual panning.'),
 (4.2,'The lesson board keeps large non-text circles and a triangle, an accessible cream field and a clear silhouette. The uniform heavy rim and thin bent legs read as an interface card on wires, with little toy-board material or warm painted volume. At the190px hotspot the12px rim is about8.9px, too dominant beside authored career art. Preserve the exact six shapes and arrangement, improve the frame/supports and broad grouped values, and separately test every lesson interaction; one static board cannot pass PATTERN/COUNT/ADD/MATCH.'),
 (4.2,'The two aqua/lavender crystals and broad facets are child-readable, but the dark triangular base and heavy angled boundaries read as a coarse badge rather than a rounded collectible toy prop. Preserve the two crystal identities and large facets; add a calm rounded mineral base and broad value grouping. The declared150px object puts the10px internal borders near5.9 screen pixels. Geode splitting, crystal reveal and actual collection remain unreviewed.'),
 (4.4,'This crest exactly reuses the geologist reward silhouette. Its strong simplified crystal identity is suitable as an icon, and the compact palette is clear. The coarse dark mountain base and flat angular shapes still limit its overall artwork polish. Treat UI readability separately from world-prop realism and preserve the shared symbol; an icon-native variant can reuse the refined crystal shapes with an appropriate small-size contour. Exact mounted UI score remains unassigned.'),
]
items=[]
for x,(score,evaluation) in zip(profile['items'],opinions):
 assert sha(r/x['path'])==x['sha256']
 name=Path(x['path']).stem
 previews=[name+'_review_white.png',name+'_review_aqua.png'] if x['path'].endswith('.png') else [name+'_native.png']
 items.append(dict(**x,id='CURRENT-SOURCE-'+name.upper(),source_score=score,evaluation=evaluation,direct_full_native_review=True,preview_paths=previews,qualification='Current exact whole native source directly inspected. Source-only intended-use drafting opinion; actual mounted/complete-action/device/child/owner acceptance remains separate.',mounted_score=None,complete_action_score=None))
regions=[dict(id=f'CURRENT-NURSERY-CUSHION-{i+1:02d}',source_path=items[1]['path'],source_sha256=items[1]['sha256'],position_in_runtime_strip=i+1,source_score=4.6,direct_native_review=True,evaluation=('Lavender' if i%2==0 else 'Periwinkle')+' cushion '+str(i+1)+' keeps the shared rounded padded silhouette, broad value grouping, deep plum edge and restrained seam. Static/source opinion only; no individual landing/contact or complete-action acceptance.') for i in range(5)]
review=dict(status='ALL7_CURRENT_SOURCES_AND5_CUSHION_OBJECTS_DIRECTLY_REVIEWED',checked_utc=now,sources=items,source_object_regions=regions,qualification='Five SVG native renderings, two native PNGs and four complete neutral PNG views directly inspected. Original source opinions were unassigned in the current register. Existing nursery attempt06/attempt03 provenance is preserved and confirmed; no novel nursery redraw. Current vector sources remain runtime authority pending a separate qualified replacement.',runtime_integration=False,owner_approval=None)
write(report/'REVIEW.json',review)
style='body{background:#edf4fa;color:#26304b;font:17px/1.5 system-ui;margin:0}main{max-width:1320px;margin:auto;padding:24px}header,article{background:white;border-radius:16px;padding:20px;margin-bottom:18px}h1,h2{line-height:1.25}a{color:#504096}img{display:block;max-width:100%;height:auto;margin:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}.grid article{min-width:0}.image{background:#d0f0f1;border-radius:10px;padding:12px}.score{font-weight:bold}code,small{display:block;overflow-wrap:anywhere}'
cards=''.join('<article><h2>'+html.escape(x['id'])+'</h2><p class="score">Source '+str(x['source_score'])+'/5 · mounted/action pending</p>'+''.join('<figure class="image"><img loading="lazy" src="'+p+'" alt="Exact whole current '+html.escape(Path(x['path']).name)+' source preview"></figure>' for p in x['preview_paths'])+'<p>'+html.escape(x['evaluation'])+'</p><code>'+html.escape(x['path'])+'</code><small>'+x['sha256']+'</small></article>' for x in items)
cards+=''.join('<article><h2>'+x['id']+'</h2><p class="score">Source '+str(x['source_score'])+'/5</p><p>'+x['evaluation']+'</p><small>Individual object '+str(x['position_in_runtime_strip'])+' within the full five-cushion native row displayed above; no invented individual UV binding.</small></article>' for x in regions)
(report/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nursery, teacher and geology individual source review</title><style>'+style+'</style><main><header><a href="../job_review_v2_20261001/index.html">Current audit entry</a><h1>Nursery, teacher and geology: current individual sources</h1><p>Seven exact sources and all five cushion objects directly reviewed. Nursery source art retains4.6; five vector polish priorities remain individually identified. No current complete job or owner acceptance follows.</p><p><a href="REVIEW.json">Each written opinion and reference trace</a> · <a href="RENDER_RECEIPT.json">Unchanged original/native render proof</a></p></header><div class="grid">'+cards+'</div></main></html>',encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),report/'executed_record_and_prepare_vector_candidates_v73.py')
out=r/'assets_src/vector/job_geology_teacher_refinement_v1_20261001';assert not out.exists();out.mkdir(parents=True)
(out/'.gdignore').write_text('')
base=lambda body:'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">\n'+body+'\n</svg>\n'
fossil=base('''<defs><clipPath id="stone"><path d="M35 176Q30 150 44 88Q46 72 63 60L104 34Q113 29 128 35L196 54Q210 59 216 76L232 141Q236 154 226 168L192 211Q183 224 168 223L79 220Q65 219 58 209Z"/></clipPath></defs>
<g clip-path="url(#stone)"><rect width="256" height="256" fill="#e8c58e"/><path d="M24 181Q111 165 244 159V239H24Z" fill="#c6a1a3"/><path d="M36 70Q109 16 211 65L215 90Q118 60 37 104Z" fill="#f5dda9"/><path d="M33 187Q107 190 216 173L194 211Q109 239 58 212Z" fill="#bea0b9"/></g>
<path d="M35 176Q30 150 44 88Q46 72 63 60L104 34Q113 29 128 35L196 54Q210 59 216 76L232 141Q236 154 226 168L192 211Q183 224 168 223L79 220Q65 219 58 209Z" fill="none" stroke="#48315c" stroke-width="6" stroke-linejoin="round"/>
<path d="M177 97c-15-31-68-32-87-5-25 35 10 78 47 58 24-14 18-48-5-50-18-1-25 20-13 30" fill="none" stroke="#9a6c72" stroke-width="8" stroke-linecap="round"/>
<path d="M177 97c-15-31-68-32-87-5-25 35 10 78 47 58" fill="none" stroke="#fff0bc" stroke-width="3" stroke-linecap="round"/>''')
rock=base('''<defs><clipPath id="layers"><path d="M30 194Q40 126 54 88Q60 72 77 59L98 44Q106 38 120 42L173 55Q186 59 196 72L225 115Q234 127 229 143L208 197Q203 211 187 212L43 213Q28 213 30 194Z"/></clipPath></defs>
<g clip-path="url(#layers)"><rect width="256" height="256" fill="#756483"/><path d="M47 84Q111 58 200 72L214 99Q124 89 46 113Z" fill="#d7afe9"/><path d="M43 124Q114 104 223 111L232 140Q126 130 38 155Z" fill="#f2b78e"/><path d="M37 166Q129 147 222 151L211 195Q106 203 28 210Z" fill="#8bded6"/><path d="M27 202Q140 215 221 184L209 219H27Z" fill="#a5b6cf"/></g>
<path d="M30 194Q40 126 54 88Q60 72 77 59L98 44Q106 38 120 42L173 55Q186 59 196 72L225 115Q234 127 229 143L208 197Q203 211 187 212L43 213Q28 213 30 194Z" fill="none" stroke="#48315c" stroke-width="6" stroke-linejoin="round"/>
<circle cx="88" cy="105" r="9" fill="#fff0a8"/><circle cx="153" cy="138" r="7" fill="#fff0a8"/>''')
board=base('''<path d="M60 202 51 237M196 202l9 35" fill="none" stroke="#55415d" stroke-width="7" stroke-linecap="round"/>
<rect x="18" y="22" width="220" height="196" rx="26" fill="#edd3b1" stroke="#48315c" stroke-width="5"/>
<path d="M35 26h186q11 0 14 13H22q3-13 13-13Z" fill="#fff0d2"/>
<path d="M22 196h212q-3 18-20 18H43q-18 0-21-18Z" fill="#cbb4d0"/>
<rect x="31" y="38" width="194" height="156" rx="16" fill="#f9ebd7"/>
<circle cx="63" cy="75" r="18" fill="#80dbdc" stroke="#48315c" stroke-width="4"/>
<path d="m126 54 20 36H106Z" fill="#f1c58a" stroke="#48315c" stroke-width="4" stroke-linejoin="round"/>
<circle cx="188" cy="75" r="18" fill="#80dbdc" stroke="#48315c" stroke-width="4"/>
<path d="M43 115H213" stroke="#d6b8da" stroke-width="3" stroke-linecap="round"/>
<g fill="#c4a4e7" stroke="#48315c" stroke-width="4"><circle cx="65" cy="159" r="17"/><circle cx="130" cy="159" r="17"/><circle cx="179" cy="159" r="17"/></g>''')
crystals=base('''<path d="M28 187Q42 165 63 168L94 158Q124 151 156 161L200 162Q222 166 233 188Q239 203 225 210Q129 228 35 211Q17 206 28 187Z" fill="#b5a6cf" stroke="#48315c" stroke-width="6" stroke-linejoin="round"/>
<path d="M26 196Q116 210 235 192Q237 207 224 211Q120 229 36 211Q22 208 26 196Z" fill="#8f84b1"/>
<path d="M69 162 87 73Q89 65 95 59l22-23q6-6 10 3l20 51q3 8 0 17l-19 59Q98 176 69 162Z" fill="#89e3da" stroke="#48315c" stroke-width="6" stroke-linejoin="round"/>
<path d="m120 37 5 91-9 38 12-1 19-58q3-9 0-17l-20-51q-4-9-7-2Z" fill="#67bab9"/>
<path d="m95 59 22-23 6 45-23 22Z" fill="#e9f4c0"/>
<path d="m132 169 20-77q3-8 10-13l25-20q7-5 9 4l10 57q2 8-3 17l-23 41q-29 2-48-9Z" fill="#d0a8ee" stroke="#48315c" stroke-width="6" stroke-linejoin="round"/>
<path d="m190 59 5 81-15 37 23-40q5-9 3-17l-10-57q-2-9-6-4Z" fill="#a27ec6"/>
<path d="m164 84 23-19 5 37-27 18Z" fill="#f3c4e2"/>''')
drafts={'geologist_fossil_v1.svg':fossil,'geologist_layered_rock_v1.svg':rock,'teacher_lesson_board_v1.svg':board,'goal_geologist_v1.svg':crystals,'opera_crest_geologist_v1.svg':crystals.replace('stroke-width="6"','stroke-width="8"')}
candidate_items=[]
for x,(name,art) in zip(items[2:],drafts.items()):
 p=out/name;p.write_text(art,encoding='utf-8',newline='\n')
 candidate_items.append(dict(id='VECTOR-REFINEMENT-'+name.removesuffix('.svg').upper(),path=rel(p),sha256=sha(p),source_path=x['path'],source_sha256=x['sha256'],original_source_score=x['source_score'],source_score=None,status='NATIVE_PREVIEW_AND_REVIEW_PENDING',dimensions=[256,256],modifications='Code-native reversible SVG derivative: preserves object counts, educational shapes/colors and shared icon identity; softens mass/contours and adds calm broad value bands. Crest reuses refined crystal shapes with a small-icon contour variant.',qualification='Non-runtime derivative only; no original source, binding, character, game or timeline edits.'))
write(out/'CANDIDATE_MANIFEST.json',dict(status='PREPARED_FIVE_REVERSIBLE_VECTOR_DERIVATIVES',checked_utc=now,baseline=profile['baseline'],source_license='Project original, all rights reserved; source rows in ASSET_LICENSES.md2827/3367, no third-party pixels.',named_gap='Current source-only scores4.0–4.4 identify coarse flat symbols and overly heavy world-object contours. Preserve native vector medium and approved identity; improve only named contour/material groups. The existing nursery arms/cushions4.6 are reused without a redraw.',items=candidate_items,runtime_integration=False,owner_approval=None))
shutil.copyfile(Path(__file__),out/'executed_record_and_prepare_vector_candidates_v73.py')
script='extends SceneTree\nfunc _initialize() -> void:\n'
for n,x in enumerate(candidate_items):
 filename=Path(x['path']).stem
 script+=f'\tvar image_{n} := Image.new()\n\tassert(image_{n}.load_svg_from_string(FileAccess.get_file_as_string("res://{x["path"]}")) == OK)\n\tassert(image_{n}.save_png("res://{out.relative_to(r).as_posix()}/{filename}_native.png") == OK)\n'
script+='\tprint("JOB_VECTOR_DERIVATIVES|5_NATIVE_PREVIEWS|REVIEW_PENDING")\n\tquit(0)\n'
tmp=r/'tmp/render_job_vector_candidates_v73.gd';tmp.write_text(script,encoding='utf-8',newline='\n');shutil.copyfile(tmp,out/'render_svg_native.gd')
license=r/'ASSET_LICENSES.md';text=license.read_text(encoding='utf-8')
for folder in [report,out]:
 for p in folder.glob('*'):
  if p.suffix not in ['.png','.svg'] or f'`{rel(p)}`' in text:continue
  text+=f'\n| `{rel(p)}` | '+('Current exact source mechanically rasterized/neutral review composite; all original source attribution in adjacent REVIEW.json.' if folder==report else 'Project-original code-authored reversible vector refinement, originals and modifications recorded in adjacent CANDIDATE_MANIFEST.json.')+' | Project original, all rights reserved; underlying source provenance retained. | Internal source/native review, 2026-10-01; no third-party pixels. | '+('Complete technical display preview; no source-pixel repair or game edit.' if folder==report else 'Non-runtime SVG candidate, no binding or mounted/action/owner acceptance.')+' |\n'
license.write_text(text,encoding='utf-8',newline='\n')
recordfile=r/'design/audit_impacts/job-nursery-teacher-geology-native-review-20261001.json';record=read(recordfile)
record['files']=sorted(set(record['files'])|{rel(p) for p in report.rglob('*') if p.is_file()}|{rel(p) for p in out.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'})
record['scope']+=' Direct native review completes7 source opinions and5 cushion-object opinions; prepare5 reversible code-native vector derivatives for named4.0–4.4 polish gaps, preserving all original assets and runtime bindings.'
record['validation']=[dict(command='Direct current full-native and neutral source review with unchanged literal hashes',result='PASS',evidence=rel(report/'REVIEW.json')+'; nursery sources4.6, five original vectors4.0–4.4; no whole action pass.'),dict(command='Five vector derivative native previews and individual source opinions',result='PENDING',evidence=rel(out/'CANDIDATE_MANIFEST.json'))];write(recordfile,record)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';proc=subprocess.run([godot,'--headless','--path',str(r),'--script','res://'+tmp.relative_to(r).as_posix()],cwd=r,capture_output=True)
(out/'render.stdout.log').write_bytes(proc.stdout);(out/'render.stderr.log').write_bytes(proc.stderr)
write(out/'RENDER_RECEIPT.json',dict(status='PASS_NATIVE_PREVIEW_ONLY' if proc.returncode==0 else 'FAIL_PRESERVED',process_exit=proc.returncode,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_integration=False,qualification='Mechanical complete256x256 native SVG previews; every source/candidate opinion remains separate from current mount/action.'))
for p in out.glob('*_native.png'):
 if f'`{rel(p)}`' not in text:text+=f'\n| `{rel(p)}` | Complete native Godot4.7.2 raster preview of adjacent project-original reversible SVG candidate. | Project original, all rights reserved. | Internal native vector preview, 2026-10-01. | Unmodified complete technical raster, source/mounted/action review pending. |\n'
license.write_text(text,encoding='utf-8',newline='\n');record['files']=sorted(set(record['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(recordfile,record)
print(json.dumps(dict(current_sources=7,current_cushion_objects=5,vector_original_scores=[x['source_score'] for x in items[2:]],candidate_native_previews=5,render_exit=proc.returncode,originals_unchanged=all(sha(r/x['path'])==x['sha256'] for x in items))))
raise SystemExit(proc.returncode)
