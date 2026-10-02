from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old=b/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03'
f=b/'audit/job_wash_root_remaining_sequences_v1_20261002'
f.mkdir(exist_ok=False);(f/'.gdignore').write_text('',encoding='utf-8');(f/'review_tools').mkdir();(f/'ordered_boards').mkdir()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
data=read(old/'FRAME_VIEWER_DATA_V3.json')
cases=[x for x in data['cases'] if x['id']!='opera_training_doctor_1280']
all_frames=[];all_boards=[];refs={}
plan=dict(status='SEVEN_PRESERVED_WASH_SEQUENCES_COMPLETE_REVIEW_PENDING',baseline='c8f88df058434f1fd1b6d7fade712677003c641a',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Extend the complete real-frame washing audit to all seven remaining preserved Opera training and birthday catalog cases at 1280/1600 widths. No new engine capture or runtime change. Every dated native frame is inspected separately from current-source acceptance.',cases=cases,qualification='October 1 fixture initializes training or birthday story catalog state and then uses actual hotspot/held touch actions. It is not a natural MainMenu story launch or a newly rendered current game. Current source-boundary comparison remains dated evidence, not a visual pass.')
write(f/'PLAN.json',plan)
ip=b/'design/audit_impacts/job-wash-root-remaining-sequences-review-20261002.json'
impact=dict(id='job-wash-root-remaining-sequences-review-20261002',scope=plan['scope'],baseline=plan['baseline'],rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-07','DL-VIS-08','DL-INT-01','DL-INT-02','DL-INT-04','DL-INT-06','DL-QA-01','DL-QA-02','DL-QA-03'],findings=['MA-VIS-006','MA-PLAY-004'],files=[],validation=[dict(command='Verify every preserved native-frame hash and directly inspect every actual frame on complete ordered boards',result='PENDING',evidence=f.relative_to(b).as_posix()+'/BOARD_MANIFEST.json')],acceptance_gaps='Every-frame review pending; actual reach/rub/rinse/clean rest, current rerender, ordinary story launch, physical device/child/owner approval remain open. No runtime repairs or finding closure.')
write(ip,impact)
for case in cases:
 frames=[x.copy() for x in data['frames'] if x['case']==case['id']]
 assert len(frames)==case['frame_count']
 folder=f/'ordered_boards'/case['id'];folder.mkdir()
 for x in frames:
  p=old/'native_frames'/x['path'];assert sha(p)==x['sha256']
  x['path']=p.relative_to(b).as_posix();x['direct_review']=False
  refs[x['path']]=[p.stat().st_size,x['sha256']]
 for start in range(0,len(frames),20):
  group=frames[start:start+20];lst=folder/f'{start//20+1:02d}.txt';out=folder/f'{start//20+1:02d}.png'
  lst.write_text(''.join("file '"+(b/x['path']).as_posix()+"'\n" for x in group),encoding='utf-8',newline='\n')
  subprocess.run(['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale=320:-1,tile=5x4:nb_frames={len(group)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  all_boards.append(dict(path=out.relative_to(b).as_posix(),sha256=sha(out),case=case['id'],first_frame=start,last_frame=start+len(group)-1,count=len(group),direct_review=False,ordering='Five columns by four rows, left to right then top to bottom. Every cell contains a uniformly scaled whole native canvas. Final board has explicitly counted real images; remaining cells are blank.'))
 all_frames+=frames
 print(case['id']+' prepared '+str(len(frames))+' frames',flush=True)
assert len(all_frames)==1818
write(f/'BOARD_MANIFEST.json',dict(status='ALL1818_REMAINING_NATIVE_FRAMES_REVIEW_PENDING',cases=cases,frames=all_frames,boards=all_boards,qualification='Unedited real native captures; whole-canvas display normalization only. No synthesis, interpolation or substitution. Dated captures do not become current game approval.'))
write(f/'REQUIRED_UNCHANGED_REFERENCES.json',dict(status='PRESERVED_PREVIOUSLY_PUBLISHED_NATIVE_FRAMES_REQUIRED',files=dict(sorted(refs.items())),qualification='Every native frame must also be byte-verified at the published checkpoint revision. Boards alone do not replace originals.'))
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
impact['files']=sorted(x.relative_to(b).as_posix() for x in f.rglob('*') if x.is_file());write(ip,impact)
p=b/'tmp/v2_preview_allowed.json';write(p,sorted(set(read(p))|set(impact['files'])))
print('Prepared '+str(len(all_boards))+' complete ordered boards for all 1818 remaining dated native frames; no direct-review claim yet.',flush=True)
