from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'assets_src/vector/job_geology_teacher_refinement_v1_20261001'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(r).as_posix()
manifest=read(out/'CANDIDATE_MANIFEST.json')
grades=[(4.4,'The gentler contour and rounded slab improve the fossil, and the spiral remains clear. The broad purple bands across the lower stone look like cut color stripes rather than quiet warm stone material. Retain this attempt below floor and refine only the value grouping.'),(4.4,'The rounded boulder and thinner contour improve the teaching silhouette while keeping three colored strata and two mineral dots. The bands remain uniformly flat and diagram-like beside painted props. Retain below floor; add restrained broad material values without new speckling or changing the educational layers.'),(4.4,'The frame has better grouped values and a gentler outline; the exact six lesson shapes are preserved. The narrow bent legs still read as wires rather than sturdy rounded toy-board supports. Retain below floor and refine the existing supports only.'),(4.5,'The collectible keeps two aqua/lavender crystals, large quiet facets and an attached rounded lavender mineral base. Gentler contours and broad side values make it a coherent toy prop while avoiding small glitter/detail. This meets the native-source drafting floor only; splitting, reveal, collection and game-size mounting are not passed.'),(4.5,'The crest reuses the same refined crystal identity with a slightly stronger contour for its compact icon purpose. The attached rounded base and quiet facets give the shared symbol more polish while retaining easy color recognition. Native-source drafting floor only; actual small UI rendering remains unreviewed.')]
items=[]
for x,(score,evaluation) in zip(manifest['items'],grades):
 assert sha(r/x['path'])==x['sha256'];p=out/(Path(x['path']).stem+'_native.png')
 q=dict(x);q.update(source_score=score,status='SOURCE_FLOOR_MET_UNBOUND_CONTEXT_PENDING' if score>=4.5 else 'REJECTED_SOURCE_BELOW_FLOOR_PRESERVED',attempt=1,evaluation=evaluation,direct_full_native_review=True,preview_path=rel(p),preview_sha256=sha(p),mounted_score=None,complete_action_score=None);items.append(q)
