from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
packet=r/'assets_src/local_motion/day2_doctor_wash_reach_rub_study_v1_20261001';state_dir=r/'build/doctor_reach_local_rub_study_v1_20261001'
state=json.loads((state_dir/'STATE.json').read_text(encoding='utf-8'));assert state['status']=='MACHINE_RENDER_PASS_VISUAL_AUDIT_PENDING'
out=packet/'attempt_01';assert not out.exists();out.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
receiptpath=Path(state['receipt_path']);receipt=json.loads(receiptpath.read_text(encoding='utf-8'));assert receipt['status']=='PASS'
for name in ['RENDER_RECEIPT.json','workflow.api.json','COMFY_HISTORY.json']:shutil.copyfile(receiptpath.with_name(name),out/name)
shutil.copyfile(state_dir/'STATE.json',out/'WORKER_STATE.json');shutil.copyfile(state_dir/'CLI.stdout_stderr.log',out/'CLI.stdout_stderr.log')
source_outputs=[]
for x in receipt['outputs']:
 p=Path(x['path']);assert p.resolve().is_relative_to(Path('H:/MermaidReefTools/LocalVideo/output').resolve());assert sha(p)==x['sha256']
 target=out/('native_output'+p.suffix);assert not target.exists();shutil.copyfile(p,target);assert sha(target)==x['sha256']
 source_outputs.append({'provider_path':str(p),'path':target.relative_to(r).as_posix(),'bytes':target.stat().st_size,'sha256':sha(target),'transformation':'Byte-identical original output, no repair/retiming/interpolation.'})
native=out/'native_output.webm';assert native.exists();frames=out/'native_frames';frames.mkdir()
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
cmd=[ffmpeg,'-nostdin','-hide_banner','-loglevel','error','-n','-i',str(native),'-fps_mode','passthrough',str(frames/'%04d.png')]
with (out/'decode.stdout.log').open('wb') as so,(out/'decode.stderr.log').open('wb') as se:p=subprocess.run(cmd,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120)
assert p.returncode==0
from PIL import Image
rows=[]
for index,path in enumerate(sorted(frames.glob('*.png'))):
 with Image.open(path) as image:assert image.size==(896,512);dimensions=list(image.size)
 rows.append({'index':index,'timestamp_seconds':index/24,'path':path.relative_to(packet).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size,'dimensions':dimensions,'visual_score':None,'visual_review':'PENDING'})
assert len(rows)==41
write(out/'FRAME_CATALOG.json',{'status':'ALL41_NATIVE_FRAMES_DECODED_VISUAL_REVIEW_PENDING','source_outputs':source_outputs,'native_frames':rows,'decode_command':cmd,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Lossless decoding of the unchanged local reference video. No frame is an accepted runtime/cinematic delivery frame; no source score carries into motion.'})
shutil.copyfile(__file__,out/'executed_archive_reach_motion_frames_v66.py')
license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8')
for path in [out/'native_output.webm',out/'native_output.mp4',*sorted(frames.glob('*.png'))]:
 if not path.exists():continue
 name=path.relative_to(r).as_posix();assert name not in s
 s+='\n| '+name+' | Developed local ComfyUI Wan2.2 GGUF workflow2026-10-01, named doctor rubbing study | Project motion-reference output; model/source provenance retained in frozen workflows and RENDER_RECEIPT.json | '+('Lossless native-frame decode of preserved video' if path.suffix=='.png' else 'Byte-identical preserved local CLI output')+' | LOCAL_MOTION_REFERENCE_ONLY; all-frame artistic/runtime/cinematic and owner acceptance pending. |\n'
license.write_text(s,encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-doctor-reach-local-rub-study-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in packet.rglob('*') if x.is_file()});d['validation'].append({'command':'Pinned developed ComfyUI worker and lossless native-frame decode','result':'PASS','evidence':(out/'WORKER_STATE.json').relative_to(r).as_posix()+'; exact GGUF graph/source/prompt receipts,41 frames896x512. Artistic scores pending.'});write(impact,d)
allow=r/'tmp/v2_preview_allowed.json';a=set(json.loads(allow.read_text(encoding='utf-8')));a.update(d['files']);write(allow,sorted(a))
print(json.dumps({'status':'MACHINE_RENDER_PASS_ALL41_FRAMES_ARCHIVED_VISUAL_AUDIT_PENDING','prompt_id':receipt['prompt_id'],'native_video':native.relative_to(r).as_posix(),'frames':41,'render_seconds':receipt['elapsed_seconds']}))
