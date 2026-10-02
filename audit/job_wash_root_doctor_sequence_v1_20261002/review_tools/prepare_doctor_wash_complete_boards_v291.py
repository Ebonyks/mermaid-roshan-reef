from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old=r/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03'
f=r/'audit/job_wash_root_doctor_sequence_v1_20261002';f.mkdir(exist_ok=False);(f/'.gdignore').write_text('',encoding='utf-8');(f/'review_tools').mkdir();(f/'ordered_boards').mkdir()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
data=read(old/'FRAME_VIEWER_DATA_V3.json');case=next(x for x in data['cases'] if x['id']=='opera_training_doctor_1280')
frames=[x.copy() for x in data['frames'] if x['case']==case['id']];assert len(frames)==256
for x in frames:
 p=old/'native_frames'/x['path'];assert sha(p)==x['sha256'];x['path']=p.relative_to(r).as_posix();x['direct_review']=False
write(f/'PLAN.json',dict(status='HISTORICAL_CAPTURE_COMPLETE_SEQUENCE_REVIEW_PENDING',baseline='c8f88df058434f1fd1b6d7fade712677003c641a',scope='Review every256 consecutive native frames of the preserved2026-10-01 input-driven Doctor Opera training root WASH route, rather than only four selected views. No new capture or production/asset changes; new boards use whole-frame display normalization only. Other seven captured cases remain independently unreviewed.',case=case,source_capture_profile=(old/'PROFILE.json').relative_to(r).as_posix(),qualification='Existing route fixture opens the real hotspot and uses a held wash action, but initializes training/birthday catalog state; not an ordinary MainMenu story launch, not current candidate/device/full-action acceptance.'))
ip=r/'design/audit_impacts/job-wash-root-doctor-sequence-review-20261002.json'
impact=dict(id='job-wash-root-doctor-sequence-review-20261002',scope='Complete visual audit of one preserved Doctor training WASH sequence:256 actual captured frames; no runtime/art edits or accepted wash repair. Other source priorities and cases remain separate.',baseline='c8f88df058434f1fd1b6d7fade712677003c641a',rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-05','DL-VIS-07','DL-VIS-08','DL-INT-01','DL-INT-02','DL-INT-04','DL-INT-06','DL-QA-01','DL-QA-02','DL-QA-03'],findings=['MA-VIS-006','MA-PLAY-004'],files=[],validation=[dict(command='Verify preserved native256 frame SHA256 and ordered complete boards',result='PENDING',evidence=f.relative_to(r).as_posix()+'/BOARD_MANIFEST.json')],acceptance_gaps='Direct every-frame review pending; other1818 captured frames, ordinary story/device/child/owner washing acceptance and actual local contact remain open. No production change or full-suite claim.')
write(ip,impact)
boards=[]
for start in range(0,len(frames),12):
 group=frames[start:start+12];lst=f/'ordered_boards'/f'{start//12+1:02d}.txt';lst.write_text(''.join("file '"+(r/x['path']).as_posix()+"'\n" for x in group),encoding='utf-8',newline='\n');output=f/'ordered_boards'/f'{start//12+1:02d}.png'
 subprocess.run(['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale=320:-1,tile=4x3:nb_frames={len(group)}:padding=2:margin=2:color=white',str(output)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 boards.append(dict(path=output.relative_to(r).as_posix(),sha256=sha(output),first_frame=start,last_frame=start+len(group)-1,count=len(group),direct_review=False,ordering='Left to right, top to bottom; whole native canvases, uniform display scaling only, final22nd board four real images and eight blank cells.'))
write(f/'BOARD_MANIFEST.json',dict(status='EVERY256_NATIVE_FRAMES_ON22_BOARDS_REVIEW_PENDING',case=case,frames=frames,boards=boards,qualification='No skipped, synthesized or duplicated frames; native originals/hashes preserved in prior published capture. No artwork edits or current runtime acceptance.'))
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
impact['files']=sorted(p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file());write(ip,impact)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(impact['files'])))
print('Prepared22 ordered whole-canvas boards for every256 preserved Doctor training frames; review pending.')
