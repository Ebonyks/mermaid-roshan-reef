from pathlib import Path
import json,hashlib,datetime,html,shutil
from PIL import Image,ImageDraw
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_nursery_wash_connected_v1_20261002';S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
out=F/'current_visual_v3';assert not out.exists();out.mkdir()
cases=[]
receipt=json.loads((F/'candidate_capture_v3/native_frames/CAPTURE_RECEIPT.json').read_text())
assert receipt['status']=='PASS_FOUR_NATIVE_ROOM_ROUTES'
for case in receipt['cases']:
    rows=[dict(x,path='candidate_capture_v3/native_frames/'+x['path']) for x in receipt['frames'] if x['case']==case['id']]
    cases.append({'id':case['id'],'rows':rows,'qualification':'Direct room/catalog fixture, production approach/input; no ordinary birthday route.'})
for width in [1280,1600]:
    cap=json.loads((F/'actual_route_v3'/('CAPTURE_%d.json'%width)).read_text())
    rows=[dict(x,path='actual_route_v3/'+x['path'],capture_index=x['index'],phase_progress=x['progress'],event=x['wash_state']) for x in cap['frames']]
    cases.append({'id':'actual_bubble_bath_%d'%width,'rows':rows,'qualification':cap['qualification']})
boards=[];details=[]
for case in cases:
    rows=case['rows']
    for offset in range(0,len(rows),48):
        part=rows[offset:offset+48]
        canvas=Image.new('RGB',(1440,1232),'#f0e9db');d=ImageDraw.Draw(canvas)
        d.text((8,6),case['id']+' v3 ALL consecutive native frames '+str(offset)+'-'+str(offset+len(part)-1),fill='#243652')
        for j,row in enumerate(part):
            with Image.open(F/row['path']) as im: im.load();im.thumbnail((240,135));canvas.paste(im,(j%6*240,30+j//6*150))
            d.text((j%6*240+3,30+j//6*150+135),f"{row['capture_index']:04d} p={row['phase_progress']:.2f} {row.get('wash_state','?')}",fill='#243652')
        p=out/(case['id']+'_%02d.png'%(offset//48));canvas.save(p)
        boards.append({'path':p.relative_to(R).as_posix(),'case':case['id'],'first':offset,'count':len(part),'sha256':sha(p),'qa_only':True,'production_pixels':False})
    seen={}
    for row in rows:
        state=row.get('wash_state','none')
        if state in ['ready','wet','rub_palm','rub_back','rinse','clean'] and row.get('task_open',False):
            seen.setdefault(state,[]).append(row)
    for state,group in seen.items():
        row=group[len(group)//2]
        p=out/(case['id']+'_'+state+'.webp');shutil.copyfile(F/row['path'],p)
        details.append({'path':p.relative_to(R).as_posix(),'case':case['id'],'state':state,'frame':row['capture_index'],'sha256':sha(p)})
write(out/'INDEX.json',{'status':'DIRECT_CURRENT_V3_FULL_SEQUENCE_REVIEW_PENDING','cases':[{'id':c['id'],'frames':len(c['rows']),'qualification':c['qualification']} for c in cases],'boards':boards,'native_details':details,'qualification':'Read-only QA sheets, every consecutive captured v3 frame represented. Per-source/state/native-detail review and whole-action judgement are separate. No physical-device/child/owner acceptance.'})
css='body{margin:0;background:#edf5f8;color:#25334b;font:17px/1.55 system-ui}main{max-width:1180px;margin:auto;padding:24px}a{color:#514796}h1,h2,h3{line-height:1.25}header,section,article{background:white;border-radius:16px;padding:22px;margin:0 0 20px}figure{margin:0}img{max-width:100%;height:auto;display:block}small{display:block;color:#58647a}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}.check{background:repeating-conic-gradient(#d5e8ec 0% 25%,#f8fcfc 0% 50%) 50%/24px 24px}.check img{width:100%;height:340px;object-fit:contain}code{overflow-wrap:anywhere;font-size:13px}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px;border-bottom:1px solid #ddd}button,input,select{font:inherit;margin:6px;padding:8px}.weak{color:#8b451e}details{margin:16px 0}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}'
sources=[]
for p in sorted(S.glob('*/SOURCE_REVIEW.json')):
    d=json.loads(p.read_text());sources.append({'id':p.parent.name,'score':d['score'],'note':d['note'],'source':p.parent.relative_to(R).as_posix()+'/native.png','review':p.relative_to(R).as_posix(),'priority':d['score']<=4.5})
gallery=''.join('<article><h3>'+html.escape(d['id'].replace('_',' '))+' · '+str(d['score'])+'/5</h3><figure class="check"><a href="'+d['id']+'/native.png"><img loading="lazy" src="'+d['id']+'/native.png" alt="'+html.escape(d['id'])+'"></a></figure><p>'+html.escape(d['note'])+'</p><p><a href="'+d['id']+'/SOURCE_REVIEW.json">Individual opinion, native alpha and exact references</a> · <a href="'+d['id']+'/PROMPT.json">Exact prompt</a></p><small>Static source only; full action and owner acceptance are separate.</small></article>' for d in sources)
(S/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nursery connected wash — all source attempts</title><style>'+css+'</style><main><header><a href="../../../audit/job_nursery_wash_connected_v1_20261002/index.html">Mounted washing review</a><h1>Nursery Roshan: connected washing drawings</h1><p>Seven original RGBA imagegen attempts, each individually inspected. Six selected states use Roshan’s own Nursery costume and a fixed painted basin. The first clasp/rub4.4 remains preserved and unbound; palm02 reaches the provisional static4.5 floor. All ≤4.5 remain priorities. No accepted continuous-motion or owner claim.</p><p><a href="PLAN.json">Reuse inventory and named gap</a>. Built-in imagegen, transparent outputs; native1280 square originals preserved. Runtime copies are uniform1024 POT normalization.</p></header><div class="grid">'+gallery+'</div></main></html>',encoding='utf-8')
hero='actual_route_v3/native_views/nursery_1280_earned_clean_result.webp'
lines=['<header><a href="../job_review_v2_20261001/index.html">Whole job artwork review</a> · <a href="../job_artwork_refinement_live/all_items.html">Individual library</a><h1>Nursery washing: the work is visible again</h1><p>Current reversible v3 draft. The original empty work oval is replaced by one connected Roshan-and-basin painting: wet hands, palm scrub, back-of-hand scrub, rinse, and earned clean palms. The normal room actor returns at the next catch invitation. A first weak clasp4.4 and the generic boxing-puff overlap are preserved in earlier attempts.</p><p class="weak">Direct current sequence scores are still pending. Strong stills do not establish washing movement, whole-room quality, device performance, child or owner approval. The full current trusted Godot suite is running.</p></header>', '<section><figure><img src="'+hero+'" alt="Actual production caller earned clean palms, no generic boxing impact"></figure><p>Actual Bubble Bath card/caller; first phase earned through hold, pause and resume. Normal Back returns with no unearned career star. This is a partial-career route check.</p></section>', '<section><h2>What is covered</h2><p>Fresh original and replacement sequences at1280×720 and1600×720. Four current direct-room cases cover Nursery training and its authored Chapter Two catalog. Two additional cases use the actual Bubble Bath card and production caller. Nursery is not in ChapterTwoPartyPlan’s live birthday roster; the catalog cannot be reported as ordinary birthday gameplay.</p><p>Doctor is a sibling control in the preserved eight-case baseline and candidate1 captures. Its weak handwashing remains separate work. All current v3 frames are preserved; contact sheets are read-only QA, with full native details for every wash state.</p><p><a href="PLAN.json">Scope/rules/evidence</a> · <a href="MOVEMENT_PROFILE_AND_CLIP_CONTRACT_V1.json">Movement profile, state/contact/exit contract and acting gaps</a> · <a href="full_ci_v1/RECEIPT.json">Current full-suite receipt</a> · <a href="../../assets_src/imagegen/nursery_wash_connected_v1_20261002/index.html">Every source, prompt and individual score</a></p></section>', '<section><h2>Every current state in context</h2><div class="grid">']
for d in details:
    rel=Path(d['path']).relative_to(F.relative_to(R)).as_posix()
    lines.append('<article><h3>'+html.escape(d['case'])+' · '+d['state']+'</h3><a href="'+rel+'"><img loading="lazy" src="'+rel+'" alt="'+html.escape(d['case']+' '+d['state'])+'"></a><small>Native frame '+str(d['frame'])+'; direct individual and sequence review pending.</small></article>')
lines+=['</div></section>','<section><h2>Entire sequence evidence</h2><p>Step the original full native captures alongside exact progress and event metadata. No frame interpolation, invented motion or accepted-motion label is applied.</p><label for="sequence">Sequence</label><select id="sequence"></select><button id="prev">Previous frame</button><button id="next">Next frame</button><input id="frame" type="range" min="0" value="0" style="width:90%"><p id="stamp"></p><img id="native" alt="Full native frame"><pre id="metadata"></pre></section>','<section><h2>Ordered contact sheets</h2><p>Every captured v3 frame appears once in the ordered boards. Fine hand/material judgement uses the full native views above.</p>']
for case in cases:
    lines.append('<details><summary>'+html.escape(case['id'])+' · '+str(len(case['rows']))+' consecutive frames</summary>')
    for b in boards:
        if b['case']==case['id']:
            rel=Path(b['path']).relative_to(F.relative_to(R)).as_posix();lines.append('<a href="'+rel+'"><img loading="lazy" src="'+rel+'" alt="'+html.escape(case['id'])+' frames '+str(b['first'])+'"></a>')
    lines.append('</details>')
lines+=['</section>','<section><h2>Original missing subject and all iterations</h2><p>The fresh original Nursery action scores1.8, visible hands/contact1.5; there is no visible basin to assign a material score. Root reviewed all1051 original Nursery frames on24 ordered boards. The whole eight-case native archive has2074frames. Candidate1 and candidate2 preserve the weak clasp and puff-overlap before their targeted replacements.</p><p><a href="baseline_visual/DIRECT_REVIEW.json">Complete Nursery baseline opinions</a> · <a href="baseline_visual/INDEX.json">Original ordered boards and native details</a> · <a href="candidate_capture_v1/native_frames/CAPTURE_RECEIPT.json">Candidate1</a> · <a href="candidate_capture_v2/native_frames/CAPTURE_RECEIPT.json">Candidate2</a> · <a href="candidate_capture_v3/native_frames/CAPTURE_RECEIPT.json">Current candidate3</a></p></section>']
data=json.dumps([{'id':c['id'],'rows':c['rows']} for c in cases],ensure_ascii=False).replace('</','<\\/')
js='const cases='+data+';const s=document.querySelector("#sequence"),range=document.querySelector("#frame");cases.forEach((c,i)=>{const o=document.createElement("option");o.value=i;o.textContent=c.id;s.appendChild(o)});function show(){const c=cases[Number(s.value)],i=Number(range.value),r=c.rows[i];document.querySelector("#native").src=r.path;document.querySelector("#stamp").textContent=c.id+" · native frame "+i+"/"+(c.rows.length-1)+" · "+(r.wash_state||r.event)+" · progress "+r.phase_progress;document.querySelector("#metadata").textContent=JSON.stringify(r,null,2)}function choose(){range.max=cases[Number(s.value)].rows.length-1;range.value=0;show()}s.addEventListener("change",choose);range.addEventListener("input",show);document.querySelector("#prev").addEventListener("click",()=>{range.value=Math.max(0,Number(range.value)-1);show()});document.querySelector("#next").addEventListener("click",()=>{range.value=Math.min(Number(range.max),Number(range.value)+1);show()});choose();'
(F/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nursery washing — current complete-action review draft</title><style>'+css+'</style><main>'+''.join(lines)+'<script>'+js+'</script></main></html>',encoding='utf-8')
allowp=R/'tmp/v2_preview_allowed.json';allow=set(json.loads(allowp.read_text()));allow.update(p.relative_to(R).as_posix() for parent in [F,S,R/'assets/opera/worlds/nursery/wash_connected_v1_20261002'] for p in parent.rglob('*') if p.is_file());write(allowp,sorted(allow))
print(json.dumps({'current_cases':len(cases),'frames':sum(len(c['rows']) for c in cases),'boards':len(boards),'native_state_details':len(details),'sources':len(sources),'preview':'http://127.0.0.1:8880/audit/job_nursery_wash_connected_v1_20261002/index.html'}))
