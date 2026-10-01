from pathlib import Path
import hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
source=r/'tmp/wash_complete_action_v1'
receipt=json.loads((source/'PROCESS_RECEIPT.json').read_text())
assert receipt['status']=='FAIL_PRESERVED' and receipt['source_unchanged']
out=r/'audit/day_two_wash_complete_action_v1_20261001/failed_attempt_01'
assert not out.exists();out.mkdir(parents=True)
(out.parent/'.gdignore').write_text('',encoding='utf-8')
paths=[x for x in source.rglob('*') if x.is_file() and ('native_frames' in x.parts or x.name.endswith('.log') or x.name in ['PROFILE.json','PROCESS_RECEIPT.json'])]
for p in paths:
    dest=out/p.relative_to(source);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
for name in ['capture_complete_wash_v1.gd','run_complete_wash_v1.py']:
    shutil.copyfile(r/'tmp'/name,out/('executed_'+name))
failure={'status':'FAIL_PRESERVED','reason':'Missing _begin method on the actual gesture surface at first local press. Parser/inference/analyzer exited0 but did not establish runtime API correctness. Stopped only diagnostic Godot child59940 after the error; native process exit4294967295.','production_source_unchanged':True,'partial_frame_count':len(list((out/'native_frames').rglob('*.webp'))),'complete_action_review':None,'corrected_method':'InputEventScreenTouch through actual surface._gui_input; still a local diagnostic, not root navigation.'}
(out/'FAILURE.json').write_text(json.dumps(failure,indent=2)+'\n',encoding='utf-8')
s=(r/'tmp/capture_complete_wash_v1.gd').read_text(encoding='utf-8').replace('wash_complete_action_v1','wash_complete_action_v2')
bad='\t\t\t\t\t\tworld.surface._begin(world.surface.size*0.5)'
good='\t\t\t\t\t\tvar wash_touch: InputEventScreenTouch = InputEventScreenTouch.new()\n\t\t\t\t\t\twash_touch.index=0\n\t\t\t\t\t\twash_touch.pressed=true\n\t\t\t\t\t\twash_touch.position=world.surface.size*0.5\n\t\t\t\t\t\tworld.surface._gui_input(wash_touch)'
assert s.count(bad)==1;s=s.replace(bad,good)
(r/'tmp/capture_complete_wash_v2.gd').write_text(s,encoding='utf-8')
s=(r/'tmp/run_complete_wash_v1.py').read_text(encoding='utf-8').replace('wash_complete_action_v1','wash_complete_action_v2').replace('capture_complete_wash_v1.gd','capture_complete_wash_v2.gd')
(r/'tmp/run_complete_wash_v2.py').write_text(s,encoding='utf-8')
shutil.copyfile(Path(__file__),out/'executed_prepare_complete_wash_retry_v2.py')
p=r/'ASSET_LICENSES.md';s=p.read_text(encoding='utf-8')
for image in (out/'native_frames').rglob('*.webp'):
    path=image.relative_to(r).as_posix();digest=hashlib.sha256(image.read_bytes()).hexdigest()
    if path not in s:s+='\n| `'+path+'` | Mermaid Roshan original-game diagnostic capture | Project review evidence; underlying artwork rights unchanged | Native Godot4.7.2 failed wash fixture; SHA-256 `'+digest+'` | Lossless full native frame; failed partial fixture, no visual/action acceptance |\n'
p.write_text(s,encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in out.parent.rglob('*') if x.is_file()]));d['validation'].append({'command':'Original complete washing diagnostic attempt1','result':'FAIL','evidence':'audit/day_two_wash_complete_action_v1_20261001/failed_attempt_01/FAILURE.json; missing local helper, native error retained, source unchanged. Actual GUI-event retry pending.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Preserved',failure['partial_frame_count'],'partial native frames and runtime helper failure; corrected local GUI-touch retry ready.')
