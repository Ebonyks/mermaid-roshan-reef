from pathlib import Path
import datetime, hashlib, json, shutil

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
OLD=B/'assets_src/local_motion/nursery_connected_scrub_v4_20261002'
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
    task_next=p.with_name(p.name+'.v546_next')
    task_next.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    task_next.replace(p)
source=OLD/'review_tools/archive_nursery_scrub_a4_v425.py'
code=source.read_text(encoding='utf-8')
changes={'nursery_connected_scrub_v4_20261002':'candy_wrap_continuity_v1_20261003','nursery_local_scrub_a4_active_20261002':'candy_local_wrap_a1_active_20261003','NUR-SCRUB-A4':'CANDY-WRAP-A1','job-nursery-scrub-prompt-a4-20261002.json':'job-candy-local-wrap-continuity-20261003.json','PROMPT-ONLY NURSERY SCRUB A4':'CANDY FOLD-SLIDE-TWIST-RELEASE A1','A4_NATIVE_ARCHIVED':'CANDY_A1_NATIVE_ARCHIVED','FIFO A4':'FIFO Candy A1'}
for a,z in changes.items():
    assert a in code
    code=code.replace(a,z)
target=P/'review_tools/archive_candy_wrap_a1_v546.py'
assert not target.exists()
compile(code,str(target),'exec')
target.write_text(code,encoding='utf-8',newline='\n')
write(P/'ARCHIVER_DERIVATION.json',{'source_path':source.relative_to(B).as_posix(),'source_sha256':sha(source),'changes':changes,'qualification':'Only packet/job/state/impact identifiers and descriptive labels. Existing byte assertions, output-root containment, direct passthrough decoding,41 frame count and seven native-size non-resampled QA boards remain unchanged.'})
write(P/'EXTRACTION_SCRIPT_GATES.json',{'status':'PASS_PARSER_AND_TYPED_INFERENCE','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script':(P/'review_tools/extract_complete_open_cell.gd').relative_to(B).as_posix(),'script_sha256':sha(P/'review_tools/extract_complete_open_cell.gd'),'commands':[{'command':'python -X utf8 -B -m gdtoolkit.parser assets_src/local_motion/candy_wrap_continuity_v1_20261003/review_tools/extract_complete_open_cell.gd','process_exit':0,'tool_output':''},{'command':'python -X utf8 -B tools/lint_inference.py assets_src/local_motion/candy_wrap_continuity_v1_20261003/review_tools/extract_complete_open_cell.gd','process_exit':0,'tool_output':''}],'engine_compile':'Official4.7.2 actual extraction process exit0 in EXTRACTION stdout/stderr logs. No whole-suite rerun or error-free-log claim.'})
previous=P/'previous_v_remote_verified';assert not previous.exists();previous.mkdir()
staging=B/'tmp/candy_review_v_remote_preserved_v543'
index=read(staging/'JOURNAL_INDEX.json')
assert index['rows']==23323 and len(index['shards'])==12
for name in ['RESULT.json','JOURNAL_INDEX.json','HOSTED_V_RAW.json','HOSTED_V_VERIFICATION.json','RECEIPT.json']+[x['path'] for x in index['shards']]:
    shutil.copyfile(staging/name,previous/name)
    assert sha(previous/name)==sha(staging/name)
raw=b''.join((previous/x['path']).read_bytes() for x in index['shards'])
assert hashlib.sha256(raw).hexdigest()==index['sha256']
assert read(previous/'RESULT.json')['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
index_html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Candy wrapping continuity — local reference</title><style>body{font:18px/1.5 system-ui;max-width:1100px;margin:32px auto;padding:0 20px;background:#edf5fa;color:#25344b}img{max-width:100%;height:auto}a{color:#3c428a}.note{padding:16px;background:white;border-radius:16px}</style><h1>Candy wrapping continuity</h1><p class="note">One guarded local ComfyUI reference study: fold the same golden paper, slide both mittens to the narrow necks, counter-twist, then release the same supported sweet. Rendering and every native-frame motion evaluation are pending. Current game wrapping2.8/5 and earlier unbound actual motion4.1/5 remain below4.5.</p><h2>Exact existing opening source</h2><img src="source_frames/CANDY-WRAP-OPEN-A7.png" width="627" height="627" alt="Complete unchanged opening cell: Roshan holds one gold sheet around one red oval sweet"><p>Complete authored627×627 source cell, independent RGBA pixel equality. No redraw or appearance repair.</p><h2>Inspected technical model input</h2><img src="inputs/CANDY-WRAP-A1.png" width="896" height="512" alt="The same complete opening cell uniformly normalized on a neutral pale mat"><p><a href="MANIFEST.json">Exact source, prompt and installed workflow bindings</a> · <a href="PLAN.json">Scope and predeclared failure criteria</a> · <a href="prompts/CANDY-WRAP-A1.txt">Exact timeline prompt</a> · <a href="SOURCE_CELL_EQUIVALENCE.json">Source pixel equality</a> · <a href="previous_v_remote_verified/RESULT.json">Previous V23323-file anonymous publication verification</a></p><p>Reference-only; no runtime/cinematic/device/child/owner or full-job acceptance. Rejected sources and all783 current production bytes are preserved.</p></html>'''
(P/'index.html').write_text(index_html,encoding='utf-8',newline='\n')
d=read(IP);d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()})
d['validation'].append({'command':'Required parser/inference for exact source extractor; preserved prior V complete remote journal reassembly','result':'PASS','evidence':(P/'EXTRACTION_SCRIPT_GATES.json').relative_to(B).as_posix()+'; '+(previous/'JOURNAL_INDEX.json').relative_to(B).as_posix()})
write(IP,d)
print(json.dumps({'status':'ARCHIVER_PREPARED_RENDER_STILL_PENDING','prior_verified_rows':23323,'prior_journal_shards':12,'files_covered':len(d['files'])}))
