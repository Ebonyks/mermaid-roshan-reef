from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,html,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
source=r/'tmp/wash_complete_action_v2'
process=json.loads((source/'PROCESS_RECEIPT.json').read_text())
assert process['status']=='PASS_ORIGINAL_LOCAL_INPUT_NATIVE_CAPTURE' and process['source_unchanged']
root=r/'audit/day_two_wash_complete_action_v1_20261001'
out=root/'local_hold_attempt_02';assert not out.exists();out.mkdir()
for p in source.rglob('*'):
    if p.is_file() and ('native_frames' in p.parts or p.name.endswith('.log') or p.name in ['PROFILE.json','PROCESS_RECEIPT.json']):
        dst=out/p.relative_to(source);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
for name in ['capture_complete_wash_v2.gd','run_complete_wash_v2.py']:
    shutil.copyfile(r/'tmp'/name,out/('executed_'+name))
d=json.loads((out/'native_frames/CAPTURE_RECEIPT.json').read_text())
d['qualification']+=' This fixture opens each first task directly, so it does not test approach or hotspot navigation. Its manual controller/surface/actor tick is30Hz; other effects/tweens retain the renderer clock. It does not prove natural wall-clock timing. Chapter Two setup resolves its shipping scene adapter automatically; normal root launch, rewards/save callbacks and phone/child/owner acceptance remain separate.'
(out/'CAPTURE_QUALIFICATION_V2.json').write_text(json.dumps({'original_receipt':'native_frames/CAPTURE_RECEIPT.json','qualification':d['qualification'],'frame_count':len(d['frames']),'production_source_unchanged':True,'ordinary_route':None,'natural_wall_clock_timing':None},indent=2)+'\n',encoding='utf-8')
boards=root/'key_boards_v2';boards.mkdir()
board_rows=[]
for case in d['cases']:
    frames=d['frames'][case['first_record']:case['first_record']+case['frame_count']]
    ticks={0,11,12,case['accepted_tick']//2,case['accepted_tick']-1,case['accepted_tick'],case['accepted_tick']+1,case['accepted_tick']+6,case['accepted_tick']+16,case['next_phase_tick']-1,case['next_phase_tick'],case['next_phase_tick']+6}
    poses={}
    for row in frames[:case['accepted_tick']]:
        poses.setdefault((row['player_animation'],row['player_frame']),row['logical_tick'])
    ticks.update(poses.values());ticks=sorted(ticks)
    for number,start in enumerate(range(0,len(ticks),6)):
        chosen=ticks[start:start+6]
        sheet=Image.new('RGB',(1536,658),'#eff3f8');draw=ImageDraw.Draw(sheet)
        for n,tick in enumerate(chosen):
            row=frames[tick];im=Image.open(out/'native_frames'/row['path']).convert('RGB')
            im.thumbnail((512,288),Image.Resampling.LANCZOS)
            x=(n%3)*512;y=(n//3)*329
            sheet.paste(im,(x,y+30))
            draw.text((x+8,y+4),f'{tick:03d} {row["event"]} {row["player_animation"]}/{row["player_frame"]}',fill='#172a43')
        p=boards/(case['id']+f'_key_{number:02d}.webp');sheet.save(p,'WEBP',lossless=True)
        board_rows.append({'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'case':case['id'],'ticks':chosen,'derivation':'Six exact native views uniformly reduced to512px wide with diagnostic labels; no art correction, not delivery pixels.','direct_visual_review':'PENDING'})
(root/'KEY_BOARD_REGISTER_V2.json').write_text(json.dumps({'boards':board_rows,'qualification':'Selected boundary and each recorded work-pose keys, not every1520-frame review. Originals remain independently available.'},indent=2)+'\n',encoding='utf-8')
rows=[]
for case in d['cases']:
    frames=d['frames'][case['first_record']:case['first_record']+case['frame_count']]
    rows.append({'id':case['id'],'career':case['career'],'run_mode':case['run_mode'],'width':case['width'],'frame_count':case['frame_count'],'accepted_tick':case['accepted_tick'],'next_phase_tick':case['next_phase_tick'],'work_pose_cells':sorted(set(x['player_frame'] for x in frames[:case['accepted_tick']] if x['player_animation']=='work')),'draw_subject_score':None,'acting_score':None,'completion_score':None,'context_score':None,'direct_review':'PENDING','ordinary_route_score':None,'owner_approval':'PENDING'})
(root/'REVIEW.json').write_text(json.dumps({'status':'MACHINE_CAPTURE_COMPLETE_DIRECT_REVIEW_PENDING','cases':rows,'frames':1520,'source_hashes_checked':len(process['source_before']),'qualification':d['qualification'],'existing_priorities':'Initial doctor draw subject2.9 and missing nursery subject2.2 remain drafting opinions from earlier directly reviewed views. Source foam4.6 remains unbound; no visual/full-action pass inferred from these processes.'},indent=2)+'\n',encoding='utf-8')
data={'cases':d['cases'],'frames':d['frames'],'qualification':d['qualification']}
(root/'FRAME_VIEWER_DATA_V2.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
board_html=''.join('<figure><figcaption>'+html.escape(x['case'])+' · ticks '+str(x['ticks'])+' · visual review pending</figcaption><img loading="lazy" src="'+x['path']+'" alt="'+html.escape(x['case'])+' selected boundary views"></figure>' for x in board_rows)
page='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Washing: complete local hold sequences</title><style>body{margin:0;background:#edf3f8;color:#20304c;font:16px/1.6 system-ui}main{max-width:1200px;margin:24px auto;padding:24px}section,figure{background:white;padding:20px;border-radius:16px;margin:20px 0}img{max-width:100%;height:auto}a,code{overflow-wrap:anywhere}label{margin-right:16px}input[type=range]{width:min(600px,90%)}.note{border-left:5px solid #bf8349;padding:16px}button,select{font:inherit;padding:8px}</style></head><body><main><a href="../job_review_v2_20261001/index.html">Current review entry</a><h1>Washing: eight complete local hold sequences</h1><p>1,520 lossless native views. Doctor and nursery, Opera training and Chapter Two catalog, at 1280×720 and 1600×720. Original artwork remains bound.</p><p class="note">Machine capture succeeded; direct sequence evaluation is pending. This fixture opens the first task directly. It does not establish approach, ordinary root navigation or natural wall-clock timing. Controller, surface and actor use manual 30 Hz ticks; other presentation effects retain their renderer clock. Phone, child and owner acceptance remain separate.</p><section><h2>Every native frame</h2><label>Case <select id="case" aria-label="Washing case"></select></label><button id="previous">Previous frame</button> <button id="next">Next frame</button><p><label>Frame <input id="frame" aria-label="Native frame" type="range" min="0" value="0"></label><output id="frameLabel"></output></p><img id="native" alt="Selected original native washing frame"><p id="details"></p></section><p><a href="REVIEW.json">Written individual case review</a> · <a href="local_hold_attempt_02/PROCESS_RECEIPT.json">Processes and unchanged source hashes</a> · <a href="local_hold_attempt_02/CAPTURE_QUALIFICATION_V2.json">Full capture limitations</a> · <a href="failed_attempt_01/FAILURE.json">Preserved first fixture failure</a> · <a href="KEY_BOARD_REGISTER_V2.json">Selected board coverage</a></p><h2>Boundaries and recorded work poses</h2>'''+board_html+'''</main><script>let data,rows;const caseSelect=document.getElementById('case'),frame=document.getElementById('frame'),native=document.getElementById('native');function draw(){const x=rows[Number(frame.value)];native.src='local_hold_attempt_02/native_frames/'+x.path;document.getElementById('frameLabel').textContent=x.logical_tick+' / '+(rows.length-1);document.getElementById('details').textContent=x.event+' · logical '+x.logical_seconds.toFixed(3)+' s · phase '+x.phase_name+' · pose '+x.player_animation+'/'+x.player_frame+' · surface '+x.visual_context+' / '+x.widget_template+' · SHA-256 '+x.sha256}function selectCase(){rows=data.frames.filter(x=>x.case===caseSelect.value);frame.max=rows.length-1;frame.value=0;draw()}caseSelect.addEventListener('change',selectCase);frame.addEventListener('input',draw);document.getElementById('previous').addEventListener('click',()=>{frame.value=Math.max(0,Number(frame.value)-1);draw()});document.getElementById('next').addEventListener('click',()=>{frame.value=Math.min(rows.length-1,Number(frame.value)+1);draw()});fetch('FRAME_VIEWER_DATA_V2.json').then(x=>x.json()).then(x=>{data=x;for(const c of x.cases){const o=document.createElement('option');o.value=c.id;o.textContent=c.id;caseSelect.append(o)}selectCase()})</script></body></html>'''
(root/'index.html').write_text(page,encoding='utf-8')
shutil.copyfile(Path(__file__),root/'executed_build_complete_wash_library_v2.py')
p=r/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8')
for pimg in list((out/'native_frames').rglob('*.webp'))+list(boards.glob('*.webp')):
    path=pimg.relative_to(r).as_posix();digest=hashlib.sha256(pimg.read_bytes()).hexdigest()
    if path not in s:s+='\n| `'+path+'` | Mermaid Roshan native washing diagnostic | Project review evidence; underlying artwork rights unchanged | Godot4.7.2 local hold fixture; SHA-256 `'+digest+'` | '+('Selected diagnostic board with uniform thumbnail reduction and labels; originals retained' if pimg.parent==boards else 'Lossless full native frame; original artwork unchanged')+'; not runtime/delivery art or visual acceptance |\n'
p.write_text(s,encoding='utf-8')
p=r/'design/05_DOC_LEDGER.md';s=p.read_text(encoding='utf-8');entry='| `audit/day_two_wash_complete_action_v1_20261001/index.html` | 🟣 | `CANDIDATE`; eight unchanged-art local GUI-touch/manual-tick first-task sequences,1520 lossless native frames and individually addressable viewer. Machine capture passes with literal source hashes unchanged; selected-board/direct complete evaluation pending. Direct task opening bypasses approach; natural wall-clock/root/device/child/owner acceptance separate. |\n';assert '`audit/day_two_wash_complete_action_v1_20261001/index.html`' not in s;p.write_text(s+'\n'+entry,encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';impact=json.loads(p.read_text());impact['files']=sorted(set(impact['files']+[p.relative_to(r).as_posix() for p in root.rglob('*') if p.is_file()]));impact['validation'].append({'command':'run_complete_wash_v2.py unchanged-source eight local GUI-touch/manual-tick washing fixtures','result':'PASS','evidence':'audit/day_two_wash_complete_action_v1_20261001/local_hold_attempt_02/PROCESS_RECEIPT.json; parser/inference/analyzer/native all0, source unchanged. This is process/fixture evidence only; approach and all direct sequence/route/device/child/owner acceptance remain pending.'});p.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'native_frames':len(d['frames']),'selected_boards':len(board_rows),'case_count':len(rows),'license_bytes':(r/'ASSET_LICENSES.md').stat().st_size,'direct_review':'PENDING'}))
