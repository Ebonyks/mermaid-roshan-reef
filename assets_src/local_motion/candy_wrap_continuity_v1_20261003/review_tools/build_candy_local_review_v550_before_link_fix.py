from pathlib import Path
import datetime, hashlib, html, json, os, shutil

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';Q=P/'comparison_a2'
M=B/'assets_src/imagegen/candy_wrap_contact_v1_20261003';N=M/'attempt11'
IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
esc=lambda s:html.escape(str(s))
rel=lambda p:os.path.relpath(p,P).replace('\\','/')
def update(p,raw):
    task_next=p.with_name(p.name+'.v550_next');task_next.write_bytes(raw);task_next.replace(p)
def write(p,d):update(p,(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert read(P/'REVIEW_STATUS.json')['whole_reference_action_score']==2.4
assert sha(N/'native.png')==read(N/'SOURCE.json')['sha256']
if not (P/'index_v0_pending.original.html').exists():shutil.copyfile(P/'index.html',P/'index_v0_pending.original.html')
sections=[];clip_data={};native_total=0;opinion_total=0
for tag,label,packet in [('a1','A1: complete wrapping reference',P),('a2','A2: far long-edge fold component',Q)]:
    index_path=packet/'attempt01/INDEX.json';review_path=packet/'attempt01/DIRECT_REVIEW.json'
    if not index_path.exists() or not review_path.exists():
        sections.append('<section id="'+tag+'"><h2>'+esc(label)+'</h2><p class="pending">Rendering/direct native review pending. This component cannot establish full wrapping.</p><img src="'+esc(rel(packet/'inputs/CANDY-FOLD-A2.png'))+'" width="896" height="512" alt="Inspected complete far-fold model input"><p><a href="'+esc(rel(packet/'PLAN.json'))+'">Exact component contract</a></p></section>')
        continue
    idx=read(index_path);review=read(review_path);assert len(idx['frames'])==len(review['individual_frames'])==41
    assert all(sha(B/x['path'])==x['sha256'] for x in idx['frames']+idx['boards'])
    native_total+=41;opinions=review['component_opinions'];opinion_total+=len(opinions)
    score=review.get('whole_reference_action_score',review.get('whole_component_score'))
    video=next(x for x in idx['outputs'] if x['path'].endswith('.webm'))
    clip_data[tag]=[dict(index=x['index'],src=rel(B/x['path']),caption=f"Frame{x['index']} · {x['timestamp_seconds']:.3f}s · canvas{x['visual_frame_score']}/5. "+x['evaluation']) for x in review['individual_frames']]
    s='<section id="'+tag+'"><h2>'+esc(label)+'</h2><p class="rejected">'+esc(review['status'])+' · '+esc(score)+'/5. Reference-only, unbound.</p><p>'+esc(review['qualification'])+'</p><button type="button" data-play="'+tag+'">Play native '+tag.upper()+' take</button> <button type="button" data-pause="'+tag+'">Pause native '+tag.upper()+' take</button><video id="video-'+tag+'" controls preload="metadata" playsinline width="896" height="512" src="'+esc(rel(B/video['path']))+'"></video><p id="video-state-'+tag+'">Native video control ready; no interpolated or synthetic frames.</p>'
    s+='<div class="scrubber"><button type="button" data-step="'+tag+'" data-delta="-1">Previous '+tag.upper()+' frame</button> <button type="button" data-step="'+tag+'" data-delta="1">Next '+tag.upper()+' frame</button><label> '+tag.upper()+' native frame <input type="range" id="range-'+tag+'" min="0" max="40" value="0"></label><img id="selected-'+tag+'" src="'+esc(clip_data[tag][0]['src'])+'" width="896" height="512" alt="Selected complete native reference canvas"><p id="caption-'+tag+'">'+esc(clip_data[tag][0]['caption'])+'</p></div><table><thead><tr><th>Individual component</th><th>Score</th><th>Evaluation</th></tr></thead><tbody>'
    for x in opinions:s+='<tr><td>'+esc(x['item'])+'</td><td>'+esc(x['score'])+'/5</td><td>'+esc(x['evaluation'])+'</td></tr>'
    s+='</tbody></table><details><summary>Every41 native canvas and individual drafting opinion</summary><div class="frames">'
    for x in review['individual_frames']:
        s+='<article class="native-frame" data-take="'+tag+'" data-frame="'+str(x['index'])+'"><h3>Frame'+str(x['index'])+' · '+format(x['timestamp_seconds'],'.3f')+'s · '+str(x['visual_frame_score'])+'/5</h3><a href="'+esc(rel(B/x['path']))+'"><img loading="lazy" src="'+esc(rel(B/x['path']))+'" width="896" height="512" alt="Complete native '+tag+' reference frame'+str(x['index'])+'"></a><p>'+esc(x['evaluation'])+'</p></article>'
    s+='</div></details><details><summary>Every ordered original-size QA board</summary>'
    for x in idx['boards']:s+='<a href="'+esc(rel(B/x['path']))+'"><img loading="lazy" class="board" src="'+esc(rel(B/x['path']))+'" alt="Native non-resampled canvases from frame'+str(x['first'])+'"></a>'
    s+='</details><p><a href="'+esc(rel(review_path))+'">All frame/component scores</a> · <a href="'+esc(rel(packet/'attempt01/RENDER_RECEIPT.json'))+'">Native render receipt</a> · <a href="'+esc(rel(packet/'MANIFEST.json'))+'">Bound prompt/input/workflow</a></p></section>'
    sections.append(s)
style='body{font:18px/1.5 system-ui;max-width:1180px;margin:32px auto;padding:0 20px;background:#edf5fa;color:#25344b}a{color:#454590}img,video{max-width:100%;height:auto;display:block}section,.source,.note{background:white;padding:20px;margin:24px 0;border-radius:18px}.rejected{background:#fce7e8;padding:14px;border-radius:12px}.pending{background:#fff4d8;padding:14px}button{font:inherit;padding:10px 16px;margin:8px 4px 8px 0;border:1px solid #b4bfd8;border-radius:12px;background:#eaf0ff;color:#25344b}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{padding:10px;text-align:left;border-bottom:1px solid #dce2ee;vertical-align:top}.frames{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}.native-frame h3{font-size:18px}.board{margin:18px 0}.source-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}.source-grid img{background:#e3edf3}input[type=range]{width:min(420px,75vw)}summary{cursor:pointer;padding:12px;background:#f1f4fa;border-radius:12px}.scrubber{padding:12px;background:#f7f9fe;border-radius:16px}@media(max-width:600px){body{font-size:16px;padding:0 12px}section{padding:12px}table{font-size:14px}.frames{display:block}}'
sources='<div class="source-grid"><div class="source"><h2>Preserved opening cell</h2><img src="source_frames/CANDY-WRAP-OPEN-A7.png" width="627" height="627" alt="Exact unchanged A7 opening cell"><p>Complete existing authored cell; source4.5 is not a motion pass.</p><a href="SOURCE_CELL_EQUIVALENCE.json">Exact RGBA pixel equality</a></div><div class="source"><h2>Fresh A11 grip</h2><img src="'+esc(rel(N/'native.png'))+'" width="1254" height="1254" alt="New complete A11 source: far-edge mitten grip with opposite sweet support"><p>Requested near-edge role4.0 rejected. Alternate far-edge source4.5 provisional, inclusive priority. The complete returned native is preserved.</p><a href="'+esc(rel(N/'index.html'))+'">Source review and exact ImageGen prompt</a></div></div>'
script='const TAKES='+json.dumps(clip_data,separators=(',',':'))+';const positions={};function show(tag,n){const rows=TAKES[tag];n=Math.max(0,Math.min(40,n));positions[tag]=n;document.getElementById("range-"+tag).value=n;document.getElementById("selected-"+tag).src=rows[n].src;document.getElementById("caption-"+tag).textContent=rows[n].caption;}for(const tag of Object.keys(TAKES)){positions[tag]=0;document.getElementById("range-"+tag).addEventListener("input",e=>show(tag,Number(e.target.value)));const v=document.getElementById("video-"+tag);for(const event of ["play","pause","ended","timeupdate"]){v.addEventListener(event,()=>{document.getElementById("video-state-"+tag).textContent="Native "+tag+" "+(v.ended?"ended":v.paused?"paused":"playing")+" · "+v.currentTime.toFixed(3)+"s · "+v.videoWidth+"×"+v.videoHeight;});}}for(const b of document.querySelectorAll("[data-step]")){b.addEventListener("click",()=>show(b.dataset.step,positions[b.dataset.step]+Number(b.dataset.delta)));}for(const b of document.querySelectorAll("[data-play]")){b.addEventListener("click",()=>document.getElementById("video-"+b.dataset.play).play());}for(const b of document.querySelectorAll("[data-pause]")){b.addEventListener("click",()=>document.getElementById("video-"+b.dataset.pause).pause());}'
body='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Candy wrapping continuity — complete local review</title><style>'+style+'</style><h1>Candy wrapping continuity</h1><p class="note">Current in-game wrapping2.8/5; earlier unbound in-game contact study4.1/5. New A1 complete local take2.4/5 rejected: corners lift, but the sweet is never wrapped. New source A11 provides an alternate far-edge grip; its requested near-edge role failed. A2 tests one far-edge fold and cannot establish complete neck grip, opposing twist, release or runtime acceptance.</p><p>'+str(native_total)+' complete native frames currently reviewed, '+str(opinion_total)+' individual component evaluations. All783 current production members preserved. Device, child, owner, ordinary runtime/input/interruption and full-job acceptance remain open.</p><p><a href="../../../../audit/job_candy_wrap_contact_runtime_v1_20261003/index.html">Previous actual contact study</a> · <a href="../../../../audit/job_artwork_refinement_live/all_items.html">Whole job artwork library</a> · <a href="previous_v_remote_verified/RESULT.json">Previous immutable V remote verification</a> · <a href="PLAN.json">This task contract</a></p>'+sources+''.join(sections)+'<p><a href="ARCHIVER_SELF_COPY_FAILURE_V547.json">Preserved archive helper failure</a> · <a href="ARCHIVE_RECOVERY_V547.json">Complete native recovery without rerender</a> · <a href="PRODUCTION_BOUNDARY.json">Exact current source boundary</a></p><script>'+script+'</script></html>'
update(P/'index.html',body.encode())
licenses=(B/'ASSET_LICENSES.md').read_bytes();new=[]
for x in sorted(P.rglob('*')):
    if not x.is_file() or x.suffix.lower() not in {'.png','.webm','.mp4','.gif'}:continue
    path=x.relative_to(B).as_posix();marker=('| `'+path+'` |').encode()
    if marker in licenses:continue
    role='Native locally generated reference video/canvas' if ('attempt01' in x.parts and 'QA_BOARD' not in x.name) else 'Technical input or native-size QA/reference illustration'
    new.append('| `'+path+'` | '+role+'; preserved original ImageGen and developed local Wan/ComfyUI provenance | Original project source; pinned upstream model/quantization/loader Apache-2.0 notices retained in workflows/GGUF_MODEL_RECEIPT.json | Exact source/prompt/model/workflow/output hashes in bound manifest and native render receipt | Reference-only; direct decoding and non-resampled QA boards where applicable, no production/cinematic/owner acceptance. |\n')
if new:update(B/'ASSET_LICENSES.md',licenses+('\n'+''.join(new)).encode())
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
allow=B/'tmp/v2_preview_allowed.json';allowed=read(allow)
if isinstance(allowed,list):
    allowed=sorted(set(allowed)|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()}|{x.relative_to(B).as_posix() for x in N.rglob('*') if x.is_file()})
else:
    raise AssertionError('Unexpected exact preview-whitelist schema; inspect before changing.')
write(allow,allowed)
d=read(IP);d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()}|{x.relative_to(B).as_posix() for x in N.rglob('*') if x.is_file()})
write(IP,d)
print(json.dumps({'report':str(P/'index.html'),'native_frames_reviewed':native_total,'component_opinions':opinion_total,'new_asset_license_rows':len(new),'covered_files':len(d['files'])}))
