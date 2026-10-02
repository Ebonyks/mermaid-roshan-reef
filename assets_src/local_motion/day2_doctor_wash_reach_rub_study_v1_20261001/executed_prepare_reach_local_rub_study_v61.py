from pathlib import Path
import hashlib, json, shutil, subprocess, sys

r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
old=r/'assets_src/local_motion/day2_doctor_wash_rub_study_v1_20261001'
newdir='assets_src/local_motion/day2_doctor_wash_reach_rub_study_v1_20261001'
packet=r/newdir
assert not packet.exists()
prep=(old/'executed_prepare_doctor_comfy_study_v42.py').read_text(encoding='utf-8')
prep=prep.replace('assets_src/local_motion/day2_doctor_wash_rub_study_v1_20261001',newdir)
prep=prep.replace('fb03e0ac3dda1658e9ea188d33cc6e084871642b','56d66f63e375b61cf02936b426a05a2b92c14d3b')
prep=prep.replace('assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/attempt_06_native.png','assets_src/imagegen/day2_doctor_wash_reach_v1_20261001/attempt01_native.png')
prep=prep.replace('3ada2bd00859314ece42ccffa2dc20aae9543086b1161d6e8336689021c99d2c','50a63f9c7465c2b39418cd58dd5bbeef19072279416c7cadbf533d8645b41b1a')
prep=prep.replace('job-doctor-local-rub-study-20261001','job-doctor-reach-local-rub-study-20261001')
prep=prep.replace('DAY2-DOCTOR-RUB-LOCAL-V1','DAY2-DOCTOR-REACH-RUB-LOCAL-V1').replace('WASH-DOCTOR-RUB-REFERENCE01','WASH-DOCTOR-REACH-RUB-REFERENCE01').replace('d2m_doctor_rub_v1_20261001','d2m_doctor_reach_rub_v1_20261001').replace('2026100101','2026100111')
prep=prep.replace('source6','outward-reaching source').replace('Source6','Outward-reaching source')
prep=prep.replace('[535,594]','[684,680]')
prompt='Locked camera, one continuous shot of this complete small mermaid doctor in the exact same polished drawn2D storybook style and neutral aqua field. Her upper hand already rests palm-down on the BACK of the lower hand; her forearms reach out to image right. 0.00-0.30seconds: hold this exact connected contact still. 0.30-1.10: make ONE clearly visible short rubbing stroke: only the UPPER palm slides gently along the BACK of the LOWER hand toward its knuckles, then starts back. The lower hand remains relaxed, wrist attached, fingers pointing down/right in their original grouped shape. 1.10-1.50: the upper palm slides back to the exact initial contact. 1.50-1.70: settle in that initial pose. Keep BOTH hands in contact throughout; never open the lower palm or separate into a gesture. Lather stays small and attached at the contact. Keep her face, gaze, head, brown curls/rainbow lock, flower, doctor coat, satchel, torso, curled rainbow tail and paired fin fixed in identity, shape, scale and canvas position; only local wrist/forearm articulation may accompany the upper palm stroke. Keep the plain aqua field still. No sink/water is requested in this isolated rub reference. Warm brown/plum contours, broad matte painted values and aqua/lavender shadows stay stable. No clasping swap, hand opening, detached wrists, extra fingers/limbs, moving head/body/tail, fin changes, new objects/tools, foam growth, camera move, cuts, whole-card translation, photorealism,3D/plastic texture, sparkle, text or background invention. Sound: silence.\n'
a=prep.index("prompt='Locked camera,")
b=prep.index('\npromptpath=',a)
prep=prep[:a]+'prompt='+repr(prompt)+prep[b:]
prep=prep.replace("'entry':[0.0,0.25],'rub':[0.25,1.20],'settle':[1.20,1.70]","'entry':[0.0,0.30],'rub':[0.30,1.10],'return':[1.10,1.50],'settle':[1.50,1.70]")
prep=prep.replace('Roshan rubs both attached soapy hands together with a small back-of-hand stroke.','Roshan makes one clear upper-palm stroke along the back of her relaxed lower hand, then returns to exact initial outward contact.')
prep=prep.replace('One short full-character hand-rubbing motion study of the already-generated outward-reaching source through the unchanged developed local ComfyUI GGUF quick workflow.','After the first chest-clasp study failed motion4.0/return3.5, one full-character rub/return trial of the new outward-reaching source through the unchanged developed local ComfyUI GGUF workflow.')
preppath=r/'tmp/prepare_reach_local_rub_study_v61_executed.py'
assert not preppath.exists();preppath.write_text(prep,encoding='utf-8',newline='\n')
result=subprocess.run([sys.executable,'-X','utf8','-B',str(preppath)],cwd=r,capture_output=True,text=True)
(r/'tmp/prepare_reach_local_rub_study_v61.stdout.log').write_text(result.stdout,encoding='utf-8')
(r/'tmp/prepare_reach_local_rub_study_v61.stderr.log').write_text(result.stderr,encoding='utf-8')
print(result.stdout);print(result.stderr);assert result.returncode==0
# Save the exact independently pinned one-study worker; no installed service code changes.
worker=(old/'run_doctor_comfy_study_v43.py').read_text(encoding='utf-8')
worker=worker.replace('assets_src/local_motion/day2_doctor_wash_rub_study_v1_20261001',newdir).replace('build/doctor_local_rub_study_v1_20261001','build/doctor_reach_local_rub_study_v1_20261001')
workerpath=packet/'run_doctor_reach_comfy_study_v61.py';workerpath.write_text(worker,encoding='utf-8',newline='\n')
m=json.loads((packet/'MANIFEST.json').read_text(encoding='utf-8'))
m['worker_sha256']=hashlib.sha256(workerpath.read_bytes()).hexdigest()
m['worker']='run_doctor_reach_comfy_study_v61.py'
m['preceding_below_floor_motion']='assets_src/local_motion/day2_doctor_wash_rub_study_v1_20261001/attempt_01/REVIEW.json'
m['reused_art']='New complete outward-reaching source4.5 is unbound; first study had motion4.0/return3.5. This trial isolates a literal upper-palm back-of-hand stroke and exact return; same existing developed workflow, no new models/packages/service changes.'
(packet/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
shutil.copyfile(old/'MOVEMENT_INTERPRETATION_V1.json',packet/'MOVEMENT_INTERPRETATION_V1.json')
shutil.copyfile(__file__,packet/'executed_prepare_reach_local_rub_study_v61.py')
ip=r/'design/audit_impacts/job-doctor-reach-local-rub-study-20261001.json';d=json.loads(ip.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in packet.rglob('*') if p.is_file()});ip.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
allow=r/'tmp/v2_preview_allowed.json';a=set(json.loads(allow.read_text(encoding='utf-8')));a.update(d['files']);allow.write_text(json.dumps(sorted(a),indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PREPARED_REACH_RUB_REFERENCE_ONLY','job_name':m['job']['queue_name'],'worker_sha256':m['worker_sha256'],'bindings':len(m['renderer']['bindings']),'production_edits':False}))
