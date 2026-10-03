from pathlib import Path
import datetime,hashlib,json,shutil
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';C=B/'assets_src/imagegen/candy_wrap_scene_context_v1_20261003';G=P/'gates_v3'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):n=p.with_name(p.name+'.v586_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');n.replace(p)
src=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/CANDY_A6_FINAL_FRAME_BROWSER_V586.jpg');assert src.is_file();shutil.copyfile(src,P/'BROWSER_A6_FINAL_FRAME_V586.jpg')
write(P/'BROWSER_CONTEXT_CONTROLS_V586.json',dict(status='ACTUAL_SIX_TAKE_REPORT_FRAME_SCRUBBER_AND_NATIVE_PLAY_PAUSE_VERIFIED',checked_utc=now(),url='http://127.0.0.1:8880/assets_src/local_motion/candy_wrap_continuity_v1_20261003/index.html?revision=context-a6#a6',native_frame_articles=246,individual_component_rows=60,range_end_value=40,selected_frame_dimensions=[896,512],selected_frame_canvas_score=2.4,selected_frame_caption='Fully exposed red sweet with a purple point, elongated teal cuff curls, held band and no release. The declared complete-cover endpoint fails.',native_play=dict(paused=False,current_time=0.230377,width=896,height=512),native_pause=dict(paused=True,ended=False,current_time=0.260693,duration=1.709),horizontal_overflow=False,screenshot_path=(P/'BROWSER_A6_FINAL_FRAME_V586.jpg').relative_to(B).as_posix(),screenshot_sha256=sha(P/'BROWSER_A6_FINAL_FRAME_V586.jpg'),qualification='Actual desktop review-page interaction and original native video controls. Source/motion rejection retained; no ordinary game/device/child/owner acceptance.'))
licenses=B/'ASSET_LICENSES.md';raw=licenses.read_bytes();path=(P/'BROWSER_A6_FINAL_FRAME_V586.jpg').relative_to(B).as_posix()
assert ('| `'+path+'` |').encode() not in raw
raw+=('\n| `'+path+'` | Actual browser screenshot of rejected A6 native frame40 and its written review | Original project review layout; generated local reference/model attribution retained | BROWSER_CONTEXT_CONTROLS_V586.json binds screenshot/observed controls | QA screenshot only, no runtime/cinematic pixels or accepted art/action/owner claim. |\n').encode();n=licenses.with_name(licenses.name+'.v586_next');n.write_bytes(raw);n.replace(licenses)
source=(P/'review_tools/run_review_gate_v571.py').read_text(encoding='utf-8').replace("gates_v2","gates_v3").replace('CANDIDATE_REVIEW_SOURCE_V571.json','CANDIDATE_CONTEXT_SOURCE_V587.json')
runner=P/'review_tools/run_context_gate_v587.py';runner.write_text(source,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,C/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in(C,P) for p in base.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'})
for label in ['authority','development','document_tests','game2d']:
    for suffix in ['.stdout.log','.stderr.log','.receipt.json']:d['files'].append((G/(label+suffix)).relative_to(B).as_posix())
d['files'].append((G/'CANDIDATE_CONTEXT_SOURCE_V587.json').relative_to(B).as_posix());d['files']=sorted(set(d['files']));write(ip,d)
members=[]
for path in d['files']:
    p=B/path
    if not p.is_file() or path.startswith(G.relative_to(B).as_posix()+'/'):continue
    members.append(dict(path=path,bytes=p.stat().st_size,sha256=sha(p)))
write(G/'CANDIDATE_CONTEXT_SOURCE_V587.json',dict(status='EXACT_REVIEW_MEMBERS_FROZEN_BEFORE_FRESH_GATES',baseline=d['baseline'],frozen_utc=now(),member_count=len(members),members=members,source_snapshot_exclusions=['gates_v3 outputs and this self metadata','self describing impact JSON','new publication map receives its own later exact index seal'],qualification='Exact source/review snapshot for actual fresh structural/document/2D regression checks. All783 current production literals independently match the preserved Candy boundary. Graphics/action failures and external acceptance remain separate.'))
print(json.dumps(dict(status='FRESH_CONTEXT_REVIEW_GATES_PREPARED',frozen_members=len(members),runner=runner.relative_to(B).as_posix(),all246_frames_reviewed=True)))