write(out/'ATTEMPT01_REVIEW.json',dict(status='ALL5_NATIVE_VECTOR_DRAFTS_DIRECTLY_REVIEWED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),items=items,qualification='Complete256x256 native raster previews directly inspected. Three4.4 drafts require another source refinement; two4.5 source-floor drafts remain unbound. All current originals and bindings preserved. No mounted/action/device/child/owner acceptance.'))
variants={}
s=(out/'geologist_fossil_v1.svg').read_text(encoding='utf-8')
s=s.replace('<defs>','<defs><linearGradient id="clay" x1="15%" y1="0%" x2="85%" y2="100%"><stop stop-color="#f4dcb5"/><stop offset=".55" stop-color="#e8c58e"/><stop offset="1" stop-color="#d6b298"/></linearGradient>',1)
s=s.replace('<rect width="256" height="256" fill="#e8c58e"/>','<rect width="256" height="256" fill="url(#clay)"/>')
s=s.replace('<path d="M24 181Q111 165 244 159V239H24Z" fill="#c6a1a3"/>','<path d="M43 191Q133 205 233 155Q222 205 172 223L78 220Z" fill="#cfb4ae"/>')
s=s.replace('<path d="M33 187Q107 190 216 173L194 211Q109 239 58 212Z" fill="#bea0b9"/>','')
variants['geologist_fossil_v2.svg']=s
s=(out/'geologist_layered_rock_v1.svg').read_text(encoding='utf-8')
defs=''.join(f'<linearGradient id="{name}" x1="0%" y1="0%" x2="90%" y2="100%"><stop stop-color="{light}"/><stop offset=".6" stop-color="{middle}"/><stop offset="1" stop-color="{dark}"/></linearGradient>' for name,light,middle,dark in [('lilac','#e3c1ee','#d7afe9','#bc99d3'),('peach','#f8c9a1','#f2b78e','#dca389'),('aqua','#acf0e4','#8bded6','#73c4ca')])
s=s.replace('<defs>','<defs>'+defs,1)
for color,name in [('#d7afe9','lilac'),('#f2b78e','peach'),('#8bded6','aqua')]:s=s.replace(f'fill="{color}"',f'fill="url(#{name})"')
variants['geologist_layered_rock_v2.svg']=s
s=(out/'teacher_lesson_board_v1.svg').read_text(encoding='utf-8')
old='<path d="M60 202 51 237M196 202l9 35" fill="none" stroke="#55415d" stroke-width="7" stroke-linecap="round"/>'
new='<g fill="#e6c29d" stroke="#48315c" stroke-width="5" stroke-linejoin="round"><path d="M58 203 49 237Q49 244 59 241L73 206Z"/><path d="m183 206 14 35q10 3 10-4l-9-34Z"/></g><path d="m55 222-4 15 8 1 6-15Zm143 0 6 15-7 1-7-15Z" fill="#c6a9bd"/>'
assert old in s;s=s.replace(old,new)
variants['teacher_lesson_board_v2.svg']=s
provenance=[]
for filename,art in variants.items():
 p=out/filename;assert not p.exists();p.write_text(art,encoding='utf-8',newline='\n');stem=filename.replace('_v2.svg','_v1.svg');parent=next(x for x in items if x['path'].endswith('/'+stem))
 provenance.append(dict(id='VECTOR-REFINEMENT-'+filename.removesuffix('.svg').upper(),path=rel(p),sha256=sha(p),source_path=parent['source_path'],source_sha256=parent['source_sha256'],earlier_attempt_path=parent['path'],earlier_attempt_sha256=parent['sha256'],earlier_score=4.4,attempt=2,source_score=None,dimensions=[256,256],status='NATIVE_PREVIEW_AND_REVIEW_PENDING',modifications='Targeted code-native second derivative: fossil warm stone values, layered-rock broad restrained material values, or sturdy toy-board supports. Object identities/counts and all original runtime sources unchanged.'))
write(out/'ATTEMPT02_PROVENANCE.json',dict(status='PREPARED_THREE_TARGETED_VECTOR_REFINEMENTS',items=provenance,runtime_integration=False,owner_approval=None))
shutil.copyfile(Path(__file__),out/'executed_record_attempt01_prepare_attempt02_v75.py')
script='extends SceneTree\nfunc _initialize() -> void:\n'
for n,x in enumerate(provenance):
 filename=Path(x['path']).stem
 script+=f'\tvar image_{n} := Image.new()\n\tassert(image_{n}.load_svg_from_string(FileAccess.get_file_as_string("res://{x["path"]}")) == OK)\n\tassert(image_{n}.save_png("res://{out.relative_to(r).as_posix()}/{filename}_native.png") == OK)\n'
script+='\tprint("JOB_VECTOR_ATTEMPT02|3_NATIVE_PREVIEWS|REVIEW_PENDING")\n\tquit(0)\n'
tmp=r/'tmp/render_job_vector_candidates_attempt02_v75.gd';tmp.write_text(script,encoding='utf-8',newline='\n');shutil.copyfile(tmp,out/'render_svg_attempt02_native.gd')
recordfile=r/'design/audit_impacts/job-nursery-teacher-geology-native-review-20261001.json';record=read(recordfile);record['files']=sorted(set(record['files'])|{rel(p) for p in out.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'});record['validation'].append(dict(command='Direct native first-vector-attempt review',result='FAIL',evidence=rel(out/'ATTEMPT01_REVIEW.json')+'; three4.4 drafts preserved, two4.5 source floors unbound.'));write(recordfile,record)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';proc=subprocess.run([godot,'--headless','--path',str(r),'--script','res://'+tmp.relative_to(r).as_posix()],cwd=r,capture_output=True)
(out/'attempt02_render.stdout.log').write_bytes(proc.stdout);(out/'attempt02_render.stderr.log').write_bytes(proc.stderr)
write(out/'ATTEMPT02_RENDER_RECEIPT.json',dict(status='PASS_NATIVE_PREVIEW_ONLY' if proc.returncode==0 else 'FAIL_PRESERVED',process_exit=proc.returncode,runtime_integration=False))
license=r/'ASSET_LICENSES.md';text=license.read_text(encoding='utf-8')
for p in out.glob('*'):
 if p.suffix in ['.png','.svg'] and f'`{rel(p)}`' not in text:text+=f'\n| `{rel(p)}` | Targeted project-original code-authored SVG derivative or complete officialGodot4.7.2 native raster; source/first-attempt hashes in adjacent ATTEMPT02_PROVENANCE.json. | Project original, all rights reserved. | Internal source review, 2026-10-01. | Unbound second-source draft, original runtime sources preserved; no mounted/action/owner acceptance. |\n'
license.write_text(text,encoding='utf-8',newline='\n');record['files']=sorted(set(record['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(recordfile,record)
print(json.dumps(dict(first_scores=[x['source_score'] for x in items],second_previews=3,render_exit=proc.returncode)));raise SystemExit(proc.returncode)
