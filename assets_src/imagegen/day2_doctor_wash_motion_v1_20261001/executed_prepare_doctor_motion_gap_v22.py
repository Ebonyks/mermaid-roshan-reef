from pathlib import Path
import datetime,hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'assets_src/imagegen/day2_doctor_wash_motion_v1_20261001';assert not out.exists();out.mkdir()
(out/'.gdignore').write_text('',encoding='utf-8')
source='assets_src/imagegen/day2_doctor_wash_pose_v1_20261001/attempt_06_native.png'
assert hashlib.sha256((r/source).read_bytes()).hexdigest()=='3ada2bd00859314ece42ccffa2dc20aae9543086b1161d6e8336689021c99d2c'
profile=dict(status='GENERATION_PREPARED_UNBOUND',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),named_gap='The actual viewport-route doctor wash shows a medical-tool work pose beside a remote schematic basin; no existing approved doctor sheet cell depicts the full child naturally washing both hands.',reuse_inventory=['Approved doctor1024 atlas: old work1 pinned tool pose; other work cells retain role tools, not consecutive hand-rubbing keys.','Existing painted bubble_bath_sink_sheet first cell source4.6 reuse candidate; no new sink commissioned.','Generated doctor attempt6 source4.5 floor preserved as a motion study input, not owner-approved or bound.'],input=dict(path=source,sha256=hashlib.sha256((r/source).read_bytes()).hexdigest(),role='Editable generated draft; appearance/registration input, not protected original or owner acceptance'),method='Built-in imagegen, one complete full-character RGBA image per candidate; no interpolation, layer warp or rig.',qualification='Source scores, native fit/contact, sequence continuity, full actions, device, child and owner acceptance remain separate. Preserve every candidate and originals; this study does not yet change runtime.')
(out/'PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'executed_prepare_doctor_motion_gap_v22.py')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in out.rglob('*') if p.is_file()})
d['scope']+=' Named actual-route doctor washing motion gap: reuse the existing painted sink and study a small registered hand-rubbing change from generated source6, preserving source-only4.5 and all runtime/sequence/owner limits.'
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared bounded unbound doctor washing motion gap; originals unchanged.')
